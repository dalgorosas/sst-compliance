from __future__ import annotations

import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class SeveridadIncidente(str, enum.Enum):
    BAJA = "baja"
    MEDIA = "media"
    ALTA = "alta"
    CRITICA = "critica"


class Incidente(Base):
    __tablename__ = "incidentes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    empresa_id: Mapped[int] = mapped_column(ForeignKey("empresas.id"))
    titulo: Mapped[str] = mapped_column(String(200))
    descripcion: Mapped[str] = mapped_column(Text)
    severidad: Mapped[SeveridadIncidente] = mapped_column(Enum(SeveridadIncidente))
    fecha: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    acciones_tomadas: Mapped[str] = mapped_column(Text, default="")

    empresa: Mapped["Empresa"] = relationship("Empresa", back_populates="incidentes")