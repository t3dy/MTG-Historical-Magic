#!/usr/bin/env python3
"""Build per-term detail JSON for the website term pages.

For every lexicon root with at least one corpus hit OR one title-match card, emit
site/data/terms/<slug>.json with everything a term page needs:
  - gloss, category, etymology (from data/etymology.json)
  - stats: flavor_total, oracle_total, card counts, variant breakdown
  - flavor_snippets / mechanics_snippets: real passages with the term <mark>-highlighted
  - cards: every card with the term in its NAME (for the image gallery), rarity-sorted
  - is_keyword: whether the root doubles as an MTG rules keyword
  - thumb: a representative art crop for the hub card

Also writes site/data/terms_index.json (the hub grid) and copies etymology.json through.
"""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from html import escape
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
CARDS = BASE / "data" / "derived" / "cards.jsonl"
LEXICON = BASE / "data" / "derived" / "lexicon.json"
ETYM = BASE / "data" / "etymology.json"
ESSAYS = BASE / "data" / "essays.json"
DEFS = BASE / "data" / "definitions.json"
HISTORIOG = BASE / "data" / "historiography.json"
OUT_DIR = BASE / "site" / "data" / "terms"

# Roots that also function as Magic rules keywords / keyword actions.
KEYWORD_ROOTS = {"scry", "ward", "transmute", "conjure", "enchant", "haunt", "bewitch", "cascade"}

RARITY_RANK = {"mythic": 0, "rare": 1, "special": 2, "uncommon": 3, "common": 4, "bonus": 5, "": 6}
MAX_CARDS = 250         # title-match cards kept per term (gallery); only a few terms exceed ~80
MAX_FLAVOR = 14
MAX_MECH = 8


