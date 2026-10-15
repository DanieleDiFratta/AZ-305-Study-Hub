# Istruzioni del progetto AZ-305

- Rispondere in italiano. Leggere `README.md`, `studio/PIANO-GENERALE.md`, `docs/METODO.md` e la scheda del dominio prima di lavorare.
- Questa prima fase riguarda ricerca, catalogazione e piano. Non costruire dashboard, lezioni complete, flashcard, mappe di ripasso o appunti definitivi finché l’utente non avvia le sessioni di studio o cambia esplicitamente fase.
- Usare la Study Guide ufficiale corrente come programma. Conservare tutti i bullet, anche quando sembrano già noti all’utente; gli ID locali sono ancorati a sezione e posizione, non sono ID Microsoft.
- Privilegiare Microsoft Learn, documentazione Microsoft, Azure Architecture Center, Well-Architected Framework e Cloud Adoption Framework. Non utilizzare exam dumps né materiale riservato dell’esame.
- Non inventare titoli, URL, disponibilità, prezzi, limiti, SLA, date di ritiro o risultati personali. Verificare online le informazioni Azure instabili e registrare la data e la fonte. Distinguere dati attuali, materiali storici e ipotesi.
- Leggere `data/README.md` prima di modificare i dati. `data/catalog.json`, `data/coverage.json` e gli indici Markdown sono generati. Le revisioni sono in `data/reviews.json`; le associazioni editoriali riproducibili sono in `scripts/catalogue.py`.
- Un HTTP 200 da solo non certifica pertinenza o accesso al contenuto. Escludere dalla copertura fonti scadute, cambiate dopo la revisione, placeholder e pagine non leggibili. Non approvare in blocco hash nuovi senza esaminare i cambiamenti.
- Non dichiarare completa la copertura se un solo obiettivo non ha fonti primarie verificate. Riportare separatamente lacune Learn, esercizi mancanti, approfondimenti e padronanza personale.
- Il metodo deriva da Magistrale Dashboard: blocchi per obiettivo coerente, fonti precise, lettura autonoma, dubbi, spiegazione quando l’utente è pronto e breve verifica integrata. Calibrare sulla densità e sul tempo della sessione; nessuna quota fissa di pagine o unità.
- Durante lo studio proporre sezioni/fonti e tempo orientativo senza anticipare la spiegazione. Attendere la lettura autonoma e risolvere i dubbi prima del resoconto. La lettura dell’assistente e i badge del sito non sono progressi personali dell’utente.
- Registrare separatamente blocco proposto, lettura dichiarata, discussione svolta, esercizio svolto e comprensione verificata. Preservare punto di ripresa e dubbi nelle schede del dominio; non trasferire risultati o impegni settimanali dal progetto Magistrale.
- L’esperienza Azure dichiarata è un prerequisito, non prova di padronanza di tutti i trade-off AZ-305. Verificare prima le competenze praticate e dare maggiore spazio alle aree meno frequentate.
- Le decisioni architetturali future devono esplicitare requisiti, almeno due alternative, scelta, rinunce, costi/operabilità, failure mode e fonti. Ogni esempio originale va identificato come tale.
- Nelle future sessioni gli appunti saranno sviluppati per blocco tematico, ampliandoli nel tempo e mantenendo riferimenti, precisazioni e domande. Non generarli automaticamente in questa fase.
- Alla chiusura di una sessione salvare riepilogo, stato distinto e punto di ripresa. Commit e push quando autorizzati dalla sessione, controllando il diff ed escludendo cache, segreti e modifiche estranee. Mai force push o cancellazioni del lavoro altrui.
