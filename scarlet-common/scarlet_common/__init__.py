"""Pacchetto condiviso scarlet-common.

Espone i modelli Pydantic, le interfacce base e le utility comuni
utilizzati da tutti i microservizi del sistema Scarlet.
"""

from scarlet_common.logging import get_logger
from scarlet_common.models import (
    AgentMood,
    AgentState,
    AgentStatus,
    ApiResponse,
    ErrorResponse,
    Goal,
    GoalCreate,
    Message,
    MessageCreate,
    MessageRole,
    Session,
    SessionCreate,
    Task,
    TaskCreate,
    TaskPriority,
    TaskStatus,
)

__all__ = [
    "get_logger",
    "AgentMood",
    "AgentState",
    "AgentStatus",
    "ApiResponse",
    "ErrorResponse",
    "Goal",
    "GoalCreate",
    "Message",
    "MessageCreate",
    "MessageRole",
    "Session",
    "SessionCreate",
    "Task",
    "TaskCreate",
    "TaskPriority",
    "TaskStatus",
]
__version__ = "0.1.0"
