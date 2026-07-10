# Template — Historiographical Note

Governed by [`../STYLE_GUIDE.md`](../STYLE_GUIDE.md), value 7 (historiographical reflexivity) and
value 8 (every named scholar earns their name). Stored in `data/historiography.json` under
`terms.<slug>.{commentary, sources}`; rendered as a distinct **Historiographical note** section on
the term's page, flagged with a ⚑ badge.

## Job
Not "what the word meant" (that is the *history*) but **how scholars now argue about it**. For terms
whose modern study is itself a live debate, write one short, cited paragraph that names the debate,
the old view it overturned or complicates, and what the field now stresses — and takes the argument
seriously as an argument, not a fact.

## When to write one
Only for terms with a genuine, nameable historiographical problem. Reach for it when the entry touches
one of Ted's standing interests (or an equivalent):
- the **problematics of "shamanism"** as a universal category in anthropology;
- the **new historiography of alchemy** — "chymistry," and the fall of the exoteric/spiritual split;
- Kieckhefer's **clerical necromantic underworld**;
- **Fanger** on angel-magic-as-theurgy, and the policed theurgy/goetia line;
- the **witch-cult debate** (Murray → Cohn → Ginzburg → the microhistorical turn);
- the **Yates thesis** on Hermeticism and its critics;
- "**Western esotericism**"/"the occult" as recently-constructed scholarly categories.

If a term has no such debate, it gets no note — don't manufacture controversy.

## Shape
1 paragraph, ~60–110 words, in `commentary`. Structure: **the old view → the turn → what the field
now stresses**. Italicize *terms* and *titles*; American spelling; the same scholarly-but-warm voice,
a shade more meta.

## Naming scholars (Value 8)
A historiographical note is the highest-risk content type for "inside baseball," because its whole
job is to summarize a scholarly argument. Every named scholar must pass the test: **could a curious
reader who has never heard of them follow the sentence and learn something true?**
- Lead with the *finding or argument*, not the name — "modern scholarship treats X as..." often works
  better than "Scholar Y treats X as..." The name is a citation, not the subject.
- When a name does earn its place (because the note is specifically about a turn *this person*
  caused), give it a one-clause tag: "the anthropologist Alice Kehoe," "Ronald Hutton, historian of
  the Romantic Druid revival" — not a bare surname doing unexplained work.
- **Don't:** "...whom Paola Zambelli's sources still gloss with the old commonplace that *magus*
  simply 'means wise man in Persian.'"
- **Do:** "...though many older sources repeat, uncritically, the old claim that *magus* simply
  'means wise man in Persian' — a folk etymology more than a fact."

## Sourcing
2–3 works in `sources` ({label, where, url?, url_kind?, abstract}), the actual historians of the
debate — Principe, Newman, Nummedal, Kieckhefer, Fanger, Cohn, Ginzburg, Hanegraaff, Kehoe,
Znamenski, Hutton. Verify against the corpus where present. Every work needs a verified link
(publisher/journal/DOI, or a library-catalog record as fallback — never invent one) and a
plain-language abstract; see `STYLE_GUIDE.md` §6. `where` stays as internal provenance metadata
only — it is never shown to the reader as "(PDF)" or similar.

## Do
- Take a side only as far as the scholarship does; represent the debate, don't resolve it by fiat.
- Let it complicate the history above it — the note earns its place by unsettling a too-clean story.
- Ground framings in the databases, the PDF library, and Ted's `C:\Dev\megabase` discussions.
- Make every name pass the Value 8 test above.

## Don't
- Don't repeat the history or the definition.
- Don't turn it into a reading list; name 2–3 key interventions and their point.
- Don't flatten ("scholars agree…") — the value of the note is that they *don't*.
- Don't drop a surname on the reader without a clause of context or a legible claim attached.

## Worked example — *shaman*
> 'Shaman' is a genuine Tungusic word (Evenki *šamán*), but *shamanism* — the universal category — is
> largely a Western construction. From Mircea Eliade onward, anthropology stretched a specific Siberian
> office to cover every trance-specialist on earth, and critics such as Alice Kehoe and Andrei Znamenski
> have shown how much that flattening owes to Romantic primitivism and a Cold-War appetite for a single
> 'archaic technique of ecstasy.' The word names something precise; the *-ism* names a scholarly habit
> worth distrusting.
