# Linee Guida di Sviluppo

## Principi Fondamentali

Lo sviluppo di Scarlet segue principi mirati a creare un sistema mantenibile, scalabile e di alta qualità. Queste linee guida stabiliscono gli standard che ogni contributo al progetto deve rispettare, garantendo consistenza attraverso tutto il codebase e facilitando la collaborazione tra sviluppatori.

Il primo principio è la semplicità intenzionale. Ogni componente deve fare una cosa sola e farla bene. Se una funzione o un modulo diventa troppo complesso, deve essere spezzato in parti più piccole. Non bisogna mai implementare funzionalità che non sono strettamente necessarie per il funzionamento del sistema. Questo principio, derivato dalla filosofia KISS, aiuta a mantenere il codebase gestibile nel tempo.

Il secondo principio è la separazione delle responsabilità. Ogni servizio, ogni modulo, ogni funzione deve avere confini chiari di responsabilità. Le dipendenze tra componenti devono fluire in una direzione sola, dal alto livello verso il basso livello. Questo rende il sistema più facile da capire, testare e modificare.

Il terzo principio è la trasparenza operativa. Ogni operazione significativa deve essere tracciabile: chi l'ha fatta, quando, perché, e quale è stato il risultato. Il logging deve essere consistente e strutturato, permettendo di ricostruire il flusso completo delle operazioni anche dopo molto tempo.

## Struttura del Codice

### Organizzazione dei File

Ogni servizio deve risiedere in una directory dedicata con una struttura interna standardizzata. La struttura base prevede una directory per il codice sorgente, una per i test, una per la configurazione, e una per la documentazione interna. Questa uniformità permette a qualsiasi sviluppatore di orientarsi rapidamente in qualsiasi parte del progetto.

I file di codice non devono superare le 150-200 righe. Questa regola, seppur apparentemente restrittiva, forza la decomposizione funzionale e mantiene ogni componente focalizzato su una singola responsabilità. Quando un file si avvicina a questo limite, è un segnale che deve essere spezzato in moduli più piccoli. Le eccezioni sono rare e devono essere giustificate con commenti.

La convenzione per i nomi dei file segue lo snake_case per Python, con nomi descrittivi che indicano chiaramente il contenuto. I nomi come `goal_generator.py`, `memory_store.py` sono preferiti a nomi generici come `utils.py` o `helpers.py`. Ogni file deve avere un docstring che spiega brevemente il suo scopo.

### Organizzazione delle Directory

La struttura delle directory deve riflettere l'architettura del sistema. Al livello superiore troviamo le directory dei singoli servizi: cortex, volition, memory, reflection, executive_arms, gateway. Ogni servizio contiene le proprie sottodirectory: src per il codice, tests per le prove, config per le configurazioni, docs per la documentazione interna.

La directory root contiene anche file di configurazione globali come docker-compose.yml, pyproject.toml per le dipendenze Python, e README.md per la documentazione principale. Il pacchetto comune scarlet-common risiede in una directory separata perché viene utilizzato da tutti i servizi.

## Standard di Codifica

### Python

Il codice Python segue le convenzioni definite in PEP 8, con alcune personalizzazioni per adattarsi alle esigenze specifiche del progetto. L'indentazione utilizza quattro spazi, non tab. Le righe non devono superare i 100 caratteri, permettendo una visualizzazione agevole anche su schermi di dimensioni ridotte.

Le type annotations sono obbligatorie per tutte le funzioni e i metodi. Questo permette agli editor di fornire autocomplete accurato e aiuta a prevenire errori di tipo. Le annotazioni devono essere utilizzate anche per i parametri di ritorno quando non sono ovvi dal corpo della funzione.

Le docstring seguono il formato Google o NumPy, con descrizioni che spiegano cosa fa la funzione, quali parametri accetta, e cosa restituisce. Esempi di utilizzo sono apprezzati per funzioni complesse o con comportamenti non ovvi.

### API REST

