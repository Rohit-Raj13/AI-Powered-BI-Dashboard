"""
Insights Router
GET /insights
"""
import logging
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Query

from app.data_service import get_filtered_df
from app.ml.insight_engine import generate_insights
from app.schemas import InsightItem, InsightsResponse

router = APIRouter(prefix="/insights", tags=["AI Insights"])
logger = logging.getLogger(__name__)


@router.get("", response_model=InsightsResponse)
async def get_insights(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    payment_method: Optional[str] = Query(None),
):
    """
    Generate natural-language business insights from the dataset
    using rule-based templates.
    """
    df = get_filtered_df(start_date, end_date, category, payment_method)
    raw = generate_insights(df)

    return InsightsResponse(
        generated_at=datetime.utcnow().isoformat() + "Z",
        insights=[InsightItem(**i) for i in raw],
    )
