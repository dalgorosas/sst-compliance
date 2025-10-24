"""Registro de tareas programadas de la plataforma."""

from __future__ import annotations

from datetime import timedelta

from .scheduler import scheduler
from . import workers


def register_default_tasks() -> None:
    scheduler.add_task(
        "generate_periodic_reports", timedelta(hours=6), workers.generate_periodic_reports
    )
    scheduler.add_task(
        "check_subscription_renewals", timedelta(days=1), workers.check_subscription_renewals
    )


__all__ = ["scheduler", "register_default_tasks"]