from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel

from app.models.pago import EstadoPago


class PagoBase(BaseModel):
    suscripcion_id: int
    monto: Decimal
    moneda: str = "USD"


class PagoRead(PagoBase):
    id: int
    referencia: str
    estado: EstadoPago
    registrado_en: datetime

    class Config:
        from_attributes = True