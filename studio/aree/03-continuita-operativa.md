# Continuità operativa

Peso ufficiale: 15–20%. Obiettivi: 3.1.1–3.1.4, 3.2.1–3.2.3. Vedere [matrice](../../docs/MATRICE-COPERTURA.md).

## Stato — 19 ottobre 2026

Percorso specifico LP-BCDR non iniziato. Nei prerequisiti l’utente ha dichiarato lette le unità 1–5 del primo modulo il 19 ottobre 2026, inclusa l’introduzione all’infrastruttura fisica Azure, contesto per 3.2.1. Nel richiamo finale l’utente ha spiegato correttamente che la replica del database non risolve l’indisponibilità dell’applicazione rimasta nella regione persa. Piano DR completo non verificato. Nessun test di restore/failover eseguito e nessun livello di preparazione personale attribuito.

## Fonti e collocazione

S09 segue compute, rete e dati. Fonti: `LP-BCDR`, WAF Reliability, `BCDR-OBJECTIVES`, matrici backup e guide specifiche `BCDR-*`, `HA-*`, `DATA-REDUNDANCY`; caso architetturale `ARC-DR` e relativi diagrammi.

`LAB-10` non contiene un caso formale. Durante lo studio si definirà un’attività originale con criteri di ripristino e misure verificabili; oggi non è stata generata o svolta.

## Ripresa

Seguire il [piano Learn](../../docs/PIANO-DIDATTICO.md). Diagnosi S00 saltata; unità 1–5 del primo modulo LP-PREREQ dichiarate lette, come nel [registro corrente](../sessioni/2026-10-19-LP-PREREQ-M01.md). Dopo «chiaro» dell’utente è stata fornita la spiegazione integrata; prima risposta al caso originale ricevuta e valutata; richiamo finale corretto sullo scope della policy in A e sulla dipendenza applicativa. Sessione chiusa su richiesta; motivazione A/B da approfondire nel modulo governance. Assessment e riepilogo del modulo ancora da svolgere. Questo dominio verrà affrontato nel percorso `LP-BCDR`. Le collocazioni S01–S11 sopra sono riferimenti della pianificazione precedente. Nessun obiettivo del dominio completato o verificato.

| Blocco | Proposto | Letto dall’utente | Discusso | Esercitato | Comprensione verificata |
| --- | --- | --- | --- | --- | --- |
| LP-PREREQ, modulo 1, unità 1–5: fondamenti per 3.2.1 | 2026-10-15 | 2026-10-19 | 2026-10-19 | 2026-10-19, caso originale | Due punti circoscritti confermati; obiettivo completo non verificato |

## Punti da verificare con i casi

Differenza tra HA, backup e DR; obiettivi applicativi rispetto alle garanzie dei singoli servizi; dipendenze ibride; modalità di test e validazione. Le cifre RTO/RPO/SLA andranno verificate per servizio, tier, regione e scenario.
