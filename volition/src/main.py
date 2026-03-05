"""Volition Service — motore dell'autonomia di Scarlet.

Genera obiettivi e compiti in modo proattivo basandosi
sulle direttive primarie e sul contesto corrente dell'agente.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from config.settings import settings
from scarlet_common.logging import get_logger

logger = get_logger(__name__, level=settings.log_level)


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncGenerator[None, None]:
    """Gestione del ciclo di vita del Volition Service."""
    logger.info("Volition Service avviato su porta %s", settings.service_port)
    yield


app = FastAPI(
    title="Scarlet Volition",
    description="Volition Service — generazione autonoma di obiettivi e compiti.",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok", "service": "volition"}
