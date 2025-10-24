import hashlib
import importlib
import json
import os
import sys
from pathlib import Path

import pytest

TEST_DATA_FILE = Path(__file__).parent / "data" / "documents.json"
MINIMAL_PDF_BYTES = b"%PDF-1.4\n1 0 obj\n<<>>\nendobj\nxref\n0 1\n0000000000 65535 f \ntrailer\n<<>>\nstartxref\n0\n%%EOF"


@pytest.fixture(scope="session", autouse=True)
def configure_test_environment(tmp_path_factory):
    data_dir = tmp_path_factory.mktemp("data")
    db_path = data_dir / "test.db"
    storage_dir = tmp_path_factory.mktemp("storage") / "pdfs"
    storage_dir.mkdir(parents=True, exist_ok=True)

    os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"
    os.environ["PDF_STORAGE_DIR"] = str(storage_dir)

    for module_name in [
        "app.main",
        "app.repositories.documento_repo",
        "app.models.documento",
        "app.db.session",
        "app.core.config",
    ]:
        sys.modules.pop(module_name, None)

    config_module = importlib.import_module("app.core.config")
    session_module = importlib.import_module("app.db.session")
    importlib.import_module("app.models.documento")
    importlib.import_module("app.repositories.documento_repo")
    main_module = importlib.import_module("app.main")

    from app.db.session import Base, engine

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    yield {
        "storage_dir": storage_dir,
        "main_module": main_module,
    }


@pytest.fixture
def app_with_documents(configure_test_environment):
    from app.db.session import Base, SessionLocal, engine
    from app.models.documento import Documento, DocumentoHistorial

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    storage_dir = configure_test_environment["storage_dir"]
    for existing in storage_dir.glob("*"):
        if existing.is_file():
            existing.unlink()

    session = SessionLocal()
    created_docs = []
    try:
        data = json.loads(TEST_DATA_FILE.read_text())
        for entry in data:
            file_path = storage_dir / entry["archivo"]
            file_path.write_bytes(MINIMAL_PDF_BYTES)
            tamano = file_path.stat().st_size
            hash_sha = hashlib.sha256(file_path.read_bytes()).hexdigest()

            doc = Documento(
                nombre=entry["nombre"],
                etiqueta=entry["etiqueta"],
                ruta_relativa=entry["archivo"],
                mimetype="application/pdf",
                tamano_bytes=tamano,
                hash_sha256=hash_sha,
            )
            session.add(doc)
            session.flush()

            for hist_entry in entry["historial"]:
                hist = DocumentoHistorial(
                    documento_id=doc.id,
                    version=hist_entry["version"],
                    origen=hist_entry["origen"],
                    descripcion=hist_entry["descripcion"],
                    generado_por=hist_entry["generado_por"],
                    ruta_relativa=entry["archivo"],
                    hash_sha256=hash_sha,
                )
                session.add(hist)

            created_docs.append({
                "id": doc.id,
                "archivo": entry["archivo"],
                "nombre": entry["nombre"],
                "etiqueta": entry["etiqueta"],
                "historial": entry["historial"],
            })

        session.commit()
    finally:
        session.close()

    return {
        "app": configure_test_environment["main_module"],
        "documents": created_docs,
        "session_factory": SessionLocal,
    }