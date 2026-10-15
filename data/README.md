# Dati della biblioteca

I JSON sono UTF-8. Sono conservati metadati, non copie degli articoli o delle soluzioni.

La dashboard legge il catalogo senza modificarlo. I progressi personali sono in `studio/progressi.json` e il manifesto dei materiali di ripasso in `studio/materiali.json`, entrambi mantenuti durante le sessioni. Non scrivere i progressi in `catalog.json`, `coverage.json` o nel campo storico `learning_status` di `objectives.json`. Vedere [DASHBOARD.md](../docs/DASHBOARD.md).

| File | Ruolo |
| --- | --- |
| `objectives.json` | Baseline, pesi, 12 gruppi e 49 obiettivi; etichette italiane concise originali, URL/anchor e posizione del bullet |
| `seeds.json` | Risorse candidate curate e motivazione della selezione, non prova di accessibilità |
| `resources.json` | Osservazioni GET delle pagine base, dei moduli e delle unità; dati grezzi, prima della revisione editoriale |
| `unit-seeds.json` | URL delle unità scoperti dagli indici dei moduli |
| `extra-resources.json` | GET delle voci dei casi e degli asset grafici collegati |
| `reviews.json` | Revisione: hash osservato, pertinenza, obiettivi, ruolo della fonte e limitazioni |
| `catalog.json` | **Biblioteca di riferimento**: osservazioni e revisioni unite, con accessibilità, validità e prossima verifica |
| `coverage.json` | Copertura calcolata per ogni obiettivo, con fonti primarie, unità Learn e supporti |
| `observed-guide.json` | Struttura e hash dei bullet ricavati dall’ultima acquisizione della Study Guide |
| `guide-structure.json` | Struttura accettata durante la revisione della baseline; consente di rilevare modifiche successive |
| `discovery-log.json` | URL iniziali spostati/non validi e correzioni; non sono fonti attive |
| `audit-summary.json` | Conteggi e lacune generati |

## Campi del catalogo

- `id`, `title`, `url`, `kind`, `publisher`, `language`: identità della risorsa. `title` deriva dall’H1; per i diagrammi è un’etichetta redazionale riferita alla pagina genitore.
- `objective_ids`, `mapping_scope`: competenze pertinenti e precisione dell’associazione. `direct` identifica contenuto tematico; `module_context`/`path_context` sono solo contesto; `case_context` identifica un caso utile a un insieme di obiettivi. L’associazione non promette che una pagina esaurisca da sola un obiettivo.
- `selection_reason_it` e `review.note_it`: motivazione originale della selezione e dell’associazione.
- `verified_on`: giorno dell’ultimo GET, in Europa/Roma. `access.checked_at`: istante con offset. `source_updated_at` e `source_ms_date`: metadati editoriali dichiarati dal sito, che non sostituiscono la verifica.
- `access`: metodo, stato HTTP, URL richiesto e finale, MIME, hash SHA-256 e stato di accessibilità. I redirect sono conservati; non viene inventato un HTTP status per le sole risposte del motore di ricerca.
- `review.reviewed_response_sha256`, `review_current`: la risposta corrente corrisponde a quella esaminata. Anche cambiamenti di template possono richiedere revisione; il criterio è conservativo.
- `review.coverage_role`: `primary` per documentazione/confronto tematico, `training` per unità, `support` per framework, contesto, esempi e figure. Solo fonti primarie dirette possono chiudere la copertura.
- `fresh`, `recheck_days`, `next_review_on`: scadenza della verifica. Prima di affermare copertura aggiornata rigenerare i report con la data attuale e validare.
- `eligible_for_coverage`: accesso pubblico leggibile, revisione sull’hash corrente e verifica non scaduta. È un controllo documentale, distinto dallo studio personale.
- `module_ids`, `unit_ids`, `path_ids`, `unit_order`: gerarchia Learn e ordine ufficiale. Il modulo introduttivo WAF è condiviso.
- `source_uid`, `source_commit_url`, `headings`: ulteriori riferimenti offerti da Microsoft. Un link a un commit MicrosoftDocs può richiedere autorizzazione; non viene contato come risorsa verificata distinta.

## Stati di accessibilità

| Stato | Significato |
| --- | --- |
| `public_content` | Corpo della pagina leggibile con GET anonimo; account, quiz, video o deployment non eseguiti |
| `public_asset` | Asset scaricabile con MIME immagine e hash verificati; non redistribuito |
| `public_placeholder` | Pagina leggibile ma dichiara che non esiste un caso formale; mai valida come esercizio |
| `unavailable` | HTTP 404/410 |
| `check_failed` | Verifica tecnica fallita, senza dedurre che la fonte sia scomparsa |
| `content_not_available` / `unverified` | Risposta insufficiente o contenuto non accertato; esclusa dalla copertura |

Le note del template “authorization required” sono distinte dal corpo effettivamente leggibile. I flag editoriali sono promemoria di confronto con fonti correnti, non dichiarazioni che un’intera unità sia obsoleta.
