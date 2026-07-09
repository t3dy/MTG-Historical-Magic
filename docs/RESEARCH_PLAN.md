# MTGMAGICWORDS — Research Plan & Backlog

Living scope doc. Append decisions; don't rewrite history. Baseline: 2026-07-08.

North star: **an etymology podcast on the history of magical words**, seeded by what the MTG
corpus reveals about how those words cluster, spread, and get used.

---

## 1. The core study (v1)

**Question:** Across every distinct MTG card, what is the vocabulary of magic — its *professions*
(wizard, shaman, cleric…), its *acts* (conjure, scry, hex…), its *qualities* (arcane, eldritch…),
and its *objects* (talisman, sigil, grimoire…) — and how often does each appear, counting
morphological variants as one root?

**Method:** `fetch → normalize → analyze → export` (see `../CLAUDE.md`). Two surfaces counted
separately: **type-line subtypes** (canonical creature classes) vs **rules/flavor text** (usage of
verbs & imagery). Morphology handled by a curated regex lexicon (`data/derived/lexicon.json`) so a
human controls what collapses into a root.

**v1 deliverable:** a findings site with (a) a ranked table of professions by creature-count,
(b) a ranked table of magical *acts/terms* by text frequency with their variant breakdown, and
(c) per-term "example cards" + a slot for the etymology write-up.

---

## 2. Sibling research projects (the backlog)

Each is a self-contained study over the same corpus; several double as podcast episodes.

1. **Profession census.** Wizard vs Shaman vs Cleric vs Druid vs Warlock… as creature types, over
   time (by set release year) and by color. *Podcast: why does English have so many words for
   "magic-user," and what distinguishes them?*
2. **Verbs of power.** Conjure / summon / invoke / evoke / incant / commune — the *acts*. Which
   dominate rules text vs flavor text? *Podcast: the grammar of spellcasting.*
3. **Divination cluster.** Scry, augur, divine, prophesy, oracle, omen, portent. MTG even has a
   keyword *Scry*. *Podcast: seeing the future, from Latin* augurium *to a card mechanic.*
4. **Curse & blessing.** Hex, curse, bane, blight vs bless, hallow, boon, ward. Polarity of magic.
5. **Loanword atlas.** Where each root entered English: Greek (necromancer, hierophant, magus),
   Latin (conjure, divine, invoke), Old English (witch, warlock, spell), Arabic (talisman, alchemy,
   elixir), Persian (magus/magi). *Podcast series backbone.*
6. **Alchemy lexicon.** Transmute, elixir, philosopher, quintessence, sublimate — cross-reference
   Ted's alchemy DBs (§4). Ties to `MTGSLIDER` and the alchemy game cluster.
7. **Color-of-magic semantics.** Do "shaman" words skew green/red, "wizard" words blue, "cleric"
   white, "necromancer" black? Quantify the flavor stereotype.
8. **Neologism & compounding.** MTG-invented or -popularized magic words (planeswalker, manaweave)
   vs inherited ones. What does a modern fantasy franchise *add* to the lexicon of magic?
9. **Keyword etymologies.** MTG's own magic keywords (Scry, Conjure, Foretell, Bewitch, Cascade,
   Convoke, Channel…) traced to their ordinary-language origins. Bridges game-mechanics → etymology.
10. **Timeline of terms.** First-appearance of each root across 30 years of sets — does the game's
    magical vocabulary broaden, and toward which language families?

---

## 3. Etymology & historical-usage sources (for the podcast layer)

- **Oxford English Dictionary** (historical citations, first-attestation dates, sense evolution) —
  primary target; needs institutional/library access. Fallback: **Etymonline** (Douglas Harper),
  **Wiktionary** (machine-readable, CC), **Century Dictionary**, **Middle English Dictionary**.
- **Corpora for historical usage curves:** Google Books Ngrams, EEBO/ECCO where available.
- **Classical roots:** Lewis & Short (Latin), Liddell–Scott–Jones (Greek) for Greco-Latin magic
  vocabulary; Bosworth–Toller for Old English (witch, warlock, spell, galdor).
