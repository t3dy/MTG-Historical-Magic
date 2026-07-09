#!/usr/bin/env python3
"""Download and cache Scryfall bulk data (oracle_cards by default).

Scryfall etiquette: one bulk download, not per-card requests. We hit the bulk-data
index, resolve the requested type's `download_uri`, and cache it locally. Re-runs
skip the download if the local copy is newer than Scryfall's `updated_at`.

Usage:
    python scripts/fetch_bulk.py                 # oracle_cards
    python scripts/fetch_bulk.py default_cards   # all printings
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

BULK_INDEX = "https://api.scryfall.com/bulk-data"
UA = "MTGMAGICWORDS/0.1 (research; contact ted.hand@gmail.com)"
RAW = Path(__file__).resolve().parent.parent / "data" / "raw"


def _get(url: str) -> bytes:
    req = Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urlopen(req, timeout=120) as r:
        return r.read()


def fetch(kind: str = "oracle_cards") -> Path:
    RAW.mkdir(parents=True, exist_ok=True)
    index = json.loads(_get(BULK_INDEX))
    entry = next((e for e in index["data"] if e["type"] == kind), None)
    if entry is None:
        avail = ", ".join(e["type"] for e in index["data"])
        raise SystemExit(f"Unknown bulk type {kind!r}. Available: {avail}")

    out = RAW / f"{kind}.json"
    meta = RAW / f"{kind}.meta.json"
    remote_updated = entry["updated_at"]

    if out.exists() and meta.exists():
        local = json.loads(meta.read_text()).get("updated_at")
        if local == remote_updated:
            print(f"[fetch] {kind} up to date ({remote_updated}); {out.stat().st_size/1e6:.1f} MB cached")
            return out

    print(f"[fetch] downloading {kind} ({entry['size']/1e6:.1f} MB) updated {remote_updated} …")
    data = _get(entry["download_uri"])
    out.write_bytes(data)
    meta.write_text(json.dumps({
        "type": kind,
        "updated_at": remote_updated,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "count": entry.get("card_count"),
        "download_uri": entry["download_uri"],
    }, indent=2))
    print(f"[fetch] wrote {out} ({out.stat().st_size/1e6:.1f} MB)")
    return out


if __name__ == "__main__":
    fetch(sys.argv[1] if len(sys.argv) > 1 else "oracle_cards")
