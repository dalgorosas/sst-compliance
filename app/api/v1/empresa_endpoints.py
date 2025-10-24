from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.empresa_repo import EmpresaRepo
from app.schemas.empresa import EmpresaCreate, EmpresaRead, EmpresaUpdate
from app.utils.validators import validate_email, validate_ruc

router = APIRouter(prefix="/empresas", tags=["empresas"])


@router.post("", response_model=EmpresaRead, status_code=status.HTTP_201_CREATED)
def create_empresa(data: EmpresaCreate, db: Session = Depends(get_db)):
    if not validate_ruc(data.ruc):
        raise HTTPException(status_code=400, detail="RUC inválido")
    if data.correo_contacto and not validate_email(data.correo_contacto):
        raise HTTPException(status_code=400, detail="Correo de contacto inválido")
    repo = EmpresaRepo()
    if repo.get_by_ruc(db, data.ruc):
        raise HTTPException(status_code=400, detail="La empresa ya existe")
    return repo.create(db, **data.model_dump())


@router.get("", response_model=list[EmpresaRead])
def list_empresas(db: Session = Depends(get_db)):
    repo = EmpresaRepo()
    return repo.list(db)


@router.get("/{empresa_id}", response_model=EmpresaRead)
def get_empresa(empresa_id: int, db: Session = Depends(get_db)):
    repo = EmpresaRepo()
    empresa = repo.get(db, empresa_id)
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    return empresa


@router.patch("/{empresa_id}", response_model=EmpresaRead)
def update_empresa(empresa_id: int, data: EmpresaUpdate, db: Session = Depends(get_db)):
    repo = EmpresaRepo()
    empresa = repo.get(db, empresa_id)
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    payload = data.model_dump(exclude_unset=True)
    if "correo_contacto" in payload and payload["correo_contacto"] and not validate_email(payload["correo_contacto"]):
        raise HTTPException(status_code=400, detail="Correo de contacto inválido")
    return repo.update(db, empresa, **payload)