- **Web research** for scholarly framing of each term's magical sense.

## 4. Ted's own historical-magic databases (context & cross-links)

Draw etymological + conceptual context from these local projects (paths from `../wiki/registry.tsv`):

| DB | Path | Use for |
|----|------|---------|
| WitchcraftStudiesDB   | `C:\Dev\WitchcraftStudiesDB`      | witch/warlock/hex/curse scholarship (Clark, Hutton, Ginzburg) |
| RenaissanceMagic      | `C:\Dev\renaissance magic`        | mage/magus/arcane/occult; Ficino, Agrippa |
| MedievalMagicDB       | `C:\Dev\MedievalMagicDB`          | conjure/necromancy/ritual; grimoire tradition |
| ChristianCabalaDB     | `C:\Dev\ChristianCabalaDB`        | divine names, sigil, hierophant |
| AgrippaDOP            | `C:\Dev\AgrippaDOP`               | *De Occulta Philosophia* — the occult-vocabulary source text |
| CrowleyDB             | `C:\Dev\CROWLEYDB`                | modern occult usage (invoke/evoke, magick) |
| Neoplatonism portal   | `C:\Dev\neoplatonism-portal`      | theurgy, divine, commune |
| GoetiaRevEng          | `C:\Dev\GoetiaRevEng`             | conjuration, summoning of spirits, sigils |
| OccultImgDB           | `C:\Dev\OCCULTIMGDB`              | visual glossary for site illustration |
| MagicalLatin          | `C:\Dev\MagicalLatin`             | Latin magical vocabulary, incantation formulae |

(Resolve any others via `C:\Dev\wiki\registry.md` → "esoteric portals" theme.)

---

## 5. Open scope questions (for Ted — see the question prompt)

1. **Corpus grain:** `oracle_cards` (~30k unique) — agreed default. Include tokens/emblems? (Default: no.)
2. **Morphology engine:** curated regex lexicon (control) vs NLP lemmatization (recall) vs both.
3. **Lexicon breadth:** stay tight on "magic proper," or widen to adjacent (religion, monsters,
   psychic/mind, alchemy, herblore)?
4. **Site depth:** static findings dashboard now, or build toward an interactive explorer + the
   etymology write-ups inline?
5. **Etymology sourcing:** is OED access available, or do we build on Etymonline/Wiktionary +
   Ted's DBs + web research?
6. **Episode-first vs atlas-first:** optimize output for producing podcast episodes one term at a
   time, or for a complete quantitative "atlas" first, episodes second?

Decisions get logged below as we make them.

## Decision log
- 2026-07-08 — Project bootstrapped. Pipeline + curated-lexicon approach chosen as the default
  spine; NLP lemmatization kept as an optional discovery aid.
- 2026-07-08 — **Ted's scope answers:**
  - **Lexicon breadth = TIGHT (magic proper).** Trim to unambiguously magical roots. Dropped
    religion-general terms (priest, ritual, sacrifice, hallow, profane) from the seed; kept divine
    *casters* (cleric) and the divination cluster (scry, augur, divine, prophesy, oracle, omen).
    Borderline calls noted here so they're easy to revisit.
  - **Rules vs flavor = SPLIT.** `analyze.py` now reports `oracle_total`/`flavor_total` separately
    per root (rules-keyword use vs natural-language use). The word-study foregrounds flavor text;
    rules-text counts shown alongside as the mechanical layer.
  - **Output = BOTH IN PARALLEL.** Ranked atlas + deep-dive template pages for 2–3 flagship terms
    (candidates: conjure, scry, necromancer). Flagship pages weave corpus stats + etymology.
  - **Etymology sources = Etymonline + Wiktionary + Ted's magic DBs + web research** (no OED).
    Classical lexica (Lewis&Short, LSJ, Bosworth–Toller) still fair game for roots.
  - Also: professions table now whitelists magic-user creature classes (was showing all subtypes
    incl. Human/Warrior).
