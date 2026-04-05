"""
Anomaly Detection Service
- Method 1: Z-score on daily revenue (statistical)
- Method 2: Isolation Forest (ML-based)
Returns merged results with severity scoring and explanations.
"""
import logging
from typing import List, Tuple

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger(__name__)

ZSCORE_THRESHOLD = 2.5
ISOFOREST_CONTAMINATION = 0.05


def _daily_revenue(df: pd.DataFrame) -> pd.DataFrame:
    daily = (
        df.groupby("date")
        .agg(revenue=("final_price", "sum"), orders=("product_id", "count"))
        .reset_index()
        .sort_values("date")
    )
    daily["date"] = daily["date"].astype(str)
    return daily


def _zscore_detect(daily: pd.DataFrame) -> pd.DataFrame:
    daily = daily.copy()
    z = np.abs(stats.zscore(daily["revenue"]))
    daily["z_score"] = z
    daily["is_anomaly_zscore"] = z > ZSCORE_THRESHOLD
    return daily


def _isoforest_detect(daily: pd.DataFrame) -> pd.DataFrame:
    daily = daily.copy()
    features = daily[["revenue", "orders"]].values
    scaler = StandardScaler()
    X = scaler.fit_transform(features)

    model = IsolationForest(contamination=ISOFOREST_CONTAMINATION, random_state=42, n_estimators=100)
    preds = model.fit_predict(X)
    scores = model.decision_function(X)

    daily["is_anomaly_isoforest"] = preds == -1
    # Normalise anomaly score to 0-1 (higher = more anomalous)
    daily["iso_score"] = 1 - (scores - scores.min()) / (scores.max() - scores.min() + 1e-9)
    return daily


def _severity(row: pd.Series) -> Tuple[str, float]:
    score = max(
        (abs(row.get("z_score", 0)) / (ZSCORE_THRESHOLD * 2)),
        float(row.get("iso_score", 0)),
    )
    score = min(score, 1.0)
    if score > 0.75:
        return "high", score
    elif score > 0.45:
        return "medium", score
    else:
        return "low", score


def _explanation(row: pd.Series, mean_rev: float) -> str:
    pct = ((row["revenue"] - mean_rev) / mean_rev) * 100
    direction = "spike" if pct > 0 else "drop"
    methods = []
    if row.get("is_anomaly_zscore"):
        methods.append(f"Z-score={row['z_score']:.1f}σ")
    if row.get("is_anomaly_isoforest"):
        methods.append("Isolation Forest")
    method_str = " & ".join(methods) if methods else "statistical heuristic"
    return (
        f"Revenue {direction} of {abs(pct):.1f}% vs baseline "
        f"(₹{row['revenue']:,.0f} vs avg ₹{mean_rev:,.0f}). "
        f"Detected by: {method_str}."
    )


def detect_anomalies(df: pd.DataFrame) -> List[dict]:
    daily = _daily_revenue(df)
    if len(daily) < 10:
        return []

    daily = _zscore_detect(daily)
    daily = _isoforest_detect(daily)
    daily["is_anomaly"] = daily["is_anomaly_zscore"] | daily["is_anomaly_isoforest"]

    mean_rev = daily["revenue"].mean()

    results = []
    for _, row in daily.iterrows():
        sev_label, sev_score = _severity(row)
        explanation = _explanation(row, mean_rev) if row["is_anomaly"] else "No anomaly detected."
        results.append({
            "date": row["date"],
            "revenue": round(float(row["revenue"]), 2),
            "orders": int(row["orders"]),
            "z_score": round(float(row.get("z_score", 0)), 3),
            "is_anomaly_zscore": bool(row["is_anomaly_zscore"]),
            "is_anomaly_isoforest": bool(row["is_anomaly_isoforest"]),
            "is_anomaly": bool(row["is_anomaly"]),
            "severity": sev_label,
            "severity_score": round(sev_score, 4),
            "explanation": explanation,
        })

    logger.info("Anomaly detection complete: %d anomalies found", sum(r["is_anomaly"] for r in results))
    return results
