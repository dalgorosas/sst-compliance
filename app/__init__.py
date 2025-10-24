from __future__ import annotations

from fastapi import FastAPI

from app.api import router as api_router
from app.core.events import create_start_app_handler, create_stop_app_handler
from app.core.config import settings


def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)
    app.include_router(api_router)
    app.add_event_handler("startup", create_start_app_handler(app))
    app.add_event_handler("shutdown", create_stop_app_handler(app))
    return app
