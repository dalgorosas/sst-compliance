#!/usr/bin/env python3
"""
Rellena archivos vacíos con stubs funcionales mínimos para que el sistema corra.
- No toca .json ni archivos de interfaz (html, css, js) ni nada bajo app/frontend, ui, static.
- No sobreescribe archivos que ya tienen contenido (> 0 bytes).
- Es idempotente: solo escribe si está vacío.
"""

from __future__ import annotations
from pathlib import Path
import os
import sys
from textwrap import dedent

ROOT = Path(__file__).resolve().parents[1]

# Directorios o patrones a EXCLUIR del autofill (diseño UI)
EXCLUDE_DIRS = {
    "app/frontend",
    "frontend",
    "ui",
    "static",
    "node_modules",
    ".git",
    ".venv",
    "venv",
    "env",
    "storage",    # PDFs
    "data",       # BD SQLite
}

# Extensiones a EXCLUIR
EXCLUDE_EXTS = {".json", ".html", ".css", ".js"}

# Stubs por ruta/archivo (clave: sufijo de ruta)
STUBS = {}

def add_stub(suffix: str, content: str):
    STUBS[suffix.replace("\\", "/")] = dedent(content).lstrip("\n")

# -------- STUBS ESENCIALES (solo se aplican si el archivo está vacío) --------

add_stub("app/__init__.py", """
# Marca el paquete de la aplicación
""")

add_stub("app/core/config.py", """
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from pathlib import Path

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)

    ENV: str = Field(default="dev")
    APP_NAME: str = Field(default="SST Compliance API")
    APP_VERSION: str = Field(default="0.1.0")
    APP_HOST: str = Field(default="127.0.0.1")
    APP_PORT: int = Field(default=8000)

    DATABASE_URL: str = Field(default="sqlite:///./data/app.db")

    # Subidas desactivadas por defecto (no deja archivos temporales)
    UPLOADS_ENABLED: bool = Field(default=False)

    PDF_STORAGE_DIR: str = Field(default="./storage/pdfs")

    def ensure_dirs(self) -> None:
        Path("./data").mkdir(parents=True, exist_ok=True)
        if self.UPLOADS_ENABLED:
            Path(self.PDF_STORAGE_DIR).mkdir(parents=True, exist_ok=True)

settings = Settings()
""")

add_stub("app/db/session.py", """
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import settings

class Base(DeclarativeBase):
    pass

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {},
    echo=False,
    future=True,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
""")

add_stub("app/models/__init__.py", """
from app.db.session import Base  # noqa
from app.models.documento import Documento, DocumentoHistorial  # noqa
""")

add_stub("app/models/documento.py", """
from sqlalchemy import String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.db.session import Base

class Documento(Base):
    __tablename__ = "documentos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(200), index=True)
    etiqueta: Mapped[str] = mapped_column(String(100), index=True)
    ruta_relativa: Mapped[str] = mapped_column(String(300))
    mimetype: Mapped[str] = mapped_column(String(50), default="application/pdf")
    tamano_bytes: Mapped[int] = mapped_column(Integer, default=0)
    hash_sha256: Mapped[str] = mapped_column(String(64), default="")
    creado_en: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    actualizado_en: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    historial: Mapped[list["DocumentoHistorial"]] = relationship(
        "DocumentoHistorial", back_populates="documento", cascade="all, delete-orphan"
    )

class DocumentoHistorial(Base):
    __tablename__ = "documento_historial"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    documento_id: Mapped[int] = mapped_column(ForeignKey("documentos.id"))
    version: Mapped[int] = mapped_column(Integer, index=True)
    origen: Mapped[str] = mapped_column(String(80), default="sistema")
    descripcion: Mapped[str] = mapped_column(Text, default="")
    generado_por: Mapped[str] = mapped_column(String(120), default="")
    ruta_relativa: Mapped[str] = mapped_column(String(300))
    hash_sha256: Mapped[str] = mapped_column(String(64), default="")
    creado_en: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    documento: Mapped["Documento"] = relationship("Documento", back_populates="historial")
""")

add_stub("app/repositories/base.py", """
from sqlalchemy.orm import Session
from typing import TypeVar, Generic, Type

T = TypeVar("T")

class BaseRepo(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model

    def get(self, db: Session, id: int) -> T | None:
        return db.get(self.model, id)

    def list(self, db: Session, limit: int = 100, offset: int = 0) -> list[T]:
        return db.query(self.model).offset(offset).limit(limit).all()
""")

