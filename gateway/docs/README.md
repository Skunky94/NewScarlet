# Gateway Service

Punto di ingresso unico del sistema Scarlet.

**Porta**: 8000  
**Dipendenze**: Cortex (`http://cortex:8001`)

## Endpoint

| Metodo | Path | Descrizione |
|---|---|---|
| `GET` | `/health` | Health check |
| `POST` | `/api/v1/interact` | Invio messaggio (implementato in T3) |
| `GET` | `/api/v1/status` | Stato agente (implementato in T3) |
| `WS` | `/api/v1/observe` | Stream pensieri in tempo reale (implementato in T3) |
