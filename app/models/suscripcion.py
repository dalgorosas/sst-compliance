from __future__ import annotations

import enum
from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, Enum, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class EstadoSuscripcion(str, enum.Enum):
    ACTIVA = "activa"
    PENDIENTE = "pendiente"
    SUSPENDIDA = "suspendida"
    CANCELADA = "cancelada"


class PlanSuscripcion(str, enum.Enum):
    BASIC = "basic"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"


class Suscripcion(Base):
    __tablename__ = "suscripciones"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    empresa_id: Mapped[int] = mapped_column(ForeignKey("empresas.id"))
    plan: Mapped[PlanSuscripcion] = mapped_column(Enum(PlanSuscripcion))
    estado: Mapped[EstadoSuscripcion] = mapped_column(
        Enum(EstadoSuscripcion), default=EstadoSuscripcion.PENDIENTE
    )
    inicio: Mapped[date] = mapped_column(Date)
    fin: Mapped[date] = mapped_column(Date)
    renovacion_automatica: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    empresa: Mapped["Empresa"] = relationship("Empresa", back_populates="suscripciones")
    pagos: Mapped[list["Pago"]] = relationship(
        "Pago", back_populates="suscripcion", cascade="all, delete-orphan"
    )