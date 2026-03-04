# Specifica dei Componenti

## Introduzione ai Componenti

I componenti di Scarlet rappresentano le unità funzionali che estendono le capacità del Core per fornire funzionalità avanzate. Ogni componente è un servizio indipendente che opera attraverso API REST, permettendo sviluppo, testing, e deployment separati. Questa sezione descrive in dettaglio ogni componente, le sue responsabilità, le interfacce che espone, e come si integra con gli altri componenti del sistema.

La separazione in componenti risponde a esigenze multiple: la manutenibilità del codice è migliorata perché ogni componente ha confini chiari e responsabilità limitate; la scalabilità permette di dimensionare individualmente ogni componente in base al carico; l'affidabilità garantisce che il fallimento di un componente non compromette l'intero sistema; e l'evolutività consente di aggiungere nuove funzionalità senza modificare il codice esistente.

## Componenti Core

### Cortex

Il Cortex costituisce il componente più critico del sistema, fungendo da orchestratore centrale che governa tutte le decisioni ad alto livello. La sua responsabilità principale non è l'esecuzione di operazioni complesse, ma il coordinamento del lavoro degli altri componenti e il mantenimento di uno stato coerente dell'identità dell'agente.

Le funzionalità principali del Cortex includono la gestione dello stato interno, che comprende l'umore corrente, il livello di attenzione, gli obiettivi attivi e la cronologia recente delle azioni. Questo stato deve essere persistente e accessibile a tutti i componenti che ne hanno necessità. Il Cortex gestisce anche la ricezione degli input esterni, analizzando i messaggi provenienti dall'API Gateway per determinare priorità e urgenza. Infine, implementa la logica di decisione di interruzione, determinando quando l'agente deve fermarsi per rispondere all'utente o quando può continuare le attività correnti.

L'interfaccia del Cortex espone endpoint per la lettura e scrittura dello stato, per la gestione dei compiti in coda, e per il controllo del ciclo di vita dell'agente. Le comunicazioni interne utilizzano Redis per la coda dei compiti e PostgreSQL per la persistenza dello stato a lungo termine.

## Componenti di Autonomia

### Volition

Volition è il motore dell'autonomia che genera continuamente obiettivi e compiti per l'agente. Questo componente implementa la capacità di operare in modo proattivo, senza attendere input esterni. Senza Volition, Scarlet sarebbe un semplice chatbot reattivo; con Volition, diventa un agente con iniziativa propria.

Le funzionalità principali si dividono in tre aree. La generazione obiettivi analizza le direttive primarie definite nella configurazione dell'agente e le traduce in obiettivi concreti e misurabili. Questo processo considera il contesto corrente, le esperienze passate, e le priorità strategiche per produrre obiettivi rilevanti. La scomposizione in compiti prende ogni obiettivo e lo spezza in singole azioni eseguibili, ognuna con input e output definiti. La prioritizzazione assegna punteggi a ogni compito basandosi su urgenza, importanza, e correlazione con gli obiettivi correnti.

Volition opera in un loop continuo che controlla la coda dei compiti, genera nuovi obiettivi quando necessario, e valuta i risultati delle azioni precedenti. L'interfaccia espone endpoint per la creazione e lettura degli obiettivi, per la gestione dei compiti, e per la configurazione delle direttive primarie.

## Componenti di Memoria

### Memory

Il sistema di memoria implementa la capacità di conservare e recuperare informazioni nel tempo. A differenza di un semplice database, questo componente supporta diversi tipi di memoria con caratteristiche differenti, ottimizzati per diversi casi d'uso.

La memoria a breve termine gestisce il contesto corrente, le variabili temporanee necessarie per l'esecuzione dei compiti attivi, e le informazioni immediatamente rilevanti per le decisioni immediate. È implementata utilizzando strutture dati in-memory con persistenza opzionale per sopravvivere ai riavvii.

La memoria a lungo termine utilizza un database vettoriale per memorizzare le esperienze passate in forma di embedding. Questo permette ricerche semantiche efficienti: cercando un concetto simile a "feedback negativo", il sistema può trovare tutte le occasioni in cui l'agente ha ricevuto critiche, anche se la terminologia esatta era diversa.

L'interfaccia espone endpoint per la scrittura e lettura di memorie, per la ricerca semantica, e per la gestione del ciclo di vita delle informazioni. Il sistema supporta la dimenticanza selettiva: informazioni obsolete o irrilevanti possono essere rimosse automaticamente per liberare spazio.

## Componenti di Apprendimento

