# Percorso di studio progressivo

Piano personalizzato per esperienza professionale Azure, .NET, microservizi, AKS, Functions, App Service, Cosmos DB, Key Vault e Azure DevOps, oltre allo studio AZ-104. Questa esperienza è dichiarata dall’utente; non sono stati ancora verificati risultati o lacune personali.

Le ore sono **stime redazionali da calibrare**, comprensive di lettura, confronto e attività, non durate Microsoft né un impegno settimanale concordato. Non si importa la disponibilità del progetto Magistrale. Data d’esame indicata dall’utente: **1 dicembre 2026**; disponibilità settimanale da concordare.

## Ordine e dipendenze

Ogni fase usa la stessa sequenza: prerequisito mirato → fonti teoriche → caso progettuale → attività → richiamo. Il completamento richiede evidenze personali, non il solo tempo trascorso. Gli ID rimandano alla [matrice](MATRICE-COPERTURA.md); titoli e URL completi sono nella [biblioteca](BIBLIOTECA.md).

| Fase | Obiettivi | Prerequisiti e teoria | Casi / esercizi pianificati | Ripasso e criterio di uscita | Stima |
| --- | --- | --- | --- | --- | --- |
| S00 — Diagnosi mirata | Prerequisiti trasversali | `LP-PREREQ`: scegliere solo le sezioni necessarie; rilevare dimestichezza con reti, identità, storage e disponibilità | Colloquio diagnostico originale da svolgere nella prima sessione; nessun risultato presunto | Elenco delle lacune dimostrate e delle parti comprimibili | 1–2 h |
| S01 — Requisiti, WAF, CAF, governance | 1.3.1–1.3.2, base 4.3.1 | Cinque pilastri WAF; CAF; `M-design-governance`; `GOV-HIERARCHY`, `GOV-TAGS`, `GOV-POLICY`, `CAF-LZ` | `LAB-01`, diagramma `FIG-HUB-1`; pianificare gerarchia e confini di responsabilità | Motivare struttura, scope, policy e tagging; distinguere governance della piattaforma e qualità del workload | 4–6 h |
| S02 — Identità, autorizzazione e osservabilità | 1.1.*, 1.2.*, 1.3.3 | Moduli identità/monitoraggio di `LP-IDENTITY`; integrare `ID-ONPREM`, `ID-DOMAIN`, DCR, PIM/access reviews | `LAB-07`, parte osservabilità di `LAB-08`; confronto di due soluzioni di accesso e di routing log | Spiegare autenticazione/autorizzazione, identità di workload, accesso on-premises e confini dei dati di telemetria | 6–8 h |
| S03 — Rete ibrida e delivery | 4.4.* | `M-design-network-solutions`; `NET-HYBRID`, `NET-EXPRESSROUTE`, `NET-OUTBOUND`, `NET-PRIVATE`, `NET-DNS`, `NET-LB-CHOICE` | `LAB-09`, `ARC-HUB`; seguire un flusso DNS/ingress/egress sul diagramma | Motivare VPN/ExpressRoute, Private Link, sicurezza e L4/L7 regionale/globale; considerare guasti e latenza | 7–10 h |
| S04 — Compute per requisiti | 4.1.* | `M-design-compute-solution`; confronti `COMP-CHOICE`, `COMP-CONTAINERS`, piani Functions, VMSS e Batch | `LAB-02`, `ARC-AKS` / `ARC-WEB`; confrontare una scelta familiare con un’alternativa gestita | Giustificare VM/container/serverless/batch considerando rete, scaling e operatività | 5–7 h |
| S05 — Dati relazionali | 2.1.* | `M-design-data-storage-solution-for-relational-data`, `DATA-SQL-CHOICE`, tier vCore/DTU/serverless, elastic pool/Hyperscale, sicurezza | `LAB-04`; confronto SQL Database/MI/VM e alternativa PostgreSQL/MySQL ove pertinente | Legare compatibilità, tier, scaling e protezione ai requisiti; motivare anche l’alternativa scartata | 6–9 h |
| S06 — Dati non relazionali e storage | 2.2.* | Modulo non relazionale e unità Cosmos/Table del modulo relazionale; `DATA-STORE-CHOICE`, tier Blob, Files, ridondanza/protezione | `LAB-03`, `CASE-AWARE`; ipotizzare access pattern e confrontare costo/prestazioni senza assumere prezzi fissi | Distinguere dati semi/non strutturati, consistenza, ridondanza, durabilità e backup | 4–6 h |
| S07 — Integrazione e analisi | 2.3.* | `M-design-data-integration`, runtime ADF, Lake, Synapse, Databricks, Stream Analytics e confronto analitico | `ARC-DATA`, `FIG-DATA-1/2`; progettare una pipeline originale durante lo studio; `LAB-05` è un placeholder | Motivare batch/streaming, orchestrazione/trasformazione e hot/warm/cold path | 4–6 h |
| S08 — Architettura applicativa | 4.2.* | `M-design-application-architecture`; confronto messaging/eventi, APIM, Managed Redis/cache-aside, App Configuration, deployment | `LAB-06`; revisione di una decisione microservizi e confronto CI/CD/GitOps | Motivare semantica, integrazione API, cache, configurazione e rilascio; verificare timeline Redis | 5–7 h |
| S09 — Affidabilità e recupero | 3.1.*, 3.2.* | `LP-BCDR`, WAF Reliability; metriche, matrici backup e guide HA specifiche di compute/database/storage | `ARC-DR`, `FIG-DR-1/2`; piano originale di test ripristino/failover da sviluppare; `LAB-10` è un placeholder | Collegare RTO/RPO e SLO ai flussi completi; distinguere backup, HA e DR; prevedere un test misurabile | 7–10 h |
| S10 — Migrazioni | 4.3.* | `M-design-migrations`, CAF, discovery/dipendenze, assessment e matrici aggiornate DMS/storage | Attività originale futura: ondate, scelta IaaS/PaaS, migrazione dati, cutover e rollback; `LAB-11` è un placeholder | Motivare strumenti e ordine delle dipendenze; verificare tooling supportato e validazione post-migrazione | 4–6 h |
| S11 — Sintesi e ripasso | Tutti i 49 obiettivi | `LAB-08` come caso trasversale; matrice e registro errori; riaprire le fonti cambiate | Confronto finale di architetture e Practice Assessment ufficiale raggiungibile dalla Study Guide | Nessun obiettivo senza fonti fresche; spiegare scelte e variazioni dei requisiti; correggere gli errori ricorrenti prima di fissare l’esame | 4–6 h |

