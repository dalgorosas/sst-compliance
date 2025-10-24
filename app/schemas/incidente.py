from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel

from app.models.incidente import SeveridadIncidente


class IncidenteBase(BaseModel):
    empresa_id: int
    titulo: str
    descripcion: str
    severidad: SeveridadIncidente
    fecha: datetime | None = None
    acciones_tomadas: str | None = None


class IncidenteCreate(IncidenteBase):
    pass


class IncidenteRead(IncidenteBase):
    id: int

    class Config:
        from_attributes = True