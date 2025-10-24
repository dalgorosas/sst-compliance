from __future__ import annotations

import enum
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class EstadoPago(str, enum.Enum):
    PENDIENTE = "pendiente"
    COMPLETADO = "completado"
    FALLIDO = "fallido"


class Pago(Base):
    __tablename__ = "pagos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    suscripcion_id: Mapped[int] = mapped_column(ForeignKey("suscripciones.id"))
    referencia: Mapped[str] = mapped_column(String(64), unique=True)
    monto: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    moneda: Mapped[str] = mapped_column(String(5), default="USD")
    estado: Mapped[EstadoPago] = mapped_column(Enum(EstadoPago), default=EstadoPago.PENDIENTE)
    registrado_en: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    suscripcion: Mapped["Suscripcion"] = relationship("Suscripcion", back_populates="pagos")