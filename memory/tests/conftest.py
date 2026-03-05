"""Configurazione pytest per il servizio Memory.

Autouse fixture che isola src/config del Memory in sys.modules
per ogni singolo test, prevenendo contaminazione cross-service.
"""

import sys
from pathlib import Path

import pytest

_SERVICE_ROOT = str(Path(__file__).parent.parent)


@pytest.fixture(autouse=True)
def _setup_memory_imports() -> None:
    """Garantisce che `src` e `config` puntino a Memory durante ogni test."""
    for key in list(sys.modules.keys()):
        if key in ("src", "config") or key.startswith("src.") or key.startswith("config."):
            del sys.modules[key]
    if _SERVICE_ROOT in sys.path:
        sys.path.remove(_SERVICE_ROOT)
    sys.path.insert(0, _SERVICE_ROOT)
    yield
    for key in list(sys.modules.keys()):
        if key in ("src", "config") or key.startswith("src.") or key.startswith("config."):
            del sys.modules[key]
