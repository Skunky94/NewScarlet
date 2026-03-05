"""Modelli Pydantic per task e obiettivi generati da Volition.

Rappresentano le unità di lavoro che Scarlet esegue in modo autonomo.
"""

from datetime import UTC, datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    """Stato di avanzamento di un task."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskPriority(int, Enum):
    """Livello di priorità di un task (più alto = più urgente)."""

    LOW = 1
    NORMAL = 5
    HIGH = 8
    CRITICAL = 10


class Task(BaseModel):
    """Unità di lavoro eseguibile dall'agente."""

    id: UUID = Field(default_factory=uuid4)
    goal_id: Optional[UUID] = None
    title: str
    description: str
    priority: TaskPriority = TaskPriority.NORMAL
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class Goal(BaseModel):
    """Obiettivo di alto livello generato da Volition."""

    id: UUID = Field(default_factory=uuid4)
    title: str
    description: str
    directive_source: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    completed: bool = False


class TaskCreate(BaseModel):
    """Payload per la creazione di un nuovo task."""

    title: str
    description: str
    priority: TaskPriority = TaskPriority.NORMAL
    goal_id: Optional[UUID] = None


class GoalCreate(BaseModel):
    """Payload per la creazione di un nuovo obiettivo."""

    title: str
    description: str
    directive_source: str
