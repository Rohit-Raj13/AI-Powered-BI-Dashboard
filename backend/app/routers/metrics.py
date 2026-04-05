"""
Metrics Router
GET /metrics/summary   — KPI summary
GET /metrics/timeseries — aggregated time-series
GET /metrics/categories — revenue by category
GET /metrics/payments   — order count by payment method
"""
import logging
from typing import Optional

from fastapi import APIRouter, Query

from app.data_service import get_filtered_df
from app.schemas import (
    CategoryBreakdown,
    PaymentBreakdown,
    SummaryResponse,
    TimeseriesPoint,
    TimeseriesResponse,
)

router = APIRouter(prefix="/metrics", tags=["Metrics"])
logger = logging.getLogger(__name__)


@router.get("/summary", response_model=SummaryResponse)
async def get_summary(
    start_date: Optional[str] = Query(None, description="YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="YYYY-MM-DD"),
    category: Optional[str] = Query(None),
    payment_method: Optional[str] = Query(None),
):
    """Return high-level KPI metrics."""
    df = get_filtered_df(start_date, end_date, category, payment_method)

    if df.empty:
        return SummaryResponse(
            total_revenue=0, total_orders=0, unique_customers=0,
            avg_order_value=0, avg_discount_pct=0,
            top_category="N/A", top_payment_method="N/A",
        )

    total_revenue = round(float(df["final_price"].sum()), 2)
    total_orders = len(df)
    unique_customers = int(df["user_id"].nunique())
    avg_order_value = round(total_revenue / total_orders, 2) if total_orders else 0
    avg_discount_pct = round(float(df["discount_pct"].mean()), 1)
    top_category = str(df.groupby("category")["final_price"].sum().idxmax())
    top_payment_method = str(df["payment_method"].value_counts().idxmax())

    # WoW & MoM
    import pandas as pd
    df["purchase_date"] = pd.to_datetime(df["purchase_date"])
    weekly = df.groupby(df["purchase_date"].dt.to_period("W"))["final_price"].sum()
    monthly = df.groupby(df["purchase_date"].dt.to_period("M"))["final_price"].sum()

    wow = None
    if len(weekly) >= 2:
        cw, pw = float(weekly.iloc[-1]), float(weekly.iloc[-2])
        wow = round(((cw - pw) / pw) * 100, 1) if pw else None

    mom = None
    if len(monthly) >= 2:
        cm, pm_ = float(monthly.iloc[-1]), float(monthly.iloc[-2])
        mom = round(((cm - pm_) / pm_) * 100, 1) if pm_ else None

    return SummaryResponse(
        total_revenue=total_revenue,
        total_orders=total_orders,
        unique_customers=unique_customers,
        avg_order_value=avg_order_value,
        avg_discount_pct=avg_discount_pct,
        top_category=top_category,
        top_payment_method=top_payment_method,
        revenue_change_wow=wow,
        revenue_change_mom=mom,
    )


@router.get("/timeseries", response_model=TimeseriesResponse)
async def get_timeseries(
    granularity: str = Query("daily", enum=["daily", "weekly", "monthly"]),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    payment_method: Optional[str] = Query(None),
):
    """Return time-series of revenue & orders at chosen granularity."""
    import pandas as pd
    df = get_filtered_df(start_date, end_date, category, payment_method)
    df["purchase_date"] = pd.to_datetime(df["purchase_date"])

    if granularity == "monthly":
        df["period"] = df["purchase_date"].dt.to_period("M").astype(str)
    elif granularity == "weekly":
        df["period"] = df["purchase_date"].dt.to_period("W").astype(str)
    else:
        df["period"] = df["purchase_date"].dt.date.astype(str)

    grouped = (
        df.groupby("period")
        .agg(revenue=("final_price", "sum"), orders=("product_id", "count"), avg_discount_pct=("discount_pct", "mean"))
        .reset_index()
        .sort_values("period")
    )

    data = [
        TimeseriesPoint(
            period=row["period"],
            revenue=round(float(row["revenue"]), 2),
            orders=int(row["orders"]),
            avg_discount_pct=round(float(row["avg_discount_pct"]), 1),
        )
        for _, row in grouped.iterrows()
    ]

    return TimeseriesResponse(granularity=granularity, data=data)


@router.get("/categories", response_model=list[CategoryBreakdown])
async def get_categories(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    payment_method: Optional[str] = Query(None),
):
    """Revenue breakdown by category."""
    df = get_filtered_df(start_date, end_date, None, payment_method)
    cat_rev = df.groupby("category")["final_price"].sum()
    cat_orders = df.groupby("category")["product_id"].count()
    total = float(cat_rev.sum())

    return [
        CategoryBreakdown(
            category=cat,
            revenue=round(float(cat_rev[cat]), 2),
            orders=int(cat_orders[cat]),
            share_pct=round((float(cat_rev[cat]) / total) * 100, 1) if total else 0,
        )
        for cat in cat_rev.sort_values(ascending=False).index
    ]


@router.get("/payments", response_model=list[PaymentBreakdown])
async def get_payments(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
):
    """Order count breakdown by payment method."""
    df = get_filtered_df(start_date, end_date, category, None)
    pm_counts = df["payment_method"].value_counts()
    total = pm_counts.sum()

    return [
        PaymentBreakdown(
            payment_method=pm,
            orders=int(count),
            share_pct=round((int(count) / total) * 100, 1) if total else 0,
        )
        for pm, count in pm_counts.items()
    ]