def load_cards():
    with CARDS.open(encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                yield json.loads(line)


def compile_lexicon(lex: dict) -> dict[str, re.Pattern]:
    out = {}
    for root, spec in lex["roots"].items():
        pat = spec["pattern"] if isinstance(spec, dict) else spec
        out[root] = re.compile(rf"\b(?:{pat})\b", re.IGNORECASE)
    return out


def highlight(text: str, rx: re.Pattern) -> str:
    """HTML-escape text and wrap regex matches in <mark>."""
    out, i = [], 0
    for m in rx.finditer(text):
        out.append(escape(text[i:m.start()]))
        out.append(f"<mark>{escape(m.group(0))}</mark>")
        i = m.end()
    out.append(escape(text[i:]))
    return "".join(out)


def first_sentence_with(text: str, rx: re.Pattern) -> str:
    """Return the flavor line/sentence containing the first match (whole text if short)."""
    text = text.strip()
    if len(text) <= 240:
        return text
    # Prefer the line, else the sentence, around the first match.
    m = rx.search(text)
    if not m:
        return text[:240]
    start = text.rfind("\n", 0, m.start()) + 1
    end = text.find("\n", m.end())
    if end == -1:
        end = len(text)
    seg = text[start:end].strip()
    return seg if seg else text[:240]


def main() -> None:
    lex = json.loads(LEXICON.read_text(encoding="utf-8"))
    patterns = compile_lexicon(lex)
    cat_of = {r: (s.get("category", "") if isinstance(s, dict) else "") for r, s in lex["roots"].items()}
    etym = json.loads(ETYM.read_text(encoding="utf-8"))
    etym_terms = etym.get("terms", {})
    essays = json.loads(ESSAYS.read_text(encoding="utf-8")).get("essays", {}) if ESSAYS.exists() else {}
    defs = json.loads(DEFS.read_text(encoding="utf-8")).get("terms", {}) if DEFS.exists() else {}
    histo = json.loads(HISTORIOG.read_text(encoding="utf-8")).get("terms", {}) if HISTORIOG.exists() else {}
    research_dir = BASE / "data" / "research"
    researched = {p.stem for p in research_dir.glob("*.json")} if research_dir.exists() else set()

    # Per-root accumulators
    variant: dict[str, Counter] = defaultdict(Counter)
    o_total: Counter = Counter()
    f_total: Counter = Counter()
    in_o: Counter = Counter()
    in_f: Counter = Counter()
    name_cards: dict[str, list] = defaultdict(list)
    flavor_snips: dict[str, list] = defaultdict(list)
    mech_snips: dict[str, list] = defaultdict(list)
    thumb: dict[str, dict] = {}
    color_dist: dict[str, Counter] = defaultdict(Counter)   # root -> WUBRG(C) over matching cards
    year_ct: dict[str, Counter] = defaultdict(Counter)      # root -> year -> matching cards
    # aggregates
    cat_year: dict[str, Counter] = defaultdict(Counter)     # category -> year -> distinct cards using it
    cat_color: dict[str, Counter] = defaultdict(Counter)    # category -> WUBRG(C)
    year_total: Counter = Counter()

    n = 0
    for card in load_cards():
        n += 1
        name = card["name"]
        oracle = card["oracle_text"] or ""
        flavor = card["flavor_text"] or ""
        img = card.get("img", {}) or {}
        year = (card.get("released_at") or "")[:4]
        cols = card.get("colors") or ["C"]
        if year:
            year_total[year] += 1
        cats_hit: set[str] = set()
        for root, rx in patterns.items():
            name_hit = rx.search(name)
            o_hits = rx.findall(oracle)
            f_hits = rx.findall(flavor)
            if not (name_hit or o_hits or f_hits):
                continue
            for col in cols:
                color_dist[root][col] += 1
            if year:
                year_ct[root][year] += 1
            cats_hit.add(cat_of.get(root, ""))
            for h in o_hits + f_hits:
                variant[root][h.lower()] += 1
            o_total[root] += len(o_hits)
            f_total[root] += len(f_hits)
            if o_hits:
                in_o[root] += 1
            if f_hits:
                in_f[root] += 1
            if name_hit and len(name_cards[root]) < MAX_CARDS:
                slug = root
                name_cards[root].append({
                    "id": card["id"],
                    "name": name,
                    "set": card["set"].upper(),
                    "set_name": card.get("set_name", ""),
                    "released": card.get("released_at", ""),
                    "type_line": card["type_line"],
                    "rarity": card["rarity"],
                    "colors": card["colors"],
                    "img_small": img.get("small", ""),
                    "img_normal": img.get("normal", ""),
                    "scryfall_uri": card.get("scryfall_uri", ""),
                    "local": f"img/{slug}/{card['id']}.jpg",
                })
            if f_hits and len(flavor_snips[root]) < MAX_FLAVOR:
                seg = first_sentence_with(flavor, rx)
                flavor_snips[root].append({
                    "card": name, "set": card["set"].upper(),
                    "html": highlight(seg, rx),
                    "art": img.get("art_crop", ""),
                })
            if o_hits and len(mech_snips[root]) < MAX_MECH:
                seg = first_sentence_with(oracle, rx)
                mech_snips[root].append({
                    "card": name, "set": card["set"].upper(),
                    "html": highlight(seg, rx),
                })
            # Representative thumbnail: first name-match wins, else first card seen.
            if root not in thumb and (name_hit or img.get("art_crop")):
                thumb[root] = {"art": img.get("art_crop", ""), "small": img.get("small", ""), "card": name}
        # category aggregates (once per category per card)
        for c in cats_hit:
            if year:
                cat_year[c][year] += 1
            for col in cols:
                cat_color[c][col] += 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    # Clear stale term files.
    for old in OUT_DIR.glob("*.json"):
        old.unlink()

    index = []
    for root, spec in lex["roots"].items():
        f, o = f_total[root], o_total[root]
        ncards = len(name_cards[root])
        # Generate a page for any term with corpus presence, OR one that carries a Word History
        # (e.g. theurgy/goetia — magical words absent from the cards but worth a full etymology page).
        if f == 0 and o == 0 and ncards == 0 and root not in essays:
            continue
        # Chronological: earliest sets first, cards within a set grouped and alphabetized.
        cards = sorted(name_cards[root],
                       key=lambda c: (c.get("released") or "9999", c["set"], c["name"]))
        years = sorted(year_ct[root])
        first_year = int(years[0]) if years else None
        ety = etym_terms.get(root)
        d = defs.get(root, {})
        detail = {
            "slug": root,
            "root": root,
            "category": spec.get("category", ""),
            "gloss": spec.get("gloss", ""),
            "definition": d.get("definition"),
            "history": d.get("history"),
            "def_sources": d.get("sources", []),
            "commentary": histo.get(root, {}).get("commentary"),
            "commentary_sources": histo.get(root, {}).get("sources", []),
            "is_keyword": root in KEYWORD_ROOTS,
            "etymology": ety,
            "essay": essays.get(root),
            "sources": etym.get("_default_sources", []),
            "stats": {
                "flavor_total": f,
                "oracle_total": o,
                "in_flavor_cards": in_f[root],
                "in_oracle_cards": in_o[root],
                "name_match_count": ncards,
                "by_variant": dict(variant[root].most_common()),
                "first_year": first_year,
                "colors": dict(color_dist[root]),
                "by_year": {y: year_ct[root][y] for y in years},
            },
            "cards": cards,
            "flavor_snippets": flavor_snips[root],
            "mechanics_snippets": mech_snips[root],
            "thumb": thumb.get(root, {}),
        }
        (OUT_DIR / f"{root}.json").write_text(json.dumps(detail, ensure_ascii=False), encoding="utf-8")
        index.append({
            "slug": root, "root": root, "category": spec.get("category", ""),
            "gloss": spec.get("gloss", ""), "flavor_total": f, "oracle_total": o,
            "name_match_count": ncards, "is_keyword": root in KEYWORD_ROOTS,
            "has_etym": root in etym_terms,
            "has_essay": root in essays,
            "has_def": root in defs,
            "has_commentary": root in histo,
            "has_research": root in researched,
            "lang": (ety or {}).get("lang", ""),
            "first_year": first_year,
            "colors": dict(color_dist[root]),
            "thumb": thumb.get(root, {}).get("art", "") or thumb.get(root, {}).get("small", ""),
        })

    index.sort(key=lambda d: (d["flavor_total"] + d["name_match_count"]), reverse=True)
    (OUT_DIR.parent / "terms_index.json").write_text(
        json.dumps({"count": len(index), "terms": index}, ensure_ascii=False), encoding="utf-8")
    # Pass etymology + word-history (essays) data through for client use.
    (OUT_DIR.parent / "etymology.json").write_text(json.dumps(etym, ensure_ascii=False), encoding="utf-8")
    if ESSAYS.exists():
        (OUT_DIR.parent / "essays.json").write_text(ESSAYS.read_text(encoding="utf-8"), encoding="utf-8")

    # ---- aggregate: timeline (magic-vocabulary presence by category & year) ----
    all_years = sorted(y for y in year_total if y.isdigit())
    timeline = {
        "years": all_years,
        "totals": {y: year_total[y] for y in all_years},
        "categories": {c: {y: cat_year[c][y] for y in all_years} for c in cat_year},
    }
    (OUT_DIR.parent / "timeline.json").write_text(json.dumps(timeline, ensure_ascii=False), encoding="utf-8")

    # ---- aggregate: color identity by category ----
    colors = {"byCategory": {c: dict(cat_color[c]) for c in cat_color},
              "note": "WUBRG(+C) counts over distinct cards whose name/text uses any term in the family"}
    (OUT_DIR.parent / "colors.json").write_text(json.dumps(colors, ensure_ascii=False), encoding="utf-8")

    print(f"[build_terms] {n} cards | {len(index)} term pages | "
          f"images referenced: {sum(len(v) for v in name_cards.values())} | "
          f"timeline {len(all_years)}y | colors {len(cat_color)} cats")


if __name__ == "__main__":
    main()
