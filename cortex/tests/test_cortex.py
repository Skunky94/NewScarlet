"""Test per il Cortex: stato interno e coda priorità."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def mock_redis():
    """Mock del client Redis per test isolati."""
    with patch("src.state.get_redis") as mock:
        redis_mock = AsyncMock()
        redis_mock.get = AsyncMock(return_value=None)
        redis_mock.set = AsyncMock(return_value=True)
        redis_mock.zadd = AsyncMock(return_value=1)
        redis_mock.zpopmin = AsyncMock(return_value=[])
        redis_mock.aclose = AsyncMock()
        mock.return_value = redis_mock
        yield redis_mock


@pytest.fixture
def mock_redis_loop(mock_redis):
    """Mock Redis anche per il loop."""
    with patch("src.loop.get_redis") as mock:
        mock.return_value = mock_redis
        yield mock_redis


@pytest.fixture
def client(mock_redis, mock_redis_loop):
    """TestClient con Redis mockato e loop non avviato."""
    with patch("src.main.run_loop", new_callable=AsyncMock):
        with patch("asyncio.create_task"):
            from src.main import app
            return TestClient(app)


def test_health(client) -> None:
    """Verifica che /health risponda correttamente."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["service"] == "cortex"


def test_get_state_default(client, mock_redis) -> None:
    """Verifica che /internal/state restituisca lo stato di default."""
    response = client.get("/internal/state")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "idle"
    assert data["mood"] == "neutral"


def test_receive_message(client, mock_redis) -> None:
    """Verifica che /internal/message accetti un messaggio e restituisca session_id."""
    response = client.post(
        "/internal/message",
        json={"content": "ciao", "role": "user"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert "session_id" in body["data"]
    assert "task_id" in body["data"]
