"""Memory Service — gestione della memoria del sistema Scarlet.

Gestisce la memorizzazione e il recupero delle informazioni
a breve e lungo termine, incluse sessioni e messaggi.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from config.settings import settings
from scarlet_common.logging import get_logger
from src.database import init_db
from src.router import router

logger = get_logger(__name__, level=settings.log_level)


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncGenerator[None, None]:
    """Gestione del ciclo di vita: inizializza lo schema DB all'avvio."""
    logger.info("Memory Service avviato su porta %s", settings.service_port)
    await init_db()
    yield


app = FastAPI(
    title="Scarlet Memory",
    description="Memory Service — memorizzazione e ricerca semantica.",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(router)


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok", "service": "memory"}
