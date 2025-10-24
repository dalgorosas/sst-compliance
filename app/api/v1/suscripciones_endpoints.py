from __future__ import annotations

from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.suscripcion_repo import SuscripcionRepo
from app.schemas.suscripcion import SuscripcionCreate, SuscripcionRead
from app.services.subscription_manager import SubscriptionManager

router = APIRouter(prefix="/suscripciones", tags=["suscripciones"])


@router.post("", response_model=SuscripcionRead, status_code=status.HTTP_201_CREATED)
def create_suscripcion(payload: SuscripcionCreate, db: Session = Depends(get_db)):
    manager = SubscriptionManager()
    suscripcion = manager.create_subscription(
        db,
        empresa_id=payload.empresa_id,
        plan=payload.plan,
        monto=Decimal(payload.monto),
        periodo_meses=(payload.fin - payload.inicio).days // 30 or 12,
    )
    return suscripcion


@router.get("", response_model=list[SuscripcionRead])
def list_suscripciones(db: Session = Depends(get_db)):
    repo = SuscripcionRepo()
    return repo.list(db)


@router.post("/{suscripcion_id}/cancel", response_model=SuscripcionRead)
def cancel_suscripcion(suscripcion_id: int, db: Session = Depends(get_db)):
    repo = SuscripcionRepo()
    manager = SubscriptionManager(repo=repo)
    suscripcion = repo.get(db, suscripcion_id)
    if not suscripcion:
        raise HTTPException(status_code=404, detail="Suscripción no encontrada")
    return manager.cancel_subscription(db, suscripcion)


@router.post("/{suscripcion_id}/renew", response_model=SuscripcionRead)
def renew_suscripcion(suscripcion_id: int, meses: int, monto: Decimal, db: Session = Depends(get_db)):
    repo = SuscripcionRepo()
    manager = SubscriptionManager(repo=repo)
    suscripcion = repo.get(db, suscripcion_id)
    if not suscripcion:
        raise HTTPException(status_code=404, detail="Suscripción no encontrada")
    return manager.renew(db, suscripcion, meses, monto)
