"""
WebSocket Router — broadcasts live metrics updates every 5 seconds.
Provides a basic pub/sub channel for real-time dashboard refresh.
"""
import asyncio
import json
import logging
from datetime import datetime

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.data_service import get_df

router = APIRouter(tags=["WebSocket"])
logger = logging.getLogger(__name__)


class ConnectionManager:
    def __init__(self):
        self.active: list[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active.append(ws)
        logger.info("WS client connected. Total: %d", len(self.active))

    def disconnect(self, ws: WebSocket):
        self.active.remove(ws)
        logger.info("WS client disconnected. Total: %d", len(self.active))

    async def broadcast(self, message: str):
        dead = []
        for ws in self.active:
            try:
                await ws.send_text(message)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.disconnect(ws)


manager = ConnectionManager()


def _build_live_snapshot() -> dict:
    df = get_df()
    latest_date = str(df["date"].max())
    latest_day = df[df["date"] == df["date"].max()]
    return {
        "ts": datetime.utcnow().isoformat() + "Z",
        "latest_date": latest_date,
        "daily_revenue": round(float(latest_day["final_price"].sum()), 2),
        "daily_orders": int(len(latest_day)),
        "total_revenue": round(float(df["final_price"].sum()), 2),
        "total_orders": int(len(df)),
    }


@router.websocket("/ws/live")
async def websocket_endpoint(ws: WebSocket):
    await manager.connect(ws)
    try:
        while True:
            snapshot = _build_live_snapshot()
            await ws.send_text(json.dumps(snapshot))
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        manager.disconnect(ws)
    except Exception as e:
        logger.error("WS error: %s", e)
        manager.disconnect(ws)
