# Metodo delle sessioni

Metodo adattato da [Magistrale Dashboard](https://github.com/DanieleDiFratta/-Magistrale-Dashboard), consultato il 15 ottobre 2026. Riferimenti esaminati: `AGENTS.md` (SHA `558af0966dc359987c5005aeb028c524ac9f1b95`), `studio/PIANO-GENERALE.md` (SHA `c89de0753f2271c0c49efe01bd2a41a09b528410`), README e guida dei materiali. Sono ripresi i principi di lavoro, senza importare progressi, scadenze o dati accademici.

## Un blocco, un obiettivo coerente

La sessione parte dalla scheda del dominio e dal punto di ripresa. L’assistente apre le fonti pertinenti e propone un blocco con ID degli obiettivi, URL, sezioni, prerequisiti e durata orientativa. Un’unità Learn può essere affiancata da una pagina di confronto o da un diagramma: il criterio è la decisione da comprendere, non un numero fisso di pagine.

L’utente legge autonomamente. L’assistente risponde ai dubbi e attende che l’utente sia pronto prima della spiegazione integrata. La spiegazione approfondirà motivazioni, condizioni, limiti ed esempi, conservando i riferimenti e distinguendo gli esempi originali da quelli Microsoft. L’implementazione della dashboard non avvia automaticamente lo studio e non genera tali lezioni.

Una breve verifica chiude il blocco: spiegare una scelta, scartare un’alternativa plausibile e indicare quale requisito potrebbe cambiare la decisione. Se emerge una difficoltà si restringe il blocco successivo. I concetti già acquisiti non vengono ripetuti per riorganizzare il percorso.

## Stati distinti e memoria condivisa

| Stato | Evidenza richiesta |
| --- | --- |
| Proposto | Fonti e sezioni definite |
| Letto | Dichiarazione dell’utente |
| Discusso | Resoconto e dubbi affrontati nella sessione |
| Esercitato | Attività realmente svolta, con esito e limiti |
| Verificato | Ragionamento o soluzione valutati, con eventuali errori residui |
| Da ripassare | Motivo e prossimo richiamo registrati |

La raccolta dell’assistente non avanza questi stati. Le etichette “Completed” presenti nell’HTML Learn non sono evidenza del progresso dell’utente. Le schede in `studio/aree/` conservano fonti, dubbi e punto di ripresa; il piano generale coordina le dipendenze tra domini.

## Come esercitare il giudizio architetturale

Ogni caso produrrà, durante lo studio, una decisione breve: requisiti funzionali e non funzionali, vincoli, alternative, compromessi, scelta motivata e metodo di verifica. Il modello è in [DECISIONE.md](../templates/DECISIONE.md). L’esperienza su AKS, Functions, App Service e Cosmos DB sarà usata come base per confrontare alternative, evitando di scegliere sempre il servizio più familiare.

Le attività potranno essere analisi su carta, lettura di diagrammi, review di configurazioni o piccoli laboratori. Prima di un laboratorio Azure saranno definiti risorse necessarie, costo stimato aggiornato e pulizia finale. Nessun deployment è previsto da questa ricerca.

## Chiusura e ripresa

Registrare fonti/sezioni effettivamente trattate, stati separati, errori e prossima azione precisa. Alla fine delle sessioni sviluppare appunti approfonditi, mappe e flashcard per il blocco effettivamente trattato, senza riprodurre gli articoli Microsoft; ampliarli nel tempo con riferimenti, precisazioni e domande.

Aggiornare insieme riepilogo della sessione, scheda del dominio, piano generale e `studio/progressi.json`. Pubblicare i materiali nel manifesto `studio/materiali.json` secondo [DASHBOARD.md](DASHBOARD.md). Il sito mostra lo stato registrato nei file, senza scritture dal browser. Le sessioni di studio non sono ancora iniziate: la raccolta di ripasso è vuota.
