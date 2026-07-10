# Template — Term History

Governed by [`../STYLE_GUIDE.md`](../STYLE_GUIDE.md). Stored in `data/definitions.json` under
`terms.<slug>.history` (+ `terms.<slug>.sources`); shown in the **History** section of the term's
page, above the etymology detail and the auto-surfaced scholarship dossier.

This is the workhorse: **every one of the ~112 terms gets a history**, whether or not it also has a
flagship Word History essay. Where a flagship exists, this is the short version and may point to it.

## Job
Narrate, in **one tight paragraph**, how the word came to mean what it means — its origin, the key
turn(s) in its sense, and (where apt) how it reaches the card. Not a full essay; the single most
interesting true arc, told once.

## Shape
1 paragraph, ~70–130 words. Structure the arc:

1. **Root** — the origin language and literal sense (draw from `data/etymology.json`).
2. **Turn** — the pivotal development: a sense-shift, a transmission (Greek → Arabic → Latin), a text
   or figure that fixed the meaning, a folk-etymology, a coinage. This is the paragraph's spine.
3. **Landing** — where it ends up, and (optionally, one clause) how MTG uses it.

## Sourcing
2–4 citations in the `sources` array (`{label, where, url?, url_kind?, abstract}`), drawn from the
term's research dossier (`data/research/<slug>.json`) and `etymology.json`. **Verify each against
its source before using.** Prefer the corpus: Klaassen, Fanger, Yates, the *Picatrix*, Lyndy Abraham,
RenaissanceMagicDB, etc. Every non-database work needs a verified reader-facing link (publisher/
journal/DOI, or a library catalog as fallback) and a short plain-language abstract — see
`STYLE_GUIDE.md` §6. `where` is internal provenance only, never shown to the reader as "(PDF)."

## Do
- Give the paragraph **one turn** — the moment the word became interesting. Cut the rest.
- Use the dossier: if RenaissanceMagicDB defines the Latin form (*necromantia*, *sigillum*), lean on it.
- End with a concrete landing, not a summary sentence.
- If you name a modern scholar in the prose, give their claim enough context to stand without their
  name (Value 8) — e.g. "one historian traces the shift to..." rather than a bare surname.

## Don't
- Don't recap the definition — assume the reader just read it.
- Don't chain three developments; pick the one that matters.
- Don't invent a citation. If the dossier is thin, cite only Etymonline/the lexica and keep the arc
  to what they support.
- Don't drop a scholar's name into the prose as if their reputation alone explains the point.

## Worked example — *necromancer*
> To a Greek, *nekromanteia* was **corpse-divination** — summoning the dead to *ask* them, as Odysseus
> does in the Odyssey — and it belonged with augury and scrying, not with armies of the dead. The turn
> came in medieval Latin, which reshaped *necromantia* into *nigromantia*, as if from *niger*, 'black':
> death-divination was folk-etymologized into 'the black arts,' and once the word meant black magic in
> general its link to the dead loosened. Magic: The Gathering inherits the later sense wholesale — its
> necromancers reanimate — but the older meaning turns on a single mistaken vowel.

*Sources:* RenaissanceMagicDB, s.v. necromantia · Klaassen, *The Transformations of Magic* (linked to
its publisher page, with an abstract) · Etymonline, s.v. necromancy.
