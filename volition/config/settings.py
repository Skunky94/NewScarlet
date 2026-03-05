"""Configurazione del Volition Service caricata da variabili d'ambiente."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Impostazioni del Volition Service."""

    service_host: str = "0.0.0.0"
    service_port: int = 8002
    log_level: str = "INFO"

    redis_url: str = "redis://redis:6379/0"
    cortex_url: str = "http://cortex:8001"

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
