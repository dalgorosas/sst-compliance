from __future__ import annotations

import os
from datetime import datetime

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.repositories.documento_repo import DocumentoRepo
from app.schemas.documento import DocumentoHistorialRead, DocumentoRead
from app.utils.crypto import generate_file_hash
from app.utils.file_storage import FileStorage

router = APIRouter(prefix="/archivos", tags=["archivos"])


@router.get("/pdf", response_model=list[DocumentoRead])
def list_pdf(etiqueta: str | None = None, db: Session = Depends(get_db)):
    repo = DocumentoRepo()
    documentos = repo.listar(db, etiqueta=etiqueta)
    return documentos


@router.post("/pdf", response_model=DocumentoRead, status_code=status.HTTP_201_CREATED)
async def upload_pdf(
    etiqueta: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Solo se permiten archivos PDF")
    storage = FileStorage(settings.PDF_STORAGE_DIR)
    filename = f"{int(datetime.utcnow().timestamp())}_{file.filename}"
    path = storage.base_dir / filename
    with open(path, "wb") as fh:
        fh.write(await file.read())
    file_size = path.stat().st_size
    file_hash = generate_file_hash(str(path))
    repo = DocumentoRepo()
    documento = repo.create(
        db,
        nombre=os.path.splitext(file.filename)[0],
        etiqueta=etiqueta,
        ruta_relativa=str(path),
        mimetype=file.content_type or "application/pdf",
        tamano_bytes=file_size,
        hash_sha256=file_hash,
    )
    return documento


@router.get("/pdf/{doc_id}", response_model=DocumentoRead)
def get_pdf(doc_id: int, db: Session = Depends(get_db)):
    repo = DocumentoRepo()
    documento = repo.get(db, doc_id)
    if not documento:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    return documento


@router.get("/pdf/{doc_id}/historial", response_model=list[DocumentoHistorialRead])
def pdf_historial(doc_id: int, db: Session = Depends(get_db)):
    repo = DocumentoRepo()
    documento = repo.get(db, doc_id)
    if not documento:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    return repo.historial(db, doc_id)
