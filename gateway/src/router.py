"""Router per gli endpoint principali dell'API v1 del Gateway.

Gestisce la ricezione messaggi, la lettura dello stato agente
e lo stream WebSocket dei pensieri interni.
"""

import httpx
from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

from config.settings import settings
from scarlet_common.logging import get_logger
from scarlet_common.models import ApiResponse, MessageRole

logger = get_logger(__name__)

router = APIRouter(prefix="/api/v1", tags=["v1"])


class InteractRequest(BaseModel):
    """Payload per l'invio di un messaggio al sistema."""

    content: str
    session_id: str | None = None


class InteractAck(BaseModel):
    """Acknowledgment restituito al client dopo la ricezione del messaggio."""

    acknowledged: bool
    session_id: str
    message: str


@router.post("/interact", response_model=ApiResponse[InteractAck])
async def interact(request: InteractRequest) -> ApiResponse[InteractAck]:
    """Invia un messaggio all'agente.

    La risposta è un acknowledgment immediato; l'agente processerà
    il messaggio in modo asincrono secondo la coda delle priorità.

    Args:
        request: Contenuto del messaggio e session_id opzionale.

    Returns:
        ApiResponse con acknowledgment e session_id assegnato.
    """
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            payload = {
                "content": request.content,
                "role": MessageRole.USER,
                "session_id": request.session_id,
            }
            response = await client.post(
                f"{settings.cortex_url}/internal/message",
                json=payload,
            )
            response.raise_for_status()
            data = response.json()
    except httpx.HTTPError as exc:
        logger.error("Errore comunicazione con Cortex: %s", exc)
        raise HTTPException(status_code=503, detail="Cortex non raggiungibile") from exc

    ack = InteractAck(
        acknowledged=True,
        session_id=data.get("data", {}).get("session_id", ""),
        message="Messaggio ricevuto, elaborazione in corso.",
    )
    return ApiResponse(success=True, data=ack)


@router.get("/status", response_model=ApiResponse[dict])
async def get_status() -> ApiResponse[dict]:
    """Restituisce lo stato corrente dell'agente.

    Returns:
        ApiResponse con lo stato operativo, umore e task attivi.
    """
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{settings.cortex_url}/internal/state")
            response.raise_for_status()
            state = response.json()
    except httpx.HTTPError as exc:
        logger.error("Errore lettura stato Cortex: %s", exc)
        raise HTTPException(status_code=503, detail="Cortex non raggiungibile") from exc

    return ApiResponse(success=True, data=state)


@router.websocket("/observe")
async def observe(websocket: WebSocket) -> None:
    """Stream WebSocket dei pensieri interni dell'agente in tempo reale.

    Il client riceve eventi JSON con aggiornamenti sullo stato e le decisioni
    man mano che vengono generati dal Cortex.
    """
    await websocket.accept()
    logger.info("Nuova connessione WebSocket /observe")
    try:
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream("GET", f"{settings.cortex_url}/internal/observe") as stream:
                async for line in stream.aiter_lines():
                    if line:
                        await websocket.send_text(line)
    except httpx.HTTPError as exc:
        logger.error("Errore stream Cortex: %s", exc)
        await websocket.send_text('{"error": "stream interrotto"}')
    except WebSocketDisconnect:
        logger.info("Client WebSocket disconnesso")
