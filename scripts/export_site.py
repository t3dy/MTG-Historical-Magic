#!/usr/bin/env python3
"""Copy analysis outputs into site/data/ as the JSON the static site fetches."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
COUNTS = BASE / "data" / "derived" / "counts.json"
SITE_DATA = BASE / "site" / "data"


def main() -> None:
    SITE_DATA.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(COUNTS, SITE_DATA / "counts.json")
    # Small top-N convenience slices for the landing view.
    counts = json.loads(COUNTS.read_text(encoding="utf-8"))
    summary = {
        "cards_analyzed": counts["meta"]["cards_analyzed"],
        "top_subtypes": counts["subtypes"][:25],
        "top_terms": counts["terms"][:25],
        "by_category": {},
    }
    for t in counts["terms"]:
        summary["by_category"].setdefault(t.get("category", "uncategorized"), 0)
        summary["by_category"][t["category"]] += t["total"]
    (SITE_DATA / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"[export] wrote site/data/counts.json + summary.json")


if __name__ == "__main__":
    main()
