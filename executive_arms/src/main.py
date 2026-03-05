"""Executive Arms Service — servizi esecutivi di Scarlet.

Esegue fisicamente le operazioni richieste dall'agente:
navigazione web, esecuzione codice, operazioni sul filesystem.
Ogni operazione avviene in ambienti sandbox isolati.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from config.settings import settings
from scarlet_common.logging import get_logger

logger = get_logger(__name__, level=settings.log_level)


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncGenerator[None, None]:
    """Gestione del ciclo di vita degli Executive Arms."""
    logger.info("Executive Arms avviato su porta %s", settings.service_port)
    yield


app = FastAPI(
    title="Scarlet Executive Arms",
    description="Executive Arms — esecuzione operativa in ambienti sandbox.",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok", "service": "executive_arms"}
