# app/db/base.py
"""
Punto central para importar modelos y que Alembic conozca todas las tablas.
IMPORTANTE: importa aquí cada nuevo modelo que vayas creando.
"""
from app.db.session import Base

# importa tus modelos aquí:
from app.models.user import User  # ejemplo; ajusta a tus modelos reales

__all__ = ["Base", "User"]
