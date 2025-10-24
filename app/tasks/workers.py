from __future__ import annotations

import logging
from datetime import datetime

from app.services.alerting import AlertService
from app.services.report_builder import ReportBuilder
from app.services.subscription_manager import SubscriptionManager

logger = logging.getLogger(__name__)


def generate_periodic_reports() -> None:
    """Genera reportes resumidos para todas las empresas activas."""

    builder = ReportBuilder()
    reports = builder.build_scheduled_reports()
    logger.info("Reportes generados: %s", len(reports))


def check_subscription_renewals() -> None:
    """Verifica suscripciones próximas a vencer y genera recordatorios."""

    manager = SubscriptionManager()
    from app.db.session import SessionLocal

    with SessionLocal() as db:
        reminders = manager.generate_renewal_reminders(db, reference=datetime.utcnow())
        alert = AlertService()
        for reminder in reminders:
            alert.send_email(reminder["email"], reminder["subject"], reminder["body"])
    logger.info("Recordatorios enviados: %s", len(reminders))