add_stub("app/repositories/documento_repo.py", """
from sqlalchemy.orm import Session
from sqlalchemy import select, desc, func, and_
from app.repositories.base import BaseRepo
from app.models.documento import Documento, DocumentoHistorial

class DocumentoRepo(BaseRepo[Documento]):
    def __init__(self) -> None:
        super().__init__(Documento)

    def listar(self, db: Session, etiqueta: str | None = None):
        q = select(Documento).order_by(desc(Documento.actualizado_en))
        if etiqueta:
            q = q.where(Documento.etiqueta == etiqueta)
        return db.execute(q).scalars().all()

    def by_nombre_etiqueta(self, db: Session, nombre: str, etiqueta: str) -> Documento | None:
        q = select(Documento).where(and_(Documento.nombre == nombre, Documento.etiqueta == etiqueta)).limit(1)
        return db.execute(q).scalar_one_or_none()

    def historial(self, db: Session, doc_id: int):
        q = (
            select(DocumentoHistorial)
            .where(DocumentoHistorial.documento_id == doc_id)
            .order_by(desc(DocumentoHistorial.version))
        )
        return db.execute(q).scalars().all()

    def proxima_version(self, db: Session, doc_id: int) -> int:
        q = select(func.max(DocumentoHistorial.version)).where(DocumentoHistorial.documento_id == doc_id)
        latest = db.execute(q).scalar()
        return (latest or 0) + 1
""")

add_stub("app/services/evidence_manager.py", """
from pathlib import Path
from uuid import uuid4
import hashlib
from typing import Tuple
from fastapi import UploadFile
from app.core.config import settings

def _compute_sha256(file_path: Path) -> str:
    h = hashlib.sha256()
    with file_path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def save_pdf(upload: UploadFile) -> Tuple[str, int, str]:
    storage = Path(settings.PDF_STORAGE_DIR)
    storage.mkdir(parents=True, exist_ok=True)

    filename = f"{uuid4().hex}.pdf"
    dest = storage / filename

    with dest.open("wb") as f:
        while True:
            chunk = upload.file.read(1024 * 1024)
            if not chunk:
                break
            f.write(chunk)

    size = dest.stat().st_size
    sha256 = _compute_sha256(dest)
    return str(dest), size, sha256
""")

add_stub("app/main.py", """
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from sqlalchemy.orm import Session
import os
from pathlib import Path

from app.core.config import settings
from app.db.session import Base, engine, get_db
from app.repositories.documento_repo import DocumentoRepo
from app.models.documento import Documento, DocumentoHistorial
from app.services.evidence_manager import save_pdf

settings.ensure_dirs()
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

# Montar /files solo si existe físicamente
pdf_dir = Path(settings.PDF_STORAGE_DIR)
if pdf_dir.exists():
    app.mount("/files", StaticFiles(directory=settings.PDF_STORAGE_DIR), name="files")

@app.get("/health")
def health():
    return {"status": "ok", "env": settings.ENV, "version": settings.APP_VERSION}

@app.get("/api/v1/pdf")
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
    doc = db.get(Documento, doc_id)
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

# Registro condicional del endpoint POST (no se muestra ni se ejecuta si UPLOADS_ENABLED = False)
if settings.UPLOADS_ENABLED:
    @app.post("/api/v1/pdf", include_in_schema=True)
    def subir_pdf(
        file: UploadFile = File(..., description="Archivo PDF"),
        nombre: str = Form(..., description="Nombre lógico"),
        etiqueta: str = Form(..., description="Etiqueta/categoría"),
        descripcion: str = Form("", description="Descripción"),
        generado_por: str = Form("sistema", description="Usuario/proceso"),
        db: Session = Depends(get_db),
    ):
        if file.content_type not in ("application/pdf", "application/octet-stream"):
            raise HTTPException(status_code=400, detail="El archivo debe ser un PDF.")
        ruta_relativa, tamano_bytes, sha256 = save_pdf(file)
        repo = DocumentoRepo()
        existente = repo.by_nombre_etiqueta(db, nombre=nombre, etiqueta=etiqueta)
        if existente is None:
            doc = Documento(
                nombre=nombre, etiqueta=etiqueta, ruta_relativa=ruta_relativa,
                tamano_bytes=tamano_bytes, hash_sha256=sha256, mimetype="application/pdf",
            )
            db.add(doc); db.commit(); db.refresh(doc)
            version = 1
        else:
            existente.ruta_relativa = ruta_relativa
            existente.tamano_bytes = tamano_bytes
            existente.hash_sha256 = sha256
            db.add(existente); db.commit(); db.refresh(existente)
            doc = existente
            version = repo.proxima_version(db, doc.id)

        hist = DocumentoHistorial(
            documento_id=doc.id, version=version, origen="upload",
            descripcion=descripcion, generado_por=generado_por,
            ruta_relativa=ruta_relativa, hash_sha256=sha256,
        )
        db.add(hist); db.commit()

        return {
            "id": doc.id,
            "nombre": doc.nombre,
            "etiqueta": doc.etiqueta,
            "version": version,
            "ruta_relativa": ruta_relativa,
            "tamano_bytes": tamano_bytes,
            "hash_sha256": sha256,
        }

@app.get("/viewer/{doc_id}", response_class=HTMLResponse)
def viewer(doc_id: int, db: Session = Depends(get_db)):
    doc = db.get(Documento, doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    filename = os.path.basename(doc.ruta_relativa)
    html = f\"\"\"<!doctype html>
    <html><head><meta charset="utf-8" />
    <title>Visor PDF - {doc.nombre}</title>
    <style>
      body,html {{ margin:0; height:100%; }}
      .wrap {{ height:100%; display:flex; flex-direction:column; }}
      header {{ padding:10px 14px; font-family:Arial; border-bottom:1px solid #ddd; }}
      iframe {{ flex:1; border:0; width:100%; }}
    </style></head>
    <body><div class="wrap">
      <header><strong>{doc.nombre}</strong> — etiqueta: {doc.etiqueta} — actualizado: {doc.actualizado_en}</header>
      <iframe src="/files/{filename}#zoom=page-width"></iframe>
    </div></body></html>\"\"\"
    return HTMLResponse(content=html, status_code=200)
""")

