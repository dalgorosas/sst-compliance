from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.types import EmailStr


class EmpresaBase(BaseModel):
    nombre: str = Field(min_length=3)
    ruc: str = Field(min_length=9, max_length=13)
    direccion: str
    telefono: str | None = None
    correo_contacto: EmailStr | None = None
    owner_id: int


class EmpresaCreate(EmpresaBase):
    pass


class EmpresaUpdate(BaseModel):
    nombre: str | None = None
    direccion: str | None = None
    telefono: str | None = None
    correo_contacto: EmailStr | None = None


class EmpresaRead(EmpresaBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True