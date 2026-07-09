#!/usr/bin/env python3
"""Merge agent-drafted definition batches into data/definitions.json.

Each file in data/_agent_out/*.json is a {slug: {definition, history, sources}} map.
Existing entries are preserved unless --overwrite. Validates shape and reports.
"""
from __future__ import annotations
import json, sys, glob
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DEFS = BASE / "data" / "definitions.json"
OUT_DIR = BASE / "data" / "_agent_out"

WHERE_OK = {"RenaissanceMagicDB", "MedievalMagicDB", "Medieval magic (PDF)",
            "Renaissance magic (PDF)", "Alchemy (PDF)", "Etymology reference",
            "Classical lexica", "Reference", "Corpus"}


def main(overwrite=False):
    doc = json.loads(DEFS.read_text(encoding="utf-8"))
    terms = doc["terms"]
    added, skipped, bad = [], [], []
    for f in sorted(glob.glob(str(OUT_DIR / "*.json"))):
        batch = json.loads(Path(f).read_text(encoding="utf-8"))
        for slug, e in batch.items():
            if not isinstance(e, dict) or not e.get("definition") or not e.get("history"):
                bad.append(f"{slug} (missing fields)"); continue
            if slug in terms and not overwrite:
                skipped.append(slug); continue
            srcs = []
            for s in e.get("sources", []):
                if not isinstance(s, dict):
                    continue
                lab = (s.get("label") or "").strip()
                if not lab or lab in WHERE_OK:   # drop bare category-name placeholders
                    continue
                if lab == "Etymology reference":
                    lab = "Etymonline"
                w = s.get("where")
                srcs.append({"label": lab, "where": w if w in WHERE_OK else "Reference"})
            terms[slug] = {"definition": e["definition"].strip(),
                           "history": e["history"].strip(),
                           "sources": srcs}
            added.append(slug)
    DEFS.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[merge] added {len(added)}: {', '.join(sorted(added))}")
    if skipped: print(f"[merge] skipped {len(skipped)} existing: {', '.join(sorted(skipped))}")
    if bad: print(f"[merge] BAD {len(bad)}: {', '.join(bad)}")
    print(f"[merge] total defined now: {len(terms)}")


if __name__ == "__main__":
    main(overwrite="--overwrite" in sys.argv)
