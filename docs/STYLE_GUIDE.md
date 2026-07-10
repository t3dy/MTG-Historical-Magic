# The Vocabulary of Magic — Master Style Guide

This is the governing style guide for **every word on the site**. It is drawn from the goals and
values stated across the project's commissioning prompts, and it is binding on all content: term
definitions, term histories, flagship Word Histories, timeline entries, data-visualization
explanations, page introductions, and UI copy.

Per-content-type templates live in [`docs/templates/`](templates/). When they and this guide
disagree, **this guide wins**.

---

## 1. The thesis (what every page is arguing)

> **The magic on a Magic: The Gathering card has a genealogy worth knowing.** The words the game uses
> for magic — *wizard, conjure, scry, talisman, grimoire* — are fossils of five thousand years of
> real intellectual history. Taking them seriously is a way into that history.

Every piece of writing should, somewhere, serve that thesis: connect a game-word to its real past.

## 2. The two audiences

Write so that **both** can read every page with pleasure:

- **The Magic player / content creator** — knows the cards, the colours, the keywords; may know no
  history of magic. Never condescend; never assume they've read Yates.
- **The historian of magic / curious scholar** — knows Ficino from Agrippa; may know nothing about
  MTG. Never fake rigour; never let a claim stand unsourced that a scholar would challenge.

The bridge between them is the whole point. A good sentence teaches the player some history and shows
the scholar why the game is worth their attention.

## 3. Values (non-negotiable)

1. **Sourced, not vibes.** Every historical or etymological claim is dated and attributable. If you
   can't source it, hedge it explicitly ("perhaps," "the record is a dead end") or cut it.
2. **Ground in Ted's corpus first.** Use the research databases and PDF library (see
   [`RESEARCH_METHOD.md`](RESEARCH_METHOD.md)) before generic web knowledge. Run `research.py <slug>`
   and quote from the dossier. Cite the database (`RenaissanceMagicDB, s.v. necromantia`) or the work
   (`Klaassen, The Transformations of Magic`).
3. **Verify before quoting.** The research tool surfaces candidates; a human confirms. Never quote a
   passage you haven't seen in its source file. Discard the tool's off-topic (stem-collision) hits.
4. **Honesty about limits.** Distinguish established etymologies from contested ones. Flag words that
   never appear on a card ("not in the card set"). Say when a date is an estimate.
5. **The flavor/rules principle.** The project's core analytical finding: a word's use in *flavor
   text* (story) and *rules text* (mechanic) are different things. Never conflate a keyword with a
   word. *Spell* and *transmute* are mechanics; *mage* and *curse* are literary words.
6. **Morphology is meaning.** Treat a term as a lemma, not a string: *conjure/conjures/conjured/
   conjuration* are one word with a spread of forms. Show the spread; don't hide it.
