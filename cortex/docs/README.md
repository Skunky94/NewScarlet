# Cortex Service

Orchestratore centrale del sistema Scarlet.

**Porta**: 8001  
**Dipendenze**: Redis, PostgreSQL, Memory Service

## Responsabilità

- Gestione stato interno dell'agente (umore, attenzione, obiettivi attivi)
- Loop principale asincrono di gestione priorità
- Coordinamento tra i componenti
- Integrazione con MiniMax LLM per generazione risposte
