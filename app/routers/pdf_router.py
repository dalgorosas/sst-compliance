from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
import os
from app.db.database import get_db
from app.models.pdf import PDFDocument
from app.schemas.pdf import PDFResponse

router = APIRouter()

PDFS_DIR = os.path.join("app", "storage", "pdfs")
os.makedirs(PDFS_DIR, exist_ok=True)

@router.post("/api/v1/pdf", response_model=PDFResponse)
async def subir_pdf(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Sube un PDF al servidor y lo registra en la base de datos.
    """
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Solo se permiten archivos PDF.")

    save_path = os.path.join(PDFS_DIR, file.filename)

    # Guarda el archivo físicamente
    with open(save_path, "wb") as f:
        f.write(await file.read())

    # Guarda el registro en la base
    nuevo_pdf = PDFDocument(nombre=file.filename, ruta=save_path)
    db.add(nuevo_pdf)
    db.commit()
    db.refresh(nuevo_pdf)

    return PDFResponse(
        id=nuevo_pdf.id,
        nombre=nuevo_pdf.nombre,
        ruta=nuevo_pdf.ruta
    )
