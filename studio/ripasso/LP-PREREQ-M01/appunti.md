# Fondamenti Azure: collocazione, gestione e recupero

Sessione del 19 ottobre 2026. Percorso LP-PREREQ, primo modulo, unità 1–5. Appunti originali del blocco letto e discusso; assessment e riepilogo Learn ancora da svolgere. Fonti consultate il 19 ottobre 2026, senza nuova approvazione delle revisioni del catalogo.

## Il collegamento tra i concetti

Per ragionare su un’applicazione Azure servono due descrizioni complementari: la distribuzione fisica dei componenti e la loro organizzazione gestionale. La prima permette di interrogarsi sui guasti; la seconda su responsabilità e regole. Durante la sessione abbiamo applicato entrambe a un caso con sviluppo e produzione. Una scelta nella gerarchia non dimostra, da sola, come il servizio reagirà a un’interruzione.

Le unità introduttive presentano Azure come piattaforma di servizi per eseguire e modernizzare applicazioni. Non bisogna dedurre la qualità di un progetto dal solo utilizzo del cloud: nel nostro esercizio era necessario esplicitare che cosa sarebbe rimasto disponibile dopo il guasto. [Unità: What is Microsoft Azure](https://learn.microsoft.com/en-us/training/modules/describe-core-architectural-components-of-azure/2-what-microsoft-azure).

## Account e subscription

La subscription consente di creare e utilizzare risorse Azure; possono esistere più subscription associate allo stesso account. L’unità sugli account introduce anche offerte commerciali: qui non ne fissiamo importi o condizioni. La lettura non ha comportato attivazioni, acquisti o creazione di risorse. [Unità: Get started with Azure accounts](https://learn.microsoft.com/en-us/training/modules/describe-core-architectural-components-of-azure/3-get-started-azure-accounts).

Il collegamento didattico da conservare è questo: avere accesso ad Azure e progettare la separazione fra ambienti sono questioni differenti. La risposta alla seconda deve partire dai requisiti del caso, non dall’offerta con cui è stato aperto l’account.

## Regione, datacenter e availability zone

Una regione Azure comprende datacenter in un’area geografica. All’interno di una regione che le supporta, le availability zone separano infrastrutture con alimentazione, raffreddamento e rete indipendenti. Non tutti i servizi e tutte le configurazioni offrono le stesse possibilità zonali. Nella scelta fisica occorre verificare il supporto dei componenti utilizzati. [Unità: infrastruttura fisica](https://learn.microsoft.com/en-us/training/modules/describe-core-architectural-components-of-azure/5-describe-azure-physical-infrastructure).

Distribuire componenti tra zone affronta una classe di guasti all’interno della regione. Il requisito di resistere alla perdita della regione è diverso. La verifica della sessione ha cambiato proprio questo requisito, chiedendo che cosa dovesse essere riconsiderato. Non abbiamo selezionato SKU, regioni concrete o SLA. [Panoramica delle availability zone](https://learn.microsoft.com/en-us/azure/reliability/availability-zones-overview).

## Pairing e recupero dell’applicazione

Il pairing associa alcune regioni ed è utilizzato da determinate funzionalità dei servizi. Non crea automaticamente una copia operativa di un’applicazione e non costituisce una garanzia generale di failover. Esistono anche regioni senza pairing. La documentazione specifica precisa la formulazione introduttiva di Learn. [Region pair e regioni non associate](https://learn.microsoft.com/en-us/azure/reliability/regions-paired).

Nel richiamo originale l’utente ha spiegato correttamente che, se il database è replicato ma l’applicazione rimane soltanto nella regione indisponibile, il servizio può restare offline. Questa è evidenza della distinzione tra protezione di un componente e disponibilità dell’insieme; non dimostra ancora la capacità di progettare o collaudare un piano DR completo. Non sono stati verificati tempi di ripristino, perdita dati, modalità di instradamento o procedure operative.

## Gerarchia gestionale e scope

La sequenza studiata è management group, subscription, resource group, risorsa. I management group aggregano subscription per la governance; le subscription introducono confini di gestione e fatturazione; i gruppi raccolgono risorse correlate. Gli scope superiori permettono di applicare impostazioni a quelli sottostanti. [Unità: infrastruttura di gestione](https://learn.microsoft.com/en-us/training/modules/describe-core-architectural-components-of-azure/6-describe-azure-management-infrastructure).

La scelta dello scope cambia l’estensione dell’intervento. Per i permessi RBAC bisogna concedere l’accesso necessario all’ambito necessario: nel caso B, una subscription di sviluppo interamente amministrata dagli sviluppatori può essere lo scope pertinente. Non ne segue che questi debbano amministrare anche produzione. Ruoli specifici e privilegi minimi non sono stati verificati nella sessione. [Scope Azure RBAC](https://learn.microsoft.com/en-us/azure/role-based-access-control/scope-overview).

## Resource group: ciclo di vita e location

Microsoft raccomanda di organizzare un resource group intorno a risorse con ciclo di vita condiviso. La sua location riguarda metadati; le risorse contenute possono essere in regioni diverse. Non è una configurazione di replica. Un’altra precisazione discussa: i tag applicati al gruppo non vengono ereditati automaticamente dalle risorse. [Azure Resource Manager: resource group](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/overview#what-is-a-resource-group).

## Il confronto A/B affrontato nella sessione

Questo è un esercizio originale, non una domanda Microsoft né un’architettura approvata. A prevedeva una subscription con gruppi sviluppo/produzione; B due subscription sotto un management group. Requisiti: accessi degli sviluppatori limitati a sviluppo, regole comuni e disponibilità di produzione durante un guasto di zona.

L’utente ha scelto B per l’ereditarietà delle regole. Abbiamo chiarito che anche A permette una policy comune alla subscription, applicabile ai due gruppi. Il successivo richiamo «alla subscription» è corretto. Rimane da argomentare un requisito che renda preferibile B e una rinuncia operativa rispetto ad A: non attribuiamo all’utente una motivazione che non ha ancora espresso. [ARM: scope](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/overview#understand-scope).

## Esito e ripresa

Confermati nel richiamo: scope comune della policy in A e insufficienza della sola replica del database per la disponibilità applicativa. Da riprendere: motivazione discriminante e compromessi di A/B. Non verificati per intero gli obiettivi AZ-305 1.3.1 e 3.2.1, né il modulo o il percorso. Prossima attività: Module assessment e Summary del primo modulo, senza presumere che siano già completati. Nessuna scadenza di ripasso concordata.
