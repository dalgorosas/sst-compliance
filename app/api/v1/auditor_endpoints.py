from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.cumplimiento_repo import CumplimientoRepo
from app.repositories.empresa_repo import EmpresaRepo
from app.repositories.incidente_repo import IncidenteRepo
from app.services.compliance_engine import ComplianceEngine

router = APIRouter(prefix="/auditor", tags=["auditor"])


@router.get("/{empresa_id}/resumen")
def resumen_cumplimiento(empresa_id: int, db: Session = Depends(get_db)):
    empresa_repo = EmpresaRepo()
    if not empresa_repo.get(db, empresa_id):
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    cumplimiento_repo = CumplimientoRepo()
    incidente_repo = IncidenteRepo()
    engine = ComplianceEngine()
    cumplimientos = cumplimiento_repo.por_empresa(db, empresa_id)
    incidentes = incidente_repo.por_empresa(db, empresa_id)
    return engine.evaluate_company(cumplimientos, incidentes)
