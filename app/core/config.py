# app/core/config.py
from __future__ import annotations
from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    # --- App ---
    APP_NAME: str = "SST Compliance - DALGORO"
    APP_VERSION: str = "0.1.0"

    # --- Entorno ---
    ENV: str = "dev"

    # --- DB ---
    DATABASE_URL: str = "sqlite:///./data/dev.db"

    # --- CORS ---
    ALLOWED_ORIGINS: List[str] | str = ["http://127.0.0.1:8000", "http://localhost:8000"]

    # --- JWT (si aplica) ---
    JWT_SECRET: str = "change-me"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # --- Storage PDF ---
    PDF_STORAGE_DIR: Path = Field(default=Path("pdfs"))

    # --- Google Service Account (dos modos soportados por google_sheets.py) ---
    GOOGLE_SERVICE_ACCOUNT_FILE: str | None = None
    GOOGLE_SERVICE_ACCOUNT_JSON: str | None = None

    # --- Google Sheets (compat con nombres previos y los que requiere google_sheets.py) ---
    # Hoja de usuarios (la que usa GoogleSheetsRegistry)
    GOOGLE_SHEETS_USER_SPREADSHEET_ID: str | None = None
    GOOGLE_SHEETS_USER_WORKSHEET: str | None = None

    # Hoja de citas / docs (si otra parte la usa con estos nombres antiguos)
    GOOGLE_APPLICATION_CREDENTIALS: str | None = None
    GOOGLE_SHEETS_DOC_KEY: str | None = None
    GOOGLE_SHEETS_TAB: str = "Citas"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Utilidad para crear carpetas necesarias (llamada en main.py)
    def ensure_dirs(self) -> None:
        Path("data").mkdir(parents=True, exist_ok=True)
        Path(self.PDF_STORAGE_DIR).mkdir(parents=True, exist_ok=True)

settings = Settings()
