# Piano generale AZ-305

## Stato corrente — 15 ottobre 2026

Biblioteca verificabile, copertura del programma e percorso didattico predisposti nella prima fase. Dashboard statica implementata su richiesta dell’utente: panoramica, blocchi, biblioteca e raccolta di ripasso. Gli esiti della ricerca sono in [audit-summary.json](../data/audit-summary.json); il [rapporto](../docs/RAPPORTO-RICERCA.md) ne esplicita i limiti. Nessuna lezione completa, mappa, flashcard o nota definitiva prodotta. **Nessuna sessione di studio svolta e nessun obiettivo personale completato.**

Profilo dichiarato: esperienza professionale con Azure, .NET, microservizi, AKS, Functions, App Service, Cosmos DB, Key Vault e Azure DevOps; studio AZ-104. Possesso della certificazione AZ-104/Azure Administrator Associate non dichiarato. Esame indicato dall’utente: **1 dicembre 2026**. Tempo settimanale e lingua d’esame ancora non concordati.

## Decisioni confermate

- Usare il repository esistente `DanieleDiFratta/AZ-305-Study-Hub`, come chiarito dall’utente in questa sessione.
- Implementazione autorizzata dopo la pianificazione: sito statico semplice, senza database, su GitHub Pages pubblico. Progressi ed elaborati inclusi sono pubblici; nessun login, backend o sincronizzazione da introdurre.
- Privilegiare le fonti Microsoft, mantenere la tracciabilità e non usare exam dumps.
- Adattare il metodo da [Magistrale Dashboard](https://github.com/DanieleDiFratta/-Magistrale-Dashboard): blocchi coerenti, lettura autonoma, dubbi, resoconto e verifica; stati distinti e memoria su file.
- Baseline ufficiale corrente: obiettivi dal 17 aprile 2026, verificati il 15 ottobre 2026. Le etichette locali rimandano ai bullet della guida.
- Preparazione centrata sulle decisioni architetturali e sulle lacune dimostrate; nessun corso introduttivo obbligatorio se i prerequisiti vengono verificati.
- A fine sessione sviluppare appunti approfonditi, mappe e flashcard, salvare il punto di ripresa e aggiornare gli stati distinti in [progressi.json](progressi.json). I materiali pubblicati sono elencati in [materiali.json](materiali.json). Istruzioni in [DASHBOARD.md](../docs/DASHBOARD.md).

## Schede dei domini

| Dominio | Scheda | Stato personale |
| --- | --- | --- |
| Identità, governance e monitoraggio | [01-identita-governance-monitoraggio.md](aree/01-identita-governance-monitoraggio.md) | Non iniziato |
| Dati e storage | [02-dati-storage.md](aree/02-dati-storage.md) | Non iniziato |
| Continuità operativa | [03-continuita-operativa.md](aree/03-continuita-operativa.md) | Non iniziato |
| Infrastruttura | [04-infrastruttura.md](aree/04-infrastruttura.md) | Non iniziato |

## Punto di ripresa preciso

Avviare **S00 — diagnosi mirata** del [piano didattico](../docs/PIANO-DIDATTICO.md). Non è già stata proposta una lettura all’utente. Prima azione: scegliere il tempo della sessione e rilevare dimestichezza con decisioni su identità, reti, dati e BCDR. Registrare soltanto le evidenze effettive.

Segue S01: requisiti/WAF/CAF e governance, usando `WAF-HOME`, `CAF-LZ`, `GOV-HIERARCHY` e il modulo governance. L’assistente aprirà le fonti aggiornate, definirà un blocco preciso e attenderà la lettura autonoma. Nessun salto automatico alle lezioni in questa fase.

## Manutenzione e dubbi aperti

- Primo controllo periodico: 14 novembre 2026 per programma e lifecycle; altre date per risorsa nel catalogo.
- Lacune didattiche note: unità dedicata sull’accesso on-premises assente; tre placeholder dei casi. Fonti di compensazione e attività future nel [registro](../docs/LACUNE-E-AGGIORNAMENTI.md).
- La lingua italiana delle risorse non è stata verificata; baseline tecnica inglese. Confermare la preferenza quando utile alla prima sessione.
- Nessuna capacità personale marcata come acquisita, nessun errore personale ancora osservato.

## Avvio di una nuova chat

> Questa chat riguarda AZ-305. Leggi AGENTS.md, studio/PIANO-GENERALE.md, docs/METODO.md e la scheda del dominio pertinente. Riprendi dal punto registrato, usando le fonti verificate e distinguendo lettura, discussione, esercizi e comprensione. La dashboard statica è implementata; lo studio non è ancora iniziato. A fine sessione salva riepilogo, appunti/mappe/flashcard del blocco trattato, stati distinti e punto di ripresa anche nei dati della dashboard. Segui docs/DASHBOARD.md; commit e push soltanto quando autorizzati.
