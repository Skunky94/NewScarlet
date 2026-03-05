"""Modelli Pydantic per le risposte API standardizzate.

Garantisce uniformità nelle risposte di tutti i microservizi.
"""

from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """Risposta API generica con campo dati opzionale."""

    success: bool
    data: Optional[T] = None
    message: Optional[str] = None


class ErrorResponse(BaseModel):
    """Risposta di errore standardizzata."""

    success: bool = False
    error: str
    detail: Optional[str] = None
