from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.reporte import Reporte
from .base import BaseRepo


class ReporteRepo(BaseRepo[Reporte]):
    def __init__(self) -> None:
        super().__init__(Reporte)

    def por_empresa(self, db: Session, empresa_id: int) -> list[Reporte]:
        stmt = select(Reporte).where(Reporte.empresa_id == empresa_id)
        return list(db.execute(stmt).scalars())