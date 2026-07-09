#!/usr/bin/env python3
r"""Research a magical term across Ted's databases + PDF text corpora, and emit a
citable dossier for writing a Word History.

WHAT IT SEARCHES
  Structured databases (C:\Dev):
    - renaissance magic\data\definitions.json   (139 scholarly term-entries w/ citations)
    - renaissance magic\data\kwic_concordance.json (keyword-in-context lines)
    - MedievalMagicDB\site\data.json            (concepts / persons / bibliography)
    - TheosophicalAlchemyDB\data\master_citation_index.json (alchemy concepts/figures)
  Full-text PDF corpora (E:\pdf — extracted .txt / .md):
    - magic\medieval magic         (Klaassen, Fanger, Page, Picatrix, Peterson grimoires…)
    - renaissance magic            (Yates, Couliano, Keith Thomas, Clark, Zambelli…)
    - alchemy\Markdown             (Lyndy Abraham's Dictionary of Alchemical Imagery, Principe…) [alchemy terms]
    - magic\ancient magic PGM, hermetic, Grimoire

USAGE
    python scripts/research.py necromancer          # by lexicon slug (uses its morphology regex)
    python scripts/research.py sigil talisman        # several
    python scripts/research.py --word "philtre|philter" alchemy   # ad-hoc regex + category hint

OUTPUT
    data/research/<slug>.json  — { db_hits[], corpus_hits[], counts }  (also copied to site/data/research/)
    Prints a summary you can skim before writing.

See docs/RESEARCH_METHOD.md for the full workflow and citation conventions.
"""
from __future__ import annotations

import json
import re
import sys
from html import escape
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
LEXICON = BASE / "data" / "derived" / "lexicon.json"
OUT = BASE / "data" / "research"
SITE_OUT = BASE / "site" / "data" / "research"

DEV = Path("C:/Dev")
PDF = Path("E:/pdf")

# Structured databases (path, kind).
REN_DEFS = DEV / "renaissance magic" / "data" / "definitions.json"
REN_KWIC = DEV / "renaissance magic" / "data" / "kwic_concordance.json"
MED_DATA = DEV / "MedievalMagicDB" / "site" / "data.json"
THEO_CIT = DEV / "TheosophicalAlchemyDB" / "data" / "master_citation_index.json"

# Full-text corpora: (label, root, extensions, categories-or-None=all)
CORPORA = [
    ("Medieval magic",     PDF / "magic" / "medieval magic",   (".txt",), None),
    ("Renaissance magic",  PDF / "renaissance magic",          (".txt", ".md"), None),
    ("Ancient magic (PGM)", PDF / "magic" / "ancient magic PGM", (".txt",), None),
    ("Hermetica",          PDF / "hermetic",                   (".txt", ".md"), None),
    ("Alchemy",            PDF / "alchemy" / "Markdown",       (".md",), {"alchemy"}),
]

CTX = 260          # chars of context around a corpus hit
MAX_PER_CORPUS = 10
MAX_FILES = 2500   # scan ceiling per corpus (rare terms)
MAX_BYTES = 4_000_000  # skip files larger than this


def lexicon():
    return json.loads(LEXICON.read_text(encoding="utf-8"))["roots"]


def build_regex(slug: str, roots: dict, word: str | None):
    if word:
        pat = word
    else:
        spec = roots.get(slug)
        pat = (spec["pattern"] if isinstance(spec, dict) else spec) if spec else re.escape(slug)
    return re.compile(rf"\b(?:{pat})\b", re.IGNORECASE)


def stem(slug: str, roots: dict) -> str:
    """Leading literal of the pattern — used as a loose substring needle for Latin cognates."""
    spec = roots.get(slug)
    pat = (spec["pattern"] if isinstance(spec, dict) else spec) if spec else slug
    m = re.match(r"[a-z]+", pat)
    s = m.group(0) if m else slug
    return s[:6]


