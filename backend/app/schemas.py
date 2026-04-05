"""
Pydantic schemas for all API request/response models.
"""
from typing import List, Optional
from pydantic import BaseModel


# ─── Metrics ─────────────────────────────────────────────────────────────────

class SummaryResponse(BaseModel):
    total_revenue: float
    total_orders: int
    unique_customers: int
    avg_order_value: float
    avg_discount_pct: float
    top_category: str
    top_payment_method: str
    revenue_change_wow: Optional[float] = None   # % week-over-week
    revenue_change_mom: Optional[float] = None   # % month-over-month


class TimeseriesPoint(BaseModel):
    period: str
    revenue: float
    orders: int
    avg_discount_pct: float


class TimeseriesResponse(BaseModel):
    granularity: str
    data: List[TimeseriesPoint]


# ─── Category Breakdown ───────────────────────────────────────────────────────

class CategoryBreakdown(BaseModel):
    category: str
    revenue: float
    orders: int
    share_pct: float


# ─── Payment Breakdown ────────────────────────────────────────────────────────

class PaymentBreakdown(BaseModel):
    payment_method: str
    orders: int
    share_pct: float


# ─── Anomaly ─────────────────────────────────────────────────────────────────

class AnomalyPoint(BaseModel):
    date: str
    revenue: float
    orders: int
    z_score: Optional[float] = None
    is_anomaly_zscore: bool
    is_anomaly_isoforest: bool
    is_anomaly: bool            # union of both methods
    severity: str               # "low" | "medium" | "high"
    severity_score: float       # 0-1
    explanation: str


class AnomalyResponse(BaseModel):
    total_anomalies: int
    anomalies: List[AnomalyPoint]
    all_dates: List[AnomalyPoint]   # full timeseries for chart overlay


# ─── Forecast ────────────────────────────────────────────────────────────────

class ForecastPoint(BaseModel):
    ds: str          # date string
    yhat: float
    yhat_lower: float
    yhat_upper: float
    is_forecast: bool


class ForecastResponse(BaseModel):
    metric: str
    periods: int
    history: List[ForecastPoint]
    forecast: List[ForecastPoint]


# ─── Insights ────────────────────────────────────────────────────────────────

class InsightItem(BaseModel):
    id: str
    type: str          # "trend" | "anomaly" | "category" | "payment" | "forecast"
    severity: str      # "info" | "warning" | "success" | "danger"
    title: str
    description: str
    value: Optional[str] = None


class InsightsResponse(BaseModel):
    generated_at: str
    insights: List[InsightItem]