Tutti gli endpoint API devono essere documentati con OpenAPI. FastAPI genera automaticamente questa documentazione, ma commenti aggiuntivi nei docstring aiutano gli sviluppatori a capire il comportamento atteso. Ogni endpoint deve avere descrizioni chiare dei parametri, dei possibili codici di errore, e esempi di richiesta e risposta.

Gli errori devono essere gestiti in modo consistente. Ogni endpoint deve restituire codici HTTP appropriati: 200 per successo, 400 per errori del client, 500 per errori del server. I messaggi di errore devono essere utili per il debug ma non devono esporre informazioni sensibili.

La versione delle API deve essere inclusa nel path dell'endpoint: /api/v1/. Questo permette di evolvere l'API mantenendo la compatibilità con le versioni precedenti.

## Testing

### Strategia di Testing

Ogni servizio deve avere una suite di test completa che copra almeno l'80% del codice. I test non sono opzionali: il codice senza test è considerato incompleto e non verrà mergiato nel branch principale.

I test sono organizzati in tre categorie: test unitari per le funzioni singole, test di integrazione per le API e le interazioni tra componenti, e test end-to-end per i flussi completi. I test unitari devono essere veloci e indipendenti, eseguibili in isolamento senza necessità di servizi esterni. I test di integrazione possono richiedere servizi come database o Redis, ma devono essere configurati automaticamente prima dell'esecuzione.

### Esecuzione dei Test

I test devono poter essere eseguiti con un singolo comando. Idealmente pytest viene configurato per scoprire automaticamente tutti i test nel progetto. La configurazione di CI/CD esegue i test automaticamente prima di permettere il merge di qualsiasi branch.

I test devono essere idempotenti: eseguirli più volte deve dare sempre lo stesso risultato. Devono anche essere isolati: un test non deve dipendere dallo stato lasciato da un altro test. Se i test modificano dati persistenti, devono pulire dopo di sé.

## Comunicazione tra Servizi

### Principi di Comunicazione

La comunicazione tra servizi avviene esclusivamente attraverso API REST definite con OpenAPI. Non sono ammesse chiamate dirette a database di altri servizi o accesso a file system condivisi. Questa separazione rigida garantisce che ogni servizio possa essere sostituito, aggiornato, o scalato in modo indipendente senza impattare gli altri.

Le chiamate sincrone vengono utilizzate per operazioni che richiedono una risposta immediata, con un timeout ragionevole per evitare attese indefinite. Le chiamate asincrone attraverso code di messaggi vengono utilizzate per operazioni che possono essere processate in background, permettendo al sistema di rimanere responsivo.

### Formato dei Dati

Tutti i dati scambiati tra servizi utilizzano JSON standardizzato. I modelli Pydantic definiscono la struttura di questi dati e vengono condivisi attraverso il pacchetto scarlet-common. Questo garantisce che ogni servizio parli la stessa lingua dati e permette la validazione automatica delle richieste e delle risposte.

I modelli includono versionamento per gestire l'evoluzione delle strutture dati. Quando un modello cambia, viene creata una nuova versione e quella vecchia viene mantenuta per retrocompatibilità per un periodo transitorio.

## Pacchetto Comune

### Struttura di scarlet-common

Il pacchetto comune contiene le definizioni condivise tra tutti i servizi. Include i modelli Pydantic per la validazione dei dati, le interfacce di base che ogni servizio deve implementare, le utility comuni, e le costanti condivise come codici di errore e stati.

Questo pacchetto è l'unico punto dove le modifiche devono essere fatte quando il formato dei dati cambia. Quando un modello viene aggiornato in scarlet-common, tutti i servizi che lo utilizzano devono essere aggiornati di conseguenza. Questo garantisce consistenza in tutto il sistema.

### Utilizzo

Ogni servizio importa scarlet-common come dipendenza. Questo significa che quando il pacchetto viene aggiornato, ogni servizio può essere aggiornato per utilizzare le nuove versioni. Il versionamento semantico del pacchetto indica quando gli aggiornamenti sono compatibili all'indietro.

