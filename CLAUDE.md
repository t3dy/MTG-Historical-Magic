# MTGMAGICWORDS — Claude Code Instructions

**One-line:** Data-mine the complete Magic: The Gathering card corpus (via Scryfall) for the
vocabulary of magic — professions (wizard, shaman, cleric…), acts (conjure, scry, hex…), and
their morphological variants — count and contextualize them, publish findings as a website, and
feed an **etymology podcast** on the history of magical words.

Owner: Ted. Part of the `C:\Dev` workspace — see `../CLAUDE.md` and `../wiki/registry.md`.
Sibling MTG project: `../MTGSLIDER` (theme→slideshow). Historical-magic databases to draw on for
etymology/context are listed in `docs/RESEARCH_PLAN.md`.

## Prime directives

1. **Never scrape card-by-card.** Use Scryfall **bulk data** (one download of the whole corpus).
   Endpoint: `https://api.scryfall.com/bulk-data`. We want the `oracle_cards` bulk file (one entry
   per unique Oracle text, ~30k cards) for text analysis, and optionally `default_cards` (all
   printings) only when print-level data is needed. Respect Scryfall's rate limits & caching; set a
   descriptive `User-Agent`. Data is CC-licensed; card text © Wizards — cite, don't republish wholesale.
2. **Morphology-aware counting.** A "term" is a *lemma* (root), not a string. `conjure`, `conjures`,
   `conjured`, `conjuring`, `conjurer`, `conjuration` collapse to the root **conjure/conjur-**. Track
   variants explicitly so we can show the spread. See `scripts/analyze.py` and `data/derived/lexicon.json`.
3. **Separate the two text surfaces.** Magic vocabulary lives in two places with different meaning:
   - **Type line / subtypes** (e.g. `Creature — Human Wizard`) → *canonical* creature classes.
   - **Rules text / flavor text** → *usage* of verbs and imagery ("conjure", "hex", "commune").
   Count them separately, then compare. Don't conflate a Wizard creature-type with the word "wizard"
   appearing in flavor text.
4. **Reproducible pipeline.** `fetch → normalize → analyze → export` (see `scripts/`). Every output
   in `data/derived/` must be regenerable from a fresh `fetch`. No hand-edited data files except the
   curated `lexicon.json` seed.

## Pipeline

```
scripts/fetch_bulk.py         # download + cache Scryfall bulk data -> data/raw/oracle_cards.json
scripts/normalize.py          # flatten to a tidy card table (+ image URIs) -> data/derived/cards.jsonl
scripts/analyze.py            # lemma/variant counting -> data/derived/counts.json (Atlas aggregate)
scripts/build_terms.py        # per-term detail (snippets, galleries, etym) -> site/data/terms/*.json
scripts/fetch_card_images.py  # download gallery thumbnails -> site/img/<term>/*.jpg
scripts/export_site.py        # summary.json for the hub
site/                         # static site: index (hub) / term / atlas / insights / about
```

Curated inputs (hand-edited, everything else regenerates): `data/derived/lexicon.json` (~120 roots
across 7 categories) and `data/etymology.json` (per-term etymologies — the podcast layer).
Console: set `PYTHONUTF8=1` on Windows or prints with non-ASCII will crash.

Run order documented in `README.md`. Prefer Python + stdlib + `requests`; use `nltk`/`spaCy` for
lemmatization only if we commit to it (see open question in RESEARCH_PLAN). A regex-root fallback is
built in so the pipeline runs with zero heavy deps.

## Researching terms (Word Histories) — cite Ted's own scholarship

The site's **Word Histories** (deep pages on a term's origin/etymology/historical usage) must be
grounded in Ted's databases and PDF library, **not** generic web knowledge. Full method:
[`docs/RESEARCH_METHOD.md`](docs/RESEARCH_METHOD.md). In short:

- **Tool:** `python scripts/research.py <slug>` searches the magic/alchemy databases in `C:\Dev`
  (Renaissance `definitions.json` + KWIC concordance, `MedievalMagicDB`, `TheosophicalAlchemyDB`)
  and the full-text PDF corpora in `E:\pdf` (`magic\medieval magic`, `renaissance magic`,
  `alchemy\Markdown` incl. Lyndy Abraham's *Dictionary of Alchemical Imagery*). It writes a citable
  dossier to `data/research/<slug>.json` (+ `site/data/research/`).
- **DB list of record:** `C:\Dev\wiki\registry.md` (theme "esoteric portals") → `registry.tsv`.
- **Always verify a `cite` against its source file before quoting**; attribute (author, short title).
- Curated histories live in `data/histories.json`; the Etymology tab auto-surfaces the dossier's
  cited quotes when a research file exists.

## Conventions

- Timestamps absolute (workspace rule). Today's baseline: 2026-07-08.
- Keep `docs/RESEARCH_PLAN.md` as the living scope doc; append decisions, don't rewrite history.
- When findings are worth preserving, drop a note in `wiki_notes/` and (on request) ingest into
  `C:\Dev\wiki\`.
- Podcast angle is the *north star*: every metric should be answerable as "and here's the story of
  that word." Etymology sources & DB pointers live in `docs/RESEARCH_PLAN.md`.

## Status

2026-07-08 — Live, populated, and fully featured. 34,629 cards mined; ~120-root lexicon across 7
themed families; 110 term pages, each with a Scryfall card-image gallery (1,684 images cached);
tabs Overview (colour identity + first-printed year + morphology) / Gallery / Flavor / Mechanics /
Etymology / Essay. **All 110 etymologies written** (`data/etymology.json`, 115 entries, each tagged
with an origin `lang`). 5 flagship long-form essays (`data/essays.json`). Podcast season:
ep-1 full script + 4 outlines (`data/podcast.json`, `docs/podcast/`). Visualization suite under
Charts: Insights (flavor-vs-rules scatter), **Loanword Atlas** (origins by language), **Color of
Magic** (WUBRG per family), **Timeline** (stacked-area 1993–2026 + debuts), **Mosaic** (treemap).
Pipeline gained `build_terms.py` (per-term detail + timeline.json + colors.json aggregates) and
`fetch_card_images.py`. Portfolio piece for Ted's MTG-content-creator coach. Next: record ep 1;
optional per-card set/rarity filters in galleries; deploy (GitHub Pages/Vercel — run build first).
