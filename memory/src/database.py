"""Schema SQLAlchemy e gestione connessione al database PostgreSQL.

Definisce le tabelle per sessioni e messaggi, e fornisce
la factory della sessione asincrona per le operazioni CRUD.
"""

from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import JSON, Boolean, DateTime, String, Text, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from config.settings import settings
from scarlet_common.logging import get_logger

logger = get_logger(__name__)

engine = create_async_engine(settings.database_url, echo=False, pool_pre_ping=True)
AsyncSessionFactory = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    """Base per tutti i modelli ORM del Memory Service."""


class SessionRecord(Base):
    """Tabella delle sessioni di conversazione."""

    __tablename__ = "sessions"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )
    metadata_: Mapped[dict] = mapped_column("metadata", JSON, default=dict)


class MessageRecord(Base):
    """Tabella dei messaggi all'interno di una sessione."""

    __tablename__ = "messages"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
    )
    session_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )


async def init_db() -> None:
    """Crea le tabelle nel database se non esistono.

    Invocato all'avvio del Memory Service.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Schema database inizializzato")


async def get_session() -> AsyncSession:
    """Restituisce una sessione database asincrona.

    Returns:
        AsyncSession pronta per le operazioni CRUD.
    """
    return AsyncSessionFactory()
