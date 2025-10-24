from __future__ import annotations

from pathlib import Path
from typing import Iterable


def _collect_ids(items: Iterable[dict]) -> set[int]:
    return {item["id"] for item in items}


def test_listar_pdfs_returns_documents(app_with_documents):
    app_ctx = app_with_documents
    session = app_ctx["session_factory"]()
    try:
        payload = app_ctx["app"].listar_pdfs(db=session)
    finally:
        session.close()

    assert _collect_ids(payload) == _collect_ids(app_ctx["documents"])
    sample = payload[0]
    assert {"id", "nombre", "etiqueta", "ruta_relativa", "archivo"}.issubset(sample)


def test_listar_pdfs_allows_filter_by_etiqueta(app_with_documents):
    app_ctx = app_with_documents
    session = app_ctx["session_factory"]()
    etiqueta = app_ctx["documents"][-1]["etiqueta"]
    try:
        payload = app_ctx["app"].listar_pdfs(etiqueta=etiqueta, db=session)
    finally:
        session.close()

    assert len(payload) == 1
    assert payload[0]["etiqueta"] == etiqueta


def test_obtener_pdf_metadata(app_with_documents):
    app_ctx = app_with_documents
    target = app_ctx["documents"][0]
    session = app_ctx["session_factory"]()
    try:
        data = app_ctx["app"].obtener_pdf(doc_id=target["id"], db=session)
    finally:
        session.close()

    assert data["nombre"] == target["nombre"]
    assert data["archivo"] == target["archivo"]
    assert data["hash_sha256"]


def test_descargar_pdf(app_with_documents):
    app_ctx = app_with_documents
    target = app_ctx["documents"][0]
    session = app_ctx["session_factory"]()
    try:
        response = app_ctx["app"].descargar_pdf(doc_id=target["id"], db=session)
    finally:
        session.close()

    assert response.media_type.startswith("application/pdf")
    file_path = Path(response.path)
    assert file_path.exists()
    assert file_path.read_bytes().startswith(b"%PDF")


def test_historial_pdf_returns_entries(app_with_documents):
    app_ctx = app_with_documents
    target = app_ctx["documents"][0]
    session = app_ctx["session_factory"]()
    try:
        historial = app_ctx["app"].historial_pdf(doc_id=target["id"], db=session)
    finally:
        session.close()

    assert len(historial) == len(target["historial"])
    versiones = [item["version"] for item in historial]
    assert versiones == sorted(versiones, reverse=True)
    fechas = [item.get("fecha") for item in historial]
    assert all(fechas)