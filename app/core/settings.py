from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl
from typing import List

class Settings(BaseSettings):
    ENV: str = "dev"
    ALLOWED_ORIGINS: List[AnyHttpUrl] | List[str] = ["http://127.0.0.1:8000"]
    JWT_SECRET: str

    DATABASE_URL: str = "sqlite:///./data/dev.db"

    GOOGLE_APPLICATION_CREDENTIALS: str | None = None
    GOOGLE_SHEETS_DOC_KEY: str | None = None
    GOOGLE_SHEETS_TAB: str = "Citas"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
