"""Reflection Service — modulo di apprendimento di Scarlet.

Valuta le azioni eseguite confrontandole con gli obiettivi prefissati
e adatta il comportamento futuro sulla base dei risultati.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from config.settings import settings
from scarlet_common.logging import get_logger

logger = get_logger(__name__, level=settings.log_level)


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncGenerator[None, None]:
    """Gestione del ciclo di vita del Reflection Service."""
    logger.info("Reflection Service avviato su porta %s", settings.service_port)
    yield


app = FastAPI(
    title="Scarlet Reflection",
    description="Reflection Service — valutazione azioni e apprendimento continuo.",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok", "service": "reflection"}
