"""
Forecasting Service — uses Prophet (with statsmodels fallback).
Trains on daily revenue and returns forecast with confidence intervals.
"""
import logging
from typing import List

import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


def _build_daily(df: pd.DataFrame) -> pd.DataFrame:
    daily = (
        df.groupby("date")["final_price"]
        .sum()
        .reset_index()
        .rename(columns={"date": "ds", "final_price": "y"})
    )
    daily["ds"] = pd.to_datetime(daily["ds"])
    daily = daily.sort_values("ds").reset_index(drop=True)
    return daily


def _prophet_forecast(prophet_df: pd.DataFrame, periods: int) -> pd.DataFrame:
    from prophet import Prophet  # type: ignore

    m = Prophet(
        interval_width=0.95,
        daily_seasonality=False,
        weekly_seasonality=True,
        yearly_seasonality=True,
        changepoint_prior_scale=0.05,
    )
    m.fit(prophet_df)
    future = m.make_future_dataframe(periods=periods)
    forecast = m.predict(future)
    return forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]]


def _arima_forecast(daily: pd.DataFrame, periods: int) -> pd.DataFrame:
    """Lightweight fallback using exponential smoothing."""
    from statsmodels.tsa.holtwinters import ExponentialSmoothing  # type: ignore

    series = daily["y"].values
    model = ExponentialSmoothing(series, trend="add", seasonal=None)
    fit = model.fit()
    pred = fit.forecast(periods)

    std = np.std(fit.resid) * 1.96
    last_date = daily["ds"].max()
    future_dates = pd.date_range(last_date + pd.Timedelta(days=1), periods=periods)

    hist_df = daily.rename(columns={"y": "yhat"}).copy()
    hist_df["yhat_lower"] = hist_df["yhat"] - std
    hist_df["yhat_upper"] = hist_df["yhat"] + std

    fut_df = pd.DataFrame({
        "ds": future_dates,
        "yhat": pred,
        "yhat_lower": pred - std,
        "yhat_upper": pred + std,
    })
    return pd.concat([hist_df[["ds", "yhat", "yhat_lower", "yhat_upper"]], fut_df], ignore_index=True)


def run_forecast(df: pd.DataFrame, periods: int = 30) -> dict:
    if df.empty:
        return {"history": [], "forecast": [], "engine": "empty"}
    daily = _build_daily(df)
    if len(daily) < 5:
        return {"history": [], "forecast": [], "engine": "insufficient_data"}

    try:
        forecast_df = _prophet_forecast(daily.rename(columns={"date": "ds"}) if "date" in daily.columns else daily, periods)
        engine = "prophet"
    except Exception as e:
        logger.warning("Prophet failed (%s), falling back to ARIMA/ETS", e)
        forecast_df = _arima_forecast(daily, periods)
        engine = "ets"

    last_hist_date = daily["ds"].max()

    history = []
    forecast = []

    for _, row in forecast_df.iterrows():
        point = {
            "ds": str(row["ds"].date()),
            "yhat": round(float(row["yhat"]), 2),
            "yhat_lower": round(float(row["yhat_lower"]), 2),
            "yhat_upper": round(float(row["yhat_upper"]), 2),
        }
        if pd.to_datetime(row["ds"]) <= pd.to_datetime(last_hist_date):
            point["is_forecast"] = False
            history.append(point)
        else:
            point["is_forecast"] = True
            forecast.append(point)

    logger.info("Forecast complete: engine=%s, %d history points, %d forecast points", engine, len(history), len(forecast))
    return {"history": history, "forecast": forecast, "engine": engine}
