"""Gestione dello stato interno dell'agente su Redis.

Lo stato è persistito in Redis come JSON e aggiornato dal loop principale.
Ogni componente che necessita dello stato lo legge via questo modulo.
"""

import json
from datetime import UTC, datetime

import redis.asyncio as aioredis

from config.settings import settings
from scarlet_common.logging import get_logger
from scarlet_common.models import AgentState, AgentStatus

logger = get_logger(__name__)

_REDIS_STATE_KEY = "scarlet:agent_state"


async def get_redis() -> aioredis.Redis:
    """Restituisce un client Redis asincrono.

    Returns:
        Connessione Redis pronta all'uso.
    """
    return aioredis.from_url(settings.redis_url, decode_responses=True)


async def read_state() -> AgentState:
    """Legge lo stato corrente dell'agente da Redis.

    Returns:
        AgentState corrente. Se non esiste restituisce lo stato di default.
    """
    redis = await get_redis()
    try:
        raw = await redis.get(_REDIS_STATE_KEY)
        if raw:
            return AgentState.model_validate_json(raw)
        return AgentState()
    finally:
        await redis.aclose()


async def write_state(state: AgentState) -> None:
    """Scrive lo stato aggiornato dell'agente su Redis.

    Args:
        state: Nuovo stato da persistere.
    """
    state.updated_at = datetime.now(UTC)
    redis = await get_redis()
    try:
        await redis.set(_REDIS_STATE_KEY, state.model_dump_json())
    finally:
        await redis.aclose()


async def update_status(status: AgentStatus) -> None:
    """Aggiorna solo il campo status dello stato agente.

    Args:
        status: Nuovo status operativo.
    """
    state = await read_state()
    state.status = status
    await write_state(state)