## Containerizzazione

### Docker

Tutti i servizi devono essere containerizzati utilizzando Docker. Ogni servizio ha un proprio Dockerfile che definisce come costruire l'immagine. Le immagini devono essere leggere e sicure, utilizzando utenti non-root e eliminando file non necessari.

Le immagini vengono costruite in stages multipli per separare le dipendenze di build da quelle di runtime. Questo riduce la dimensione delle immagini finali e minimizza la superficie di attacco.

### Docker Compose

Il file docker-compose.yml alla radice del progetto permette di avviare l'intero sistema con un singolo comando. Definisce non solo i servizi applicativi, ma anche le infrastrutture di supporto come Redis, PostgreSQL, e il database vettoriale. Ogni servizio può essere avviato indipendentemente per il debugging, ma l'ambiente completo è disponibile con un comando.

La configurazione dell'ambiente avviene attraverso variabili d'ambiente. I file .env definiscono i valori di default per lo sviluppo locale, mentre in produzione questi valori vengono sovrascritti dalla configurazione dell'ambiente di deployment.

## Gestione della Configurazione

### Configurazione per Ambiente

La configurazione varia tra ambienti diversi: sviluppo, testing, produzione. Ogni ambiente ha un proprio set di variabili d'ambiente che definiscono parametri come URL dei database, credenziali, e livelli di logging.

I valori sensibili come password e chiavi API non sono mai inclusi nel codice o nel repository. Vengono gestiti attraverso secrets esterni che vengono iniettati nei container in fase di deployment.

### Override Locali

Gli sviluppatori possono avere file di configurazione locali che vengono caricati dopo quelli standard. Questi file permettono di personalizzare il comportamento per il debugging senza modificare i file condivisi. I file locali sono esclusi dal controllo versione attraverso .gitignore.

## Documentazione

### Documentazione del Codice

Ogni funzione pubblica deve avere un docstring che spiega il suo scopo, i parametri, e i valori di ritorno. I commenti nel codice spiegano il perché delle scelte implementative, non il cosa: il cosa è evidente dal codice stesso.

Le classi e i moduli complessi hanno documentazione aggiuntiva che spiega come utilizzarli. Esempi di utilizzo sono particolarmente utili per API non banali.

### Documentazione di Servizio

Ogni servizio ha un proprio file README che spiega il suo scopo, le dipendenze, e come configurarlo. Questa documentazione è importante per nuovi sviluppatori che devono capire rapidamente come funziona ogni componente.

La documentazione delle API viene generata automaticamente da FastAPI. Gli sviluppatori devono assicurarsi che la documentazione sia accurata e rifletta il comportamento effettivo degli endpoint.

## Continuous Integration

### Pipeline CI

Ogni push al repository attiva automaticamente la pipeline CI. La pipeline esegue i test, verifica la qualità del codice, e costruisce le immagini Docker. Solo se tutti questi passaggi hanno successo il codice può essere mergiato nel branch principale.

La pipeline include anche controlli di sicurezza che analizzano le dipendenze per vulnerabilità note. Se vengono trovate vulnerabilità critiche, il merge viene bloccato fino a quando non vengono risolte.

### Review del Codice

Tutti i commit devono passare attraverso code review prima di essere mergiati. Almeno un altro sviluppatore deve approvare le modifiche. La review non è solo controllo qualità ma anche opportunità di condividere conoscenza sul codebase.

## Convenzioni di Commit

I commit seguono il formato Conventional Commits. Il messaggio inizia con un tipo: feat per nuove funzionalità, fix per correzioni di bug, docs per documentazione, refactor per ristrutturazione del codice, test per i test. Segue una descrizione breve del cambiamento.

I commit atomici sono preferiti: ogni commit deve contenere una singola modifica logica. Commit che toccano molte parti del codebase sono più difficili da revieware e da ripristinare se necessario.
