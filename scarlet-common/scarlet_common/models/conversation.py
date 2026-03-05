"""Modelli Pydantic condivisi per la gestione delle sessioni e dei messaggi.

Utilizzati da Cortex, Gateway e Memory Service.
"""

from datetime import UTC, datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class MessageRole(str, Enum):
    """Ruolo del mittente in un messaggio."""

    USER = "user"
    AGENT = "agent"
    SYSTEM = "system"


class Message(BaseModel):
    """Singolo messaggio all'interno di una sessione."""

    id: UUID = Field(default_factory=uuid4)
    session_id: UUID
    role: MessageRole
    content: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class Session(BaseModel):
    """Sessione di conversazione tra utente e agente."""

    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    metadata: dict = Field(default_factory=dict)


class MessageCreate(BaseModel):
    """Payload per la creazione di un nuovo messaggio."""

    session_id: UUID
    role: MessageRole
    content: str


class SessionCreate(BaseModel):
    """Payload per la creazione di una nuova sessione."""

    metadata: Optional[dict] = Field(default_factory=dict)
