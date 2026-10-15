# Materiali delle sessioni

Questa cartella accoglie gli elaborati originali prodotti durante lo studio. Non contiene ancora appunti, mappe o flashcard: nessuna sessione è stata svolta.

La dashboard pubblica esclusivamente i materiali dichiarati in [materiali.json](../materiali.json). Aggiungere un file qui non basta a pubblicarlo. Tutti i materiali elencati sono pubblici, come i progressi mostrati dal sito.

## Formati

- Appunti: file `.md`, con titoli, paragrafi, link HTTPS, elenchi, grassetto e blocchi di codice. HTML incorporato e immagini remote non vengono eseguiti. Le tabelle Markdown e Mermaid non sono supportati: per confronti usare elenchi, per diagrammi pubblicare SVG.
- Mappe: file `.svg` originali con `viewBox`, testo leggibile e descrizione; oppure `.md` con una struttura testuale. Per mobile, preferire diagrammi verticali. Il generatore rifiuta script, eventi e riferimenti esterni negli SVG. Nessuna copia di diagrammi Microsoft.
- Flashcard: file `.json` contenente un elenco di oggetti con `question` e `answer`, entrambi testi non vuoti. Domanda e risposta sono visualizzate come testo, senza HTML.

## Manifesto

Ogni voce di `studio/materiali.json` contiene:

```json
{
  "id": "s01-appunti",
  "kind": "notes",
  "title": "Titolo del materiale effettivamente sviluppato",
  "block_id": "S01",
  "published_on": "2026-10-15",
  "summary": "Descrizione del contenuto studiato",
  "path": "studio/ripasso/S01/appunti.md"
}
```

Questo è soltanto un esempio di struttura, non un materiale pubblicato. I tipi sono `notes`, `map` e `flashcards`. Ogni file deve risiedere sotto `studio/ripasso/`. Citare nei materiali fonti, sezioni e data di verifica; identificare gli esempi originali. Aggiornare gli elaborati nel tempo, conservando precisazioni e dubbi.
