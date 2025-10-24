from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.pago import Pago, EstadoPago
from .base import BaseRepo


class PagoRepo(BaseRepo[Pago]):
    def __init__(self) -> None:
        super().__init__(Pago)

    def por_suscripcion(self, db: Session, suscripcion_id: int) -> list[Pago]:
        stmt = select(Pago).where(Pago.suscripcion_id == suscripcion_id)
        return list(db.execute(stmt).scalars())

    def registrar_pago(self, db: Session, suscripcion_id: int, monto: float, referencia: str, moneda: str = "USD") -> Pago:
        return self.create(
            db,
            suscripcion_id=suscripcion_id,
            monto=monto,
            referencia=referencia,
            moneda=moneda,
            estado=EstadoPago.COMPLETADO,
        )