### Reflection

Il modulo di riflessione implementa la capacità dell'agente di valutare le proprie azioni e imparare dai risultati. Questo è ciò che trasforma Scarlet da un esecutore meccanico a un sistema che migliora nel tempo.

Le funzionalità principali includono la valutazione delle azioni, che analizza i risultati delle operazioni confrontandoli con gli obiettivi prefissati. Ogni azione viene classificata come successo, fallimento, o risultato ambiguo, con motivazioni documentate. Il sistema di feedback identifica i pattern: se una strategia porta ripetutamente a fallimenti, viene modificata. Se porta a successi, viene rafforzata e applicata in situazioni simili.

Il modulo mantiene una cronologia delle valutazioni che permette di tracciare l'evoluzione del comportamento dell'agente nel tempo. L'interfaccia espone endpoint per la registrazione delle valutazioni, per la lettura delle cronologie, e per la query su pattern specifici.

## Componenti Esecutivi

### Executive Arms

Gli Executive Arms sono i servizi che eseguono fisicamente le operazioni richieste dall'agente. A differenza dei componenti di pensiero, questi servizi fanno: navigano sul web, eseguono codice, gestiscono file.

Il Browser Service gestisce la navigazione web e l'estrazione di contenuti. Opera in un ambiente sandbox isolato per ragioni di sicurezza, con timeout rigorosi per evitare situazioni di stallo. Supporta l'estrazione di testo, immagini, e altri media, nonché l'interazione con moduli web come form e bottoni.

Il Coder Service gestisce la scrittura, l'esecuzione, e il debugging del codice. Supporta linguaggi multipli e opera in container Docker temporanei che vengono distrutti dopo l'uso per garantire isolamento e sicurezza. Include funzionalità di linting e analisi statica per identificare problemi prima dell'esecuzione.

Il System Service gestisce le operazioni sul filesystem locale, l'accesso alle risorse del sistema, e l'interazione con API esterne. Opera con permessi limitati per minimizzare i rischi di sicurezza.

Ogni Executive Arm espone un'interfaccia standardizzata con endpoint per l'esecuzione di comandi, il controllo dello stato, e la gestione delle risorse. Tutte le operazioni sono tracciate per permettere il debugging e l'audit.

## Componenti di Interfaccia

### API Gateway

L'API Gateway rappresenta l'unico punto di contatto tra l'utente e il sistema. Gestisce l'autenticazione, la validazione delle richieste, il rate limiting, e l'inoltro ai componenti appropriati.

L'endpoint /api/v1/interact accetta messaggi testuali e file come input. Restituisce un acknowledgment immediato, non la risposta completa, riflettendo la natura asincrona del sistema. L'endpoint /api/v1/status fornisce informazioni sullo stato corrente dell'agente, inclusi compiti in esecuzione, obiettivi attivi, e metriche di performance. L'endpoint /api/v1/observe tramite WebSocket offre uno stream in tempo reale dei pensieri interni dell'agente.

Il Gateway implementa anche la gestione delle sessioni, tracciando le interazioni dell'utente e mantenendo il contesto conversazionale. Supporta multiple sessioni simultanee con isolamento tra utenti.

## Integrazione dei Componenti

### Flussi di Comunicazione

I componenti comunicano attraverso pattern specifici a seconda del tipo di interazione. Le richieste sincrone utilizzano chiamate HTTP dirette con timeout definiti, utilizzate quando una risposta immediata è necessaria. Le risposte asincrone utilizzano code di messaggi come Redis, utilizzate per operazioni che possono essere processate in background. Gli eventi utilizzano un sistema di pub/sub per notificare i componenti interessati quando accadono eventi significativi.

Il Cortex funge da orchestratore, inizializando le interazioni tra componenti. Quando arriva un messaggio dell'utente, il Gateway lo invia al Cortex, che determina come procedere. Se è necessario un compito, il Cortex lo assegna a Volition che lo genera. Reflection valuta il risultato, Memory lo memorizza, e gli Executive Arms lo eseguono.

### Gestione degli Errori

Ogni componente implementa la gestione degli errori a livello locale e propagate gli errori non risolvibili al componente chiamante. I timeout proteggono il sistema da operazioni che non completano mai. I circuit breaker prevengono cascate di fallimenti quando un componente diventa non disponibile.

Il sistema include meccanismi di retry automatico per errori temporanei, con backoff esponenziale per evitare sovraccarichi. Gli errori persistenti vengono registrati e segnalati per l'intervento manuale.
