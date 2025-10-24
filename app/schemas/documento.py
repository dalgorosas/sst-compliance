from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel


class DocumentoBase(BaseModel):
    nombre: str
    etiqueta: str
    ruta_relativa: str
    mimetype: str = "application/pdf"


class DocumentoRead(DocumentoBase):
    id: int
    tamano_bytes: int
    hash_sha256: str
    creado_en: datetime
    actualizado_en: datetime

    class Config:
        from_attributes = True


class DocumentoHistorialRead(BaseModel):
    version: int
    origen: str
    descripcion: str
    generado_por: str
    ruta_relativa: str
    hash_sha256: str
    creado_en: datetime

    class Config:
        from_attributes = True