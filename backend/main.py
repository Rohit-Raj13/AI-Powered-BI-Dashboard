"""
FastAPI Application Entry Point
Run: uvicorn main:app --reload --port 8000
"""
import logging
import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import API_DESCRIPTION, API_TITLE, API_VERSION, CORS_ORIGINS
from app.data_service import _load_raw  # warm cache on startup
from app.routers import anomaly, forecast, insights, metrics
from app.routers import websocket as ws_router

# ── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("main")

# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(
    title=API_TITLE,
    version=API_VERSION,
    description=API_DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Request timing middleware ─────────────────────────────────────────────────
@app.middleware("http")
async def add_process_time(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    elapsed = round((time.time() - start) * 1000, 2)
    response.headers["X-Process-Time-Ms"] = str(elapsed)
    return response


# ── Global error handler ──────────────────────────────────────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error("Unhandled error on %s: %s", request.url, exc, exc_info=True)
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error", "error": str(exc)})


# ── Startup event ─────────────────────────────────────────────────────────────
@app.on_event("startup")
async def startup():
    logger.info("Warming up data cache...")
    _load_raw()
    logger.info("Data cache ready. API is live.")


# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(metrics.router)
app.include_router(anomaly.router)
app.include_router(forecast.router)
app.include_router(insights.router)
app.include_router(ws_router.router)


# ── Health check ──────────────────────────────────────────────────────────────
@app.get("/health", tags=["Health"])
async def health():
    return {"status": "ok", "version": API_VERSION}


@app.get("/", tags=["Health"])
async def root():
    return {
        "message": "AI-Powered BI Dashboard API",
        "docs": "/docs",
        "version": API_VERSION,
    }