Totale orientativo **57–83 ore**, da rivedere dopo S00 e le prime due sessioni effettive. I prerequisiti già dimostrati riducono il tempo di ripasso; non eliminano obiettivi dal programma. Le aree probabilmente da approfondire, ancora da confermare, sono dati relazionali/analytics, identità ibrida/governance, reti, BCDR e migrazioni.

## Ripasso distribuito

Alla chiusura di ciascun blocco registrare la decisione e gli errori, senza preparare oggi lezioni o flashcard. Nelle sessioni successive richiamare una decisione precedente e modificarne un requisito. Dopo alcuni blocchi svolgere un caso che attraversi più domini. Prima dell’esame ricontrollare programma, fonti, ritiri e requisiti della certificazione.

Le soglie della nostra verifica didattica non sono il punteggio dell’esame. Un Practice Assessment ripetuto a memoria non dimostra padronanza. Non si raccolgono domande riservate né si copiano set di risposte.

## Prima sessione pronta da avviare

S00: partire da una descrizione dell’esperienza e da decisioni recenti su rete, identità, dati e affidabilità. Registrare ciò che emerge senza attribuire automaticamente livelli. Poi proporre il primo blocco di S01 con `WAF-HOME`, `CAF-LZ` e le sezioni pertinenti di `GOV-HIERARCHY`; attendere la lettura autonoma prima del resoconto.
