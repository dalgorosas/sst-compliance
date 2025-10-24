from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from pydantic import BaseModel, Field

from app.models.suscripcion import EstadoSuscripcion, PlanSuscripcion


class SuscripcionBase(BaseModel):
    empresa_id: int
    plan: PlanSuscripcion
    inicio: date
    fin: date
    renovacion_automatica: bool = True


class SuscripcionCreate(SuscripcionBase):
    monto: Decimal = Field(gt=0)


class SuscripcionRead(SuscripcionBase):
    id: int
    estado: EstadoSuscripcion
    created_at: datetime

    class Config:
        from_attributes = True