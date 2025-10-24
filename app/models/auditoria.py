from __future__ import annotations

import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class EstadoAuditoria(str, enum.Enum):
    PROGRAMADA = "programada"
    EN_PROCESO = "en_proceso"
    FINALIZADA = "finalizada"
    CANCELADA = "cancelada"


class Auditoria(Base):
    __tablename__ = "auditorias"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    empresa_id: Mapped[int] = mapped_column(ForeignKey("empresas.id"))
    auditor_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    fecha_programada: Mapped[datetime] = mapped_column(DateTime)
    estado: Mapped[EstadoAuditoria] = mapped_column(Enum(EstadoAuditoria), default=EstadoAuditoria.PROGRAMADA)
    hallazgos: Mapped[str] = mapped_column(Text, default="")
    recomendaciones: Mapped[str] = mapped_column(Text, default="")

    empresa: Mapped["Empresa"] = relationship("Empresa", back_populates="auditorias")
    auditor: Mapped["User"] = relationship("User", back_populates="auditorias")
    