#!/usr/bin/env python3
"""
lookup.py — print ONE generator record without making the agent load a whole
chapter or JSON file into context.

  python3 scripts/lookup.py tag <Name>      # a tag's summary + d3 sub-tables
  python3 scripts/lookup.py tag "blood feud"  # fuzzy, case-insensitive

It reads only the small detail file it needs.  Name matching is
case-insensitive and fuzzy (exact -> startswith -> substring -> token overlap).

Adding new kinds later (focus / spell / monster) is a one-line edit: register a
loader in KINDS that returns {name: record}.  The CLI plumbing stays the same.

Std-lib only; Python 3.6+.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GEN = os.path.join(os.path.dirname(HERE), "bridge", "generators")


def _load(fname):
    p = os.path.join(GEN, fname)
    if not os.path.exists(p):
        return None
    return json.load(open(p, encoding="utf-8"))


# --- kind loaders ----------------------------------------------------------
# Each loader returns a dict {display_name: record-dict}.  The record-dict is
# whatever the printer for that kind expects.

def _load_tags():
    """All five *_tags_detail.json merged into one {tag_name: detail-entry}.
    The detail-entry is augmented with its family + labels for printing."""
    index = {}
    for fam in ("character", "community", "court", "ruin", "wilderness"):
        doc = _load(f"{fam}_tags_detail.json")
        if not doc:
            continue
        for name, rec in doc["tags"].items():
            entry = dict(rec)
            entry["_family"] = fam
            entry["_labels"] = doc["labels"]
            # later families won't clobber earlier same-named tags (rare);
            # disambiguate by suffixing family if a clash occurs.
            key = name
            if key in index and index[key]["_family"] != fam:
                key = f"{name} ({fam})"
            index[key] = entry
    return index


def _load_lookup(fname):
    """A `kind:"lookup"` bundle ({records:{name:rec}}) → {name: rec}."""
    doc = _load(fname)
    return dict(doc.get("records", {})) if doc else {}


def _load_foci():
    return _load_lookup("foci.json")


def _load_spells():
    return _load_lookup("spells.json")


def _load_monsters():
    return _load_lookup("bestiary.json")


KINDS = {
    "tag": _load_tags,
    "focus": _load_foci,
    "spell": _load_spells,
    "monster": _load_monsters,
}


# --- printers --------------------------------------------------------------
def print_tag(name, rec):
    fam = rec["_family"]
    lo, hi = rec["d100"]
    print(f"{name}   [{fam} tag · d100 {lo}-{hi}]")
    print()
    print(rec["summary"])
    sub = rec["subtables"]
    for label in rec["_labels"]:
        opts = sub.get(label, [])
        print()
        print(f"{label} (d3):")
        for i, o in enumerate(opts, 1):
            print(f"  {i}. {o}")


def print_record(name, rec):
    """Generic printer for a flat lookup record (focus / spell / monster)."""
    print(name)
    print()
    for k, v in rec.items():
        if k.startswith("_") or v in (None, "", [], {}):
            continue
        print(f"  {k}: {v}")


PRINTERS = {
    "tag": print_tag,
    "focus": print_record,
    "spell": print_record,
    "monster": print_record,
}


# --- fuzzy match -----------------------------------------------------------
def fuzzy(query, names):
    """Return the best-matching name (or None) for `query` over `names`."""
    q = query.strip().lower()
    lowered = {n.lower(): n for n in names}
    # 1) exact
    if q in lowered:
        return lowered[q]
    # 2) unique startswith
    starts = [n for low, n in lowered.items() if low.startswith(q)]
    if len(starts) == 1:
        return starts[0]
    # 3) unique substring
    subs = [n for low, n in lowered.items() if q in low]
    if len(subs) == 1:
        return subs[0]
    if starts:
        return sorted(starts, key=len)[0]
    if subs:
        return sorted(subs, key=len)[0]
    # 4) token overlap
    qt = set(q.split())
    best, score = None, 0
    for low, n in lowered.items():
        s = len(qt & set(low.split()))
        if s > score:
            best, score = n, s
    return best


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return
    kind = args[0].lower()
    if kind not in KINDS:
        sys.exit(f"Unknown kind '{kind}'. Known: {', '.join(sorted(KINDS))}.")
    if len(args) < 2:
        sys.exit(f"Usage: lookup.py {kind} <name>")
    name_query = " ".join(args[1:])

    index = KINDS[kind]()
    if not index:
        sys.exit(f"No data for kind '{kind}' (did you run build_data.py?).")

    match = fuzzy(name_query, index.keys())
    if not match:
        # show a few candidates to help the caller
        cands = sorted(index.keys())[:12]
        sys.exit(f"No '{kind}' matching '{name_query}'. "
                 f"e.g. {', '.join(cands)} ...")
    PRINTERS[kind](match, index[match])


if __name__ == "__main__":
    main()
