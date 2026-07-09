#!/usr/bin/env python3
"""Morphology-aware counting of magical vocabulary across the corpus.

Two counting surfaces, kept separate (see CLAUDE.md rule 3):
  * SUBTYPE counts  — canonical creature classes from the type line (Wizard, Shaman…).
  * TEXT counts     — lemma/variant hits in oracle_text and flavor_text (conjure, hex…).

Morphology strategy (layered, degrade gracefully):
  1. Curated lexicon (data/derived/lexicon.json) maps each ROOT to a regex that matches
     its inflections/derivations, e.g. conjure -> r"conjur(e|es|ed|ing|er|ers|ation|ations)?".
     This is the authoritative, reviewable layer — we *want* human control over what
     collapses into one lemma.
  2. If `nltk` is installed, we additionally lemmatize tokens as a discovery aid to
     surface roots not yet in the lexicon (printed as suggestions, never silently counted).

Outputs data/derived/counts.json:
  {
    "meta": {...},
    "subtypes": [{"subtype","count"} ...],
    "terms": [{"root","total","by_variant":{...},"in_oracle","in_flavor","example_cards":[...]}]
  }
"""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
CARDS = BASE / "data" / "derived" / "cards.jsonl"
LEXICON = BASE / "data" / "derived" / "lexicon.json"
OUT = BASE / "data" / "derived" / "counts.json"

WORD = re.compile(r"[A-Za-z][A-Za-z'-]*")


def load_cards():
    with CARDS.open(encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                yield json.loads(line)


def compile_lexicon(lex: dict) -> dict[str, re.Pattern]:
    """root -> compiled case-insensitive whole-word regex."""
    compiled = {}
    for root, spec in lex["roots"].items():
        pat = spec["pattern"] if isinstance(spec, dict) else spec
        compiled[root] = re.compile(rf"\b(?:{pat})\b", re.IGNORECASE)
    return compiled


def main() -> None:
    lex = json.loads(LEXICON.read_text(encoding="utf-8"))
    patterns = compile_lexicon(lex)

    magical_subtypes = set(lex.get("magical_subtypes", []))

    subtype_counts: Counter[str] = Counter()
    term_total: Counter[str] = Counter()
    oracle_total: Counter[str] = Counter()   # rules-text hits (mechanical layer)
    flavor_total: Counter[str] = Counter()   # flavor-text hits (natural-language layer)
    term_variant: dict[str, Counter[str]] = defaultdict(Counter)
    term_in_oracle: Counter[str] = Counter()
    term_in_flavor: Counter[str] = Counter()
    flavor_examples: dict[str, list[str]] = defaultdict(list)

    n = 0
    for card in load_cards():
        n += 1
        for st in card["subtypes"]:
            subtype_counts[st] += 1

        oracle = card["oracle_text"] or ""
        flavor = card["flavor_text"] or ""
        for root, rx in patterns.items():
            o_hits = rx.findall(oracle)
            f_hits = rx.findall(flavor)
            if not o_hits and not f_hits:
                continue
            for h in o_hits + f_hits:
                term_variant[root][h.lower()] += 1
            oracle_total[root] += len(o_hits)
            flavor_total[root] += len(f_hits)
            term_total[root] += len(o_hits) + len(f_hits)
            if o_hits:
                term_in_oracle[root] += 1
            if f_hits:
                term_in_flavor[root] += 1
            # Prefer flavor-text example cards — that's where the *word* lives, not the mechanic.
            if f_hits and len(flavor_examples[root]) < 8:
                flavor_examples[root].append(card["name"])

    result = {
        "meta": {
            "cards_analyzed": n,
            "lexicon_roots": len(patterns),
            "note": "professions = whitelisted magic-user creature classes; terms split oracle (rules) vs flavor (prose)",
        },
        # Whitelisted magic-user creature classes (Ted: professions table should be magic, not all subtypes).
        "magical_professions": [
            {"subtype": s, "count": subtype_counts[s]}
            for s in sorted(magical_subtypes, key=lambda s: subtype_counts[s], reverse=True)
            if subtype_counts[s] > 0
        ],
        # Full subtype census retained for reference / other studies.
        "subtypes": [
            {"subtype": s, "count": c}
            for s, c in subtype_counts.most_common()
        ],
        "terms": sorted(
            (
                {
                    "root": root,
                    "gloss": (lex["roots"][root].get("gloss", "") if isinstance(lex["roots"][root], dict) else ""),
                    "category": (lex["roots"][root].get("category", "") if isinstance(lex["roots"][root], dict) else ""),
                    "total": term_total[root],
                    "oracle_total": oracle_total[root],   # mechanical / rules-text uses
                    "flavor_total": flavor_total[root],   # natural-language / prose uses
                    "by_variant": dict(term_variant[root].most_common()),
                    "in_oracle_cards": term_in_oracle[root],
                    "in_flavor_cards": term_in_flavor[root],
                    "flavor_example_cards": flavor_examples[root],
                }
                for root in patterns
                if term_total[root] > 0
            ),
            # Rank by flavor (natural-language) use — the linguistic signal Ted cares about.
            key=lambda d: (d["flavor_total"], d["total"]),
            reverse=True,
        ),
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[analyze] {n} cards | {len(result['magical_professions'])} magic professions | "
          f"{len(result['terms'])} matched roots -> {OUT}")


if __name__ == "__main__":
    main()
