# app/db/session.py
from collections.abc import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import settings  # ← usamos tu ruta real

class Base(DeclarativeBase):
    """Base declarativa única para todos los modelos."""
    pass

# Conexión: si es SQLite, agrega check_same_thread para uso en FastAPI (hilos)
connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    echo=False,
    future=True,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

def get_db() -> Generator:
    """Dependencia de FastAPI que entrega un Session y lo cierra al final."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
