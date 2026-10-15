# Continuità operativa

Peso ufficiale: 15–20%. Obiettivi: 3.1.1–3.1.4, 3.2.1–3.2.3. Vedere [matrice](../../docs/MATRICE-COPERTURA.md).

## Stato — 15 ottobre 2026

Non iniziato. Nessun test di restore/failover eseguito e nessun livello di preparazione personale attribuito.

## Fonti e collocazione

S09 segue compute, rete e dati. Fonti: `LP-BCDR`, WAF Reliability, `BCDR-OBJECTIVES`, matrici backup e guide specifiche `BCDR-*`, `HA-*`, `DATA-REDUNDANCY`; caso architetturale `ARC-DR` e relativi diagrammi.

`LAB-10` non contiene un caso formale. Durante lo studio si definirà un’attività originale con criteri di ripristino e misure verificabili; oggi non è stata generata o svolta.

## Ripresa

Seguire il [piano Learn](../../docs/PIANO-DIDATTICO.md): ordine del syllabus, poi moduli e unità nell’ordine originale. Diagnosi S00 saltata; partenza da LP-PREREQ, primo modulo, unità 1–5, come nel [registro corrente](../sessioni/2026-10-15-LP-PREREQ-M01.md). Questo dominio verrà affrontato nel percorso `LP-BCDR`. Le collocazioni S01–S11 sopra sono riferimenti tematici della pianificazione precedente, non l’ordine attivo. Nessun blocco specifico del dominio attualmente assegnato; nessun risultato personale registrato.

| Blocco | Proposto | Letto dall’utente | Discusso | Esercitato | Comprensione verificata |
| --- | --- | --- | --- | --- | --- |
| Nessuno | — | — | — | — | — |

## Punti da verificare con i casi

Differenza tra HA, backup e DR; obiettivi applicativi rispetto alle garanzie dei singoli servizi; dipendenze ibride; modalità di test e validazione. Le cifre RTO/RPO/SLA andranno verificate per servizio, tier, regione e scenario.
