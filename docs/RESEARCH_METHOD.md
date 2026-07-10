# Research Method — grounding Word Histories in Ted's databases & PDF library

This is the repeatable method for researching a magical term's **origin, etymology, and historical
usage** against Ted's own scholarship, so every Word History on the site cites primary and secondary
sources rather than generic web knowledge. **Cite these materials as much as possible.**

The tool that does the searching is [`scripts/research.py`](../scripts/research.py); this doc
explains what it searches, how to read the results, and how to turn them into a cited page.

---

## The sources (what exists, where)

### A. Structured databases (`C:\Dev`)
Registry of all of Ted's magic/alchemy DBs: `C:\Dev\wiki\registry.md` (theme **"esoteric portals"**)
and `registry.tsv`. The ones with directly-queryable data:

| Database | Path | What's citable |
|---|---|---|
| **Renaissance magic** | `C:\Dev\renaissance magic\data\` | `definitions.json` — **139 scholarly term-entries** (`term`, `definition_brief`, `definition_long`) with inline citations (Yates, Copenhaver, Zambelli). `kwic_concordance.json` — keyword-in-context lines tagged with source document. `biographies.json`, `latin_seed_list.json`. |
| **Medieval magic** | `C:\Dev\MedievalMagicDB\site\data.json` | `concepts` (54, with `definition_long` + `significance` + `source_method`), `persons`, `bibliography`, `timeline_events`. Also `medieval_magic.db` (SQLite). |
| **Theosophical alchemy** | `C:\Dev\TheosophicalAlchemyDB\data\` | `master_citation_index.json` (`concepts`, `figures`), `markdown_citations.json`. |
| Others (grep by keyword) | `AgrippaDOP`, `ChristianCabalaDB`, `CROWLEYDB`, `neoplatonism-portal`, `GoetiaRevEng`, `PicoDB`, `MagicalLatin`, `WitchcraftStudiesDB`, `OCCULTIMGDB` | Project-specific JSON/MD; resolve paths via `registry.tsv`. |

Renaissance `definitions.json` skews Latin/Neoplatonic/Kabbalist — great for **conjure, invoke,
divine, necromancy, goetia, sigil, pentacle, exorcism, maleficium, theurgy, characteres, ligature**
(as *incantatio, invocatio, divinatio, necromantia, goetia, sigillum, pentaculum, exorcismus,
maleficium, theurgia, characteres, ligatura*). The tool bridges English→Latin via a stem match.

### B. Full-text PDF corpora (`E:\pdf` — extracted `.txt` / `.md`, grep-able)

| Corpus | Path | Highlights |
|---|---|---|
| **Medieval magic** | `E:\pdf\magic\medieval magic\` (23 texts) | Klaassen *Transformations of Magic*; Fanger *Invoking Angels* / *Rewriting Magic*; Page *Magic in the Cloister*; Attrell & Porreca *Picatrix*; Peterson *Lesser Key of Solomon* / *Grimorium Verum*; Skinner *Ars Notoria*; Bailey *The Sacred and the Sinister*. |
| **Renaissance magic** | `E:\pdf\renaissance magic\` (381 texts + Markdown) | Yates *Giordano Bruno and the Hermetic Tradition*; Couliano *Eros and Magic in the Renaissance*; Keith Thomas *Religion and the Decline of Magic*; Clark *Thinking with Demons*; Zambelli; Copenhaver; primary authors foldered (Agrippa, Ficino, Dee, Pico, Reuchlin, Trithemius, Bruno/Lull, Kircher, Fludd). |
| **Alchemy** | `E:\pdf\alchemy\Markdown\` (4,078 md) | **Lyndy Abraham *A Dictionary of Alchemical Imagery*** (ideal for term senses); Principe; Newman; Nummedal *Alchemy and Authority*; Linden *The Alchemy Reader*; Obrist; the Maier/*Atalanta* extracts. |
| Ancient magic | `E:\pdf\magic\ancient magic PGM\` | Greek Magical Papyri. |
| Hermetica | `E:\pdf\hermetic\` | Corpus Hermeticum scholarship. |
| Grimoire | `E:\pdf\Grimoire\` | Grimoire tradition (some PDF-only). |

`plain_text_drafts\` subfolders hold the OCR/extracted text — that's what gets searched.

---

## The workflow

1. **Run the tool** for the term (by lexicon slug — it reuses the term's morphology regex):
   ```
   python scripts/research.py necromancer
   python scripts/research.py sigil talisman pentacle
   python scripts/research.py --word "philtre|philter" potion   # ad-hoc regex + slug
   ```
   It writes `data/research/<slug>.json` (and a copy to `site/data/research/`), and prints a summary.

2. **Read the dossier.** `db_hits[]` are structured entries (definition + source DB); `corpus_hits[]`
   are `{corpus, file, cite, snippet}` grepped from the PDFs. The `cite` is a cleaned filename —
   **open the source file to verify and quote precisely** before using it.

3. **Write the Word History** in `data/histories.json` (keyed by slug):
   - Lead with the etymology (from `data/etymology.json`), then historical usage, drawing on the
     dossier. Quote sparingly and attribute (author, short title).
   - Populate the entry's `sources[]` with `{label, where}` — `label` = the citation, `where` =
     which DB/corpus it came from. These render as a **Sources & further reading** block.
   - The term page's **Etymology section** also auto-renders the dossier's DB definitions + top
     cited quotes when `site/data/research/<slug>.json` exists — so citations show even before a
     full history is written.

4. **Verify, don't paraphrase-hallucinate.** The tool surfaces candidates; the scholar confirms. The
   stem-bridge can over-match (a Latin entry sharing a prefix) — discard off-topic hits.

## Citation conventions
- Corpus quote → *Author, Short Title* (from the filename), e.g. *Klaassen, The Transformations of
  Magic*. Page numbers aren't in the extracted text; cite work-level, or open the PDF for the page.
- DB definition → the database name as author, e.g. "RenaissanceMagicDB, s.v. *necromantia*",
  passing through any scholars it names (Yates, Copenhaver).
- Keep a light touch: these pages are popular scholarship, not a critical apparatus — 3–6 good
  citations per history beats an exhaustive list.

## Extending
- New corpus? Add a `(label, root, exts, categories)` row to `CORPORA` in `research.py`.
- New database? Add a branch in `search_db()` (match on term/label + definition full-text).
- Batch-refresh all researched terms: loop `research.py` over the slugs in `data/histories.json`.
