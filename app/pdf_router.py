from __future__ import annotations

import os
from datetime import datetime

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.models.documento import Documento
from app.repositories.documento_repo import DocumentoRepo
from app.schemas.documento import DocumentoRead
from app.utils.crypto import generate_file_hash

router = APIRouter(prefix="/pdf", tags=["pdf"])

@router.post("", response_model=DocumentoRead, status_code=status.HTTP_201_CREATED)
async def subir_pdf(etiqueta: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Solo se permiten archivos PDF")
    settings.ensure_dirs()
    filename = f"{int(datetime.utcnow().timestamp())}_{file.filename}"
    destino = os.path.join(settings.PDF_STORAGE_DIR, filename)
    with open(destino, "wb") as fh:
        fh.write(await file.read())
    repo = DocumentoRepo()
    documento = repo.create(
        db,
        nombre=os.path.splitext(file.filename)[0],
        etiqueta=etiqueta,
        ruta_relativa=destino,
        mimetype=file.content_type or "application/pdf",
        tamano_bytes=os.path.getsize(destino),
        hash_sha256=generate_file_hash(destino),
    )
    return documento
