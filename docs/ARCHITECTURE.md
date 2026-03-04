# Architettura di Scarlet

## Panoramica Generale

L'architettura di Scarlet è progettata seguendo i principi dei microservizi, dove ogni funzionalità è implementata come servizio indipendente che comunica attraverso API REST. Questo approccio garantisce che il sistema possa scalare individualmente per ciascun componente, che il codice rimanga manutenibile grazie a dimensioni ridotte dei moduli, e che ogni parte possa essere sviluppata e testata in isolamento prima dell'integrazione.

Il sistema è organizzato in due livelli distinti: il Core, che contiene la logica essenziale per il funzionamento dell'agente, e i Componenti, che estendono le capacità base con funzionalità specializzate. Il Core è minimalista per natura, includendo solo ciò che è strettamente necessario per l'operatività dell'agente. Ogni capacità aggiuntiva viene relegata a componenti esterni che possono essere attivati, disattivati o sostituiti senza modificare il funzionamento base.

## Il Core: Fondamenta del Sistema

### Cortex: L'Orchestratore Centrale

Il Cortex rappresenta il cuore del sistema, il componente che governa tutte le decisioni ad alto livello. La sua funzione primaria non è eseguire operazioni complesse, ma coordinare il lavoro degli altri componenti e mantenere uno stato coerente dell'identità dell'agente. Questo pattern è analogo al ruolo di un direttore d'orchestra: non suona nessuno strumento, ma coordina ogni musicista per produrre un'esecuzione armoniosa.

Le responsabilità principali del Cortex si dividono in tre aree fondamentali. La prima è la gestione dello stato interno, che include variabili come l'umore corrente, il livello di attenzione, gli obiettivi attivi e la cronologia recente delle azioni. Questo stato deve essere persistente e accessibile a tutti i componenti che ne hanno necessità. La seconda responsabilità è la ricezione degli input esterni, che arrivano attraverso l'API Gateway e vengono analizzati per determinare priorità e urgenza. La terza è la decisione di interruzione: quando l'agente sta eseguendo un compito e arriva un messaggio dall'utente, spetta al Cortex decidere se fermarsi immediatamente, posticipare la risposta, o continuare l'esecuzione attuale.

L'implementazione del Cortex richiede un loop principale che controlla costantemente la coda delle priorità. Questo loop non deve essere bloccante, ma deve permettere l'esecuzione asincrona dei compiti. Un'architettura efficace prevede l'utilizzo di Redis per memorizzare la coda dei compiti con relativi punteggi di priorità, permettendo al Cortex di estrarre sempre il compito più importante.

### Sistema di Configurazione Base

Il Core include un sistema di configurazione che definisce le proprietà essenziali dell'agente. Le direttive primarie stabiliscono gli obiettivi fondamentali che l'agente deve perseguire, come migliorare le proprie capacità, aiutare l'utente, o mantenere l'infrastruttura operativa. La definizione della personalità stabilisce caratteristiche come il tono comunicativo, le preferenze comportamentali, e i valori fondamentali che guidano le decisioni. I parametri operativi configurano limiti come timeout massimi, dimensioni delle code, e soglie di priorità per i diversi tipi di attività.

## Componenti del Sistema

### Volition: Il Motore dell'Autonomia

Volition è il componente che conferisce a Scarlet la capacità di operare in modo proattivo. A differenza dei sistemi tradizionali che attendono istruzioni, Volition genera continuamente nuovi obiettivi e compiti basandosi sulle direttive primarie dell'agente. Questo componente implementa quello che potremmo definire il "desiderio di fare", la spinta intrinseca che porta l'agente ad agire anche in assenza di input esterni.

Il funzionamento di Volition si articola in tre fasi distinte ma interconnesse. La prima fase è la generazione degli obiettivi, dove il sistema analizza le direttive primarie e il contesto corrente per produrre obiettivi concreti e misurabili. La seconda fase è la scomposizione in compiti, dove ogni obiettivo viene spezzato in singole azioni eseguibili, ognuna con input e output definiti. La terza fase è la prioritizzazione, dove ogni compito riceve un punteggio basato su urgenza, importanza, e correlazione con gli obiettivi correnti.