add_stub("tests/test_smoke.py", """
def test_placeholder():
    assert 1 + 1 == 2
""")

# --------------------------- LÓGICA DEL AUTOFILL ---------------------------

def should_exclude(path: Path) -> bool:
    if path.suffix.lower() in EXCLUDE_EXTS:
        return True
    parts = [p.lower() for p in path.parts]
    for ex in EXCLUDE_DIRS:
        ex_parts = [p.lower() for p in Path(ex).parts]
        # excluir si la ruta contiene el prefijo del excluido
        for i in range(len(parts) - len(ex_parts) + 1):
            if parts[i:i+len(ex_parts)] == ex_parts:
                return True
    return False

def fill_if_empty(file_path: Path, suffix: str, content: str, report: list[str]):
    if not file_path.exists():
        return
    if should_exclude(file_path):
        report.append(f"SKIP (UI/JSON): {file_path}")
        return
    if file_path.stat().st_size > 0:
        report.append(f"KEEP (has content): {file_path}")
        return
    file_path.write_text(content, encoding="utf-8")
    report.append(f"FILLED: {file_path}")

def main():
    report = []

    # Asegura __init__.py en paquetes clave
    for p in [ROOT / "app", ROOT / "app" / "api", ROOT / "app" / "models",
              ROOT / "app" / "repositories", ROOT / "app" / "services",
              ROOT / "app" / "db", ROOT / "app" / "utils", ROOT / "tests"]:
        p.mkdir(parents=True, exist_ok=True)
        initf = p / "__init__.py"
        if not initf.exists():
            initf.write_text("# package\n", encoding="utf-8")
            report.append(f"CREATED: {initf}")

    # Recorre todos los stubs y escribe solo si el archivo existe y está vacío
    for suffix, content in STUBS.items():
        target = ROOT / suffix
        if target.exists():
            fill_if_empty(target, suffix, content, report)

    # Reporta archivos vacíos restantes (no stubeados) para informar acción
    empties = []
    for path in ROOT.rglob("*"):
        if path.is_dir():
            continue
        if path.suffix.lower() in EXCLUDE_EXTS:
            continue
        if should_exclude(path):
            continue
        try:
            if path.stat().st_size == 0:
                empties.append(str(path.relative_to(ROOT)))
        except FileNotFoundError:
            pass

    print("=== AUTOFILL REPORT ===")
    for line in report:
        print(line)
    print("=== EMPTY FILES (remaining, to be handled later) ===")
    for e in empties:
        print(e)
    if not empties:
        print("(none)")

if __name__ == "__main__":
    main()
