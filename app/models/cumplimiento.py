from __future__ import annotations

import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class EstadoCumplimiento(str, enum.Enum):
    CUMPLIDO = "cumplido"
    EN_PROCESO = "en_proceso"
    NO_CUMPLIDO = "no_cumplido"


class Cumplimiento(Base):
    __tablename__ = "cumplimientos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    empresa_id: Mapped[int] = mapped_column(ForeignKey("empresas.id"))
    normativa: Mapped[str] = mapped_column(String(120))
    requisito: Mapped[str] = mapped_column(String(120))
    estado: Mapped[EstadoCumplimiento] = mapped_column(Enum(EstadoCumplimiento), default=EstadoCumplimiento.EN_PROCESO)
    evidencia: Mapped[str] = mapped_column(String(255), default="")
    observaciones: Mapped[str] = mapped_column(Text, default="")
    actualizado_en: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    empresa: Mapped["Empresa"] = relationship("Empresa", back_populates="cumplimientos")
    