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
    """
    Guarda un UploadFile (PDF) en storage/pdfs con nombre unico.
    Retorna: (ruta_relativa, tamano_bytes, sha256)
    """
    storage = Path(settings.PDF_STORAGE_DIR)
    storage.mkdir(parents=True, exist_ok=True)

    ext = ".pdf"
    filename = f"{uuid4().hex}{ext}"
    dest = storage / filename

    # Guardar contenido
    with dest.open("wb") as f:
        while True:
            chunk = upload.file.read(1024 * 1024)
            if not chunk:
                break
            f.write(chunk)

    size = dest.stat().st_size
    sha256 = _compute_sha256(dest)
    return str(dest), size, sha256
