# DEVNOTES — Scarlet Development Notepad

> File di appunti personale per l'agente. Contiene piano corrente, task, stato avanzamento e note tecniche.
> Viene aggiornato continuamente e le parti obsolete vengono rimosse.

---

## Stato Corrente

**Fase attiva**: Fase 1 — Fondamenta ✅ COMPLETATA  
**Ultima implementazione**: T7 — Test integrazione E2E (26/26 test passano)  
**Prossimo step**: Presentare riepilogo Fase 1 + piano Fase 2 (Volition) per approvazione utente

---

## Piano Fase 1 — Fondamenta

### Obiettivo
Chatbot funzionante con personalità persistente, memoria delle conversazioni, avviabile con `docker-compose up`.

### Task

| ID  | Titolo                                      | Stato       | Dipende da |
|-----|---------------------------------------------|-------------|------------|
| T1  | Struttura repository + infrastruttura base  | ✅ fatto    | —          |
| T2  | `scarlet-common`: modelli Pydantic condivisi | ✅ fatto    | T1         |
| T3  | API Gateway scheletro FastAPI + endpoint    | ✅ fatto    | T2         |
| T4  | Cortex: stato interno + loop principale     | ✅ fatto    | T2         |
| T5  | Cortex: integrazione MiniMax LLM + identità | ✅ fatto    | T4         |
| T6  | Memory Service: schema PostgreSQL + CRUD    | ✅ fatto    | T2         |
| T7  | Test integrazione end-to-end Fase 1         | ✅ fatto    | T3, T5, T6 |

### Legenda stato
`⬜ todo` | `🔄 in corso` | `✅ fatto` | `❌ bloccato`

---

## Note Tecniche Correnti

- **LLM**: MiniMax Cloud, Code Plan (solo text), `https://api.minimax.io`
- **API Key**: variabile `MINIMAX_API_KEY` in `.env` (non nel repo)
- **Docker**: `docker-compose up` deve avviare tutto da zero senza configurazione manuale
- **Pacchetto comune**: `scarlet-common` importato da tutti i servizi come dipendenza locale
- **Redis**: uso esclusivo per code priorità asincrona e stato condiviso
- **PostgreSQL**: persistenza sessioni, messaggi, stato agente
- **pytest**: 26 test, tutti passano. Isolamento `sys.modules` via autouse fixture in ogni `service/tests/conftest.py` + `__init__.py` nei root dei servizi per nomi conftest univoci.

---

## Decisioni Prese

- `importmode=importlib` in pytest.ini per evitare collisioni tra package `tests/` di servizi diversi
- Ogni servizio ha `__init__.py` nella root (es. `cortex/__init__.py`) per rendere i conftest univoci (`cortex.tests.conftest`, `gateway.tests.conftest` ecc.)
- Autouse fixture in ogni `conftest.py` che isola `src/*` e `config/*` in `sys.modules` per ogni test
- `patch("httpx.AsyncClient")` preferito a `patch("src.llm_client.httpx.AsyncClient")` per i test LLM (evita problemi di risoluzione moduli con importlib)
- Gateway estrae `session_id` da `data["data"]["session_id"]` (risposta Cortex usa `ApiResponse[dict]`)

---

## Blocchi / Problemi Aperti

- Nessuno

---

## Informazioni utili / Da ricordare

- Suite completa: `pytest` dalla root → 26 test, ~7s
- `docker-compose config` OK (nessun errore di sintassi)

