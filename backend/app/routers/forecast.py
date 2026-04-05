"""
Forecasting Router
GET /forecast
"""
import logging
from typing import Optional

from fastapi import APIRouter, Query

from app.data_service import get_filtered_df
from app.ml.forecaster import run_forecast
from app.schemas import ForecastPoint, ForecastResponse

router = APIRouter(prefix="/forecast", tags=["Forecasting"])
logger = logging.getLogger(__name__)


@router.get("", response_model=ForecastResponse)
async def get_forecast(
    periods: int = Query(30, ge=7, le=90, description="Number of days to forecast"),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    payment_method: Optional[str] = Query(None),
):
    """
    Forecast daily revenue for the next N days (default 30).
    Returns historical fit + forecast with 95% confidence intervals.
    """
    df = get_filtered_df(start_date, end_date, category, payment_method)
    result = run_forecast(df, periods=periods)

    return ForecastResponse(
        metric="revenue",
        periods=periods,
        history=[ForecastPoint(**p) for p in result["history"]],
        forecast=[ForecastPoint(**p) for p in result["forecast"]],
    )
