"""
Rule-based Insight Engine
Generates human-readable AI-style insights from the dataset.
"""
import logging
from datetime import datetime
from typing import List

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def _pct(new: float, old: float) -> float:
    if old == 0:
        return 0.0
    return round(((new - old) / old) * 100, 1)


def generate_insights(df: pd.DataFrame) -> List[dict]:
    if df.empty:
        return []
    df = df.copy()
    df["purchase_date"] = pd.to_datetime(df["purchase_date"])
    insights = []

    # ── 1. Week-over-Week Revenue ────────────────────────────────────────────
    weekly = df.groupby(df["purchase_date"].dt.to_period("W"))["final_price"].sum()
    if len(weekly) >= 2:
        curr_w = float(weekly.iloc[-1])
        prev_w = float(weekly.iloc[-2])
        wow = _pct(curr_w, prev_w)
        direction = "increased" if wow >= 0 else "decreased"
        insights.append({
            "id": "wow_revenue",
            "type": "trend",
            "severity": "success" if wow >= 0 else "warning",
            "title": "Week-over-Week Revenue",
            "description": f"Revenue {direction} by {abs(wow)}% compared to last week (₹{curr_w:,.0f} vs ₹{prev_w:,.0f}).",
            "value": f"{'+' if wow >= 0 else ''}{wow}%",
        })

    # ── 2. Month-over-Month Revenue ──────────────────────────────────────────
    monthly = df.groupby(df["purchase_date"].dt.to_period("M"))["final_price"].sum()
    if len(monthly) >= 2:
        curr_m = float(monthly.iloc[-1])
        prev_m = float(monthly.iloc[-2])
        mom = _pct(curr_m, prev_m)
        direction = "grew" if mom >= 0 else "declined"
        insights.append({
            "id": "mom_revenue",
            "type": "trend",
            "severity": "success" if mom >= 5 else ("info" if mom >= 0 else "warning"),
            "title": "Month-over-Month Revenue",
            "description": f"Monthly revenue {direction} by {abs(mom)}% ({str(monthly.index[-2])} → {str(monthly.index[-1])}).",
            "value": f"{'+' if mom >= 0 else ''}{mom}%",
        })

    # ── 3. Top-performing category ───────────────────────────────────────────
    cat_rev = df.groupby("category")["final_price"].sum()
    top_cat = cat_rev.idxmax()
    top_cat_rev = float(cat_rev.max())
    total_rev = float(cat_rev.sum())
    share = round((top_cat_rev / total_rev) * 100, 1)
    insights.append({
        "id": "top_category",
        "type": "category",
        "severity": "info",
        "title": "Top Revenue Category",
        "description": f"'{top_cat}' leads all categories with ₹{top_cat_rev:,.0f} in revenue ({share}% share).",
        "value": top_cat,
    })

    # ── 4. Fastest-growing category (MoM) ───────────────────────────────────
    if len(monthly) >= 2:
        last_two = df[df["purchase_date"].dt.to_period("M") >= monthly.index[-2]]
        monthly_cat = last_two.groupby([last_two["purchase_date"].dt.to_period("M"), "category"])["final_price"].sum().unstack(fill_value=0)
        if monthly_cat.shape[0] >= 2:
            growth = _pct(float(monthly_cat.iloc[-1].max()), float(monthly_cat.iloc[-2].max()))
            fastest = monthly_cat.iloc[-1].idxmax()
            insights.append({
                "id": "fastest_category",
                "type": "category",
                "severity": "success" if growth > 0 else "warning",
                "title": "Fastest Growing Category",
                "description": f"'{fastest}' showed the highest MoM growth at {growth:+.1f}% this month.",
                "value": f"{growth:+.1f}%",
            })

    # ── 5. Most popular payment method ──────────────────────────────────────
    pm_counts = df["payment_method"].value_counts()
    top_pm = pm_counts.index[0]
    pm_share = round((pm_counts.iloc[0] / pm_counts.sum()) * 100, 1)
    insights.append({
        "id": "top_payment",
        "type": "payment",
        "severity": "info",
        "title": "Preferred Payment Method",
        "description": f"'{top_pm}' is the most used payment method ({pm_share}% of all orders).",
        "value": top_pm,
    })

    # ── 6. Discount impact ──────────────────────────────────────────────────
    avg_discount = round(float(df["discount_pct"].mean()), 1)
    total_discount_value = float((df["price"] - df["final_price"]).sum())
    insights.append({
        "id": "discount_impact",
        "type": "trend",
        "severity": "info",
        "title": "Discount Impact",
        "description": f"Average discount is {avg_discount}%, representing a total of ₹{total_discount_value:,.0f} in savings across all transactions.",
        "value": f"{avg_discount}%",
    })

    # ── 7. Peak day of week ──────────────────────────────────────────────────
    dow_rev = df.groupby("day_of_week")["final_price"].sum()
    peak_day = dow_rev.idxmax()
    insights.append({
        "id": "peak_day",
        "type": "trend",
        "severity": "info",
        "title": "Peak Sales Day",
        "description": f"'{peak_day}' consistently records the highest revenue (₹{float(dow_rev.max()):,.0f} total across dataset).",
        "value": peak_day,
    })

    # ── 8. Anomaly alert ────────────────────────────────────────────────────
    daily = df.groupby("date")["final_price"].sum()
    if len(daily) > 10:
        from scipy import stats as sp_stats
        z = np.abs(sp_stats.zscore(daily.values))
        n_anomalies = int((z > 2.5).sum())
        if n_anomalies > 0:
            worst_date = str(daily.index[np.argmax(z)])
            insights.append({
                "id": "anomaly_alert",
                "type": "anomaly",
                "severity": "danger",
                "title": "Anomalies Detected",
                "description": f"{n_anomalies} revenue anomaly/anomalies detected. Most significant spike/drop on {worst_date} (Z={np.max(z):.1f}σ). Review the Anomaly chart for details.",
                "value": str(n_anomalies),
            })

    logger.info("Generated %d insights", len(insights))
    return insights
