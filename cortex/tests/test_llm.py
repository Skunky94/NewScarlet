"""Test integrazione T5: client MiniMax e loop di processamento messaggi.

Tutti gli import da `src` avvengono DENTRO i test (non a livello modulo),
così l'autouse fixture di conftest.py può isolare Cortex correttamente.
Httpx viene patchato nel modulo httpx direttamente, non through src.llm_client.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest


@pytest.mark.asyncio
async def test_generate_response_success() -> None:
    """Verifica che generate_response restituisca il testo dalla risposta MiniMax."""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "choices": [{"message": {"content": "Ciao! Sono Scarlet."}}]
    }
    mock_response.raise_for_status = MagicMock()

    mock_client = AsyncMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=None)
    mock_client.post = AsyncMock(return_value=mock_response)

    with patch("httpx.AsyncClient", return_value=mock_client):
        from src.llm_client import generate_response
        result = await generate_response("Ciao", [])

    assert result == "Ciao! Sono Scarlet."


@pytest.mark.asyncio
async def test_generate_response_malformed() -> None:
    """Verifica che una risposta malformata alzi ValueError."""
    mock_response = MagicMock()
    mock_response.json.return_value = {"choices": []}
    mock_response.raise_for_status = MagicMock()

    mock_client = AsyncMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=None)
    mock_client.post = AsyncMock(return_value=mock_response)

    with patch("httpx.AsyncClient", return_value=mock_client):
        from src.llm_client import generate_response
        with pytest.raises(ValueError):
            await generate_response("test", [])


@pytest.mark.asyncio
async def test_system_prompt_included() -> None:
    """Verifica che il System Prompt sia sempre il primo messaggio inviato."""
    captured_payload: dict = {}

    async def mock_post(url, json, headers):
        captured_payload.update(json)
        resp = MagicMock()
        resp.json.return_value = {"choices": [{"message": {"content": "ok"}}]}
        resp.raise_for_status = MagicMock()
        return resp

    mock_client = AsyncMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=None)
    mock_client.post = mock_post

    with patch("httpx.AsyncClient", return_value=mock_client):
        from src.llm_client import generate_response, SYSTEM_PROMPT
        await generate_response("test", [])

    assert captured_payload["messages"][0]["role"] == "system"
    assert captured_payload["messages"][0]["content"] == SYSTEM_PROMPT
