"""Configurazione del Cortex caricata da variabili d'ambiente."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Impostazioni del Cortex."""

    service_host: str = "0.0.0.0"
    service_port: int = 8001
    log_level: str = "INFO"

    redis_url: str = "redis://redis:6379/0"
    database_url: str = "postgresql+asyncpg://scarlet:scarlet@postgres:5432/scarlet"
    memory_url: str = "http://memory:8003"

    minimax_api_key: str = ""
    minimax_api_url: str = "https://api.minimax.io"

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
