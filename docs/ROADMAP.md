# Roadmap di Implementazione

## Introduzione alla Roadmap

Questa roadmap delinea le fasi di sviluppo previste per il sistema Scarlet, dalla creazione delle fondamenta fino al rilascio di funzionalità avanzate. Ogni fase ha obiettivi chiari e deliverable misurabili che permettono di valutare i progressi e identificare eventuali problemi tempestivamente.

Le tempistiche indicate sono stime basate su un team di sviluppo di dimensioni contenute e supponendo che lo sviluppo possa procedere a tempo pieno. Le circostanze reali potrebbero richiedere aggiustamenti, ma le dipendenze tra le fasi rimangono valide indipendentemente dalla durata effettiva.

## Fase 1: Fondamenta del Sistema

### Descrizione della Fase

La prima fase concentra tutte le energie sulla costruzione delle fondamenta del sistema. L'obiettivo principale è ottenere un sistema base funzionante che possa essere espanso nelle fasi successive. In questa fase vengono implementati la struttura dei microservizi, il Cortex come orchestratore centrale, la definizione dell'identità e della personalità, e una memoria di base funzionante.

Questa fase è critica perché stabilisce le convenzioni di codice, gli standard di comunicazione, e l'architettura di base che verrà utilizzata in tutte le fasi successive. Un errore in questa fase potrebbe propagarsi e causare problemi significativi nelle fasi successive, rendendo fondamentale un'attenta pianificazione e esecuzione.

### Obiettivi Specifici

Il primo obiettivo è la creazione della struttura dei microservizi con FastAPI. Questo include la definizione della struttura delle directory, la configurazione di Docker Compose per l'ambiente di sviluppo, l'implementazione del sistema di logging centralizzato, e la creazione del pacchetto comune scarlet-common contenente modelli e interfacce condivise.

Il secondo obiettivo è l'implementazione del Cortex come orchestratore centrale. Il Cortex deve gestire lo stato interno dell'agente, coordinare le comunicazioni tra i componenti, e implementare il loop principale di gestione delle priorità. Inizialmente il Cortex sarà relativamente semplice, gestendo solo i casi base senza tutta la logica avanzata che verrà aggiunta nelle fasi successive.

Il terzo obiettivo è la definizione dell'identità e della personalità attraverso un System Prompt sofisticato. Questo include la creazione del profilo psicologico dell'agente, la definizione del tono comunicativo, l'impostazione dei valori fondamentali, e la configurazione delle risposte predefinite per situazioni comuni.

Il quarto obiettivo è l'implementazione della memoria di base su PostgreSQL. Questo include la definizione dello schema del database, l'implementazione delle operazioni CRUD di base, la gestione delle sessioni, e l'integrazione con il Cortex per il recupero delle informazioni.

### Deliverable di Fase

Il deliverable principale di questa fase è un chatbot che ricorda le conversazioni passate e mantiene una personalità consistente. L'agente non è ancora proattivo, ma risponde in modo intelligente e ricorda le informazioni condivise dall'utente nelle interazioni precedenti. Questo rappresenta il punto di partenza minimo viable prima di aggiungere funzionalità più avanzate.

### Criteri di Completamento

La fase è completata quando il sistema può mantenere una conversazione coerente per almeno 30 minuti senza perdere il contesto, quando le risposte mantengono una personalità consistente definita nel System Prompt, quando le informazioni importanti vengono memorizzate e recuperate correttamente, e quando il sistema può essere avviato con un singolo comando docker-compose up.

### Durata Stimata

La durata stimata per questa fase è di due settimane, assumendo uno sviluppo a tempo pieno. La prima settimana dovrebbe concentrarsi sulla struttura tecnica e l'infrastruttura, mentre la seconda settimana dovrebbe dedicarsi all'implementazione del Cortex e della memoria base.

## Fase 2: Motore dell'Autonomia

### Descrizione della Fase

La seconda fase introduce l'autonomia vera e propria nel sistema. Il Volition Service viene implementato per generare obiettivi e compiti in modo autonomo. Il sistema di code di priorità viene rafforzato per gestire sia le attività interne che i messaggi dell'utente. L'agente inizia a fare qualcosa anche quando l'utente non interagisce, perseguendo obiettivi definiti nelle sue direttive primarie.

