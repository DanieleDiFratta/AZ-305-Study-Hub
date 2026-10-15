# Rapporto della prima fase

Data: **15 ottobre 2026**. Ambito autorizzato: ricerca, catalogazione, copertura del programma e piano didattico. Nome concordato: `AZ-305-Study-Hub`, usando il repository già configurato. Nessuna dashboard o materiale didattico definitivo generato.

## Programma identificato

La [Study Guide Microsoft](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/az-305) riporta gli obiettivi in vigore dal 17 aprile 2026 e ultimo aggiornamento della guida il 19 marzo 2026. Sono stati censiti i 49 bullet nei 12 gruppi dei quattro domini. Il cambiamento elencato nel changelog rispetto alla versione precedente riguarda il profilo del candidato.

Le etichette della matrice sono parafrasi concise originali. La corrispondenza con il programma conserva URL, anchor, posizione e hash del testo di ogni bullet; non è stata redistribuita una copia integrale della guida.

Il conseguimento della certificazione Expert richiede anche Azure Administrator Associate, come indicato nella [pagina della certificazione](https://learn.microsoft.com/en-us/credentials/certifications/azure-solutions-architect/). L’utente ha studiato AZ-104; non è stato dichiarato né verificato il possesso della certificazione. Questa distinzione non impedisce il percorso di preparazione AZ-305.

## Inventario e qualità

Il [syllabus AZ-305T00](https://learn.microsoft.com/en-us/training/courses/az-305t00) identifica sei percorsi: prerequisiti, identità/governance/monitoraggio, continuità, storage, infrastruttura e WAF. Sono stati seguiti gli indici reali fino alle singole unità, verificando ogni pagina tramite GET anonimo. I metadati `learn_item` del corso permettono di confrontare l’insieme dei percorsi anche se il syllabus è caricato dinamicamente nel browser.

L’inventario comprende 23 moduli unici e 206 unità uniche. Il modulo introduttivo WAF condiviso non è contato due volte. È stata verificata la pertinenza delle unità e sono state approfondite le sezioni necessarie alla scelta delle fonti e ai problemi di aggiornamento; non si dichiara di avere svolto il corso, gli assessment, i video o i laboratori.

Il catalogo contiene **381 record**: 371 pagine leggibili, 7 asset grafici verificati e 3 placeholder pubblici. Tra le risorse: 102 documenti/confronti tematici, WAF/CAF, 5 architetture di riferimento, 1 customer story e le 12 voci dell’indice dei casi MicrosoftLearning. Dei 12 casi, 8 sono casi nel percorso, 3 sono placeholder e 1 è AI opzionale fuori dai bullet espliciti. Non confondere il totale dei record con altrettante lezioni obbligatorie.

## Esito di copertura e limiti

**49/49 obiettivi hanno fonti primarie dirette, leggibili, revisionate e non scadute alla data della ricerca.** Il criterio non considera sufficiente una homepage, un diagramma, un assessment o un framework generico. La [matrice](MATRICE-COPERTURA.md) mostra le fonti per ogni singolo bullet.

Restano una lacuna Learn dedicata per l’accesso on-premises e tre voci prive di caso formale. Queste carenze sono compensate nel piano con documentazione già verificata e attività future esplicitamente pianificate. [Lacune e aggiornamenti](LACUNE-E-AGGIORNAMENTI.md) elenca anche problemi di versionamento, priorità di approfondimento e dati da riverificare.

La verifica di accessibilità riguarda il corpo della pagina o il file immagine. I banner generici di autorizzazione sono stati distinti dall’effettiva leggibilità degli articoli. Non sono verificate tutte le destinazioni dei link presenti negli articoli, le localizzazioni italiane, gli asset video o le operazioni dietro login. Il perimetro dei percorsi è l’insieme ufficiale del corso AZ-305, non ogni percorso Microsoft Learn potenzialmente collegato ad Azure.

La ricerca produce una biblioteca pronta all’uso e una copertura completa della baseline, con manutenzione prevista. Non equivale a una raccolta definitiva di tutta la conoscenza Azure o a un giudizio sulla preparazione personale. Tutti gli obiettivi personali restano `not_started`.

## Riproducibilità

Per ogni risorsa sono conservati titolo, URL, lingua, competenze, GET/status, URL finale, timestamp, hash, riferimenti editoriali quando presenti e prossima verifica. La revisione semantica è separata dall’osservazione tecnica. La cache delle risposte originali è ignorata da Git; il repository contiene solo i metadati necessari e materiali originali.

I controlli verificano integrità degli ID, corrispondenza con tutti i bullet, gerarchia Learn, deduplicazione, freschezza e copertura effettiva. I controlli non dimostrano da soli la correttezza di una decisione architetturale: la comprensione sarà verificata nelle sessioni.
