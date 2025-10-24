from __future__ import annotations

import os

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from app import create_app
from app.core.config import settings
from app.db.session import Base, engine, get_db
from app.models.documento import Documento
from app.repositories.documento_repo import DocumentoRepo

# Inicializar almacenamiento y BD
settings.ensure_dirs()
Base.metadata.create_all(bind=engine)

app: FastAPI = create_app()


@app.get("/health")
def health():
    return {"status": "ok", "env": settings.ENV, "version": settings.APP_VERSION}


@app.get("/api/v1/pdf", response_model=list[dict])
def listar_pdfs(etiqueta: str | None = None, db: Session = Depends(get_db)):
    repo = DocumentoRepo()
    data = repo.listar(db, etiqueta=etiqueta)
    return [
        {
            "id": d.id,
            "nombre": d.nombre,
            "etiqueta": d.etiqueta,
            "ruta_relativa": d.ruta_relativa,
            "tamano_bytes": d.tamano_bytes,
            "actualizado_en": d.actualizado_en,
        }
        for d in data
    ]


@app.get("/api/v1/pdf/{doc_id}", response_class=FileResponse)
def descargar_pdf(doc_id: int, db: Session = Depends(get_db)):
    doc: Documento | None = db.get(Documento, doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    return FileResponse(doc.ruta_relativa, media_type=doc.mimetype, filename=f"{doc.nombre}.pdf")


@app.get("/api/v1/pdf/{doc_id}/historial")
def historial_pdf(doc_id: int, db: Session = Depends(get_db)):
    repo = DocumentoRepo()
    hist = repo.historial(db, doc_id)
    return [
        {
            "version": h.version,
            "origen": h.origen,
            "descripcion": h.descripcion,
            "generado_por": h.generado_por,
            "ruta_relativa": h.ruta_relativa,
            "hash_sha256": h.hash_sha256,
            "creado_en": h.creado_en,
        }
        for h in hist
    ]


@app.get("/viewer/{doc_id}", response_class=HTMLResponse)
def viewer(doc_id: int, db: Session = Depends(get_db)):
    doc: Documento | None = db.get(Documento, doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    html = f"""
    <!doctype html>
    <html>
      <head>
        <meta charset="utf-8" />
        <title>Visor PDF - {doc.nombre}</title>
        <style>
          body,html {{ margin:0; height:100%; }}
          .wrap {{ height:100%; display:flex; flex-direction:column; }}
          header {{ padding:10px 14px; font-family:Arial; border-bottom:1px solid #ddd; }}
          iframe {{ flex:1; border:0; width:100%; }}
        </style>
      </head>
      <body>
        <div class="wrap">
          <header>
            <strong>{doc.nombre}</strong> — etiqueta: {doc.etiqueta} — actualizado: {doc.actualizado_en}
          </header>
          <iframe src="/files/{os.path.basename(doc.ruta_relativa)}#zoom=page-width"></iframe>
        </div>
      </body>
    </html>
    """
    return HTMLResponse(content=html, status_code=200)



frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")
app.mount("/viewer", StaticFiles(directory=frontend_dir), name="frontend")


@app.get("/view/{pdf_id}")
def view_pdf(pdf_id: int):
    index_path = os.path.join(frontend_dir, "viewer", "index.html")
    return FileResponse(index_path)
