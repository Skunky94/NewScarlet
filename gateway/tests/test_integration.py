"""Test di integrazione T7 per il Gateway.

Verifica il flusso completo Gateway → Cortex con risposta simulata di Cortex:
il Gateway deve instradare correttamente il messaggio e restituire l'acknowledgment.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client() -> TestClient:
    """TestClient Gateway con ciclo di vita disabilitato."""
    from src.main import app
    return TestClient(app)


def test_interact_success_full_flow(client: TestClient) -> None:
    """Verifica il flusso completo: Gateway riceve messaggio, Cortex risponde OK.

    Simula Cortex che accetta il messaggio e restituisce session_id + task_id.
    Verifica che Gateway risponda con acknowledgment e dati corretti.
    """
    cortex_response = MagicMock()
    cortex_response.status_code = 200
    cortex_response.raise_for_status = MagicMock()
    cortex_response.json.return_value = {
        "success": True,
        "data": {
            "session_id": "sess-abc-123",
            "task_id": "task-xyz-456",
        },
    }

    mock_http = AsyncMock()
    mock_http.__aenter__ = AsyncMock(return_value=mock_http)
    mock_http.__aexit__ = AsyncMock(return_value=None)
    mock_http.post = AsyncMock(return_value=cortex_response)

    with patch("httpx.AsyncClient", return_value=mock_http):
        response = client.post(
            "/api/v1/interact",
            json={"content": "Ciao Scarlet, chi sei?"},
        )

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["acknowledged"] is True
    assert body["data"]["session_id"] == "sess-abc-123"


def test_interact_preserves_session_id(client: TestClient) -> None:
    """Verifica che il session_id fornito dal client venga mantenuto nel flusso."""
    provided_session_id = "existing-session-999"

    cortex_response = MagicMock()
    cortex_response.status_code = 200
    cortex_response.raise_for_status = MagicMock()
    cortex_response.json.return_value = {
        "success": True,
        "data": {"session_id": provided_session_id, "task_id": "task-001"},
    }

    mock_http = AsyncMock()
    mock_http.__aenter__ = AsyncMock(return_value=mock_http)
    mock_http.__aexit__ = AsyncMock(return_value=None)
    mock_http.post = AsyncMock(return_value=cortex_response)

    with patch("httpx.AsyncClient", return_value=mock_http):
        response = client.post(
            "/api/v1/interact",
            json={"content": "Continua la conversazione", "session_id": provided_session_id},
        )

    assert response.status_code == 200
    body = response.json()
    assert body["data"]["session_id"] == provided_session_id


def test_status_endpoint_with_cortex_available(client: TestClient) -> None:
    """Verifica che /status restituisca lo stato quando Cortex è disponibile."""
    cortex_state = {
        "status": "idle",
        "mood": "neutral",
        "active_task_id": None,
        "updated_at": "2025-01-01T00:00:00",
    }

    mock_http = AsyncMock()
    mock_http.__aenter__ = AsyncMock(return_value=mock_http)
    mock_http.__aexit__ = AsyncMock(return_value=None)
    mock_http.get = AsyncMock(return_value=MagicMock(
        status_code=200,
        raise_for_status=MagicMock(),
        json=MagicMock(return_value=cortex_state),
    ))

    with patch("httpx.AsyncClient", return_value=mock_http):
        response = client.get("/api/v1/status")

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["status"] == "idle"
