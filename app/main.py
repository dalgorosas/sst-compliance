from pathlib import Path
from typing import Any

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import Base, engine, get_db
from app.models.documento import Documento
from app.repositories.documento_repo import DocumentoRepo


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

# Inicializar almacenamiento y BD
settings.ensure_dirs()
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

storage_path = _get_storage_path()
frontend_dir = Path(__file__).parent / "frontend"

# Servir PDFs estáticos (lectura)
app.mount("/files", StaticFiles(directory=storage_path), name="files")
app.mount("/viewer-assets", StaticFiles(directory=frontend_dir), name="viewer-assets")


@app.get("/", include_in_schema=False)
def index() -> RedirectResponse:
    """Redirige al visor estático principal.

    Cuando la aplicación se sirve en local suele visitarse ``/`` desde el
    navegador, lo que anteriormente devolvía 404.  Para mantener los recursos
    relativos del visor funcionando (CSS, JS, worker de PDF.js) redirigimos a la
    versión estática ubicada en ``/viewer-assets``.
    """

    return RedirectResponse(url="/viewer-assets/viewer/index.html")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "env": settings.ENV, "version": settings.APP_VERSION}

# ----------- Endpoints PDF -----------

@app.get("/api/v1/pdf")
def listar_pdfs(etiqueta: str | None = None, db: Session = Depends(get_db)):
    repo = DocumentoRepo()
    data = repo.listar(db, etiqueta=etiqueta)
    return [_document_payload(doc) for doc in data]


@app.get("/api/v1/pdf/{doc_id}")
def obtener_pdf(doc_id: int, db: Session = Depends(get_db)):
    doc: Documento | None = db.get(Documento, doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    return _document_payload(doc)


@app.get("/api/v1/pdf/{doc_id}/download", response_class=FileResponse)
def descargar_pdf(doc_id: int, db: Session = Depends(get_db)):
    doc: Documento | None = db.get(Documento, doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    pdf_path = _resolve_pdf_path(doc)
    if not pdf_path.exists():
        raise HTTPException(status_code=404, detail="Archivo físico no encontrado")

    return FileResponse(pdf_path, media_type=doc.mimetype, filename=f"{doc.nombre}.pdf")


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
            "fecha": h.creado_en,
        }
        for h in hist
    ]


# Visualizador HTML simple (embebido)
@app.get("/viewer/{doc_id}", response_class=HTMLResponse)
def viewer(doc_id: int, db: Session = Depends(get_db)):
    doc: Documento | None = db.get(Documento, doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Documento no encontrado")

    archivo_publico = _document_payload(doc)["archivo"]
    html = f"""
    <!doctype html>
    <html>
      <head>
        <meta charset=\"utf-8\" />
        <title>Visor PDF - {doc.nombre}</title>
        <style>
          body,html {{ margin:0; height:100%; }}
          .wrap {{ height:100%; display:flex; flex-direction:column; }}
          header {{ padding:10px 14px; font-family:Arial; border-bottom:1px solid #ddd; }}
          iframe {{ flex:1; border:0; width:100%; }}
        </style>
      </head>
      <body>
        <div class=\"wrap\">
          <header>
            <strong>{doc.nombre}</strong> — etiqueta: {doc.etiqueta} — actualizado: {doc.actualizado_en}
          </header>
          <iframe src=\"/files/{archivo_publico}#zoom=page-width\"></iframe>
        </div>
      </body>
    </html>
    """
    return HTMLResponse(content=html, status_code=200)
