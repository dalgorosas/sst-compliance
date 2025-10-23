from sqlalchemy import String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.db.session import Base

class Documento(Base):
    __tablename__ = "documentos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(200), index=True)          # nombre visible
    etiqueta: Mapped[str] = mapped_column(String(100), index=True)        # ej. "SUT", "ISO", "Legal"
    ruta_relativa: Mapped[str] = mapped_column(String(300))               # ej. storage/pdfs/abc.pdf
    mimetype: Mapped[str] = mapped_column(String(50), default="application/pdf")
    tamano_bytes: Mapped[int] = mapped_column(Integer, default=0)
    hash_sha256: Mapped[str] = mapped_column(String(64), default="")
    creado_en: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    actualizado_en: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    historial: Mapped[list["DocumentoHistorial"]] = relationship(
        "DocumentoHistorial", back_populates="documento", cascade="all, delete-orphan"
    )

class DocumentoHistorial(Base):
    __tablename__ = "documento_historial"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    documento_id: Mapped[int] = mapped_column(ForeignKey("documentos.id"))
    version: Mapped[int] = mapped_column(Integer, index=True)   # 1,2,3...
    origen: Mapped[str] = mapped_column(String(80), default="sistema") # quién/qué generó
    descripcion: Mapped[str] = mapped_column(Text, default="")  # por qué se generó
    generado_por: Mapped[str] = mapped_column(String(120), default="")  # usuario/proceso
    ruta_relativa: Mapped[str] = mapped_column(String(300))
    hash_sha256: Mapped[str] = mapped_column(String(64), default="")
    creado_en: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    documento: Mapped["Documento"] = relationship("Documento", back_populates="historial")
