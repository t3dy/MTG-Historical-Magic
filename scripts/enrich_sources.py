#!/usr/bin/env python3
"""Merge researched url/url_kind/abstract data (from data/_source_enrich/batch_*_out.json)
into data/definitions.json, data/historiography.json, and data/essays.json source entries,
matched by the same canon_key() used to dedupe the bibliography. Never overwrites an existing
url/abstract; only fills gaps. Rerun build_terms.py + build_bibliography.py after this.
"""
from __future__ import annotations
import json, glob, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_bibliography import normalize, canon_key  # noqa: E402

BASE = Path(__file__).resolve().parent.parent
ENRICH_DIR = BASE / "data" / "_source_enrich"


def load_enrichment() -> dict:
    enrich = {}
    files = sorted(glob.glob(str(ENRICH_DIR / "batch_*_out.json")))
    for f in files:
        batch = json.loads(Path(f).read_text(encoding="utf-8"))
        for work, info in batch.items():
            if not isinstance(info, dict):
                continue
            url = (info.get("url") or "").strip()
            abstract = (info.get("abstract") or "").strip()
            if not url and not abstract:
                continue
            enrich[canon_key(work)] = {
                "url": url,
                "url_kind": (info.get("url_kind") or "").strip(),
                "abstract": abstract,
            }
    print(f"[enrich] read {len(files)} batch file(s) -> {len(enrich)} researched works")
    return enrich


def apply_to_file(path: Path, key: str, enrich: dict) -> tuple[int, int]:
    d = json.loads(path.read_text(encoding="utf-8"))
    n_url, n_abs = 0, 0
    for entry in d[key].values():
        for s in entry.get("sources", []):
            w = normalize(s.get("label", ""))
            e = enrich.get(canon_key(w))
            if not e:
                continue
            if e["url"] and not s.get("url"):
                s["url"], s["url_kind"] = e["url"], e["url_kind"]
                n_url += 1
            if e["abstract"] and not s.get("abstract"):
                s["abstract"] = e["abstract"]
                n_abs += 1
    path.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
    return n_url, n_abs


def main() -> None:
    enrich = load_enrichment()
    for fn, key in [
        (BASE / "data" / "definitions.json", "terms"),
        (BASE / "data" / "historiography.json", "terms"),
        (BASE / "data" / "essays.json", "essays"),
    ]:
        n_url, n_abs = apply_to_file(fn, key, enrich)
        print(f"[enrich] {fn.name}: {n_url} sources got a url, {n_abs} got an abstract")


if __name__ == "__main__":
    main()
