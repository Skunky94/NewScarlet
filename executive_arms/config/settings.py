"""Configurazione degli Executive Arms caricata da variabili d'ambiente."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Impostazioni degli Executive Arms."""

    service_host: str = "0.0.0.0"
    service_port: int = 8005
    log_level: str = "INFO"

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
