"""Router del Memory Service — endpoint CRUD per sessioni e messaggi."""

from fastapi import APIRouter, HTTPException

from scarlet_common.logging import get_logger
from scarlet_common.models import (
    ApiResponse,
    Message,
    MessageCreate,
    Session,
    SessionCreate,
)
from src.crud import (
    add_message,
    create_session,
    get_messages_by_session,
    get_session_by_id,
)
from src.database import get_session

logger = get_logger(__name__)

router = APIRouter(prefix="/api/v1", tags=["memory"])


@router.post("/sessions", response_model=ApiResponse[Session])
async def create_new_session(data: SessionCreate) -> ApiResponse[Session]:
    """Crea una nuova sessione di conversazione.

    Returns:
        ApiResponse con la Session creata.
    """
    async with await get_session() as db:
        session = await create_session(db, data)
    return ApiResponse(success=True, data=session)


@router.get("/sessions/{session_id}", response_model=ApiResponse[Session])
async def get_session_endpoint(session_id: str) -> ApiResponse[Session]:
    """Recupera una sessione per ID.

    Args:
        session_id: UUID della sessione.

    Returns:
        ApiResponse con la Session trovata.
    """
    async with await get_session() as db:
        session = await get_session_by_id(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Sessione non trovata")
    return ApiResponse(success=True, data=session)


@router.post("/messages", response_model=ApiResponse[Message])
async def add_new_message(data: MessageCreate) -> ApiResponse[Message]:
    """Aggiunge un messaggio a una sessione.

    Args:
        data: Contenuto del messaggio con session_id e role.

    Returns:
        ApiResponse con il Message salvato.
    """
    async with await get_session() as db:
        message = await add_message(db, data)
    return ApiResponse(success=True, data=message)


@router.get("/sessions/{session_id}/messages", response_model=ApiResponse[list[Message]])
async def get_session_messages(session_id: str, limit: int = 50) -> ApiResponse[list[Message]]:
    """Recupera i messaggi di una sessione.

    Args:
        session_id: UUID della sessione.
        limit: Numero massimo di messaggi (default 50).

    Returns:
        ApiResponse con la lista di Message ordinati cronologicamente.
    """
    async with await get_session() as db:
        messages = await get_messages_by_session(db, session_id, limit=limit)
    return ApiResponse(success=True, data=messages)