Questa fase trasforma Scarlet da un semplice chatbot reattivo a un agente proattivo capace di iniziativa propria. È una transizione fondamentale che cambia la natura del sistema da passiva ad attiva, da rispondente a generante.

### Obiettivi Specifici

Il primo obiettivo è l'implementazione del Volition Service. Questo include lo sviluppo del motore di generazione obiettivi che analizza le direttive primarie e produce obiettivi concreti, l'implementazione del sistema di scomposizione che traduce gli obiettivi in compiti eseguibili, e la creazione del sistema di prioritizzazione che assegna punteggi a ogni compito.

Il secondo obiettivo è il rafforzamento del sistema di code. Questo include l'integrazione con Redis per la gestione delle code di priorità, l'implementazione della logica di prelazione che permette ai compiti urgenti di interrompere quelli meno importanti, e la creazione del sistema di notifica che informa l'utente quando compiti specifici vengono completati.

Il terzo obiettivo è l'implementazione dei compiti autonomi base. L'agente deve essere in grado di eseguire operazioni semplici senza input esterno, come analizzare dati precedenti, cercare informazioni su argomenti rilevanti, o eseguire operazioni di manutenzione. Questi compiti iniziali dimostrano la capacità del sistema di operare in modo indipendente.

### Deliverable di Fase

Il deliverable di questa fase è un agente che lavora in modo indipendente. Se l'utente non invia messaggi per un'ora, l'agente dovrebbe comunque aver completato alcuni compiti produttivi. L'utente può osservare questa attività attraverso l'endpoint di stato, che mostra i compiti in esecuzione, gli obiettivi attivi, e il progresso verso il loro completamento.

### Criteri di Completamento

La fase è completata quando l'agente genera almeno tre obiettivi autonomi durante un'ora di inattività dell'utente, quando il sistema di priorità gestisce correttamente sia i compiti interni che i messaggi dell'utente, quando la risposta a messaggi urgenti ha priorità su qualsiasi compito in corso, e quando l'utente può osservare l'attività autonoma attraverso l'endpoint di stato.

### Durata Stimata

La durata stimata per questa fase è di due settimane. La prima settimana si concentra sull'implementazione di Volition, mentre la seconda settimana rafforza le code di priorità e implementa i compiti autonomi base.

## Fase 3: Sistema di Apprendimento

### Descrizione della Fase

La terza fase porta l'apprendimento nel sistema. Il modulo di riflessione viene implementato per valutare i risultati delle azioni e modificare il comportamento di conseguenza. Il database vettoriale viene integrato per memorizzare le esperienze in forma semanticamente ricercabile. L'agente inizia a filtrare gli input basandosi sulla loro utilità, imparando a distinguere informazioni preziose da rumore.

Questa fase è cruciale perché trasforma l'agente da un sistema che esegue compiti in un sistema che migliora attraverso l'esperienza. Ogni azione diventa un'opportunità di apprendimento, e il comportamento dell'agente evolve nel tempo diventando sempre più efficace.

### Obiettivi Specifici

Il primo obiettivo è l'implementazione del modulo di riflessione. Questo include lo sviluppo del sistema di valutazione che analizza i risultati delle azioni confrontandoli con gli obiettivi prefissati, l'implementazione del sistema di feedback che identifica i successi e gli insuccessi, e la creazione del meccanismo di adattamento che modifica il comportamento futuro basandosi sui risultati passati.

Il secondo obiettivo è l'integrazione del database vettoriale. Questo include la configurazione di Qdrant o ChromaDB come backend di memoria a lungo termine, l'implementazione del sistema di embedding che converte le esperienze in vettori, e lo sviluppo del sistema di recupero che utilizza la ricerca semantica per trovare informazioni rilevanti.

Il terzo obiettivo è il sistema di valutazione degli input. Questo include l'implementazione del classificatore che determina se un messaggio dell'utente è utile, inutile o dannoso, lo sviluppo del sistema di integrazione che aggiorna la conoscenza con le informazioni utili, e la creazione del filtro che ignora o segnala gli input dannosi.

### Deliverable di Fase

Il deliverable di questa fase è un agente che migliora nel tempo. L'agente non ripete gli stessi errori, riconosce i pattern che hanno funzionato in passato, e adatta le strategie in base ai risultati ottenuti. L'utente noterà che l'agente diventa sempre più efficace nelle sue attività e più preciso nel filtrare gli input irrilevanti.

