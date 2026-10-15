# Riverifica delle fonti

Le pagine sono state controllate il 15 ottobre 2026. Ogni record ha `verified_on`, `recheck_days` e `next_review_on`. La cadenza è 30 giorni per programma/ritiri, 60 per documentazione e Learn, 90 per il customer story. Il primo gruppo scade il **14 novembre 2026**. Fare un controllo aggiuntivo prima delle sessioni su temi instabili e prima dell’esame.

## Controllo locale

```powershell
python scripts/catalogue.py
python scripts/validate.py
python -m unittest discover -s tests -v
```

Queste operazioni non richiedono connessione e non modificano gli stati personali. La rigenerazione applica la data corrente: i report non vanno presentati come aggiornati senza rieseguirla. Se una fonte scade, cambia hash o diventa illeggibile, esce dalla copertura utile. Il validatore segnala il problema e non autorizza una dichiarazione di completezza.

## Riverifica pubblica tramite rete

```powershell
python scripts/research.py --refresh
python scripts/extra_sources.py --refresh
python scripts/catalogue.py
python scripts/validate.py
```

`research.py` riparte da `data/seeds.json`, usa GET e segue gli indici dei percorsi/moduli; `extra_sources.py` segue i casi e verifica gli asset grafici. Richieste limitate a sei contemporanee e al perimetro pubblico selezionato; niente credenziali, quiz inviati o risorse Azure create. Le risposte HTML finiscono in `.cache/`, esclusa da Git. I metadati sono registrati anche per i fallimenti, senza mascherarli.

Se si modifica la selezione iniziale, aggiornare `scripts/build_seeds.py` e poi rigenerare `data/seeds.json` con `python scripts/build_seeds.py`. Lo script ricrea anche la baseline degli obiettivi dichiarata: non usarlo come approvazione automatica di un nuovo programma. Se Microsoft cambia il programma, aggiornare consapevolmente gruppi, conteggi, parafrasi, piano e associazioni dopo aver letto la nuova guida.

## Revisione dopo un cambiamento

1. Esaminare il diff di dati, titoli, URL finali e metadati. Confrontare i bullet in `observed-guide.json` con `guide-structure.json`; i loro hash segnalano anche cambiamenti a parità di numero.
2. Riaprire le fonti cambiate e verificare il contenuto delle sezioni utilizzate. Le date di aggiornamento o un HTTP 200 non bastano. Se una pagina è stata sostituita da una homepage o da un tema diverso, cercare una fonte adatta.
3. Aggiornare `scripts/catalogue.py` per le associazioni tra unità e obiettivi, e il registro delle lacune. `scripts/review_extracts.py ID...` aiuta a ispezionare la cache locale, ma un estratto iniziale può non bastare: consultare tutte le sezioni necessarie.
4. Solo dopo la revisione editoriale completa delle modifiche, registrare i nuovi hash e rigenerare:

```powershell
python scripts/catalogue.py --record-review
python scripts/validate.py
python -m unittest discover -s tests -v
```

`--record-review` aggiorna tutte le revisioni e accetta la struttura osservata della guida. È un’azione editoriale esplicita: **non inserirla in un aggiornamento periodico automatico**. Conservare il diff in Git per ricostruire cosa è cambiato. Uno script non può certificare da solo la pertinenza delle fonti.

## Scelta delle prossime fonti

Usare prima i rimandi ufficiali e le guide di scelta, poi una ricerca limitata a Microsoft. Registrare sempre l’esito reale di apertura. I risultati indicizzati ma illeggibili vanno nel registro delle verifiche fallite, senza contarli come copertura. Non sostituire fonti primarie con riassunti di terzi o exam dumps.
