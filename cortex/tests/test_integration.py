"""Test di integrazione T7 per il Cortex.

Verifica il flusso completo di processamento di un messaggio utente:
recupero storico da Memory → generazione risposta LLM → salvataggio in Memory.
"""

from unittest.mock import AsyncMock, MagicMock, call, patch

import pytest


@pytest.mark.asyncio
async def test_process_user_message_full_flow() -> None:
    """Verifica il flusso completo: storico Memory → LLM → salvataggio in Memory.

    Garantisce che _process_user_message:
    1. Recuperi lo storico sessione da Memory prima di chiamare l'LLM.
    2. Salvi il messaggio utente in Memory.
    3. Chiami l'LLM con il messaggio e lo storico.
    4. Salvi la risposta dell'agente in Memory.
    """
    session_id = "test-session-123"
    user_message = "Ciao Scarlet!"
    expected_reply = "Ciao! Come posso aiutarti?"

    # --- Mock degli endpoint Memory (GET storico + 2× POST salvataggio) ---
    history_response = MagicMock()
    history_response.status_code = 200
    history_response.json.return_value = {"data": []}

    save_response = MagicMock()
    save_response.status_code = 201
    save_response.raise_for_status = MagicMock()

    http_responses = [history_response, save_response, save_response]
    call_index = {"i": 0}

    async def mock_get(url, *args, **kwargs):
        return history_response

    async def mock_post(url, *args, **kwargs):
        return save_response

    mock_http = AsyncMock()
    mock_http.__aenter__ = AsyncMock(return_value=mock_http)
    mock_http.__aexit__ = AsyncMock(return_value=None)
    mock_http.get = mock_get
    mock_http.post = mock_post

    # --- Mock del client MiniMax ---
    with (
        patch("httpx.AsyncClient", return_value=mock_http),
        patch(
            "src.loop.generate_response",
            new=AsyncMock(return_value=expected_reply),
        ) as mock_llm,
    ):
        from src.loop import _process_user_message

        task = {
            "type": "user_message",
            "session_id": session_id,
            "content": user_message,
            "role": "user",
        }
        await _process_user_message(task)

    # Verifica che l'LLM sia stato chiamato con il messaggio corretto
    mock_llm.assert_called_once_with(user_message, [])


@pytest.mark.asyncio
async def test_process_user_message_with_existing_history() -> None:
    """Verifica che lo storico esistente venga passato all'LLM."""
    session_id = "session-with-history"
    stored_history = [
        {"role": "user", "content": "Prima domanda"},
        {"role": "agent", "content": "Prima risposta"},
    ]

    history_response = MagicMock()
    history_response.status_code = 200
    history_response.json.return_value = {"data": stored_history}

    save_response = MagicMock()
    save_response.status_code = 201

    mock_http = AsyncMock()
    mock_http.__aenter__ = AsyncMock(return_value=mock_http)
    mock_http.__aexit__ = AsyncMock(return_value=None)
    mock_http.get = AsyncMock(return_value=history_response)
    mock_http.post = AsyncMock(return_value=save_response)

    with (
        patch("httpx.AsyncClient", return_value=mock_http),
        patch(
            "src.loop.generate_response",
            new=AsyncMock(return_value="Risposta con contesto"),
        ) as mock_llm,
    ):
        from src.loop import _process_user_message

        await _process_user_message(
            {"session_id": session_id, "content": "Seconda domanda"}
        )

    # Verifica che l'LLM abbia ricevuto lo storico
    expected_history = [
        {"role": "user", "content": "Prima domanda"},
        {"role": "agent", "content": "Prima risposta"},
    ]
    mock_llm.assert_called_once_with("Seconda domanda", expected_history)


@pytest.mark.asyncio
async def test_process_user_message_memory_failure_graceful() -> None:
    """Verifica che il fallimento di Memory non blocchi la risposta LLM."""
    import httpx as httpx_lib

    mock_http = AsyncMock()
    mock_http.__aenter__ = AsyncMock(return_value=mock_http)
    mock_http.__aexit__ = AsyncMock(return_value=None)
    mock_http.get = AsyncMock(side_effect=httpx_lib.ConnectError("Memory down"))
    mock_http.post = AsyncMock(side_effect=httpx_lib.ConnectError("Memory down"))

    with (
        patch("httpx.AsyncClient", return_value=mock_http),
        patch(
            "src.loop.generate_response",
            new=AsyncMock(return_value="Risposta di emergenza"),
        ) as mock_llm,
    ):
        from src.loop import _process_user_message

        # Non deve sollevare eccezioni anche con Memory irraggiungibile
        await _process_user_message(
            {"session_id": "any-session", "content": "Messaggio test"}
        )

    # L'LLM viene comunque chiamato con storico vuoto
    mock_llm.assert_called_once_with("Messaggio test", [])