### Memory: Sistema di Memorizzazione

Il sistema di memoria di Scarlet adotta un approccio stratificato che combina diverse tecnologie per ottimizzare sia le prestazioni che la capacità di recupero delle informazioni. La memoria a breve termine gestisce il contesto corrente, le variabili temporanee necessarie per l'esecuzione dei compiti attivi, e le informazioni immediatamente rilevanti per le decisioni immediate. La memoria a lungo termine utilizza un database vettoriale per memorizzare le esperienze passate in forma embedding, permettendo ricerche semantiche efficienti.

Il sistema supporta diversi backend di memorizzazione, selezionabili in base alle esigenze specifiche. L'implementazione di default utilizza PostgreSQL per i dati strutturati e Qdrant per le ricerche vettoriali. Alternative come ChromaDB o database locali SQLite possono essere configurate per scenari con requisiti differenti.

### Reflection: Modulo di Apprendimento

Il modulo di riflessione è ciò che trasforma i dati grezzi in apprendimento effettivo. Dopo ogni azione significativa, questo modulo analizza il risultato confrontandolo con l'obiettivo prefissato. Se l'obiettivo è stato raggiunto, il sistema registra quali strategie hanno funzionato per utilizzarle in futuro. Se l'obiettivo non è stato raggiunto, il sistema analizza le cause del fallimento e modifica il proprio comportamento di conseguenza.

Un aspetto cruciale della riflessione è la valutazione degli input dell'utente. Quando qualcuno invia un messaggio, il sistema deve determinare se quell'informazione è utile, inutile, o potenzialmente dannosa. Le informazioni utili vengono integrate nella conoscenza dell'agente, quelle inutili vengono ignorate, quelle dannose vengono memorizzate come casi da evitare. Questo processo di filtraggio evolve nel tempo, diventando sempre più preciso man mano che l'agente accumula esperienze.

### Executive Arms: Servizi Esecutivi

Gli Executive Arms sono i componenti che eseguono fisicamente le operazioni. A differenza del Cortex e di Volition, che pensano e pianificano, gli Executive Arms fanno. Questi servizi sono progettati per essere "stupidi" nel senso che non contengono logica di business complessa: ricevono un comando, lo eseguono, restituiscono il risultato.

Il Browser Service gestisce la navigazione web, l'estrazione di contenuti, e le interazioni con siti esterni. Questo servizio deve essere eseguito in un ambiente sandbox per ragioni di sicurezza, con timeout rigorosi per evitare situazioni di stallo. Il Coder Service gestisce la scrittura, l'esecuzione, e il debugging del codice. Anche questo deve operare in isolamento, preferibilmente in container Docker temporanei che vengono distrutti dopo l'uso. Il System Service gestisce le operazioni sul filesystem locale, l'accesso alle risorse del sistema, e l'interazione con API esterne.

### API Gateway: Punto di Ingresso

L'API Gateway rappresenta l'unico punto di contatto tra l'utente e il sistema. Questa centralizzazione semplifica la gestione della sicurezza, del logging, e delle policy di accesso. L'utente non comunica mai direttamente con i componenti interni, ma passa sempre attraverso questo strato di astrazione.

L'endpoint principale per l'interazione è `/api/v1/interact`, che accetta messaggi testuali e file come input. La risposta immediata è sempre un riconoscimento, non la risposta completa dell'agente. Questo design riflette la natura asincrona del sistema: l'utente invia il messaggio e continua con le proprie attività, mentre Scarlet processa il messaggio quando la sua coda lo permette. L'endpoint `/api/v1/status` permette all'utente di verificare cosa sta facendo l'agente in un dato momento, visualizzando i compiti in esecuzione, gli obiettivi attivi, e lo stato emotivo corrente. L'endpoint `/api/v1/observe` basato su WebSocket offre uno stream in tempo reale dei "pensieri" interni dell'agente, permettendo all'utente di seguire il processo decisionale in diretta.

## Comunicazione tra Componenti

