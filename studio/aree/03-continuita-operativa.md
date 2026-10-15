# Continuità operativa

Peso ufficiale: 15–20%. Obiettivi: 3.1.1–3.1.4, 3.2.1–3.2.3. Vedere [matrice](../../docs/MATRICE-COPERTURA.md).

## Stato — 15 ottobre 2026

Non iniziato. Nessun test di restore/failover eseguito e nessun livello di preparazione personale attribuito.

## Fonti e collocazione

S09 segue compute, rete e dati. Fonti: `LP-BCDR`, WAF Reliability, `BCDR-OBJECTIVES`, matrici backup e guide specifiche `BCDR-*`, `HA-*`, `DATA-REDUNDANCY`; caso architetturale `ARC-DR` e relativi diagrammi.

`LAB-10` non contiene un caso formale. Durante lo studio si definirà un’attività originale con criteri di ripristino e misure verificabili; oggi non è stata generata o svolta.

## Ripresa

Attendere la diagnosi e le fasi precedenti. Prima lettura futura da definire sulle sezioni di metriche e obiettivi del workload. Nessun blocco già proposto.

| Blocco | Proposto | Letto dall’utente | Discusso | Esercitato | Comprensione verificata |
| --- | --- | --- | --- | --- | --- |
| Nessuno | — | — | — | — | — |

## Punti da verificare con i casi

Differenza tra HA, backup e DR; obiettivi applicativi rispetto alle garanzie dei singoli servizi; dipendenze ibride; modalità di test e validazione. Le cifre RTO/RPO/SLA andranno verificate per servizio, tier, regione e scenario.
