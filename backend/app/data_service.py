"""
Data Service — loads & caches the e-commerce CSV once at startup.
All routers call get_filtered_df() to query data.
"""
import logging
from functools import lru_cache
from typing import Optional

import pandas as pd
from fastapi import HTTPException

from app.config import DATA_PATH

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def _load_raw() -> pd.DataFrame:
    """Load CSV once and parse dates."""
    logger.info("Loading dataset from %s", DATA_PATH)
    df = pd.read_csv(DATA_PATH)

    # Normalise column names
    df.columns = [c.strip() for c in df.columns]
    df.rename(columns={
        "Price (Rs.)": "price",
        "Discount (%)": "discount_pct",
        "Final_Price(Rs.)": "final_price",
        "Payment_Method": "payment_method",
        "Purchase_Date": "purchase_date",
        "Category": "category",
        "User_ID": "user_id",
        "Product_ID": "product_id",
    }, inplace=True)

    df["purchase_date"] = pd.to_datetime(df["purchase_date"], dayfirst=True)
    df["date"] = df["purchase_date"].dt.date
    df["month"] = df["purchase_date"].dt.to_period("M").astype(str)
    df["week"] = df["purchase_date"].dt.to_period("W").astype(str)
    df["day_of_week"] = df["purchase_date"].dt.day_name()
    df["discount_amount"] = df["price"] - df["final_price"]

    logger.info("Dataset loaded: %d rows", len(df))
    return df


def get_df() -> pd.DataFrame:
    return _load_raw().copy()


def get_filtered_df(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    category: Optional[str] = None,
    payment_method: Optional[str] = None,
) -> pd.DataFrame:
    df = _load_raw().copy()

    if start_date:
        try:
            df = df[df["purchase_date"] >= pd.to_datetime(start_date)]
        except Exception:
            raise HTTPException(status_code=400, detail=f"Invalid start_date format: {start_date}")
    if end_date:
        try:
            df = df[df["purchase_date"] <= pd.to_datetime(end_date)]
        except Exception:
            raise HTTPException(status_code=400, detail=f"Invalid end_date format: {end_date}")
    if category and category.lower() != "all":
        df = df[df["category"].str.lower() == category.lower()]
    if payment_method and payment_method.lower() != "all":
        df = df[df["payment_method"].str.lower() == payment_method.lower()]

    return df
