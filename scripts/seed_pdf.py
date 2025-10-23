from app.core.config import settings
from app.db.session import SessionLocal, Base, engine
from app.models.documento import Documento, DocumentoHistorial
from datetime import datetime

def run():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Ajusta a un archivo que ya esté en storage/pdfs/
        ruta = f"{settings.PDF_STORAGE_DIR}/flujo.pdf"
        doc = Documento(
            nombre="Flujo SST Cumplimiento",
            etiqueta="Legal",
            ruta_relativa=ruta,
            tamano_bytes=0,
            hash_sha256="",
            creado_en=datetime.utcnow(),
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
            ruta_relativa=ruta,
            hash_sha256="",
        )
        db.add(hist)
        db.commit()
        print(f"Documento creado con id={doc.id}")
    finally:
        db.close()

if __name__ == "__main__":
    run()
