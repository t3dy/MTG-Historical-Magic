#!/usr/bin/env python3
"""Aggregate every work cited across the site's writing into a bibliography.

Scans data/definitions.json (per-term def+history sources) and data/essays.json
(flagship Word Histories), normalizes each citation to its underlying work, counts
how many term pages cite it, and groups by corpus. Writes site/data/bibliography.json
for bibliography.html.
"""
from __future__ import annotations
import json, re
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DEFS = BASE / "data" / "definitions.json"
ESSAYS = BASE / "data" / "essays.json"
OUT = BASE / "site" / "data" / "bibliography.json"

DBS = ("RenaissanceMagicDB", "MedievalMagicDB", "TheosophicalAlchemyDB")

GROUPS = [
    ("databases", "The databases", "Structured, cited term-databases queried by scripts/research.py"),
    ("Medieval magic (PDF)", "Medieval magic — the PDF library", "Full-text scholarship on medieval learned magic"),
    ("Renaissance magic (PDF)", "Renaissance magic — the PDF library", "Full-text scholarship on Renaissance & early-modern magic"),
    ("Alchemy (PDF)", "Alchemy — the PDF library", "The alchemy corpus, incl. Lyndy Abraham's Dictionary of Alchemical Imagery"),
    ("etymology", "Etymological & lexical references", "Etymonline, the OED, and the classical lexica"),
    ("Reference", "Further reference", "Standard scholarly works consulted alongside the corpus"),
]


def normalize(label: str) -> str:
    l = label.strip()
    l = re.sub(r"\s*\([^)]*\)\s*$", "", l).strip()          # trailing (note)
    for db in DBS:
        if l.startswith(db):
            return db
    l = re.sub(r",?\s*s\.vv?\..*$", "", l, flags=re.I).strip()  # ", s.v. wizard"
    low = l.lower()
    if low.startswith("etymonline"):
        return "Etymonline (Douglas Harper)"
    if "bosworth" in low:
        return "Bosworth–Toller, An Anglo-Saxon Dictionary"
    if "liddell" in low or l == "LSJ" or "scott-jones" in low or "scott–jones" in low:
        return "Liddell–Scott–Jones, A Greek–English Lexicon"
    if "classical lexica" in low:
        return "Classical lexica (Lewis & Short; LSJ; Bosworth–Toller)"
    return l


def group_of(work: str, where: str) -> str:
    if work in DBS:
        return "databases"
    low = work.lower()
    if work.startswith(("Etymonline", "Bosworth", "Liddell", "Classical lexica")) or where == "Etymology reference":
        return "etymology"
    if where in ("Medieval magic (PDF)", "Renaissance magic (PDF)", "Alchemy (PDF)"):
        return where
    return "Reference"


def main() -> None:
    # work -> {"group":.., "cites": set(of page-ids), "wheres": Counter}
    works: dict[str, dict] = {}
    total_citations = 0

    def add(label, where, page):
        nonlocal total_citations
        w = normalize(label)
        low = w.lower()
        # skip self-references (the MTG corpus / this project are not bibliography works)
        if not w or where == "Corpus" or "the corpus" in low or "this project" in low:
            return
        total_citations += 1
        g = group_of(w, where)
        e = works.setdefault(w, {"group": g, "cites": set()})
        # databases/etymology stay in their fixed group; PDF works keep first PDF group
        if e["group"] == "Reference" and g != "Reference":
            e["group"] = g
        e["cites"].add(page)

    defs = json.loads(DEFS.read_text(encoding="utf-8")).get("terms", {})
    for slug, t in defs.items():
        for s in t.get("sources", []):
            add(s.get("label", ""), s.get("where", ""), slug)
    essays = json.loads(ESSAYS.read_text(encoding="utf-8")).get("essays", {})
    for slug, t in essays.items():
        for s in t.get("sources", []):
            add(s.get("label", ""), s.get("where", ""), slug + "·essay")
    histo_path = BASE / "data" / "historiography.json"
    if histo_path.exists():
        histo = json.loads(histo_path.read_text(encoding="utf-8")).get("terms", {})
        for slug, t in histo.items():
            for s in t.get("sources", []):
                add(s.get("label", ""), s.get("where", ""), slug + "·histo")

    out_groups = []
    for key, title, sub in GROUPS:
        items = [{"work": w, "count": len(e["cites"]),
                  "terms": sorted({p.replace("·essay", "") for p in e["cites"]})}
                 for w, e in works.items() if e["group"] == key]
        items.sort(key=lambda x: (-x["count"], x["work"].lower()))
        if items:
            out_groups.append({"key": key, "title": title, "sub": sub,
                               "count": len(items), "items": items})

    OUT.write_text(json.dumps({
        "total_works": len(works),
        "total_citations": total_citations,
        "groups": out_groups,
        "note": "Aggregated from the sources cited on the term pages and Word Histories. "
                "Databases collapse their many s.v. citations into one entry.",
    }, ensure_ascii=False), encoding="utf-8")
    print(f"[bibliography] {len(works)} works, {total_citations} citations, "
          f"{len(out_groups)} groups -> {OUT}")
    for g in out_groups:
        print(f"  {g['title']}: {g['count']} works (top: {g['items'][0]['work'][:40]} ×{g['items'][0]['count']})")


if __name__ == "__main__":
    main()
