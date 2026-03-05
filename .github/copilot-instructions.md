# Copilot Instructions — Progetto Scarlet

## Panoramica del Progetto

Scarlet è un sistema AI autonomo avanzato basato su architettura a microservizi. L'agente opera in modo proattivo, genera obiettivi autonomamente, apprende dalle esperienze, e collabora con l'utente come partner. Il progetto è in fase di pianificazione iniziale con documentazione architetturale definita.

## Tech Stack

- **Linguaggio**: Python 3.10+
- **Framework Web**: FastAPI (servizi REST asincroni)
- **Code e stato condiviso**: Redis
- **Database relazionale**: PostgreSQL
- **Database vettoriale**: Qdrant o ChromaDB
- **Orchestrazione LLM**: LangChain o LlamaIndex
- **LLM principale**: MiniMax Cloud (modello Code Plan, solo text generation)
- **API LLM**: `https://api.minimax.io` — docs: `https://platform.minimax.io/docs/guides/text-generation`
- **Containerizzazione**: Docker + Docker Compose
- **Testing**: pytest
- **Validazione dati**: Pydantic

> **Nota**: La API key MiniMax va configurata nella variabile d'ambiente `MINIMAX_API_KEY` nel file `.env` locale (mai nel repository).

## Architettura

Il sistema è composto da sei componenti principali, ciascuno un microservizio indipendente con API REST:

| Componente | Ruolo |
|---|---|
| **Cortex** | Orchestratore centrale, gestione stato e decisioni ad alto livello |
| **Volition** | Motore dell'autonomia, generazione obiettivi e compiti |
| **Memory** | Memorizzazione a breve/lungo termine, ricerca semantica |
| **Reflection** | Valutazione azioni e apprendimento continuo |
| **Executive Arms** | Esecuzione operativa (Browser, Coder, System Service) |
| **API Gateway** | Punto di ingresso unico per utenti esterni |

### Comunicazione tra servizi

- I servizi comunicano esclusivamente via API REST con JSON.
- Non accedere direttamente ai database di altri servizi.
- Usare Redis per le code di messaggi asincrone.
- Validare tutti i dati con modelli Pydantic da `scarlet-common`.

## Struttura delle Directory

```
scarlet/
├── cortex/
│   ├── src/
│   ├── tests/
│   ├── config/
│   └── docs/
├── volition/
│   ├── src/
│   ├── tests/
│   ├── config/
│   └── docs/
├── memory/
│   ├── src/
│   ├── tests/
│   ├── config/
│   └── docs/
├── reflection/
│   ├── src/
│   ├── tests/
│   ├── config/
│   └── docs/
├── executive_arms/
│   ├── src/
│   ├── tests/
│   ├── config/
│   └── docs/
├── gateway/
│   ├── src/
│   ├── tests/
│   ├── config/
│   └── docs/
├── scarlet-common/          # Pacchetto condiviso (modelli Pydantic, interfacce, utility)
├── docker-compose.yml
├── pyproject.toml
└── README.md
```

## Standard di Codifica Python

### Formattazione

- Indentazione: **4 spazi** (mai tab).
- Lunghezza massima riga: **100 caratteri**.
- Seguire **PEP 8** per stile e convenzioni.

### Naming

- File: **snake_case** con nomi descrittivi (es. `goal_generator.py`, `memory_store.py`).
- **Vietati** nomi generici come `utils.py` o `helpers.py`.
- Classi: **PascalCase**.
- Funzioni e variabili: **snake_case**.

### Type Annotations

Le type annotations sono **obbligatorie** per tutte le funzioni e metodi, inclusi i parametri di ritorno:

```python
def generate_goal(directive: str, context: AgentState) -> Goal:
    ...
```

### Docstring

Formato **Google** o **NumPy**. Ogni funzione pubblica deve documentare scopo, parametri e valori di ritorno:

```python
def evaluate_action(action: Action, expected: Outcome) -> Evaluation:
    """Valuta il risultato di un'azione confrontandolo con l'obiettivo.

    Args:
        action: L'azione eseguita da valutare.
        expected: L'outcome atteso dall'azione.

    Returns:
        Evaluation con classificazione successo/fallimento e motivazione.
    """
```

### Dimensione dei file

- Massimo **150-200 righe** per file.
- Se un file si avvicina al limite, scomporlo in moduli più piccoli.
- Ogni file deve avere un docstring che spiega brevemente il suo scopo.

## API REST

### Convenzioni endpoint

- Versioning nel path: `/api/v1/...`
- Documentare tutti gli endpoint con OpenAPI (generazione automatica FastAPI).
- Codici HTTP: `200` successo, `400` errore client, `500` errore server.
- Messaggi di errore utili per debug ma **senza informazioni sensibili**.

### Endpoint principali del Gateway

- `POST /api/v1/interact` — Invio messaggi (risposta asincrona con acknowledgment).
- `GET /api/v1/status` — Stato corrente dell'agente.
- `WS /api/v1/observe` — Stream WebSocket dei pensieri interni.

## Testing

- Copertura minima: **80%**.
- Framework: **pytest**.
- Tre livelli: **unitari**, **integrazione**, **end-to-end**.
- I test devono essere **idempotenti** e **isolati**.
- Codice senza test è considerato incompleto e non va mergiato.
- Un singolo comando deve eseguire tutti i test.

## Gestione Configurazione e Sicurezza

