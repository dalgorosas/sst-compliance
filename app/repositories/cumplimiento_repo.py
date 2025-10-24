from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.cumplimiento import Cumplimiento, EstadoCumplimiento
from .base import BaseRepo


class CumplimientoRepo(BaseRepo[Cumplimiento]):
    def __init__(self) -> None:
        super().__init__(Cumplimiento)

    def por_empresa(self, db: Session, empresa_id: int) -> list[Cumplimiento]:
        stmt = select(Cumplimiento).where(Cumplimiento.empresa_id == empresa_id)
        return list(db.execute(stmt).scalars())

    def por_estado(self, db: Session, estado: EstadoCumplimiento) -> list[Cumplimiento]:
        stmt = select(Cumplimiento).where(Cumplimiento.estado == estado)
        return list(db.execute(stmt).scalars())