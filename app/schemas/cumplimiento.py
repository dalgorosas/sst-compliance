from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel

from app.models.cumplimiento import EstadoCumplimiento


class CumplimientoBase(BaseModel):
    empresa_id: int
    normativa: str
    requisito: str
    estado: EstadoCumplimiento = EstadoCumplimiento.EN_PROCESO
    evidencia: str | None = None
    observaciones: str | None = None


class CumplimientoCreate(CumplimientoBase):
    pass


class CumplimientoRead(CumplimientoBase):
    id: int
    actualizado_en: datetime

    class Config:
        from_attributes = True