- Configurazione tramite **variabili d'ambiente**.
- File `.env` per sviluppo locale (escluso da Git).
- **Mai** includere password, chiavi API o credenziali nel codice o nel repository.
- I servizi Docker usano **utenti non-root**.
- Gli Executive Arms operano in **ambienti sandbox** isolati.
- Il Coder Service esegue codice in **container Docker temporanei**.

## Containerizzazione

- Ogni servizio ha il proprio **Dockerfile** con build multi-stage.
- `docker-compose.yml` alla radice per avviare l'intero sistema.
- Immagini leggere: eliminare file non necessari dal runtime.
- L'intero stack si avvia con `docker-compose up`.

## Pacchetto Condiviso `scarlet-common`

- Contiene modelli Pydantic, interfacce base, utility e costanti condivise.
- È l'**unico punto** dove modificare i formati dati inter-servizio.
- Usa **versionamento semantico**.
- Tutti i servizi lo importano come dipendenza.

## Convenzioni Git

### Commit

Formato **Conventional Commits**:

```
feat: aggiunta generazione obiettivi in Volition
fix: corretto timeout nella coda Redis del Cortex
docs: aggiornata documentazione API Gateway
refactor: semplificato loop principale del Cortex
test: aggiunti test unitari per Memory store
```

- Commit **atomici**: una singola modifica logica per commit.
- Code review obbligatoria prima del merge.

### CI/CD

- Ogni push attiva la pipeline CI (test, qualità codice, build Docker).
- Controlli di sicurezza sulle dipendenze (vulnerabilità note).
- Il merge è bloccato se la pipeline fallisce.

## Principi di Sviluppo

1. **Semplicità intenzionale** — Ogni componente fa una cosa sola e la fa bene. Non implementare funzionalità non strettamente necessarie (KISS).
2. **Separazione delle responsabilità** — Confini chiari tra moduli. Le dipendenze fluiscono dall'alto verso il basso.
3. **Trasparenza operativa** — Logging strutturato e consistente. Ogni operazione significativa deve essere tracciabile (chi, quando, perché, risultato).
4. **Autonomia proattiva** — L'agente genera obiettivi e agisce senza attendere comandi.
5. **Apprendimento continuo** — Ogni azione viene valutata; successi rafforzati, errori analizzati.
6. **Collaborazione intelligente** — L'utente è un partner, non un master.

## Gestione Errori tra Servizi

- Gestire errori localmente e propagare solo quelli non risolvibili.
- Timeout su tutte le chiamate sincrone.
- Circuit breaker per prevenire cascate di fallimenti.
- Retry automatico con **backoff esponenziale** per errori temporanei.

## File di Annotazioni di Sviluppo (`DEVNOTES.md`)

Il file `DEVNOTES.md` nella root del progetto è il notepad personale dell'agente. Va usato come segue:

- **All'inizio di ogni sessione**: leggere `DEVNOTES.md` per riprendere il contesto esatto (fase attiva, task in corso, blocchi aperti).
- **Durante lo sviluppo**: aggiornare lo stato dei task man mano che avanzano (`⬜ todo` → `🔄 in corso` → `✅ fatto`).
- **Al completamento di una task**: aggiornare la tabella, spostare decisioni rilevanti nella sezione "Decisioni Prese", rimuovere note ormai obsolete.
- **Quando si completa una fase**: pulire le sezioni della fase completata e preparare il piano della fase successiva.
- Il file può essere **modificato, sovrascritto o ripulito liberamente** — è un notepad, non documentazione permanente.
- Le informazioni di lungo termine (architettura, convenzioni) stanno nella documentazione ufficiale in `docs/`, non qui.

## Processo di Sviluppo Obbligatorio

### Regola di discussione pre-implementazione

**OBBLIGATORIO**: prima di iniziare qualsiasi fase o sotto-fase di implementazione, si deve:

1. **Riepilogo breve** — Riassumere in poche righe cosa è stato completato nell'ultima implementazione (risultati, stato corrente).
2. **Piano dettagliato** — Descrivere in dettaglio cosa si farà nella nuova implementazione:
   - Obiettivi specifici della fase.
   - Lista ordinata di task con ordine di esecuzione coerente.
   - Dipendenze tra i task.
   - Criteri di verifica/test per ogni task.
3. **Approvazione** — L'utente deve confermare il piano prima che l'implementazione inizi.

Questo processo si applica a **ogni transizione tra fasi e sotto-fasi**, senza eccezioni.

### Scomposizione delle macro-fasi in task

Le macro-fasi della roadmap devono essere scomposte in **task atomici** prima dell'esecuzione:

- Ogni macro-fase va suddivisa in sotto-task concreti, piccoli e indipendenti.
- I task devono avere un **ordine di esecuzione coerente** rispetto alle dipendenze.
- Ogni task deve avere un **test di valutazione** associato (criterio per considerarlo completato).
- I task devono essere presentati all'utente per discussione e approvazione prima di procedere.

## Fasi di Sviluppo (Roadmap)

Le fasi sono **sequenziali** — ogni fase dipende dalle precedenti:

1. **Fase 1** — Fondamenta: struttura microservizi, Cortex, identità/personalità, memoria base (PostgreSQL).
2. **Fase 2** — Autonomia: Volition Service, code di priorità Redis, compiti autonomi.
3. **Fase 3** — Apprendimento: Reflection module, database vettoriale, valutazione input.
4. **Fase 4** — Capacità avanzate: Executive Arms completi, comunicazione raffinata, dashboard di monitoraggio.

> Ogni macro-fase sarà scomposta in task dettagliati al momento della discussione pre-implementazione (vedi sezione "Processo di Sviluppo Obbligatorio").
