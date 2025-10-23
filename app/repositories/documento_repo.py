from sqlalchemy.orm import Session
from sqlalchemy import select, desc, func
from app.repositories.base import BaseRepo
from app.models.documento import Documento, DocumentoHistorial

class DocumentoRepo(BaseRepo[Documento]):
    def __init__(self) -> None:
        super().__init__(Documento)

    def listar(self, db: Session, etiqueta: str | None = None):
        q = select(Documento).order_by(desc(Documento.actualizado_en))
        if etiqueta:
            q = q.where(Documento.etiqueta == etiqueta)
        return db.execute(q).scalars().all()

    def historial(self, db: Session, doc_id: int):
        q = (
            select(DocumentoHistorial)
            .where(DocumentoHistorial.documento_id == doc_id)
            .order_by(desc(DocumentoHistorial.version))
        )
        return db.execute(q).scalars().all()

    def proxima_version(self, db: Session, doc_id: int) -> int:
        q = select(func.max(DocumentoHistorial.version)).where(DocumentoHistorial.documento_id == doc_id)
        latest = db.execute(q).scalar()
        return (latest or 0) + 1