- 2026-07-08 — **Scope expansion (Ted).** Core magic stays tight, but four themed sections added,
  each its own lexicon `category` + site section (71 roots total, all with ≥1 corpus hit):
  - **divination** (15) — scry, divine, augur, prophesy, oracle, seer, omen/portent, + the -mancy
    family (geomancy, astrology, haruspex, pyromancy, hydromancy, oneiromancy, chiromancy),
    sortilege, clairvoyance. (Divination cluster pulled out of `act`/`profession`.)
  - **alchemy** (8 matched) — alchemy, transmute, elixir, philosopher's-stone, quintessence,
    distill, calcine, putrefy, coagulate, tincture, vitriol, alembic, athanor, crucible, potion,
    nigredo/albedo/rubedo. Standouts: alchemy·26, potion·17.
  - **item** = *classical* magical items only (historical magic, not modern-fantasy coinage):
    talisman, amulet, periapt, phylactery, sigil, pentacle, rune, philter, poppet, fetish,
    mandrake, wand. (Explicitly excludes 20th-c. fantasy inventions.) Standouts: rune·19, sigil·19.
  - **book** = history-of-the-book terms (any word for a historical book): grimoire, tome, codex,
    scroll, manuscript, folio, almanac, bestiary, herbal, primer, compendium, treatise, breviary,
    psalter, missal, lexicon, formulary, palimpsest, testament. Standouts: scroll·21, tome·14.
  - Known-noise roots flagged in `lexicon.json` `_caveats` (herbal, testament, fetish, divine,
    phylactery). Phylactery is a *great* etymology beat: Greek amulet → D&D lich-vessel.
- 2026-07-08 — **Full website + term pages shipped.** Lexicon expanded to ~120 roots (added
  exorcism/theurgy/goetia/geas/glamour to acts, auspice/sibyl/haruspex family to divination,
  azoth/hermetic/spagyric to alchemy, cauldron/besom/reliquary/grail to items,
  incunabulum/chapbook/hornbook to books, numinous/chthonic/infernal to qualities). Built:
  `build_terms.py` (110 per-term detail files w/ flavor+mechanics snippets, morphology bars,
  name-match card galleries), `fetch_card_images.py` (1,684 Scryfall thumbnails cached to
  `site/img/`), `data/etymology.json` (~45 curated etymologies with a "podcast angle" each).
  Front-end rebuilt: hub (search/filter/sort grid), `term.html` (5 tabs), `atlas.html` (census),
  `insights.html` (log-log flavor-vs-rules scatter — the "word vs keyword" thesis visualized),
  `about.html`. Purpose: portfolio piece for Ted's MTG-content-creator coach. Verified in-browser.
  - **Next backlog:** (a) fill the ~65 pending etymologies; (b) 3–5 flagship long-form term essays
    (phylactery, scry, glamour/grimoire pair, alchemy, necromancer); (c) draft podcast episode 1
    from a flagship; (d) optional: by-era timeline + color-of-magic per term.
- 2026-07-08 — **Backlog cleared + visualization suite built (autonomous pass).**
  - (a) **All 110 etymologies written** — `data/etymology.json` (115 entries), each tagged with an
    origin `lang` (Latin 57, Greek 25, Old English 11, French 5, Arabic 4, Persian, Celtic, Old
    Norse, Germanic, Siberian, Unknown).
  - (b) **5 flagship essays** in `data/essays.json` (phylactery, scry, glamour, alchemy, necromancer),
    surfaced as an "Essay ✦" tab on those term pages.
  - (c) **Podcast** — `data/podcast.json`: episode 1 ("Glamour & Grimoire") full segmented script +
    episodes 2–5 outlines; rendered on `podcast.html`; working copy in `docs/podcast/`.
  - (d+) **Data enrichment**: `build_terms.py` now computes per-term colour identity (WUBRG) and
    first-printed year, and emits `timeline.json` + `colors.json` aggregates.
  - **New visualizations** (Charts hub + 5 pages): Insights (flavor↔rules scatter), **Loanword
    Atlas** (`origins.html` — magic-words by source language), **Color of Magic** (`colors.html` —
    the finding: divination 33% blue, books/items colorless), **Timeline** (`timeline.html` —
    stacked-area of family presence 1993–2026 w/ Absolute|Share toggle + debut lists), **Mosaic**
    (`mosaic.html` — treemap of all 110 terms). Term pages gained a colour-identity bar + first-year.
  - Verified in-browser via DOM (screenshot tool was flaky this session). Remaining ideas: gallery
    set/rarity/color filters; a term-comparison view; deploy.
