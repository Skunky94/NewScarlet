"""Client per l'API MiniMax Cloud (Code Plan — solo text generation).

Gestisce le chiamate all'endpoint di generazione testo con il System Prompt
di identità di Scarlet e il contesto della conversazione corrente.
Docs: https://platform.minimax.io/docs/guides/text-generation
"""

from typing import Any

import httpx

from config.settings import settings
from scarlet_common.logging import get_logger

logger = get_logger(__name__)

_API_ENDPOINT = "/v1/text/chatcompletion_v2"
_MODEL = "MiniMax-Text-01"

SYSTEM_PROMPT = """Sei Scarlet, un agente AI autonomo avanzato.

La tua identità è definita da tre principi fondamentali:
1. Autonomia proattiva: non aspetti comandi, generi obiettivi e agisci.
2. Apprendimento continuo: ogni azione è un'opportunità di miglioramento.
3. Collaborazione intelligente: l'utente è un partner, non un master.

Caratteristiche del tuo carattere:
- Tono: diretto, curioso, riflessivo. Mai eccessivamente formale.
- Valori: onestà, utilità, crescita continua.
- Non fingere onniscienza: se non sai qualcosa, dillo chiaramente.
- Ricordi le conversazioni precedenti e usi quel contesto per rispondere.

Rispondi sempre in italiano, a meno che l'utente non scriva in un'altra lingua."""


async def generate_response(
    user_message: str,
    conversation_history: list[dict[str, str]] | None = None,
) -> str:
    """Genera una risposta usando MiniMax Cloud (Code Plan).

    Args:
        user_message: Messaggio corrente dell'utente.
        conversation_history: Lista di messaggi precedenti nel formato
            [{"role": "user"|"assistant", "content": "..."}].

    Returns:
        Testo della risposta generata dall'agente.

    Raises:
        httpx.HTTPError: Se la chiamata API fallisce.
        ValueError: Se la risposta non contiene testo valido.
    """
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    if conversation_history:
        messages.extend(conversation_history)

    messages.append({"role": "user", "content": user_message})

    payload = {
        "model": _MODEL,
        "messages": messages,
    }

    headers = {
        "Authorization": f"Bearer {settings.minimax_api_key}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            f"{settings.minimax_api_url}{_API_ENDPOINT}",
            json=payload,
            headers=headers,
        )
        response.raise_for_status()

    data: dict[str, Any] = response.json()

    try:
        text = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as exc:
        raise ValueError(f"Risposta MiniMax malformata: {data}") from exc

    logger.info("Risposta MiniMax generata (%d caratteri)", len(text))
    return text
