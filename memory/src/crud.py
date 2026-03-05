"""Operazioni CRUD per sessioni e messaggi.

Ogni funzione riceve una sessione database come dipendenza
e restituisce modelli Pydantic da scarlet-common.
"""

from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from scarlet_common.logging import get_logger
from scarlet_common.models import Message, MessageCreate, MessageRole, Session, SessionCreate
from src.database import MessageRecord, SessionRecord

logger = get_logger(__name__)


async def create_session(db: AsyncSession, data: SessionCreate) -> Session:
    """Crea una nuova sessione nel database.

    Args:
        db: Sessione database asincrona.
        data: Dati della nuova sessione.

    Returns:
        Session creata con id e timestamp.
    """
    record = SessionRecord(
        id=str(uuid4()),
        metadata_=data.metadata or {},
    )
    db.add(record)
    await db.commit()
    await db.refresh(record)
    logger.info("Sessione creata: %s", record.id)
    return Session(id=record.id, metadata=record.metadata_)


async def get_session_by_id(db: AsyncSession, session_id: str) -> Session | None:
    """Recupera una sessione per ID.

    Args:
        db: Sessione database asincrona.
        session_id: UUID della sessione cercata.

    Returns:
        Session trovata oppure None.
    """
    result = await db.execute(select(SessionRecord).where(SessionRecord.id == session_id))
    record = result.scalar_one_or_none()
    if not record:
        return None
    return Session(id=record.id, metadata=record.metadata_)


async def add_message(db: AsyncSession, data: MessageCreate) -> Message:
    """Aggiunge un messaggio a una sessione esistente.

    Args:
        db: Sessione database asincrona.
        data: Contenuto e metadati del messaggio.

    Returns:
        Message salvato con id e timestamp.
    """
    record = MessageRecord(
        id=str(uuid4()),
        session_id=str(data.session_id),
        role=data.role.value,
        content=data.content,
    )
    db.add(record)
    await db.commit()
    await db.refresh(record)
    return Message(
        id=record.id,
        session_id=record.session_id,
        role=MessageRole(record.role),
        content=record.content,
    )


async def get_messages_by_session(
    db: AsyncSession,
    session_id: str,
    limit: int = 50,
) -> list[Message]:
    """Recupera i messaggi di una sessione in ordine cronologico.

    Args:
        db: Sessione database asincrona.
        session_id: UUID della sessione.
        limit: Numero massimo di messaggi da restituire.

    Returns:
        Lista di Message ordinati per created_at ascendente.
    """
    result = await db.execute(
        select(MessageRecord)
        .where(MessageRecord.session_id == session_id)
        .order_by(MessageRecord.created_at.asc())
        .limit(limit)
    )
    records = result.scalars().all()
    return [
        Message(
            id=r.id,
            session_id=r.session_id,
            role=MessageRole(r.role),
            content=r.content,
        )
        for r in records
    ]
