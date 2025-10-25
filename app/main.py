# app/main.py
from pathlib import Path
from typing import Any

from fastapi import FastAPI

from app.core.config import settings
from app.models.documento import Documento


def _get_storage_path() -> Path:
    return Path(settings.PDF_STORAGE_DIR)


def _resolve_pdf_path(documento: Documento) -> Path:
    storage_dir = _get_storage_path()
    candidate = Path(documento.ruta_relativa)
    possibilities = [candidate]

    if not candidate.is_absolute():
        possibilities.append(storage_dir / candidate)
        possibilities.append(storage_dir / candidate.name)

    for path in possibilities:
        if path.exists():
            return path

    # En última instancia devolvemos la ruta dentro del directorio de PDFs
    return storage_dir / (candidate.name or candidate)


def _document_payload(documento: Documento) -> dict[str, Any]:
    pdf_path = _resolve_pdf_path(documento)
    archivo_publico = pdf_path.name if pdf_path.name else Path(documento.ruta_relativa).name

    return {
        "id": documento.id,
        "nombre": documento.nombre,
        "etiqueta": documento.etiqueta,
        "ruta_relativa": documento.ruta_relativa,
        "archivo": archivo_publico,
        "mimetype": documento.mimetype,
        "tamano_bytes": documento.tamano_bytes,
        "hash_sha256": documento.hash_sha256,
        "creado_en": documento.creado_en,
        "actualizado_en": documento.actualizado_en,
    }


def create_app() -> FastAPI:
    # Mueve efectos de inicio aquí para evitar que se ejecuten al importar el módulo
    settings.ensure_dirs()

    app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

    @app.get("/", include_in_schema=False)
    def root():
        return {"app": settings.APP_NAME, "status": "ok"}

    @app.get("/health", include_in_schema=False)
    def health():
        return {"status": "ok"}

    # (Incluye aquí tus routers reales)
    # from app.api.v1 import ...
    # app.include_router(...)

    return app


# Instancia para Uvicorn
app = create_app()
