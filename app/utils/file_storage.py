from __future__ import annotations

import shutil
from pathlib import Path
from typing import BinaryIO

from app.core.config import settings


class FileStorage:
    def __init__(self, base_dir: str | None = None) -> None:
        self.base_dir = Path(base_dir or settings.PDF_STORAGE_DIR)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def save(self, filename: str, fileobj: BinaryIO) -> Path:
        destination = self.base_dir / filename
        with open(destination, "wb") as fh:
            shutil.copyfileobj(fileobj, fh)
        return destination

    def remove(self, filename: str) -> None:
        path = self.base_dir / filename
        if path.exists():
            path.unlink()

    def exists(self, filename: str) -> bool:
        return (self.base_dir / filename).exists()