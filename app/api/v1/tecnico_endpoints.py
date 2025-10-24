from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.empresa_repo import EmpresaRepo
from app.repositories.incidente_repo import IncidenteRepo
from app.schemas.incidente import IncidenteRead

router = APIRouter(prefix="/tecnico", tags=["tecnico"])


@router.get("/{empresa_id}/incidentes", response_model=list[IncidenteRead])
def listar_incidentes(empresa_id: int, db: Session = Depends(get_db)):
    empresa_repo = EmpresaRepo()
    if not empresa_repo.get(db, empresa_id):
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    repo = IncidenteRepo()
    return repo.por_empresa(db, empresa_id)
