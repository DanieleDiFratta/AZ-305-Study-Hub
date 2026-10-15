# Lacune, riferimenti storici e approfondimenti

Stato al **15 ottobre 2026**. La matrice ha fonti primarie verificate per tutti i 49 obiettivi; nessuna competenza è lasciata senza documentazione. Le lacune sotto riguardano il percorso Learn, gli esercizi, la precisione dei materiali o le verifiche personali ancora da svolgere.

## Lacune della raccolta didattica

| ID | Evidenza | Impatto | Azione prevista |
| --- | --- | --- | --- |
| G01 | Nessuna unità dedicata a 1.2.4 nei sei percorsi censiti | L’accesso alle risorse on-premises non va dedotto dalla sola familiarità con RBAC Azure | Studiare `ID-ONPREM`, `ID-DOMAIN` e `ID-AUTH`; verificare tipo di applicazione, protocolli e confini del dominio durante S02 |
| G02 | `LAB-05` dichiara “No formal case study” | Non esiste un esercizio formale di integrazione dati in quella voce | Usare `ARC-DATA` e progettare un’attività originale in S07; oggi solo pianificata |
| G03 | `LAB-10` dichiara “No formal case study” | Nessun caso BCDR in quella voce | Durante S09 sviluppare test di restore/failover usando guide specifiche, senza spacciare `LAB-10` per esercizio |
| G04 | `LAB-11` dichiara “No formal case study” | Nessun caso migrazione in quella voce | In S10 preparare un caso originale con dipendenze, cutover e rollback |
| G05 | `LAB-12` è un caso AI opzionale | Non corrisponde a un bullet AI autonomo nella baseline corrente | Conservarlo come opzionale, senza usarlo per gonfiare la copertura |
| G06 | Un solo customer story reale selezionato (`CASE-AWARE`, pubblicato nel 2023) | Illustra una scelta, non tutte le decisioni operative né i servizi attuali | In S06 distinguere risultati dichiarati, dati mancanti e inferenze; le architetture Microsoft restano i casi tecnici principali |
| G07 | Italiano non verificato; video, quiz e deployment non eseguiti | Accessibilità della pagina non equivale a completamento delle attività o localizzazione | Verificare lingua preferita e accessi quando si avviano le sessioni; mantenere l’inglese come baseline tecnica |

## Materiali da leggere con le fonti correnti

