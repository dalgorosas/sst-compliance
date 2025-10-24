from __future__ import annotations

import enum
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    AUDITOR = "auditor"
    TECNICO = "tecnico"
    EMPRESA = "empresa"
    MEDICO = "medico"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.EMPRESA)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    empresas: Mapped[list["Empresa"]] = relationship("Empresa", back_populates="owner")
    auditorias: Mapped[list["Auditoria"]] = relationship(
        "Auditoria", back_populates="auditor", foreign_keys="Auditoria.auditor_id"
    )

    def __repr__(self) -> str:  # pragma: no cover - representación auxiliar
        return f"User(id={self.id!r}, email={self.email!r}, role={self.role!r})"