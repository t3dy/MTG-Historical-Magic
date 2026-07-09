# The Timeline Entry Template

The historical timeline (`site/timeline-history.html`, data in `data/history_seed/*.json`) is the
spine of this project: it shows the **origin and development of the vocabulary, traditions, and
practices of magic** across real history, from Bronze-Age divination to the day *Scry* became a
Magic: The Gathering keyword.

A good entry is where three commitments meet — and every entry should visibly serve all three:

1. **Scholarly rigour (Ted's values + the research corpus).** A real, sourced date; a claim you could
   defend; a citation to the literature or to one of the databases. No vibes-history.
2. **The corpus & databases.** Where possible, ground the entry in the medieval-/renaissance-magic
   and alchemy databases and the PDF library (Klaassen, Fanger, Yates, Couliano, the *Picatrix*,
   Lyndy Abraham, RenaissanceMagicDB…). Use `scripts/research.py` to find the support.
3. **The MTG project.** Tie the history back to *our* magical words — link the entry to a term page,
   and, when apt, note how the game inherited (or mangled) the idea.

## Schema

```json
{
  "year": -250,                     // integer sort key; BCE negative. Approximate is fine.
  "date": "3rd c. BCE",             // human display: "c. 1489", "late 14c.", "1st c. CE"
  "era": "Antiquity",               // Antiquity | Late Antiquity | Middle Ages | Renaissance |
                                    //   Early Modern | Modern | Contemporary
  "kind": "text",                   // word | text | figure | tradition | practice | game
  "title": "Theophrastus coins ‘characters’ of moral type",
  "term": "characteres",            // lexicon slug to link (or "" if none)
  "region": "Greece",              // Greece | Rome | Egypt | Persia | Islamic world |
                                    //   Byzantium | Latin Europe | England | Global | Multiplayer…
  "blurb": "Two or three sentences. What happened, why it matters for the words of magic.",
  "mtg": "Optional: how MTG inherits or echoes this (a card, a keyword, a colour).",
  "source": "Author, Short Title — or a database, e.g. RenaissanceMagicDB, s.v. characteres"
}
```

`kind` drives the icon/filter: **word** (a first attestation or coinage), **text** (a book/treatise),
**figure** (a person), **tradition** (a school or current), **practice** (a technique or rite),
**game** (an MTG milestone).

## A model entry

```json
{
  "year": 1489, "date": "1489", "era": "Renaissance", "kind": "text",
  "title": "Ficino’s De vita coelitus comparanda makes talisman-magic philosophy",
  "term": "talisman", "region": "Latin Europe",
  "blurb": "Marsilio Ficino’s third book of De vita turns the drawing-down of planetary spiritus into respectable Neoplatonic natural philosophy, giving the astral talisman an intellectual pedigree instead of a witch’s reputation.",
  "mtg": "Every ‘Talisman’ mana-rock is this idea in miniature: a made object that channels cosmic power into your hand.",
  "source": "Yates, Giordano Bruno and the Hermetic Tradition; Copenhaver — RenaissanceMagicDB, s.v. anima mundi"
}
```

## Authoring rules
- **Spread across eras and regions.** The reader should feel the transmission — Egypt → Greece →
  Rome → the Islamic world → Latin Europe → England → the gaming table.
- **Prefer entries that carry a `term`** so the timeline threads into the term pages.
- **Dates:** give the most defensible date; use a representative year for centuries (late 14c → 1390;
  1530s → 1535; 3rd c. BCE → −250). Round is honest when the record is round.
- **Cite.** Even a light citation (author + short title, or a database s.v.) is required; run
  `research.py <slug>` to find one in the corpus.
- **Batch by era** in `data/history_seed/NN_era.json`; `scripts/build_history_timeline.py` merges the
  seed files with the word-attestation entries auto-derived from `data/etymology.json`, dedupes,
  sorts, and writes `site/data/history_timeline.json`.

## Values encoded here
This template is the project's thesis in operational form: **the words of a fantasy game are fossils
of real intellectual history, and taking them seriously is a way into that history.** Each entry is a
small argument that the magic on a Magic card has a genealogy worth knowing — sourced, dated, and
linked back to the word it explains.
