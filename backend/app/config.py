import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "ecommerce_dataset_updated.csv"

API_TITLE = "AI-Powered BI Dashboard API"
API_VERSION = "1.0.0"
API_DESCRIPTION = "Backend API for e-commerce analytics, anomaly detection, forecasting, and AI insights."

CORS_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
]
