# Template — Word History (flagship essay)

Governed by [`../STYLE_GUIDE.md`](../STYLE_GUIDE.md). Stored in `data/essays.json` under
`essays.<slug>`; shown as the **Word History ✦** tab and on `histories.html`. Reserved for marquee
terms whose story rewards 300–600 words.

## Job
The deep, cited long-read. Where a *term history* gives the one-paragraph arc, a Word History develops
it with evidence, texture, and a memorable through-line — the piece you'd read aloud to explain why
this project exists.

## Structure (`data/essays.json` fields)
- `title` — a headline with a claim, not a label: *"Glamour & grimoire: two spells from one grammar."*
- `dek` — one italic sentence that promises the payoff.
- `read_min` — honest estimate.
- `html` — 3–5 short paragraphs. Open on a hook (a card, a surprising fact); develop through the
  history with named sources woven in; close on the through-line and, lightly, the MTG landing.
- `sources` — 4–6 `{label, where}` entries, verified, corpus-first.

## Do
- **One controlling idea**, stated early and paid off at the end.
- Weave citations into the prose (*"as Klaassen shows in The Transformations of Magic…"*), don't
  bolt them on.
- Link to sibling term pages inline (`<a href="term.html?t=amulet">amulet</a>`).
- Earn every adjective. The delight comes from the *facts*.

## Don't
- Don't turn it into a listicle of everything known about the word.
- Don't repeat the definition/history verbatim — this is the expansion, with evidence.
- Don't overclaim: hedge contested points, and say when the game departs from the history.

See the shipped exemplars in `data/essays.json`: **glamour**, **phylactery**, **necromancer**,
**alchemy**, **talisman**, **grimoire**, **theurgy/goetia**.
