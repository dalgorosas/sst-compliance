from __future__ import annotations

from fastapi import APIRouter

from . import (
    admin_endpoints,
    archivos_endpoints,
    auditor_endpoints,
    auth_endpoints,
    empresa_endpoints,
    ia_endpoints,
    reportes_endpoints,
    suscripciones_endpoints,
    tecnico_endpoints,
)

router = APIRouter()

router.include_router(auth_endpoints.router)
router.include_router(empresa_endpoints.router)
router.include_router(suscripciones_endpoints.router)
router.include_router(reportes_endpoints.router)
router.include_router(archivos_endpoints.router)
router.include_router(ia_endpoints.router)
router.include_router(admin_endpoints.router)
router.include_router(auditor_endpoints.router)
router.include_router(tecnico_endpoints.router)
