# The Vocabulary of Magic

**A digital-humanities word study of *Magic: The Gathering* — mining the complete card corpus for
the language of magic, and tracing every word back through five thousand years of real history.**

### 🔮 Live site → **https://t3dy.github.io/MTG-Historical-Magic/**

*(Deploys automatically from `site/` via GitHub Pages. If the link 404s, the first Pages build is
still running — check the **Actions** tab.)*

---

Magic: The Gathering has, over thirty years, become one of the largest published fantasy corpora in
existence — **34,629 unique cards**, each with a name, rules text, and a line of flavor. That makes
it an unusually rich place to ask a linguistic and historical question: *what are all the words
English uses for magic, how does a modern game deploy them, and where did each one come from?*

This project answers that with a curated lexicon of **~120 magical roots** across seven families,
morphology-aware counts, **112 illustrated term pages**, cited **Word Histories**, a suite of data
visualizations, and a **300+ entry historical timeline** running from Babylonian liver-divination to
the day *Scry* became a keyword.

## What's on the site

| Page | What |
|------|------|
| **Terms** (`index.html`) | Searchable, filterable grid of all term pages, art-backed |
| **Term page** (`term.html?t=`) | Tabs: Overview (colour identity, first-printed year, morphology) · Gallery (Scryfall card images) · Flavor · Mechanics · **Etymology** (auto-surfaces cited scholarship from the databases & PDF library) · **Word History** |
| **Histories** (`histories.html`) | Cited long-form pages on a word's origin, etymology, and historical usage |
| **Timeline** (`timeline-history.html`) | 300+ dated entries — the origin and development of magical words, texts, figures, traditions, and practices, antiquity → today |
| **Atlas** (`atlas.html`) | The full quantitative census, by family, flavor vs rules |
| **Charts** (`charts.html`) | Five visualizations: **Word vs Keyword** (flavor↔rules scatter), **Loanword Atlas** (origins by language), **Color of Magic** (WUBRG per family), **Vocabulary over Time** (in Magic), **The Whole Lexicon** (treemap) |
| **About** | Methodology and the research method |

The site is **static, dependency-free, and self-contained** — plain HTML/CSS/JS reading JSON, no
build framework, no external requests (card images are cached locally with a Scryfall fallback).

## How it was made — the process

Four layers, each reproducible:

1. **Corpus.** One [Scryfall bulk download](https://scryfall.com/docs/api/bulk-data) of every unique
   card (never per-card scraping). `fetch_bulk.py → normalize.py`.
2. **Analysis.** A hand-curated regex lexicon (`data/derived/lexicon.json`) matches each magical root
   **morphologically** — *conjure/conjures/conjured/conjuration* collapse to one lemma — and counts
   two surfaces **separately**: **flavor text** (the word as story) vs **rules text** (the word as
   game mechanic). That split is the project's core finding: *spell* and *transmute* are mechanics;
   *mage*, *curse*, and *necromancer* are literary words. `analyze.py → build_terms.py`, illustrated
   by `fetch_card_images.py`.
3. **Scholarship.** Each term is researched against Ted's own libraries — the medieval-, renaissance-,
   and alchemy databases and a full-text PDF corpus (Klaassen, Fanger, Yates, Couliano, the
   *Picatrix*, Lyndy Abraham, and more) — by `research.py`, which returns a **citable dossier** that
   the site surfaces on every Etymology tab. See **[`docs/RESEARCH_METHOD.md`](docs/RESEARCH_METHOD.md)**.
4. **History.** A 300+ entry timeline built from hand-authored seed files
   (`data/history_seed/*.json`) merged with word-origin/attestation entries auto-derived from the
   etymology data and MTG debut points. Entry template: **[`docs/TIMELINE_TEMPLATE.md`](docs/TIMELINE_TEMPLATE.md)**.

## Values & goals

- **Take the words seriously.** The thesis is that *the magic on a Magic card has a genealogy worth
  knowing.* Every claim is dated, sourced, and linked back to the word it explains — no vibes-history.
- **Ground it in real scholarship.** The history is drawn from a working research library and its
  databases, not generic web summaries; citations are first-class, and the method for finding them is
  itself part of the repo.
- **Bridge two worlds.** The project is built to be legible to a *Magic* player and to a historian of
  magic at once — the corpus tells you which words matter; the scholarship tells you what they mean.
- **Reproducible and honest.** The whole site regenerates from one command; the flavor/rules split
  refuses to conflate a keyword with a word; where a "word history" term never appears on a card
  (*theurgy*, *goetia*), the page says so.

## Build it yourself

```bash
set PYTHONUTF8=1                        # Windows console: emit UTF-8
python scripts/fetch_bulk.py           # -> data/raw/oracle_cards.json  (Scryfall bulk, cached)
python scripts/normalize.py            # -> data/derived/cards.jsonl
python scripts/analyze.py              # -> data/derived/counts.json    (the Atlas aggregate)
python scripts/build_terms.py          # -> site/data/terms/*.json, terms_index.json, timeline/colors
python scripts/fetch_card_images.py    # -> site/img/<term>/*.jpg
python scripts/research.py <slug>...   # -> data/research/<slug>.json   (citable dossiers)
python scripts/build_history_timeline.py  # -> site/data/history_timeline.json
python scripts/export_site.py          # -> site/data/summary.json
python -m http.server 5177 --directory site   # open http://localhost:5177
```

Pure Python stdlib — no `pip install`. Curated inputs (everything else regenerates):
`data/derived/lexicon.json`, `data/etymology.json`, `data/essays.json`, `data/history_seed/*.json`.

## Deployment

`site/` (including `site/data/` and `site/img/`) is committed and published to GitHub Pages by
`.github/workflows/pages.yml` on every push to `main`. The 172 MB raw Scryfall download
(`data/raw/`) and the 31 MB `cards.jsonl` are git-ignored and rebuilt from the pipeline.

## License & attribution

Card data and images via **[Scryfall](https://scryfall.com)** (compilation CC0; card names, text,
and art © Wizards of the Coast — used here for research and commentary). Scholarly citations belong
to their authors. The analysis, code, histories, and timeline are this project's own.

*Built with the assistance of Claude Code.*
