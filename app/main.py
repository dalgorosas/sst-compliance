from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import Base, engine, get_db
from app.repositories.documento_repo import DocumentoRepo
from app.models.documento import Documento

# Inicializar almacenamiento y BD
settings.ensure_dirs()
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

# Servir PDFs estáticos (lectura)
app.mount("/files", StaticFiles(directory=settings.PDF_STORAGE_DIR), name="files")

@app.get("/health")
def health():
    return {"status": "ok", "env": settings.ENV, "version": settings.APP_VERSION}

# ----------- Endpoints PDF -----------

@app.get("/api/v1/pdf", response_model=None)
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

# Visualizador HTML simple (embebido)
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
          <iframe src="/files/{doc.ruta_relativa.split('/')[-1]}#zoom=page-width"></iframe>
        </div>
      </body>
    </html>
    """
    return HTMLResponse(content=html, status_code=200)
