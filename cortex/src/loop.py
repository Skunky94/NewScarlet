"""Loop principale asincrono del Cortex.

Controlla la coda delle priorità su Redis, processa i task in ordine
e mantiene lo stato dell'agente aggiornato durante l'esecuzione.
"""

import asyncio
import json

import httpx
import redis.asyncio as aioredis

from config.settings import settings
from scarlet_common.logging import get_logger
from scarlet_common.models import AgentStatus, MessageRole
from src.llm_client import generate_response
from src.state import get_redis, update_status

logger = get_logger(__name__)

_TASK_QUEUE_KEY = "scarlet:task_queue"
_LOOP_INTERVAL_SEC = 1.0


async def enqueue_task(task_id: str, priority: int, payload: dict) -> None:
    """Inserisce un task nella coda prioritaria Redis (sorted set).

    Args:
        task_id: Identificatore univoco del task.
        priority: Punteggio di priorità (più alto = più urgente).
        payload: Dati del task serializzabili in JSON.
    """
    redis = await get_redis()
    try:
        score = -priority  # Redis sorted set: score più basso = priorità massima
        await redis.zadd(_TASK_QUEUE_KEY, {json.dumps({"id": task_id, **payload}): score})
        logger.info("Task %s accodato con priorità %s", task_id, priority)
    finally:
        await redis.aclose()


async def dequeue_next_task() -> dict | None:
    """Estrae il task con priorità più alta dalla coda.

    Returns:
        Dizionario del task oppure None se la coda è vuota.
    """
    redis = await get_redis()
    try:
        results = await redis.zpopmin(_TASK_QUEUE_KEY, count=1)
        if results:
            raw, _ = results[0]
            return json.loads(raw)
        return None
    finally:
        await redis.aclose()


async def _process_user_message(task: dict) -> None:
    """Processa un messaggio utente: genera risposta LLM e salva in Memory.

    Args:
        task: Dizionario del task con session_id e content.
    """
    session_id = task.get("session_id", "")
    content = task.get("content", "")

    # Recupera storico messaggi dal Memory Service
    history: list[dict[str, str]] = []
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(
                f"{settings.memory_url}/api/v1/sessions/{session_id}/messages"
            )
            if resp.status_code == 200:
                msgs = resp.json().get("data", [])
                history = [{"role": m["role"], "content": m["content"]} for m in msgs]
    except httpx.HTTPError as exc:
        logger.warning("Impossibile recuperare storico da Memory: %s", exc)

    # Salva il messaggio utente in Memory
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            await client.post(
                f"{settings.memory_url}/api/v1/messages",
                json={"session_id": session_id, "role": "user", "content": content},
            )
    except httpx.HTTPError as exc:
        logger.warning("Impossibile salvare messaggio utente in Memory: %s", exc)

    # Genera risposta con MiniMax
    try:
        reply = await generate_response(content, history)
    except Exception as exc:
        logger.error("Errore generazione risposta LLM: %s", exc)
        reply = "Mi dispiace, si è verificato un errore nella generazione della risposta."

    # Salva risposta dell'agente in Memory
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            await client.post(
                f"{settings.memory_url}/api/v1/messages",
                json={"session_id": session_id, "role": "agent", "content": reply},
            )
    except httpx.HTTPError as exc:
        logger.warning("Impossibile salvare risposta agente in Memory: %s", exc)

    logger.info("Messaggio processato — session_id=%s", session_id)


async def run_loop() -> None:
    """Loop principale del Cortex.

    Controlla continuamente la coda dei task e li processa in ordine
    di priorità. Il loop si mantiene non bloccante tramite asyncio.sleep.
    """
    logger.info("Loop principale Cortex avviato")
    await update_status(AgentStatus.IDLE)

    while True:
        try:
            task = await dequeue_next_task()
            if task:
                task_type = task.get("type")
                logger.info("Elaborazione task: %s (tipo: %s)", task.get("id"), task_type)
                await update_status(AgentStatus.PROCESSING)

                if task_type == "user_message":
                    await _process_user_message(task)

                await update_status(AgentStatus.IDLE)
            else:
                await asyncio.sleep(_LOOP_INTERVAL_SEC)
        except asyncio.CancelledError:
            break
        except Exception as exc:
            logger.error("Errore nel loop principale: %s", exc)
            await asyncio.sleep(_LOOP_INTERVAL_SEC)
