"""
Anomaly Detection Router
GET /anomaly/detect
"""
import logging
from typing import Optional

from fastapi import APIRouter, Query

from app.data_service import get_filtered_df
from app.ml.anomaly_detector import detect_anomalies
from app.schemas import AnomalyPoint, AnomalyResponse

router = APIRouter(prefix="/anomaly", tags=["Anomaly Detection"])
logger = logging.getLogger(__name__)


@router.get("/detect", response_model=AnomalyResponse)
async def detect(
    start_date: Optional[str] = Query(None, description="YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="YYYY-MM-DD"),
    category: Optional[str] = Query(None),
    payment_method: Optional[str] = Query(None),
):
    """
    Detect revenue anomalies using Z-score and Isolation Forest.
    Returns the full daily time-series with anomaly flags for chart overlay.
    """
    df = get_filtered_df(start_date, end_date, category, payment_method)
    results = detect_anomalies(df)

    all_points = [AnomalyPoint(**r) for r in results]
    anomaly_points = [p for p in all_points if p.is_anomaly]

    return AnomalyResponse(
        total_anomalies=len(anomaly_points),
        anomalies=anomaly_points,
        all_dates=all_points,
    )
