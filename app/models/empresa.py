from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Empresa(Base):
    __tablename__ = "empresas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(255), index=True)
    ruc: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    direccion: Mapped[str] = mapped_column(String(255))
    telefono: Mapped[str] = mapped_column(String(20), default="")
    correo_contacto: Mapped[str] = mapped_column(String(255), default="")
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    owner: Mapped["User"] = relationship("User", back_populates="empresas")
    suscripciones: Mapped[list["Suscripcion"]] = relationship(
        "Suscripcion", back_populates="empresa", cascade="all, delete-orphan"
    )
    reportes: Mapped[list["Reporte"]] = relationship(
        "Reporte", back_populates="empresa", cascade="all, delete-orphan"
    )
    cumplimientos: Mapped[list["Cumplimiento"]] = relationship(
        "Cumplimiento", back_populates="empresa", cascade="all, delete-orphan"
    )
    incidentes: Mapped[list["Incidente"]] = relationship(
        "Incidente", back_populates="empresa", cascade="all, delete-orphan"
    )
    auditorias: Mapped[list["Auditoria"]] = relationship(
        "Auditoria", back_populates="empresa", cascade="all, delete-orphan"
    )