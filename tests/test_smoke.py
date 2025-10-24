import pytest

httpx = pytest.importorskip("httpx", reason="httpx es requerido por fastapi.testclient")

from fastapi.testclient import TestClient

from app.main import app


def test_health_endpoint():
    client = TestClient(app)
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"