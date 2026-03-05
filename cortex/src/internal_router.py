"""Router interno del Cortex — endpoint usati dagli altri servizi.

Non esposti pubblicamente: accessibili solo dalla rete Docker interna.
"""

import asyncio
import json as json_lib

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from scarlet_common.logging import get_logger
from scarlet_common.models import AgentState, ApiResponse, MessageRole
from src.loop import enqueue_task
from src.state import read_state, write_state

logger = get_logger(__name__)

router = APIRouter(prefix="/internal", tags=["internal"])


class IncomingMessage(BaseModel):
    """Messaggio in arrivo dal Gateway."""

    content: str
    role: MessageRole
    session_id: str | None = None


@router.post("/message", response_model=ApiResponse[dict])
async def receive_message(msg: IncomingMessage) -> ApiResponse[dict]:
    """Riceve un messaggio dal Gateway e lo accoda per l'elaborazione.

    Args:
        msg: Messaggio dell'utente con contenuto e session_id.

    Returns:
        ApiResponse con il session_id assegnato.
    """
    import uuid

    session_id = msg.session_id or str(uuid.uuid4())
    task_id = str(uuid.uuid4())

    await enqueue_task(
        task_id=task_id,
        priority=5,
        payload={
            "type": "user_message",
            "session_id": session_id,
            "content": msg.content,
            "role": msg.role,
        },
    )
    logger.info("Messaggio accodato — session_id=%s task_id=%s", session_id, task_id)
    return ApiResponse(success=True, data={"session_id": session_id, "task_id": task_id})


@router.get("/state", response_model=AgentState)
async def get_state() -> AgentState:
    """Restituisce lo stato interno corrente dell'agente.

    Returns:
        AgentState aggiornato.
    """
    return await read_state()


@router.get("/observe")
async def observe_stream() -> StreamingResponse:
    """Stream SSE dei pensieri interni dell'agente.

    Invia aggiornamenti di stato ogni secondo come Server-Sent Events.
    """

    async def event_generator():
        while True:
            state = await read_state()
            data = json_lib.dumps(state.model_dump(mode="json"), default=str)
            yield f"{data}\n"
            await asyncio.sleep(1.0)

    return StreamingResponse(event_generator(), media_type="text/plain")
