#!/usr/bin/env python3
"""Merge agent-drafted historiographical-note batches into data/historiography.json.

Each file in data/_histo_out/*.json is {slug: {commentary, sources}} for terms that
warrant a note (agents omit terms where the history suffices). Existing entries kept.
"""
from __future__ import annotations
import json, glob
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
HISTO = BASE / "data" / "historiography.json"
OUT_DIR = BASE / "data" / "_histo_out"

WHERE_OK = {"RenaissanceMagicDB", "MedievalMagicDB", "Medieval magic (PDF)",
            "Renaissance magic (PDF)", "Alchemy (PDF)", "Etymology reference",
            "Classical lexica", "Reference"}


def main():
    doc = json.loads(HISTO.read_text(encoding="utf-8"))
    terms = doc["terms"]
    added, skipped = [], []
    for f in sorted(glob.glob(str(OUT_DIR / "*.json"))):
        batch = json.loads(Path(f).read_text(encoding="utf-8"))
        for slug, e in batch.items():
            if not isinstance(e, dict) or not e.get("commentary"):
                continue
            if slug in terms:
                skipped.append(slug); continue
            srcs = []
            for s in e.get("sources", []):
                if not isinstance(s, dict) or not (s.get("label") or "").strip():
                    continue
                lab = s["label"].strip()
                if lab in WHERE_OK:
                    continue
                if lab == "Etymology reference":
                    lab = "Etymonline"
                w = s.get("where")
                srcs.append({"label": lab, "where": w if w in WHERE_OK else "Reference"})
            terms[slug] = {"commentary": e["commentary"].strip(), "sources": srcs}
            added.append(slug)
    HISTO.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[merge] added {len(added)}: {', '.join(sorted(added))}")
    if skipped:
        print(f"[merge] already present ({len(skipped)}): {', '.join(sorted(set(skipped)))}")
    print(f"[merge] total historiographical notes now: {len(terms)}")


if __name__ == "__main__":
    main()