7. **Historiographical reflexivity.** For terms whose modern *study* is itself contested, don't only
   narrate what the word meant — say **how scholars now argue about it**, and take the argument
   seriously. The categories are not neutral: *shamanism* is a Western universal imposed on diverse
   practices (Kehoe, Znamenski, Hutton); *alchemy* has been remade by the "new historiography" into
   *chymistry*, a serious protoscience, against the old spiritual/Jungian reading (Principe, Newman,
   Nummedal); *necromancy* names Kieckhefer's educated **clerical underworld**, not folk superstition;
   the *theurgy*/*goetia* line is a boundary the authorities *policed* (Fanger); the *witch* was a
   category made by prosecution (Cohn, Ginzburg); "Hermeticism" is the Yates thesis and its critics
   (Hanegraaff). This lives as a distinct **Historiographical note** (`data/historiography.json`,
   template in `templates/historiography_note.md`) — a scholarly aside, cited, that flags the debate.
   Draw framings from the databases, the PDF library, and Ted's own historiography discussions in
   `C:\Dev\megabase`. Never flatten a debate into a settled fact.

## 4. Voice & tone

- **Scholarly but warm.** The register of a great museum label or a good popular history — precise,
  confident, unstuffy. One clear idea per paragraph.
- **One argument per unit.** A definition defines; a history narrates one development; an essay makes
  one memorable point. Resist the urge to say everything.
- **Concrete and active.** "Medieval Latin reshaped *necromantia* into *nigromantia*," not "it is
  observed that a reshaping occurred."
- **Delight is allowed — earned delight.** The best entries turn on a real, surprising fact
  (*glamour* and *grimoire* are both "grammar"). Land the fact; don't manufacture drama with
  adjectives. No "mysterious," "dark arts" mood-lighting unless the source supports it.
- **Never breathless, never dry.** If a sentence sounds like ad copy ("unleash the arcane!"), cut it.
  If it sounds like a dissertation footnote, warm it up.

## 5. House conventions

- **Spelling:** **American English** (color, flavor, honor) — it matches Wizards of the Coast's own
  usage and the card text we quote. (Legacy British spellings in older files are being migrated.)
- **The term itself:** lowercase and *italic* in prose — *the sorcerer*, *to conjure*. Capitalize
  only a proper noun (the *Picatrix*, John Dee) or an MTG keyword named as such (the **Scry** keyword).
- **Titles of works:** *italic* (*The Transformations of Magic*, the *Corpus Hermeticum*).
- **Foreign/technical terms:** *italic* on first use with a gloss — *nekromanteia* ('corpse-divination').
- **Dashes:** em dash — no spaces in tight prose, thin spaces are fine visually. Use for the aside.
- **Dates:** `c.` for circa; `BCE/CE`; centuries as "the 14th century" in prose, "14c." in data.
- **MTG references:** name the mechanic in bold when introducing it (**Ward**, **Scry**); refer to
  colours by name (blue, not U) in prose, but WUBRG pips are fine in data displays.
- **Numbers:** spell out under ten in prose; numerals in data. The corpus size is **34,629 cards**.

## 6. Citations

- **Form:** *Author, Short Title* — e.g. *Fanger, Invoking Angels*. For a database: *RenaissanceMagicDB,
  s.v. goetia*. For etymology: *Etymonline, s.v. scry* (or OED / a classical lexicon).
- **How many:** 1–2 for a definition, 2–4 for a history, 3–6 for a flagship essay. Quality over
  quantity — this is popular scholarship, not a critical apparatus.
- **Page numbers:** the extracted PDF text has none; cite work-level, or open the PDF for the page.
- **Attribution passes through.** If a DB entry names Yates or Copenhaver, name them too.

## 7. What each content type is for (see the templates)

| Type | File | One-line job |
|------|------|--------------|
| **Term definition** | [`templates/term_definition.md`](templates/term_definition.md) | Say precisely what the word means, in 2–4 sentences. |
| **Term history** | [`templates/term_history.md`](templates/term_history.md) | Narrate the word's development in one tight paragraph, for *every* term. |
| **Historiographical note** | [`templates/historiography_note.md`](templates/historiography_note.md) | Flag how scholars *argue about* the term, for the contested ones. |
| **Word History (flagship)** | [`templates/word_history.md`](templates/word_history.md) | The deep, cited long-read for a marquee term. |
| **Timeline entry** | [`TIMELINE_TEMPLATE.md`](TIMELINE_TEMPLATE.md) | One dated, sourced point tying a word to a moment. |
| **Data-viz explainer** | [`templates/data_viz.md`](templates/data_viz.md) | Tell the reader what the chart shows and what to notice. |
| **Page intro / UI copy** | [`templates/page_intro.md`](templates/page_intro.md) | Orient the reader in one or two sentences. |

## 8. The definition-of-done for any writing

- [ ] Serves the thesis (connects the word to real history).
- [ ] Legible to both audiences.
- [ ] Every claim dated/sourced; nothing unverified quoted.
- [ ] Grounded in the corpus/databases where possible.
- [ ] House conventions followed (spelling, italics, dashes).
- [ ] One clear idea; no filler; no manufactured mood.
- [ ] Flags its own limits (contested? not in the card set? estimated date?).
