from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.incidente import Incidente, SeveridadIncidente
from .base import BaseRepo


class IncidenteRepo(BaseRepo[Incidente]):
    def __init__(self) -> None:
        super().__init__(Incidente)

    def por_empresa(self, db: Session, empresa_id: int) -> list[Incidente]:
        stmt = select(Incidente).where(Incidente.empresa_id == empresa_id)
        return list(db.execute(stmt).scalars())

    def por_severidad(self, db: Session, severidad: SeveridadIncidente) -> list[Incidente]:
        stmt = select(Incidente).where(Incidente.severidad == severidad)
        return list(db.execute(stmt).scalars())