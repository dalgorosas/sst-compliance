from __future__ import annotations

from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.suscripcion import Suscripcion, EstadoSuscripcion
from .base import BaseRepo


class SuscripcionRepo(BaseRepo[Suscripcion]):
    def __init__(self) -> None:
        super().__init__(Suscripcion)

    def activas(self, db: Session) -> list[Suscripcion]:
        stmt = select(Suscripcion).where(Suscripcion.estado == EstadoSuscripcion.ACTIVA)
        return list(db.execute(stmt).scalars())

    def proximas_a_vencer(self, db: Session, referencia: date) -> list[Suscripcion]:
        stmt = select(Suscripcion).where(Suscripcion.fin <= referencia)
        return list(db.execute(stmt).scalars())