### Criteri di Completamento

La fase è completata quando l'agente non ripete errori identici più di due volte consecutive, quando le ricerche semantiche restituiscono risultati pertinenti almeno l'80% delle volte, quando il sistema di valutazione degli input raggiunge una precisione accettabile dopo l'apprendimento iniziale, e quando il comportamento dell'agente evolve visibilmente dopo diverse iterazioni.

### Durata Stimata

La durata stimata per questa fase è di due settimane. La prima settimana si concentra sull'implementazione del modulo di riflessione, mentre la seconda settimana integra il database vettoriale e il sistema di valutazione degli input.

## Fase 4: Capacità Avanzate

### Descrizione della Fase

La quarta fase espande le capacità operative dell'agente. Gli Executive Arms vengono arricchiti con funzionalità avanzate come l'accesso a internet, l'esecuzione di codice complesso, e l'interazione con API esterne. La collaborazione asincrona viene raffinata per gestire conversazioni più naturali. Una dashboard di monitoraggio permette all'utente di visualizzare i pensieri interni dell'agente in tempo reale.

Questa fase rappresenta il completamento del sistema base, trasformando Scarlet in un assistente completo che può operare in modo quasi completamente autonomo gestendo una vasta gamma di attività.

### Obiettivi Specifici

Il primo obiettivo è l'arricchimento degli Executive Arms. Questo include lo sviluppo del Browser Service con capacità di navigazione avanzata, l'implementazione del Coder Service con supporto per linguaggi multipli e ambienti di esecuzione sicuri, e la creazione del System Service per interazioni col filesystem e le risorse di sistema.

Il secondo obiettivo è il raffinamento della comunicazione. Questo include il miglioramento del sistema di risposta asincrona per conversazioni più naturali, l'implementazione della memoria contestuale multi-sessione, e lo sviluppo delle capacità di gestione delle interruzioni.

Il terzo obiettivo è la dashboard di monitoraggio. Questo include l'implementazione dell'endpoint WebSocket per lo stream dei pensieri in tempo reale, la creazione dell'interfaccia web per la visualizzazione dello stato dell'agente, e lo sviluppo degli strumenti di debug per gli sviluppatori.

### Deliverable di Fase

Il deliverable di questa fase è un assistente completo che opera in modo quasi completamente autonomo, gestendo una vasta gamma di attività e mantenendo una collaborazione naturale e produttiva con l'utente. La dashboard di monitoraggio permette all'utente di osservare i processi interni dell'agente in tempo reale.

### Criteri di Completamento

La fase è completata quando tutti gli Executive Arms base sono funzionanti, quando l'agente può gestire conversazioni naturali con interruzioni e riprese, quando la dashboard mostra lo stato interno dell'agente in tempo reale, e quando il sistema nel complesso è utilizzabile per attività produttive reali.

### Durata Stimata

La durata stimata per questa fase è di quattro settimane, dato che include l'implementazione di funzionalità multiple e complesse. Le prime due settimane si concentrano sugli Executive Arms, la terza settimana sulla comunicazione avanzata, e l'ultima settimana sulla dashboard.

## Fasi Future

Dopo il completamento delle quattro fasi iniziali, il sistema sarà in uno stato funzionale completo. Le fasi future potrebbero includere l'espansione delle capacità linguistiche, l'integrazione con altri sistemi e piattaforme, l'ottimizzazione delle performance, e l'aggiunta di nuove funzionalità basate sui feedback degli utenti.

## Dipendenze tra Fasi

Le fasi sono sequenziali per una buona ragione: ogni fase dipende dalle precedenti. La Fase 1 fornisce l'infrastruttura utilizzata in tutte le fasi successive. La Fase 2 aggiunge capacità che la Fase 3 deve valutare e da cui deve apprendere. La Fase 3 crea i meccanismi di miglioramento che la Fase 4 utilizza per ottimizzare le capacità avanzate.

Saltare una fase non è raccomandato perché comprometterebbe la stabilità e la funzionalità del sistema. Ogni fase costruisce sulle fondamenta delle precedenti, e tentare di implementare funzionalità avanzate prima di quelle base porterebbe a un sistema fragile e difficile da mantenere.
