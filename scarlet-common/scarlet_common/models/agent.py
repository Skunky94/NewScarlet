"""Modelli Pydantic per lo stato interno dell'agente (Cortex).

Descrivono la condizione corrente di Scarlet in un dato momento.
"""

from datetime import UTC, datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class AgentMood(str, Enum):
    """Stato emotivo corrente dell'agente."""

    NEUTRAL = "neutral"
    FOCUSED = "focused"
    CURIOUS = "curious"
    ALERT = "alert"


class AgentStatus(str, Enum):
    """Stato operativo dell'agente."""

    IDLE = "idle"
    PROCESSING = "processing"
    EXECUTING = "executing"
    WAITING = "waiting"


class AgentState(BaseModel):
    """Stato interno corrente dell'agente Scarlet."""

    status: AgentStatus = AgentStatus.IDLE
    mood: AgentMood = AgentMood.NEUTRAL
    attention_level: float = Field(default=1.0, ge=0.0, le=1.0)
    active_task_id: Optional[UUID] = None
    current_goal: Optional[str] = None
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