- 2026-07-08 — **Pivot: podcast → cited "Word Histories" + a baked-in research method.**
  - Retired the podcast concept (deleted `podcast.html/json`, `docs/podcast/`). Reframed the deep
    pages as **Word Histories** (nav "Histories", `histories.html`, "Word History ✦" term-page tab).
  - **Research method baked into system files:** `docs/RESEARCH_METHOD.md` + `scripts/research.py`
    (registered in `CLAUDE.md`). The tool mines Ted's DBs (`renaissance magic\data\definitions.json`
    [139 cited entries] + KWIC concordance; `MedievalMagicDB\site\data.json`; `TheosophicalAlchemyDB`)
    and the `E:\pdf` full-text corpora (`magic\medieval magic`, `renaissance magic`,
    `alchemy\Markdown` incl. Lyndy Abraham) → `data/research/<slug>.json` dossiers.
  - Ran research for 15 flagship terms; the **Etymology tab now auto-surfaces the dossier** (DB
    definitions + cited corpus quotes) for any researched term.
  - Rewrote the Word Histories to cite real sources (Picatrix/Attrell-Porreca, Klaassen, Fanger,
    Bailey, Dee's Sigillum Dei Aemeth, RenaissanceMagicDB) with a **Sources & further reading** block;
    added corpus-grounded histories for **grimoire** and **talisman**.
  - **Next:** run `research.py` across the rest of the ~110 terms; write more histories from the
    dossiers; add page-level citations by opening the PDFs; deploy.
- 2026-07-08 — **Research run complete + histories doubled.** Ran `research.py` over the whole
  lexicon: **112/112 term pages now have a dossier** (`data/research/` + `site/data/research/`), so
  every Etymology tab auto-surfaces cited scholarship. Richest: mage (179 DB + 40 corpus), divine,
  diviner, occult, hermetic, transmute, astrology. Wrote **5 more Word Histories** grounded in the
  dossiers (theurgy, goetia, exorcism, conjure, pentacle) → **12 total**, each with a Sources block.
  `build_terms.py` now also emits a term page for a history-bearing word even at 0 card hits
  (theurgy, goetia — absent from the cards but worth a full etymology page; flagged "not in the card
  set" → **112 pages**). **Remaining:** more histories from the rich dossiers; page-level page
  numbers by opening the PDFs; deploy (run the build first — `site/data` + `site/img` are ignored).
- 2026-07-08 — **Historical timeline + LIVE DEPLOYMENT.**
  - **Timeline** (`site/timeline-history.html`, nav "Timeline"): 366 dated entries on the origin &
    development of magical words/texts/figures/traditions/practices, antiquity → the Scry keyword.
    Built by `build_history_timeline.py` from hand-authored `data/history_seed/*.json` (124 entries,
    7 era files) + word-origin/attestation entries auto-derived from `etymology.json` + MTG-debut
    points. Filters by kind (Words 195, Texts 63, Figures 21, Traditions 10, Practices 15, MTG 62),
    era spine, search, term-page links. Entry template: `docs/TIMELINE_TEMPLATE.md`. Disambiguated
    from the MTG stacked-area chart (`timeline.html` = "Vocabulary over Time (in Magic)").
  - **QA:** 0 dead links across 12 pages; all data files present; every viz page has an explanation.
  - **Deployed** to https://t3dy.github.io/MTG-Historical-Magic/ via GitHub Actions Pages
    (`.github/workflows/pages.yml`); `site/data` + `site/img` committed (34MB), `data/raw` +
    `cards.jsonl` ignored. Live-verified: homepage/data/dossiers/images all HTTP 200, 366 entries.
    README rewritten with live link + process/values/goals.
