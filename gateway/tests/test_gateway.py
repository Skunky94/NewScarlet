"""Test per gli endpoint del Gateway API."""

from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client() -> TestClient:
    """TestClient per il Gateway (importazione dentro fixture per isolamento)."""
    from src.main import app
    return TestClient(app)


def test_health(client: TestClient) -> None:
    """Verifica che /health risponda 200."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "gateway"}


def test_interact_cortex_unreachable(client: TestClient) -> None:
    """Verifica che /api/v1/interact restituisca 503 se Cortex non è raggiungibile."""
    response = client.post("/api/v1/interact", json={"content": "ciao"})
    assert response.status_code == 503


def test_status_cortex_unreachable(client: TestClient) -> None:
    """Verifica che /api/v1/status restituisca 503 se Cortex non è raggiungibile."""
    response = client.get("/api/v1/status")
    assert response.status_code == 503
