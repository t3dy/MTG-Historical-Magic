#!/usr/bin/env python3
"""Flatten Scryfall bulk JSON into a tidy per-card record with the fields we mine.

Emits JSON Lines to data/derived/cards.jsonl. Each line:
    {
      "id", "name", "set", "released_at",
      "type_line", "subtypes": [...],        # parsed from type_line after the em dash
      "oracle_text", "flavor_text",
      "colors", "rarity", "cmc"
    }

Handles multi-face cards (adventure, split, MDFC) by merging faces' text so a term on
either face is counted once per card. Keeps type_line from the primary face + all faces'
subtypes.
"""
from __future__ import annotations

import json
from pathlib import Path

RAW = Path(__file__).resolve().parent.parent / "data" / "raw" / "oracle_cards.json"
OUT = Path(__file__).resolve().parent.parent / "data" / "derived" / "cards.jsonl"

EM_DASH = "—"  # Scryfall separates supertypes/types — subtypes with an em dash


def subtypes_from_type_line(type_line: str) -> list[str]:
    if not type_line or EM_DASH not in type_line:
        return []
    tail = type_line.split(EM_DASH, 1)[1]
    return [t for t in tail.replace("//", " ").split() if t]


def faces(card: dict) -> list[dict]:
    return card.get("card_faces") or [card]


def image_uris(card: dict) -> dict:
    """Pull the front-face image URIs (single- or double-faced)."""
    imgs = card.get("image_uris")
    if not imgs:
        fs = card.get("card_faces") or []
        if fs and fs[0].get("image_uris"):
            imgs = fs[0]["image_uris"]
    imgs = imgs or {}
    return {
        "small": imgs.get("small", ""),
        "normal": imgs.get("normal", ""),
        "art_crop": imgs.get("art_crop", ""),
    }


def normalize_card(card: dict) -> dict:
    fs = faces(card)
    type_line = card.get("type_line") or " // ".join(f.get("type_line", "") for f in fs)
    subs: list[str] = []
    for f in fs:
        subs.extend(subtypes_from_type_line(f.get("type_line", "")))
    oracle = "\n".join(f.get("oracle_text", "") for f in fs if f.get("oracle_text"))
    flavor = "\n".join(f.get("flavor_text", "") for f in fs if f.get("flavor_text"))
    return {
        "id": card.get("oracle_id") or card.get("id"),
        "name": card.get("name", ""),
        "set": card.get("set", ""),
        "released_at": card.get("released_at", ""),
        "type_line": type_line,
        "subtypes": sorted(set(subs)),
        "oracle_text": oracle,
        "flavor_text": flavor,
        "colors": card.get("colors") or card.get("color_identity") or [],
        "rarity": card.get("rarity", ""),
        "cmc": card.get("cmc", 0),
        "scryfall_uri": card.get("scryfall_uri", ""),
        "img": image_uris(card),
    }


def main() -> None:
    cards = json.loads(RAW.read_text(encoding="utf-8"))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with OUT.open("w", encoding="utf-8") as fh:
        for c in cards:
            # Skip tokens, art cards, and non-card layouts that pollute vocabulary counts.
            if c.get("layout") in {"token", "double_faced_token", "art_series", "emblem"}:
                continue
            fh.write(json.dumps(normalize_card(c), ensure_ascii=False) + "\n")
            n += 1
    print(f"[normalize] wrote {n} cards -> {OUT}")


if __name__ == "__main__":
    main()
