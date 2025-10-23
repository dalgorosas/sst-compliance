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
    PDF_STORAGE_DIR: str = Field(default="./storage/pdfs")

    def ensure_dirs(self) -> None:
        Path(self.PDF_STORAGE_DIR).mkdir(parents=True, exist_ok=True)
        Path("./data").mkdir(parents=True, exist_ok=True)

settings = Settings()
