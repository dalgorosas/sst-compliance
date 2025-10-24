from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.cumplimiento_repo import CumplimientoRepo
from app.repositories.empresa_repo import EmpresaRepo
from app.repositories.incidente_repo import IncidenteRepo
from app.services.ia_analyzer import IAAnalyzer

router = APIRouter(prefix="/ia", tags=["ia"])


@router.get("/{empresa_id}/analisis")
def analizar_empresa(empresa_id: int, db: Session = Depends(get_db)):
    empresa_repo = EmpresaRepo()
    empresa = empresa_repo.get(db, empresa_id)
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    cumplimientos = CumplimientoRepo().por_empresa(db, empresa_id)
    incidentes = IncidenteRepo().por_empresa(db, empresa_id)
    analyzer = IAAnalyzer()
    score = analyzer.risk_score(cumplimientos, incidentes)
    recomendaciones = analyzer.recommendations(cumplimientos, incidentes)
    return {
        "empresa": empresa.nombre,
        "score": score,
        "recomendaciones": recomendaciones,
    }
    