"""Test per il Memory Service: CRUD sessioni e messaggi (con DB mockato)."""

from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def mock_db():
    """Fornisce una sessione database AsyncMock per i test."""
    session = AsyncMock()
    session.__aenter__ = AsyncMock(return_value=session)
    session.__aexit__ = AsyncMock(return_value=None)
    return session


@pytest.fixture
def client():
    """TestClient con init_db e get_session mockati."""
    with patch("src.database.init_db", new_callable=AsyncMock):
        with patch("src.database.get_session"):
            from src.main import app
            return TestClient(app)


def test_health(client) -> None:
    """Verifica che /health risponda correttamente."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["service"] == "memory"


@pytest.mark.asyncio
async def test_create_session_crud() -> None:
    """Verifica la creazione di una sessione via CRUD."""
    from scarlet_common.models import SessionCreate
    from src.crud import create_session

    session_id = str(uuid4())

    mock_record = MagicMock()
    mock_record.id = session_id
    mock_record.metadata_ = {}

    db = AsyncMock()
    db.add = MagicMock()
    db.commit = AsyncMock()
    db.refresh = AsyncMock()

    result = await create_session(db, SessionCreate())
    db.add.assert_called_once()
    db.commit.assert_called_once()


@pytest.mark.asyncio
async def test_add_message_crud() -> None:
    """Verifica l'aggiunta di un messaggio via CRUD."""
    from uuid import uuid4 as _uuid4
    from scarlet_common.models import MessageCreate, MessageRole
    from src.crud import add_message

    data = MessageCreate(
        session_id=_uuid4(),
        role=MessageRole.USER,
        content="Messaggio di test",
    )

    db = AsyncMock()
    db.add = MagicMock()
    db.commit = AsyncMock()
    db.refresh = AsyncMock()

    result = await add_message(db, data)
    db.add.assert_called_once()
    db.commit.assert_called_once()
