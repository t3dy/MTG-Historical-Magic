#!/usr/bin/env python3
"""Build the historical timeline of magical terms.

Merges the hand-authored seed (data/history_seed/*.json) with entries auto-derived from
data/etymology.json (each term's classical ORIGIN + its English ATTESTATION) and from the
MTG corpus (each prominent term's DEBUT in the card set), then dedupes, sorts, and writes
site/data/history_timeline.json for timeline-history.html.

See docs/TIMELINE_TEMPLATE.md for the entry schema.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
SEED_DIR = BASE / "data" / "history_seed"
ETYM = BASE / "data" / "etymology.json"
LEXICON = BASE / "data" / "derived" / "lexicon.json"
IDX = BASE / "site" / "data" / "terms_index.json"
OUT = BASE / "site" / "data" / "history_timeline.json"

ERA_ORDER = ["Antiquity", "Late Antiquity", "Early Medieval", "Middle Ages",
             "Renaissance", "Early Modern", "Modern", "Contemporary"]

LANG_ORIGIN = {  # language -> (representative year, region)
    "Greek": (-400, "Greece"), "Latin": (50, "Rome"), "Arabic": (850, "Islamic world"),
    "Persian": (-550, "Persia"), "Old English": (950, "England"), "Old Norse": (1000, "Scandinavia"),
    "French": (1250, "France"), "Germanic": (1150, "Germany"), "Celtic": (-300, "Ireland"),
    "Siberian": (1690, "Siberia"), "Hebrew": (-200, "Judea"),
}


def era_of(year: int) -> str:
    if year < 300: return "Antiquity"
    if year < 600: return "Late Antiquity"
    if year < 1100: return "Early Medieval"
    if year < 1450: return "Middle Ages"
    if year < 1600: return "Renaissance"
    if year < 1800: return "Early Modern"
    if year < 1970: return "Modern"
    return "Contemporary"


def parse_first(s: str):
    """Parse an attestation string like 'c. 1440', 'late 14c.', 'before 1000' -> year int."""
    if not s:
        return None
    s = s.strip()
    # explicit 4-digit year (take the first; ranges use the earliest)
    m = re.search(r"\b(1\d{3}|20\d{2})\b", s)
    if m:
        y = int(m.group(1))
        if re.search(r"\b" + m.group(1) + r"s\b", s):  # "1530s" -> mid-decade
            y += 5
        return y
    # "before 900/1000/1050"
    m = re.search(r"before\s+(\d{3,4})", s, re.I)
    if m:
        return int(m.group(1))
    # centuries: "late 14c." / "mid-14c." / "early 15c." / "13th c."
    m = re.search(r"(early|mid|late)?[- ]?(\d{1,2})(?:th|st|nd|rd)?\s*c", s, re.I)
    if m:
        c = int(m.group(2))
        base = (c - 1) * 100
        mod = (m.group(1) or "").lower()
        return base + (25 if mod == "early" else 75 if mod == "late" else 50)
    return None


def load_seed():
    out = []
    for f in sorted(SEED_DIR.glob("*.json")):
        out.extend(json.loads(f.read_text(encoding="utf-8")))
    return out


def main() -> None:
    seed = load_seed()
    etym = json.loads(ETYM.read_text(encoding="utf-8")).get("terms", {})
    lex = json.loads(LEXICON.read_text(encoding="utf-8"))["roots"]
    idx = {t["slug"]: t for t in json.loads(IDX.read_text(encoding="utf-8"))["terms"]}

    entries = list(seed)

    # 1) origin + attestation entries from etymology
    for slug, e in etym.items():
        cat = lex.get(slug, {}).get("category", "") if isinstance(lex.get(slug), dict) else ""
        lang = e.get("lang", "")
        # ORIGIN
        if lang in LANG_ORIGIN:
            oy, region = LANG_ORIGIN[lang]
            entries.append({
                "year": oy, "date": f"{lang} roots", "era": era_of(oy), "kind": "word",
                "title": f"‘{slug}’ — {lang} origin", "term": slug, "region": region,
                "blurb": e.get("origin", "") + (f" {e.get('note','')}" if e.get("note") else ""),
                "source": "data/etymology.json; Etymonline",
            })
        # ATTESTATION (English)
        y = parse_first(e.get("first", ""))
        if y is not None:
            entries.append({
                "year": y, "date": e.get("first", str(y)), "era": era_of(y), "kind": "word",
                "title": f"‘{slug}’ enters English", "term": slug, "region": "England",
                "blurb": (e.get("hook") or e.get("note") or "First English attestation.")[:220],
                "source": "data/etymology.json; Etymonline / OED",
            })

    # 2) MTG debut entries for prominent terms
    for slug, t in idx.items():
        fy = t.get("first_year")
        if not fy or t.get("name_match_count", 0) < 8:
            continue
        entries.append({
            "year": fy, "date": str(fy), "era": era_of(fy), "kind": "game",
            "title": f"‘{slug}’ in the card set", "term": slug, "region": "Multiplayer",
            "blurb": f"The word appears on Magic cards from {fy}; it now titles "
                     f"{t['name_match_count']} cards and shows in {t['flavor_total']} flavor texts.",
            "source": "the corpus (Scryfall bulk data)",
        })

    # dedupe by (title, year), keeping the first (seed wins over generated)
    seen, deduped = set(), []
    for en in entries:
        key = (en["title"].lower(), en["year"])
        if key in seen:
            continue
        seen.add(key)
        # attach whether the term has a page
        en["has_page"] = bool(en.get("term")) and en["term"] in idx
        deduped.append(en)

    deduped.sort(key=lambda e: (e["year"], ERA_ORDER.index(e["era"]) if e["era"] in ERA_ORDER else 99))
    for i, en in enumerate(deduped):
        en["id"] = i

    by_era = {}
    by_kind = {}
    for e in deduped:
        by_era[e["era"]] = by_era.get(e["era"], 0) + 1
        by_kind[e["kind"]] = by_kind.get(e["kind"], 0) + 1

    OUT.write_text(json.dumps({
        "count": len(deduped),
        "eras": [x for x in ERA_ORDER if x in by_era],
        "by_era": by_era, "by_kind": by_kind,
        "entries": deduped,
    }, ensure_ascii=False), encoding="utf-8")
    print(f"[history] {len(deduped)} entries ({len(seed)} seed + generated) -> {OUT}")
    print("  by era:", {k: by_era[k] for k in ERA_ORDER if k in by_era})
    print("  by kind:", by_kind)


if __name__ == "__main__":
    main()
