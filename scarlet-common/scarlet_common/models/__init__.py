"""Modelli Pydantic condivisi — package init."""

from scarlet_common.models.agent import AgentMood, AgentState, AgentStatus
from scarlet_common.models.conversation import (
    Message,
    MessageCreate,
    MessageRole,
    Session,
    SessionCreate,
)
from scarlet_common.models.responses import ApiResponse, ErrorResponse
from scarlet_common.models.tasks import Goal, GoalCreate, Task, TaskCreate, TaskPriority, TaskStatus

__all__ = [
    "AgentMood",
    "AgentState",
    "AgentStatus",
    "Message",
    "MessageCreate",
    "MessageRole",
    "Session",
    "SessionCreate",
    "ApiResponse",
    "ErrorResponse",
    "Goal",
    "GoalCreate",
    "Task",
    "TaskCreate",
    "TaskPriority",
    "TaskStatus",
]
