"""Main FastAPI application."""
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .core.config import get_settings
from .core.logging import configure_logging
from .core.rate_limit import rate_limit_middleware
from .db.engine import close_db, init_db
from .routers import auth, files, health, notifications, requests, rewards, slots, ws
from .workers.scheduler import init_scheduler

configure_logging()
settings = get_settings()
os.makedirs(settings.upload_dir, exist_ok=True)

app = FastAPI(title="SWMRA API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.middleware("http")(rate_limit_middleware)

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(requests.router)
app.include_router(slots.router)
app.include_router(files.router)
app.include_router(notifications.router)
app.include_router(rewards.router)
app.mount("/uploads", StaticFiles(directory=settings.upload_dir), name="uploads")
app.include_router(ws.router)


@app.on_event("startup")
async def startup_event() -> None:
    """Initialize database and scheduler on startup."""
    await init_db()
    init_scheduler()


@app.on_event("shutdown")
async def shutdown_event() -> None:
    """Close database connections on shutdown."""
    await close_db()
