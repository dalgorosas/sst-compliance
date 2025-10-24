from __future__ import annotations

import logging
from decimal import Decimal
from typing import TypedDict

from app.repositories.pago_repo import PagoRepo
from app.utils.crypto import generate_token

logger = logging.getLogger(__name__)


class PaymentResult(TypedDict):
    success: bool
    reference: str
    message: str


class PaymentGateway:
    """Simulación de un gateway de pagos externo."""

    def __init__(self, repo: PagoRepo | None = None) -> None:
        self.repo = repo or PagoRepo()

    def charge(self, db, suscripcion_id: int, monto: Decimal, moneda: str = "USD") -> PaymentResult:
        referencia = generate_token(12)
        self.repo.registrar_pago(
            db,
            suscripcion_id=suscripcion_id,
            monto=float(monto),
            referencia=referencia,
            moneda=moneda,
        )
        logger.info("Pago registrado %s por %s %s", referencia, monto, moneda)
        return PaymentResult(success=True, reference=referencia, message="Pago procesado")