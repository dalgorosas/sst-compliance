from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Reporte(Base):
    __tablename__ = "reportes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    empresa_id: Mapped[int] = mapped_column(ForeignKey("empresas.id"))
    titulo: Mapped[str] = mapped_column(String(255))
    descripcion: Mapped[str] = mapped_column(Text)
    generado_por: Mapped[str] = mapped_column(String(120), default="sistema")
    ruta_archivo: Mapped[str] = mapped_column(String(255), default="")
    generado_en: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    empresa: Mapped["Empresa"] = relationship("Empresa", back_populates="reportes")