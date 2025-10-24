from __future__ import annotations

import logging
from collections.abc import Callable
from fastapi import FastAPI

from app.core.config import settings
from app.core.logging_config import configure_logging


logger = logging.getLogger(__name__)


def create_start_app_handler(app: FastAPI) -> Callable[[], None]:
    """Regresa un handler que inicializa recursos al arrancar FastAPI."""

    def start_app() -> None:
        configure_logging()
        settings.ensure_dirs()
        from app.tasks import register_default_tasks

        register_default_tasks()
        logger.info(
            "Aplicación %s iniciada en entorno %s", settings.APP_NAME, settings.ENV
        )

    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable[[], None]:
    """Regresa un handler que libera recursos al apagar FastAPI."""

    def stop_app() -> None:
        from app.tasks import scheduler

        scheduler.stop_all()
        logger.info("Aplicación %s detenida", settings.APP_NAME)

    return stop_app
