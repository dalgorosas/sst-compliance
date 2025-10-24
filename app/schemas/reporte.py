from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel


class ReporteBase(BaseModel):
    empresa_id: int
    titulo: str
    descripcion: str
    generado_por: str = "sistema"


class ReporteCreate(ReporteBase):
    pass


class ReporteRead(ReporteBase):
    id: int
    ruta_archivo: str | None = None
    generado_en: datetime

    class Config:
        from_attributes = True