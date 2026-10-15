# AZ-305 Study Hub

Biblioteca e percorso personale per preparare **AZ-305** attraverso decisioni architetturali motivate. Repository: [DanieleDiFratta/AZ-305-Study-Hub](https://github.com/DanieleDiFratta/AZ-305-Study-Hub).

**Fase attuale: ricerca e catalogazione.** Nessuna dashboard, lezione completa, flashcard o raccolta di appunti definitivi. Studio personale non ancora iniziato.

## Da dove partire

1. [Piano generale e punto di ripresa](studio/PIANO-GENERALE.md).
2. [Piano didattico progressivo](docs/PIANO-DIDATTICO.md), calibrato sull’esperienza professionale dichiarata.
3. [Matrice dei 49 obiettivi](docs/MATRICE-COPERTURA.md), con documentazione primaria e unità Learn.
4. [Biblioteca verificabile](docs/BIBLIOTECA.md) e [inventario completo Learn](docs/PERCORSI-LEARN.md).
5. [Lacune, riferimenti storici e approfondimenti](docs/LACUNE-E-AGGIORNAMENTI.md).
6. [Rapporto della ricerca](docs/RAPPORTO-RICERCA.md) e [metodo di studio](docs/METODO.md).

## Baseline e significato della copertura

La [Study Guide Microsoft](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/az-305) consultata il **15 ottobre 2026** indica competenze in vigore dal **17 aprile 2026**. Identificati 4 domini, 12 gruppi e 49 bullet; gli ID locali mantengono sezione e posizione del bullet ufficiale.

Tutti i 49 obiettivi hanno almeno una fonte primaria Microsoft verificata. I sei percorsi del syllabus ufficiale comprendono **23 moduli unici e 206 unità uniche**. La raccolta include confronti, WAF, CAF, architetture, diagrammi e casi; i placeholder sono riconoscibili e non valgono come esercizi disponibili. Dettagli e conteggi aggiornati sono in [audit-summary.json](data/audit-summary.json).

Questa è copertura documentale del programma, non una dichiarazione di padronanza, una garanzia di superamento o un censimento di tutta la documentazione Azure. L’accesso on-premises ha documentazione primaria ma nessuna unità Learn dedicata nei percorsi censiti. Restano approfondimenti ed esercitazioni nel registro delle lacune.

## Organizzazione

| Cartella | Contenuto |
| --- | --- |
| `docs/` | Biblioteca, matrice, inventario, piano e rapporti |
| `data/` | Metadati JSON, obiettivi, revisioni e prove delle verifiche |
| `studio/` | Memoria delle sessioni, schede dei domini, decisioni ed errori |
| `templates/` | Modelli vuoti per sessioni e decisioni future |
| `materiali/` | Regole per eventuali file locali; nessun originale Microsoft redistribuito |
| `scripts/` | Ricerca, aggiornamento e controlli riproducibili con Python |

## Verificare e mantenere

Serve Python 3.10 o successivo, senza dipendenze esterne. Il controllo locale non richiede rete né la cache HTML:

```powershell
python scripts/validate.py
python -m unittest discover -s tests -v
```

La rigenerazione dei report usa i metadati già raccolti:

```powershell
python scripts/catalogue.py
```

Per riverificare le pagine pubbliche occorre accesso HTTPS. Le istruzioni complete sono in [MANUTENZIONE.md](docs/MANUTENZIONE.md). Un GET riuscito non approva automaticamente una modifica dei contenuti: le revisioni sono associate all’hash della risposta. Non eseguire `--record-review` senza esaminare i cambiamenti e aggiornare le associazioni necessarie.

Le verifiche hanno cadenza di 30, 60 o 90 giorni; ogni fonte conserva la prossima data di controllo. Nessuna attività cloud a pagamento o deployment è stata eseguita. I file `.cache/` restano locali e sono esclusi da Git.

## Fonti e diritti

Priorità esclusiva a Microsoft per i contenuti tecnici di questa prima raccolta. Materiali originali del progetto: organizzazione, associazioni, piano e criteri di lavoro. Gli articoli, le figure e gli esercizi restano presso le rispettive fonti, con i loro diritti e condizioni. Nessun exam dump. Vedere [FONTI-E-DIRITTI.md](docs/FONTI-E-DIRITTI.md).
