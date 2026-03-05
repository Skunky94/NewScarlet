"""Configurazione del servizio Gateway caricata da variabili d'ambiente."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Impostazioni del Gateway."""

    service_host: str = "0.0.0.0"
    service_port: int = 8000
    log_level: str = "INFO"
    cortex_url: str = "http://cortex:8001"

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
