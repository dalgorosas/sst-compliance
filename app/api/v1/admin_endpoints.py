from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.empresa_repo import EmpresaRepo
from app.repositories.reporte_repo import ReporteRepo
from app.repositories.suscripcion_repo import SuscripcionRepo
from app.repositories.user_repo import UserRepo

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/overview")
def overview(db: Session = Depends(get_db)):
    empresa_repo = EmpresaRepo()
    suscripcion_repo = SuscripcionRepo()
    user_repo = UserRepo()
    reporte_repo = ReporteRepo()
    return {
        "empresas": len(empresa_repo.list(db)),
        "suscripciones": len(suscripcion_repo.list(db)),
        "usuarios": len(user_repo.list(db)),
        "reportes": len(reporte_repo.list(db)),
    }
    