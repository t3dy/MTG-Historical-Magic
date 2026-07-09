#!/usr/bin/env python3
"""Download Scryfall card thumbnails for every term gallery.

Reads the per-term detail files (site/data/terms/*.json), and for each title-match
card downloads its `small` image to site/img/<slug>/<id>.jpg. Skips files already
present. Polite: descriptive User-Agent + a short delay between requests (Scryfall
image CDN, but we stay well-mannered).

Usage:
    python scripts/fetch_card_images.py            # all terms
    python scripts/fetch_card_images.py wizard scry # only these slugs
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from urllib.request import Request, urlopen

BASE = Path(__file__).resolve().parent.parent
TERMS = BASE / "site" / "data" / "terms"
IMG = BASE / "site" / "img"
UA = "MTGMAGICWORDS/0.2 (research; contact ted.hand@gmail.com)"
DELAY = 0.06  # seconds between downloads


def download(url: str, dest: Path) -> bool:
    req = Request(url, headers={"User-Agent": UA})
    try:
        with urlopen(req, timeout=30) as r:
            data = r.read()
        dest.write_bytes(data)
        return True
    except Exception as e:  # noqa: BLE001
        print(f"  ! {url} -> {e}")
        return False


def main(slugs: list[str]) -> None:
    files = sorted(TERMS.glob("*.json"))
    if slugs:
        files = [f for f in files if f.stem in slugs]
    got = skipped = failed = 0
    for f in files:
        detail = json.loads(f.read_text(encoding="utf-8"))
        cards = detail.get("cards", [])
        if not cards:
            continue
        out = IMG / detail["slug"]
        out.mkdir(parents=True, exist_ok=True)
        for c in cards:
            url = c.get("img_small")
            if not url:
                continue
            dest = out / f"{c['id']}.jpg"
            if dest.exists() and dest.stat().st_size > 0:
                skipped += 1
                continue
            if download(url, dest):
                got += 1
                time.sleep(DELAY)
            else:
                failed += 1
        print(f"[img] {detail['slug']:16} {len(cards)} cards")
    print(f"[img] done: {got} downloaded, {skipped} cached, {failed} failed -> {IMG}")


if __name__ == "__main__":
    main(sys.argv[1:])