def snippet_around(text: str, m: re.Match) -> str:
    a = max(0, m.start() - CTX // 2)
    b = min(len(text), m.end() + CTX // 2)
    seg = re.sub(r"\s+", " ", text[a:b]).strip()
    return ("…" if a > 0 else "") + seg + ("…" if b < len(text) else "")


def clean_cite(fname: str) -> str:
    base = re.sub(r"\.(txt|md|pdf)$", "", fname, flags=re.I)
    base = re.sub(r"[-_]", " ", base)
    base = re.sub(r"\s+libgen.*$", "", base, flags=re.I)
    base = re.sub(r"\s+[0-9a-f]{6,}$", "", base)  # trailing content-hash
    return re.sub(r"\s{2,}", " ", base).strip()[:140]


def search_db(slug: str, rx: re.Pattern, st: str, category: str | None):
    hits = []

    def matches(text: str) -> bool:
        return bool(rx.search(text or "") or (st and st in (text or "").lower()))

    # Renaissance definitions
    if REN_DEFS.exists():
        for e in json.loads(REN_DEFS.read_text(encoding="utf-8")):
            blob = f"{e.get('term','')} {e.get('definition_brief','')} {e.get('definition_long','')}"
            if matches(e.get("term", "")) or matches(blob):
                hits.append({"source": "RenaissanceMagicDB · definitions",
                             "term": e.get("term", ""),
                             "text": e.get("definition_long") or e.get("definition_brief", "")})
    # Renaissance KWIC
    if REN_KWIC.exists():
        kw = json.loads(REN_KWIC.read_text(encoding="utf-8"))
        for term, lines in kw.items():
            if matches(term) or (st and st in term.lower()):
                for ln in (lines[:4] if isinstance(lines, list) else []):
                    hits.append({"source": "RenaissanceMagicDB · concordance",
                                 "term": term, "text": ln.get("context", ""),
                                 "cite": clean_cite(ln.get("document", ""))})
    # Medieval concepts
    if MED_DATA.exists():
        med = json.loads(MED_DATA.read_text(encoding="utf-8"))
        for c in med.get("concepts", []):
            blob = " ".join(str(c.get(k, "")) for k in
                            ("label", "label_alt", "slug", "definition_short", "definition_long", "significance"))
            if matches(blob):
                hits.append({"source": "MedievalMagicDB · concept",
                             "term": c.get("label", ""),
                             "text": c.get("definition_long") or c.get("definition_short", ""),
                             "extra": c.get("significance", "")})
    # Theosophical alchemy concepts/figures
    if THEO_CIT.exists() and (category == "alchemy" or category is None):
        theo = json.loads(THEO_CIT.read_text(encoding="utf-8"))
        for bucket in ("concepts", "figures"):
            b = theo.get(bucket, [])
            items = b.values() if isinstance(b, dict) else b
            for c in items:
                if not isinstance(c, dict):
                    continue
                blob = " ".join(str(v) for v in c.values() if isinstance(v, str))
                if matches(blob):
                    hits.append({"source": f"TheosophicalAlchemyDB · {bucket}",
                                 "term": c.get("name") or c.get("label") or c.get("title", ""),
                                 "text": (c.get("definition") or c.get("summary") or blob)[:600]})
    return hits


def search_corpora(rx: re.Pattern, category: str | None):
    out = []
    for label, root, exts, cats in CORPORA:
        if cats is not None and (category not in cats):
            continue
        if not root.exists():
            continue
        found, scanned = [], 0
        for p in root.rglob("*"):
            if len(found) >= MAX_PER_CORPUS or scanned >= MAX_FILES:
                break
            if p.suffix.lower() not in exts or not p.is_file():
                continue
            try:
                if p.stat().st_size > MAX_BYTES:
                    continue
                text = p.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            scanned += 1
            m = rx.search(text)
            if m:
                found.append({"corpus": label, "file": p.name,
                              "cite": clean_cite(p.name), "snippet": snippet_around(text, m)})
        out.extend(found)
    return out


def research(slug: str, roots: dict, word: str | None, category: str | None):
    rx = build_regex(slug, roots, word)
    st = stem(slug, roots)
    cat = category or (roots.get(slug, {}).get("category") if isinstance(roots.get(slug), dict) else None)
    db = search_db(slug, rx, st, cat)
    corpus = search_corpora(rx, cat)
    dossier = {
        "slug": slug,
        "category": cat,
        "db_hits": db,
        "corpus_hits": corpus,
        "counts": {"db": len(db), "corpus": len(corpus)},
    }
    OUT.mkdir(parents=True, exist_ok=True)
    SITE_OUT.mkdir(parents=True, exist_ok=True)
    txt = json.dumps(dossier, ensure_ascii=False, indent=2)
    (OUT / f"{slug}.json").write_text(txt, encoding="utf-8")
    (SITE_OUT / f"{slug}.json").write_text(json.dumps(dossier, ensure_ascii=False), encoding="utf-8")
    print(f"[research] {slug} ({cat}): {len(db)} DB hits, {len(corpus)} corpus hits -> data/research/{slug}.json")
    for h in db[:4]:
        print(f"   · {h['source']} [{h.get('term','')}] {h['text'][:120]}")
    for h in corpus[:4]:
        print(f"   · {h['corpus']}: {h['cite'][:60]} — {h['snippet'][:110]}")
    return dossier


def main(argv):
    roots = lexicon()
    word = None
    slugs = []
    i = 0
    while i < len(argv):
        if argv[i] == "--word":
            word = argv[i + 1]; i += 2; continue
        slugs.append(argv[i]); i += 1
    if not slugs:
        print("usage: research.py <slug> [slug...]  |  research.py --word 'regex' <slug>")
        return
    for s in slugs:
        research(s, roots, word, None)


if __name__ == "__main__":
    main(sys.argv[1:])
