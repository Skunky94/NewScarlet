"""Configurazione del Memory Service caricata da variabili d'ambiente."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Impostazioni del Memory Service."""

    service_host: str = "0.0.0.0"
    service_port: int = 8003
    log_level: str = "INFO"

    database_url: str = "postgresql+asyncpg://scarlet:scarlet@postgres:5432/scarlet"

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
