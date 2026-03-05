"""Cortex — orchestratore centrale del sistema Scarlet.

Gestisce lo stato interno dell'agente, coordina i componenti
e mantiene il loop principale di gestione delle priorità.
"""

import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from config.settings import settings
from scarlet_common.logging import get_logger
from src.internal_router import router
from src.loop import run_loop

logger = get_logger(__name__, level=settings.log_level)


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncGenerator[None, None]:
    """Gestione del ciclo di vita del Cortex: avvia il loop principale."""
    logger.info("Cortex avviato su porta %s", settings.service_port)
    loop_task = asyncio.create_task(run_loop())
    try:
        yield
    finally:
        loop_task.cancel()
        logger.info("Cortex: loop principale fermato")


app = FastAPI(
    title="Scarlet Cortex",
    description="Orchestratore centrale — gestione stato e decisioni ad alto livello.",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(router)


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok", "service": "cortex"}
