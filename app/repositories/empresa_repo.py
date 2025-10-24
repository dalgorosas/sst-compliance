from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.empresa import Empresa
from .base import BaseRepo


class EmpresaRepo(BaseRepo[Empresa]):
    def __init__(self) -> None:
        super().__init__(Empresa)

    def get_by_ruc(self, db: Session, ruc: str) -> Empresa | None:
        stmt = select(Empresa).where(Empresa.ruc == ruc)
        return db.execute(stmt).scalar_one_or_none()

    def search(self, db: Session, query: str) -> list[Empresa]:
        stmt = select(Empresa).where(Empresa.nombre.ilike(f"%{query}%"))
        return list(db.execute(stmt).scalars())