### Protocollo di Comunicazione

Tutti i componenti comunicano attraverso API REST utilizzando JSON come formato di scambio dati. Ogni servizio espone le proprie API in formato standardizzato, utilizzando modelli Pydantic per la validazione dei dati in ingresso e in uscita. Questa uniformità garantisce che ogni componente possa interfacciarsi con qualsiasi altro senza necessità di adattamenti specifici.

Le chiamate sincrone vengono utilizzate per operazioni che richiedono una risposta immediata, come la creazione di un compito o la lettura di uno stato. Le chiamate asincrone attraverso code di messaggi vengono utilizzate per operazioni che possono essere processate in background, come l'esecuzione di compiti lunghi o l'aggiornamento di indici di ricerca.

### Gestione delle Priorità

La gestione delle priorità è cruciale per il funzionamento di Scarlet. Il sistema deve bilanciare molteplici tipi di attività: compiti generati internamente, messaggi dell'utente, operazioni di manutenzione, e risposte a emergenze. Ogni elemento nella coda ha un punteggio di priorità calcolato dinamicamente in base a criteri specifici.

I messaggi dell'utente vengono valutati in base all'urgenza esplicita, alla correlazione con gli obiettivi correnti, e al tono emotivo. Un messaggio che indica un'emergenza avrà priorità massima indipendentemente da qualsiasi altra attività. Un messaggio puramente sociale avrà priorità bassa e verrà processato quando non ci sono compiti più importanti. I compiti generati internamente hanno priorità basata sulla importanza strategica e sulla scadenza temporale. I compiti di manutenzione hanno priorità bassa e vengono eseguiti solo quando il sistema è inattivo.

## Flusso Operativo

### Scenario: Messaggio dell'Utente durante un Compito

Quando l'utente invia un messaggio mentre Scarlet sta eseguendo un compito, il sistema segue una sequenza precisa di operazioni. Prima il Gateway riceve il messaggio e lo inoltra al Cortex. Poi il Cortex analizza il contenuto del messaggio per determinare priorità e urgenza. Se il messaggio è critico, il Cortex interrompe immediatamente il compito corrente e assegna priorità massima al messaggio. Se il messaggio non è critico, viene inserito nella coda sociale con priorità bassa.

A questo punto il sistema invia una risposta immediata all'utente, riconoscendo la ricezione del messaggio e fornendo una stima di quando l'agente potrà dedicarsi alla risposta. Il compito corrente continua fino al completamento o fino a quando la priorità del messaggio non supera quella del compito. Infine, quando è il momento di processare il messaggio, Scarlet analizza il contenuto, estrae informazioni utili, formula una risposta appropriata, e aggiorna la memoria con le nuove conoscenze acquisite.

### Scenario: Operazione Autonoma

In assenza di input esterni, Scarlet opera in modo completamente autonomo. Il loop principale di Volition controlla continuamente la coda dei compiti, estraendo quello con priorità più alta e assegnandolo a un Executive Arm per l'esecuzione. Dopo l'esecuzione, il modulo di Reflection analizza il risultato, aggiorna la memoria con le informazioni apprese, e modifica eventualmente la strategia per i compiti futuri. Questo ciclo continua indefinitamente, permettendo a Scarlet di operare per lunghi periodi senza intervento umano.

## Scalabilità e Manutenzione

L'architettura a microservizi permette di scalare individualmente ogni componente in base alle necessità. Se il sistema riceve molti messaggi, solo il Gateway e il Cortex scalano per gestire il carico. Se l'agente genera molti compiti, Volition scala per tenere il passo. Se la memoria diventa troppo grande, i servizi di memorizzazione scale orizzontalmente con repliche di lettura.

La manutenzione è semplificata dalla separazione dei componenti. Ogni servizio può essere aggiornato in isolamento, senza richiedere interruzioni dell'intero sistema. Le nuove funzionalità possono essere aggiunte aggiungendo nuovi servizi senza modificare quelli esistenti. I bug possono essere isolati e risolti più facilmente perché ogni componente ha confini ben definiti.
