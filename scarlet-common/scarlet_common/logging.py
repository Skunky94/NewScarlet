"""Configurazione centralizzata del logging per tutti i servizi Scarlet.

Ogni servizio ottiene un logger strutturato in formato JSON su stdout,
garantendo uniformità di output e facilità di aggregazione dei log.
"""

import logging
import sys
from typing import Optional


def get_logger(name: str, level: Optional[str] = None) -> logging.Logger:
    """Restituisce un logger configurato per il servizio specificato.

    Args:
        name: Nome del logger (tipicamente __name__ del modulo chiamante).
        level: Livello di logging opzionale. Default: INFO.

    Returns:
        Logger configurato con output JSON strutturato su stdout.
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            fmt=(
                '{"time": "%(asctime)s", "level": "%(levelname)s",'
                ' "service": "%(name)s", "message": "%(message)s"}'
            ),
            datefmt="%Y-%m-%dT%H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.propagate = False

    log_level = level or "INFO"
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    return logger
