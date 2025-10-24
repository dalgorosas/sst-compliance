from datetime import datetime
import hashlib
from pathlib import Path

from app.core.config import settings
from app.db.session import Base, SessionLocal, engine
from app.models.documento import Documento, DocumentoHistorial


def run():
    settings.ensure_dirs()
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        archivo = "flujo.pdf"
        ruta = Path(settings.PDF_STORAGE_DIR) / archivo

        tamano = ruta.stat().st_size if ruta.exists() else 0
        hash_sha = hashlib.sha256(ruta.read_bytes()).hexdigest() if ruta.exists() else ""
        
        doc = Documento(
            nombre="Flujo SST Cumplimiento",
            etiqueta="Legal",
            ruta_relativa=archivo,
            tamano_bytes=tamano,
            hash_sha256=hash_sha,
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)

        hist = DocumentoHistorial(
            documento_id=doc.id,
            version=1,
            origen="seed",
            descripcion="Carga inicial",
            generado_por="admin",
            ruta_relativa=archivo,
            hash_sha256=hash_sha,
        )
        db.add(hist)
        db.commit()
        print(f"Documento creado con id={doc.id}")
    finally:
        db.close()


if __name__ == "__main__":
    run()
