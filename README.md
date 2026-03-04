# Scarlet - Sistema AI Autonomo Avanzato

## Panoramica del Progetto

Scarlet rappresenta un'evoluzione significativa nel campo degli assistenti AI autonomi. A differenza dei sistemi tradizionali come OpenClaw che operano in modalità reattiva attendendo istruzioni, Scarlet è progettata per funzionare come partner attivo, generando autonomamente obiettivi e compiti, valutando i risultati delle proprie azioni, e apprendendo continuamente dalle esperienze accumulate.

L'architettura del sistema si basa su un approccio modulare dove ogni componente è un servizio indipendente che comunica attraverso API REST utilizzando FastAPI. Questa scelta progettuale garantisce scalabilità, manutenibilità e la possibilità di sviluppare ciascun modulo in modo autonomo senza compromettere l'integrità del sistema complessivo.

## Filosofia di Progettazione

La filosofia fondamentale di Scarlet ruota attorno a tre principi cardine che guidano ogni decisione architetturale. Il primo principio è l'autonomia proattiva: l'agente non attende passivamente comandi ma genera continuamente nuovi obiettivi, analizza l'ambiente circostante, e prende iniziative utili. Il secondo principio è l'apprendimento continuo: ogni azione viene valutata, i successi vengono rafforzati, e gli errori vengono analizzati per evitare ripetizioni future. Il terzo principio è la collaborazione intelligente: l'utente non è un master che impartisce ordini, ma un partner con cui Scarlet interagisce in modo bidirezionale, valorizzando i contributi utili e filtrando quelli dannosi.

Questi principi si traducono in un sistema radicalmente diverso dagli assistenti convenzionali. Quando l'utente invia un messaggio, Scarlet non si limita a rispondere: analizza il contenuto, valuta la rilevanza rispetto ai propri obiettivi, integra le informazioni utili nella propria conoscenza, e prosegue con le proprie attività adattandole eventualmente in base ai nuovi input ricevuti.

## Caratteristiche Distintive

Scarlet si distingue per numerose caratteristiche che la separano dai sistemi AI convenzionali. La prima è l'identità persistente: a differenza degli assistenti che dimenticano tutto alla fine di ogni conversazione, Scarlet mantiene una personalità definita e coerente nel tempo, con stati emotivi, preferenze e obiettivi che evolvono attraverso le interazioni. La seconda è il goal generation system: un motore interno che genera autonomamente obiettivi e compiti basandosi sulle direttive primarie e sul contesto corrente, permettendo all'agente di operare anche in assenza di input esterni.

La terza caratteristica è il critic module: un sistema di valutazione che analizza ogni azione intrapresa, determina se gli obiettivi sono stati raggiunti, e modifica il comportamento di conseguenza. La quarta è la comunicazione asincrona: l'utente invia messaggi attraverso endpoint API e riceve risposte in modo non bloccante, permettendo all'agente di continuare le proprie attività mentre gestisce le interazioni in base alle priorità. La quinta è l'architettura modulare: ogni funzionalità è isolata in servizi indipendenti che comunicano attraverso interfacce standardizzate, facilitando lo sviluppo, il testing e la scalabilità.

## Architettura del Sistema

L'architettura di Scarlet è organizzata attorno a sei componenti principali che collaborano attraverso API REST e code di messaggi asincrone. Il Cortex funge da orchestratore centrale, gestendo lo stato interno dell'agente, принимая decisioni ad alto livello, e coordinando le attività degli altri componenti. Volition è il motore dell'autonomia, responsabile della generazione di obiettivi e della scomposizione in compiti eseguibili.

Il sistema di Memory gestisce la memorizzazione delle informazioni a breve e lungo termine, utilizzando database vettoriali per le ricerche semantiche. Il modulo di Reflection implementa le capacità di apprendimento, valutando le azioni e adattando il comportamento. Gli Executive Arms sono i servizi che eseguono fisicamente le operazioni, come la navigazione web, l'esecuzione di codice, e le interazioni con il sistema operativo. Infine, l'API Gateway fornisce l'interfaccia unificata per la comunicazione con l'esterno.

## Stato del Progetto

Il progetto è attualmente in fase di pianificazione iniziale. La documentazione architetturale è in fase di definizione e il primo sviluppo è pianificato per le prossime settimane. Consulta la roadmap per maggiori dettagli sulle tempistiche di implementazione.

## Tech Stack

Il sistema è sviluppato utilizzando Python 3.10+ come linguaggio principale, con FastAPI per i servizi web e la comunicazione asincrona. Redis gestisce le code di messaggi e lo stato condiviso, PostgreSQL memorizza i dati strutturati, e Qdrant o ChromaDB forniscono le capacità di memoria vettoriale. LangChain o LlamaIndex vengono utilizzati per l'orchestrazione dei modelli linguistici.

## Links

- Repository: https://github.com/Skunky94/ScarletAuto
- Documentazione: https://github.com/Skunky94/ScarletAuto/tree/main/docs
- Roadmap: https://github.com/Skunky94/ScarletAuto/blob/main/docs/ROADMAP.md
