from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.empresa_repo import EmpresaRepo
from app.repositories.reporte_repo import ReporteRepo
from app.schemas.reporte import ReporteRead
from app.services.report_builder import ReportBuilder

router = APIRouter(prefix="/reportes", tags=["reportes"])


@router.get("", response_model=list[ReporteRead])
def list_reportes(db: Session = Depends(get_db)):
    repo = ReporteRepo()
    return repo.list(db)


@router.post("/{empresa_id}", response_model=ReporteRead)
def generate_reporte(empresa_id: int, db: Session = Depends(get_db)):
    empresa_repo = EmpresaRepo()
    if not empresa_repo.get(db, empresa_id):
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    builder = ReportBuilder()
    return builder.build_report(db, empresa_id, generado_por="api")


@router.get("/{empresa_id}/export")
def export_context(empresa_id: int, db: Session = Depends(get_db)):
    empresa_repo = EmpresaRepo()
    if not empresa_repo.get(db, empresa_id):
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    builder = ReportBuilder()
    return builder.export_context(db, empresa_id)