| Argomento | Osservazione verificata | Fonti e trattamento |
| --- | --- | --- |
| Identità clienti | L’unità B2C conserva il titolo storico ma contiene anche un avviso per i nuovi progetti. L’unità introduttiva alle identità esterne usa una formulazione che può far confondere B2C ed External ID | Confrontare `U-design-authentication-authorization-solutions-05` e `U-describe-azure-identity-access-security-04` con [ID-EXTERNAL](https://learn.microsoft.com/en-us/entra/external-id/external-identities-overview) e [LIFE-B2C](https://learn.microsoft.com/en-us/azure/active-directory-b2c/faq). B2C non è acquistabile da nuovi clienti dal 1 maggio 2025; la FAQ indica supporto almeno fino a maggio 2030. Non presentare l’intera unità come inutilizzabile |
| Cache Redis | L’unità cache tratta Managed Redis e cita il ritiro del servizio precedente; le timeline vanno distinte per tier. Un annuncio vecchio conserva un blocco per clienti esistenti che è stato successivamente rimosso | [LIFE-REDIS](https://learn.microsoft.com/en-us/azure/azure-cache-for-redis/retirement-faq), [LIFE-REDIS-NEWS](https://learn.microsoft.com/en-us/azure/azure-cache-for-redis/cache-whats-new), `APP-REDIS`. La sezione luglio 2026 rimuove il blocco previsto per ottobre 2026 per clienti esistenti; Basic/Standard/Premium hanno ritiro il 30 settembre 2028. Consultare la FAQ per le timeline Enterprise, senza applicare una data unica a tutte le SKU |
| Outbound delle reti | L’unità Learn riassume il cambiamento come effetto del 31 marzo 2026; la documentazione precisa l’ambito delle nuove API e delle nuove reti | [NET-OUTBOUND](https://learn.microsoft.com/en-us/azure/virtual-network/ip-services/default-outbound-access). Il default privato riguarda nuove VNet create con API successive alla data indicata; non è uno spegnimento generale dell’outbound delle VNet esistenti. Verificare configurazione della subnet e metodo di uscita |
| Strumenti SQL | Documentazione/esercizi storici possono riferirsi ad Azure Data Studio | [LIFE-ADS](https://learn.microsoft.com/en-us/sql/tools/whats-happening-azure-data-studio), `MIG-DATABASE`. Azure Data Studio è ritirato dal 28 febbraio 2026; scegliere il tooling attuale secondo sorgente, destinazione e scenario. Non estendere questo ritiro all’intera piattaforma DMS |
| Load Balancer | La tabella SKU mantiene Basic per confronto storico | [LIFE-LB](https://learn.microsoft.com/en-us/azure/load-balancer/skus). Basic è ritirato dal 30 settembre 2025; leggere la tabella con questa condizione |
| Agenti di monitoraggio | Le guide mantengono istruzioni di transizione dal Log Analytics agent | [LIFE-MONITOR](https://learn.microsoft.com/en-us/azure/azure-monitor/agents/azure-monitor-agent-migration). Agente ritirato dal 31 agosto 2024; la guida avverte che dal 2 marzo 2026 l’upload può interrompersi senza ulteriore preavviso. Per nuovi progetti studiare AMA/DCR e verificare le eccezioni documentate |

Queste osservazioni si riferiscono a sezioni precise e non autorizzano a dichiarare obsoleta tutta una pagina in base all’età. I metadati `source_updated_at` non provano che ogni paragrafo sia stato aggiornato.

## URL, duplicati e perimetro

- Il vecchio URL `ARC-DR` per “multi-region” rimandava alla baseline zone-redundant: un redirect riuscito non bastava a coprire il caso multiregione. È stato sostituito con una guida multiregione effettiva.
- Il vecchio `choose-api` di Cosmos DB rimandava alla homepage della documentazione: sostituito con la pagina introduttiva effettiva e affiancato dai confronti dei modelli dati.
- Sei candidati iniziali restituivano 404; sostituiti con pagine Microsoft trovate e verificate. Un customer story NewDay indicizzato dal motore di ricerca restituiva 404 al GET: escluso dalle fonti attive.
- SQL, PostgreSQL, Cosmos DB, monitoraggio e CAF hanno altri redirect di riorganizzazione. URL richiesto e finale sono entrambi conservati. Il [registro degli URL](VERIFICHE-URL.md) riporta gli esiti.
- Il modulo introduttivo WAF compare in due percorsi: un unico record di modulo e unità, due appartenenze. Non è una doppia attività da svolgere.
- Nessun duplicato di URL finale normalizzato nel catalogo corrente. Questa verifica non promette assenza di sovrapposizioni concettuali fra documenti differenti.

## Approfondimenti da sviluppare durante lo studio

| Priorità | Tema | Perché richiede lavoro ulteriore | Fonti già disponibili |
| --- | --- | --- | --- |
| Alta | Identità ibrida e accesso on-premises | Separare autenticazione, pubblicazione applicativa e autorizzazione della risorsa | `ID-AUTH`, `ID-ONPREM`, `ID-DOMAIN`, PIM/access reviews |
| Alta | SQL e piattaforme relazionali | Compatibilità, tier, scaling e HA dipendono da scelte collegate | `DATA-SQL-*`, `HA-SQL*`, guide PostgreSQL/MySQL |
| Alta | BCDR completo | RTO/RPO del servizio non sono automaticamente quelli del flusso applicativo | `BCDR-OBJECTIVES`, `BCDR-*`, `HA-*`, `ARC-DR` |
| Alta | Reti e DNS privato | Connettività funzionante e isolamento richiedono coerenza tra routing, DNS e servizio | `NET-HYBRID`, `NET-DNS`, `NET-PRIVATE`, `NET-EXPRESSROUTE` |
| Alta | Migrazioni | Tooling, dipendenze, capacità e rollback vanno valutati sul caso | `MIG-*`, `LIFE-ADS` |
| Media | Analytics e integrazione | Non limitarsi al nome del prodotto: differenziare orchestrazione, trasformazione e store analitico | `DATA-ADF*`, `DATA-ANALYTICS-CHOICE`, `DATA-DATABRICKS`, `DATA-SYNAPSE`, `DATA-STREAM` |
| Media | Alternative ai servizi più familiari | L’esperienza non prova ancora il confronto con opzioni meno gestite o più gestite | `COMP-CHOICE`, `COMP-CONTAINERS`, `APP-MESSAGING`, `NET-LB-CHOICE` |

Queste sono priorità didattiche proposte, non diagnosi delle capacità personali. Specifiche regionali, prezzi e SLA andranno verificati sui requisiti di ogni caso: non sono congelati in questa raccolta. Non rimangono obiettivi senza fonti; rimangono attività di apprendimento da svolgere.
