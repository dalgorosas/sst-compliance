from __future__ import annotations

from datetime import date, datetime, timedelta
from decimal import Decimal
from typing import Any

from sqlalchemy.orm import Session

from app.models.suscripcion import EstadoSuscripcion, PlanSuscripcion, Suscripcion
from app.repositories.suscripcion_repo import SuscripcionRepo
from app.services.payment_gateway import PaymentGateway


class SubscriptionManager:
    def __init__(self, repo: SuscripcionRepo | None = None, gateway: PaymentGateway | None = None) -> None:
        self.repo = repo or SuscripcionRepo()
        self.gateway = gateway or PaymentGateway()

    def create_subscription(
        self,
        db: Session,
        empresa_id: int,
        plan: PlanSuscripcion,
        monto: Decimal,
        periodo_meses: int = 12,
    ) -> Suscripcion:
        inicio = date.today()
        fin = inicio + timedelta(days=periodo_meses * 30)
        suscripcion = self.repo.create(
            db,
            empresa_id=empresa_id,
            plan=plan,
            estado=EstadoSuscripcion.PENDIENTE,
            inicio=inicio,
            fin=fin,
        )
        self.gateway.charge(db, suscripcion.id, monto)
        return self.repo.update(db, suscripcion, estado=EstadoSuscripcion.ACTIVA)

    def cancel_subscription(self, db: Session, suscripcion: Suscripcion) -> Suscripcion:
        return self.repo.update(db, suscripcion, estado=EstadoSuscripcion.CANCELADA)

    def generate_renewal_reminders(self, db: Session, reference: datetime) -> list[dict[str, Any]]:
        proximas = self.repo.proximas_a_vencer(db, reference.date())
        reminders: list[dict[str, Any]] = []
        for sus in proximas:
            correo = getattr(sus.empresa, "correo_contacto", "")
            reminders.append(
                {
                    "suscripcion_id": sus.id,
                    "empresa_id": sus.empresa_id,
                    "email": correo,
                    "subject": "Renovación de suscripción",
                    "body": f"La suscripción al plan {sus.plan} vence el {sus.fin}",
                }
            )
        return reminders

    def renew(self, db: Session, suscripcion: Suscripcion, meses: int, monto: Decimal) -> Suscripcion:
        nuevo_fin = suscripcion.fin + timedelta(days=meses * 30)
        self.gateway.charge(db, suscripcion.id, monto)
        return self.repo.update(db, suscripcion, fin=nuevo_fin, estado=EstadoSuscripcion.ACTIVA)