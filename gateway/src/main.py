"""Gateway API — punto di ingresso unico del sistema Scarlet.

Riceve i messaggi degli utenti, li inoltra al Cortex e fornisce
endpoint per lo stato e l'osservazione in tempo reale.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from config.settings import settings
from scarlet_common.logging import get_logger
from src.router import router

logger = get_logger(__name__, level=settings.log_level)


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncGenerator[None, None]:
    """Gestione del ciclo di vita del Gateway."""
    logger.info("Gateway avviato su porta %s", settings.service_port)
    yield


app = FastAPI(
    title="Scarlet Gateway",
    description="API Gateway — punto di ingresso unico per il sistema Scarlet.",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(router)


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok", "service": "gateway"}
