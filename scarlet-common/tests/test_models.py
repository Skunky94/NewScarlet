"""Test per i modelli Pydantic di scarlet-common."""

from uuid import UUID

import pytest

from scarlet_common.models.agent import AgentMood, AgentState, AgentStatus
from scarlet_common.models.conversation import Message, MessageRole, Session
from scarlet_common.models.responses import ApiResponse, ErrorResponse
from scarlet_common.models.tasks import Goal, Task, TaskPriority, TaskStatus


def test_session_defaults() -> None:
    """Verifica i valori di default di una Session."""
    session = Session()
    assert isinstance(session.id, UUID)
    assert session.metadata == {}


def test_message_create() -> None:
    """Verifica la creazione corretta di un Message."""
    session = Session()
    msg = Message(
        session_id=session.id,
        role=MessageRole.USER,
        content="Ciao Scarlet",
    )
    assert msg.role == MessageRole.USER
    assert msg.content == "Ciao Scarlet"
    assert msg.session_id == session.id


def test_agent_state_defaults() -> None:
    """Verifica i valori di default di AgentState."""
    state = AgentState()
    assert state.status == AgentStatus.IDLE
    assert state.mood == AgentMood.NEUTRAL
    assert state.attention_level == 1.0
    assert state.active_task_id is None


def test_agent_state_attention_validation() -> None:
    """Verifica che attention_level rispetti i limiti [0.0, 1.0]."""
    with pytest.raises(Exception):
        AgentState(attention_level=1.5)


def test_task_defaults() -> None:
    """Verifica i valori di default di un Task."""
    task = Task(title="test task", description="descrizione")
    assert task.status == TaskStatus.PENDING
    assert task.priority == TaskPriority.NORMAL


def test_goal_create() -> None:
    """Verifica la creazione corretta di un Goal."""
    goal = Goal(
        title="Migliorare capacità",
        description="Analizzare dati di feedback",
        directive_source="primary_directive_1",
    )
    assert goal.completed is False
    assert isinstance(goal.id, UUID)


def test_api_response_success() -> None:
    """Verifica il formato di ApiResponse per successo."""
    response: ApiResponse[str] = ApiResponse(success=True, data="ok", message="Operazione completata")
    assert response.success is True
    assert response.data == "ok"


def test_error_response() -> None:
    """Verifica il formato di ErrorResponse."""
    err = ErrorResponse(error="Not found", detail="Sessione non trovata")
    assert err.success is False
    assert err.error == "Not found"
