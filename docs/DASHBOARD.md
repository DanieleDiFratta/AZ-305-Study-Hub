# Dashboard personale statica

Implementazione autorizzata il 15 ottobre 2026. Hosting previsto: GitHub Pages pubblico. Interfaccia, progressi ed elaborati inclusi nel sito sono pubblici. Non ci sono database, account, servizi esterni, dipendenze JavaScript o stato personale nel browser.

## Avvio locale

Python 3.10 o successivo, senza pacchetti aggiuntivi:

```powershell
python -B scripts/build_site.py
python -m http.server 8000 --bind 127.0.0.1 --directory _site
```

Aprire `http://127.0.0.1:8000`. È possibile anche aprire `_site/index.html` direttamente: i dati sono uno script locale e non richiedono fetch. I collegamenti interni usano frammenti, quindi funzionano anche sotto il percorso del repository su Pages.

## Sorgenti

| File | Responsabilità |
| --- | --- |
| `web/index.html`, `web/style.css`, `web/app.js` | Interfaccia e navigazione responsive |
| `scripts/build_site.py` | Build locale; legge le sorgenti senza riscriverle |
| `docs/PIANO-DIDATTICO.md` | Sequenza di studio Microsoft Learn e regole delle sessioni |
| `scripts/build_site.py`, `BLOCK_IDS`, `PATH_DOMAINS` | Percorsi dal syllabus, moduli e unità dagli indici censiti; associazioni agli obiettivi |
| `data/` | Catalogo e revisioni secondo il processo esistente |
| `studio/progressi.json` | Data d’esame, ripresa, evidenze, sessioni, dubbi e richiami |
| `studio/materiali.json` | Elenco esplicito degli elaborati pubblicati |
| `studio/ripasso/` | Appunti, mappe e flashcard delle sessioni future |

`_site/` è generata e ignorata da Git. Il generatore copia soltanto quattro asset web e produce il file dati e `.nojekyll`; non pubblica la cache o l’intero repository. Non aggiungere altri file manualmente nella cartella generata.

## Aggiornamento alla chiusura di una sessione

1. Salvare il riepilogo secondo [METODO.md](METODO.md) e aggiornare la scheda del dominio e `studio/PIANO-GENERALE.md`.
2. Aggiornare `studio/progressi.json`: data, punto esatto di ripresa e soltanto le evidenze effettive. Ogni stato può essere presente indipendentemente dagli altri.
3. Produrre gli appunti approfonditi, la mappa e le flashcard del blocco trattato. Inserire i file in `studio/ripasso/` e registrarli in `studio/materiali.json` secondo il [formato](../studio/ripasso/README.md).
4. Registrare dubbi, errori e prossimo richiamo, se concordato. Le date di ripasso sono editoriali, non calcolate da un algoritmo.
5. Eseguire build e controlli. Commit e push soltanto quando autorizzati dalla sessione. La pubblicazione aggiorna tutti i dispositivi alla stessa versione.

Una scheda di stato per un obiettivo o un blocco ha questa forma:

```json
{
  "read": {"on": "2026-10-15", "evidence": "Lettura dichiarata: fonte e sezione"},
  "discussed": {"on": "2026-10-15", "evidence": "Riepilogo del confronto realmente svolto"}
}
```

Questi sono esempi di formato, non progressi dell’utente. Le chiavi consentite sono `proposed`, `read`, `discussed`, `practiced`, `verified`. Ogni stato richiede data ISO ed evidenza non vuota. Le schede sono sotto `objectives`, per ID obiettivo, e `blocks`, per i sei ID `LP-*` del piano. Gli stati del blocco non completano automaticamente i singoli obiettivi, né viceversa. Il campo storico `learning_status` della baseline non è utilizzato per il progresso personale.

Le sessioni sono oggetti con `date`, `block_id`, `summary`. I dubbi hanno `block_id`, `text` ed eventuale `resolved_on`. I richiami hanno `block_id`, `due_on`, `reason` ed eventuale `completed_on`. Il sito mostra i richiami aperti, ordinati per data. I dettagli degli errori restano nel registro e nei riepiloghi delle sessioni.

## Fonti e manutenzione

La copertura è ricalcolata dalle fonti dirette primarie: contenuto pubblico, HTTP 200, revisione sull’hash corrente e scadenza non superata. Il browser usa il giorno corrente in Europa/Roma, anche per il conto alla rovescia. Una fonte scaduta smette di chiudere la copertura senza cancellare le evidenze personali.

La biblioteca permette ricerca, filtro per dominio e tipo e paginazione. I tre placeholder sono esclusi normalmente e consultabili con il filtro dedicato. L’apertura di una fonte e la risposta di una flashcard non scrivono progressi.

La build non visita o approva fonti online. Per aggiornare il catalogo seguire [MANUTENZIONE.md](MANUTENZIONE.md). La CI non usa `--record-review`. I controlli del sito possono continuare a pubblicare una biblioteca che segnala fonti scadute: la scadenza non deve bloccare l’accesso allo studio, né essere nascosta.

## GitHub Pages

Il workflow [pages.yml](../.github/workflows/pages.yml) verifica, genera e pubblica soltanto `_site/`, sui push a `main` o con avvio manuale. Nelle pull request esegue build e controlli senza deployment. In GitHub, selezionare **Settings → Pages → Source → GitHub Actions**. Nessuna impostazione remota è stata cambiata dall’implementazione locale.

## Verifiche

```powershell
python -B scripts/validate.py
python -B -m unittest discover -s tests -v
node --check web/app.js
python -B scripts/build_site.py
```

Le prove del sito verificano che nessun obiettivo scompaia dal percorso, che i progressi richiedano evidenze, che le sorgenti non vengano riscritte e che il manifesto non possa includere file fuori dalla cartella autorizzata. La verifica visiva deve coprire desktop e viewport mobile, navigazione, ricerca, filtri e assenza di scorrimento orizzontale.

Per le prove DOM facoltative serve Node.js 20.19+ (oppure 22.12+ o 24+) e jsdom, installato soltanto nella cache locale. Su Windows usare `npm.cmd` se PowerShell blocca `npm.ps1`:

```powershell
npm.cmd install --prefix .cache/site-qa --cache .cache/npm --no-save --ignore-scripts --no-audit --no-fund jsdom@27
python -B scripts/build_site.py
node --test tests/site_ui.cjs
```

Questi test coprono ricerca, filtri, paginazione, collegamenti, stati personali, scadenza delle fonti e flashcard con dati sintetici. Non richiedono un browser, non pubblicano le fixture e non sostituiscono il controllo visivo. La dashboard e la build restano senza dipendenze esterne.
