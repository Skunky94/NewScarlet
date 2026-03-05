"""Configurazione del Reflection Service caricata da variabili d'ambiente."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Impostazioni del Reflection Service."""

    service_host: str = "0.0.0.0"
    service_port: int = 8004
    log_level: str = "INFO"

    memory_url: str = "http://memory:8003"

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
