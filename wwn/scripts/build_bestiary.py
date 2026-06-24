#!/usr/bin/env python3
"""
build_bestiary.py — parse the WWN bestiary into a machine-readable lookup that a
central `lookup.py` (kind: "monster") and `monster.py --lookup` can consume.

Two trusted, on-disk sources are parsed, both bundled with this skill:

  A) Worlds Without Number Deluxe — "09 - Creatures of A Far Age" (the example
     stat lines on p.283 plus the bestiary proper, L833+).
  B) The Atlas of the Latter Earth — "03 - Beasts and Fell Things" (the group
     stat-tables, same field layout, AC sometimes carrying an 'a' suffix).

Both render their statblocks in the field order
    HD · AC · Atk · Dmg · Shock · Move · ML · Inst · Skill · Save
in one of two physical shapes:
    * whitespace-delimited rows under a "<Group> HD AC Atk. ..." header, or
    * markdown pipe tables with <br>-joined multi-creature cells.
This builder handles both, faithfully carrying the armored 'a' AC suffix, the
'x2' / 'x 2' multi-attack notation, Brass-Legion '*' footnotes, and the
non-numeric placeholders the book uses ("As Imperator", "Special", "None").

A concise `notes` string is attached per creature from the bolded special-ability
names in its prose entry, when present.

Output: ../bridge/generators/bestiary.json  (id wwn.bestiary, kind "lookup").

Re-runnable / idempotent: rewrites the target from source each run and prints a
creature count.  Does NOT touch build_data.py or any other generator.

Std-lib only; Python 3.6+.

USAGE
  python3 scripts/build_bestiary.py            # build + verify, print the count
  python3 scripts/build_bestiary.py --quiet    # build, print only the count line
"""
import json
import os
import re
import sys
import unicodedata

# ---------------------------------------------------------------------------
# Paths.  Resolve relative to this file so the script runs from anywhere.
# ---------------------------------------------------------------------------
HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(HERE)
OUT_DIR = os.path.join(SKILL_ROOT, "bridge", "generators")
BOOK_WWN = os.path.join(SKILL_ROOT, "book", "Worlds Without Number Deluxe")
BOOK_ATLAS = os.path.join(SKILL_ROOT, "book", "The Atlas of the Latter Earth")

WWN_FILE = os.path.join(BOOK_WWN, "09 - Creatures of A Far Age.md")
ATLAS_FILE = os.path.join(BOOK_ATLAS, "03 - Beasts and Fell Things.md")

# Field order shared by every statblock in both books.
FIELDS = ["hd", "ac", "atk", "damage", "shock", "move", "morale",
          "instinct", "skill", "save"]
# Column-header tokens that mark a statblock header line (and must not be parsed
# as a creature row).
HEADER_TOKENS = ("HD", "AC", "Atk", "Dmg", "Shock", "Move", "ML",
                 "Inst", "Skill", "Save")


# ---------------------------------------------------------------------------
# Text hygiene (mirrors build_data.py's approach; standalone copy).
# ---------------------------------------------------------------------------
SMART = {
    "’": "'", "‘": "'", "“": '"', "”": '"',
    "–": "-", "—": "-", "…": "...", " ": " ",
    "′": "'", "″": '"', "’".encode().decode(): "'",
    "’": "'", "’": "'",
}
# Feet apostrophe variants used for Move ("30'", "30’").
FOOT = {"’": "'", "ʼ": "'", "′": "'"}


def clean(s):
    """Normalize smart punctuation; collapse internal whitespace; trim."""
    if s is None:
        return s
    for k, v in SMART.items():
        s = s.replace(k, v)
    for k, v in FOOT.items():
        s = s.replace(k, v)
    s = unicodedata.normalize("NFC", s)
    s = re.sub(r"[ \t]+", " ", s).strip()
    return s


# ---------------------------------------------------------------------------
# Statblock-row tokenization.
#
# A creature row is: <name words> <10 stat tokens>.  The stats can contain
# spaces inside a single logical field, which the book introduces in three
# ways we must re-join before counting columns:
#   * multi-attack:        "+12 x3"  /  "+15 x 2"   -> one Atk token
#   * footnote marker:     "18*"  / "20*"           -> stays attached to AC
#   * winged/swim move:    "40' fly" / "90' swim"   -> one Move token
# We collapse those, then the row is <name...> + exactly 10 stat tokens, so the
# name is "everything left of the last 10 tokens".
# ---------------------------------------------------------------------------
def _normalize_row_tokens(line):
    """Return a token list for one statblock row with the three multi-word stat
    fields joined into single tokens, so a clean 10-field tail remains:

      * multi-attack:  "+8 x2" / "+15 x 2" / "+20 x3"  ->  Atk = "+8 x2"
      * winged/swim move:  "40' fly" / "90' swim"      ->  Move = "40' fly"
      * footnote marker "18*" stays attached to AC already.

    Works for both whitespace rows and a single de-piped pipe cell row.
    """
    s = clean(line)
    # 0) glue a spaced Shock-vs-AC value: the book writes Shock "2/AC 15" with a
    #    space (Sentient Carcass) -> normalize to one token "2/15".
    s = re.sub(r"(\d+)/AC\s+(\d+)", r"\1/\2", s)
    # 1) collapse a spaced attack multiplier first ("+15 x 2" -> "+15 x2").
    s = re.sub(r"\bx\s+(\d)", r"x\1", s)
    # 2) glue the "xN" multiplier onto the preceding attack bonus, so it becomes
    #    one Atk field token ("+8 x2").  Use an underscore placeholder to survive
    #    the split, then restore the space.
    s = re.sub(r"([+\-]?\d+)\s+(x\d)", r"\1_\2", s)
    # 3) glue "<n>' <mode>" movement (fly / swim / climb / burrow).
    s = re.sub(r"(\d+'?)\s+(fly|swim|climb|burrow)\b", r"\1_\2", s)
    toks = s.split()
    toks = [t.replace("_", " ") for t in toks]
    return toks


# Tokens that legitimately start a stat field (so we can find where the 10-field
# tail begins from the right). A field token starts with a digit, a sign, an
# 'x', "Wpn", "None"/"N/A"/"Special", "As", or a dash.
def _looks_statish(tok):
    t = tok.strip()
    if not t:
        return False
    if re.match(r"^[\d+\-]", t):           # 4, +5, -, 13a, 18*
        return True
    if t.lower() in ("none", "n/a", "special", "wpn", "wpn+1", "wpn+2",
                     "wpn+3", "wpn+4", "wpn+5", "wpn-1", "as"):
        return True
    if t.startswith("x"):                  # x2 (rare leading multiplier)
        return True
    if t.startswith("Wpn"):
        return True
    return False


def parse_statblock_row(line):
    """Parse one creature row -> (name, {field: value}) or None.

    Strategy: HD is the first stat field and is always a bare integer; a creature
    name never ends in a bare integer that is immediately followed by a stat run.
    So we scan left-to-right for the first bare-integer token that begins a run
    of stat-ish tokens and treat it as HD; the name is everything before it.

    Two irregular families are special-cased rather than mis-sliced:
      * Pure DEFER rows — "<Name> As Imperator/Type/Original Creature/Mountain/
        Same Type of Human" — carry NO numeric HD at all; the whole stat line
        defers to another entry.  We keep the name + a defer marker.
      * ELEMENTAL rows — "Elemental, Minor 4 15 +6 As Type 12 3 +1 13+" — have a
        numeric HD but substitute "As Type" for Dmg+Shock and omit Move.
    """
    toks = _normalize_row_tokens(line)
    if not toks:
        return None

    # Find HD: first bare-integer token that starts a stat run.
    hd_idx = None
    for i, t in enumerate(toks):
        if re.fullmatch(r"\d+", t):
            rest = toks[i + 1:]
            if len(rest) >= 3 and _looks_statish(rest[0]):
                hd_idx = i
                break

    # Pure DEFER row: no numeric HD, stat tail literally begins "As ...".
    if hd_idx is None:
        if "As" in toks:
            ai = toks.index("As")
            head = toks[:ai]
            if head:
                return " ".join(head), {f: None for f in FIELDS} | {
                    "_defer": " ".join(toks[ai:])}
        return None

    name = " ".join(toks[:hd_idx]).strip()
    fields = toks[hd_idx:]
    if not name:
        return None

    rec = {}
    for i, key in enumerate(FIELDS):
        rec[key] = fields[i] if i < len(fields) else None

    # ELEMENTAL row: Dmg/Shock are the literal "As Type", Move is omitted, so the
    # remaining 4 tokens are ML, Inst, Skill, Save.
    if rec.get("damage") == "As" and rec.get("shock") == "Type":
        body = fields[3:]            # tokens after Atk
        if len(body) >= 2 and body[0] == "As":
            body = body[2:]
        rec["damage"] = "As Type"
        rec["shock"] = "As Type"
        rec["move"] = None
        for k, v in zip(["morale", "instinct", "skill", "save"], body):
            rec[k] = v
    return name, rec


# ---------------------------------------------------------------------------
# Table extraction — whitespace tables and pipe tables.
# ---------------------------------------------------------------------------
def _is_header_line(line):
    s = clean(line)
    # A header has the field tokens in order, e.g. "Animals HD AC Atk. ..."
    return bool(re.search(r"\bHD\b\s+AC\b\s+Atk", s)) or bool(
        re.search(r"\|HD\|AC\|Atk", s.replace(" ", "")))


# The three generic "example stat line" tables on p.283 are TEMPLATES for
# statting a foe fast, not Latter-Earth creatures.  They live in the GM card,
# not the bestiary lookup, so we skip them here by their group-header word.
GENERIC_TEMPLATE_GROUPS = {
    "normal humans", "spellcasters", "normal animals",
}


def _header_group_word(line):
    """The group label that precedes 'HD AC Atk...' on a header line, lowered.
    Handles both 'Normal Animals HD AC ...' and '|Normal Animals|HD|AC|...'."""
    s = clean(line)
    if s.startswith("|"):
        first = s.strip("|").split("|", 1)[0]
        return clean(first).lower()
    m = re.match(r"^(.*?)\s+HD\s+AC\s+Atk", s)
    return clean(m.group(1)).lower() if m else ""


def extract_whitespace_table(lines, start_idx):
    """From a header line index, read contiguous creature rows until a blank
    line, a new header, a markdown heading, or a non-row line.  Returns
    [(name, rec, footnote)]."""
    out = []
    i = start_idx + 1
    while i < len(lines):
        raw = lines[i]
        s = clean(raw)
        if not s:
            break
        if s.startswith("#") or s.startswith("|") or _is_header_line(raw):
            break
        # Footnote / legend lines (start with '*' or '* All ...') end the table.
        if s.startswith("*"):
            break
        parsed = parse_statblock_row(raw)
        if parsed:
            out.append((parsed[0], parsed[1], None))
            i += 1
            continue
        # A non-parsable line inside the run: stop (the table has ended).
        break
    return out, i


def extract_pipe_table(lines, start_idx):
    """Parse a markdown pipe statblock table whose first data row may pack many
    creatures via <br> joins (each column is a <br>-list, row-parallel)."""
    # collect the table's lines (start_idx is the header row)
    block = []
    i = start_idx
    while i < len(lines):
        s = lines[i].strip()
        if s.startswith("|"):
            block.append(lines[i])
            i += 1
        else:
            break
    out = []
    for ln in block:
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        # skip separator rows
        joined = "".join(cells)
        if not joined or set(joined) <= set("-:| "):
            continue
        # skip the header row: signature is cells[1] == 'HD' (col 0 is the
        # group label, e.g. 'Normal Animals').
        if len(cells) > 1 and cells[1].strip().upper() == "HD":
            continue
        if len(cells) < len(FIELDS) + 1:
            continue
        # Each cell may hold a <br>-list; split all columns in parallel.
        col_lists = [c.split("<br>") for c in cells]
        depth = max(len(c) for c in col_lists)
        for r in range(depth):
            name = clean(col_lists[0][r] if r < len(col_lists[0]) else "")
            rec = {}
            for fi, key in enumerate(FIELDS):
                col = col_lists[fi + 1] if fi + 1 < len(col_lists) else []
                val = clean(col[r]) if r < len(col) else None
                rec[key] = val
            # Drop sub-header rows that leaked from a multi-group <br> cell
            # (their HD/AC literally read 'HD'/'AC').
            if not name or rec.get("hd") in ("HD", "AC") \
                    or rec.get("ac") == "AC":
                continue
            # normalize 'x 2' etc. inside atk
            if rec.get("atk"):
                rec["atk"] = re.sub(r"\bx\s+(\d)", r"x\1", rec["atk"])
            out.append((name, rec, None))
    return out, i


# ---------------------------------------------------------------------------
# Footnote / asterisk handling.
# The Brass Legion table marks every AC with '*' and a legend line
#   "* All Brass Legion automatons are immune to ... non-magical weapons ..."
# We detect such legends right after a whitespace table and append a note to the
# rows whose AC carried '*'.
# ---------------------------------------------------------------------------
def find_footnote(lines, end_idx):
    """Look at the few lines after a table for a '* ...' legend; return its
    cleaned text or None."""
    for j in range(end_idx, min(end_idx + 3, len(lines))):
        s = clean(lines[j])
        if s.startswith("*") and len(s) > 3 and not _is_header_line(lines[j]):
            return s.lstrip("* ").strip()
    return None


# ---------------------------------------------------------------------------
# Prose -> concise `notes`.
#
# Most creatures have a prose entry under a "## <Name>" heading listing their
# special abilities as bolded "- **Ability**: ..." bullets.  We harvest the
# bolded ability NAMES (not the full text) for a concise note, and fall back to
# the leading descriptive sentence when no bullets exist.
# ---------------------------------------------------------------------------
def harvest_ability_index(txt):
    """Return {lower-name: 'Ability1, Ability2'} of bolded ability names found
    in the prose section headed by that creature/group name.  Also captures the
    family-level abilities so members inherit a hint."""
    index = {}
    # Split on H2 headings; for each, collect bolded "**X**" tokens used as
    # ability labels (those followed by ':' or starting a bullet).
    sections = re.split(r"\n##+ ", "\n" + txt)
    for sec in sections:
        head, _, body = sec.partition("\n")
        name = clean(head)
        if not name or len(name) > 40:
            continue
        labels = []
        for m in re.finditer(r"\*\*([A-Z][A-Za-z' \-]{2,40}?)\*\*\s*:", body):
            lab = clean(m.group(1))
            if lab and lab not in labels and lab.lower() not in (
                    "atk", "dmg", "shock", "move", "hd", "ac"):
                labels.append(lab)
        # Also catch "- Ability: ..." bullets that are bolded as "- **X**:"
        if labels:
            index[name.lower()] = ", ".join(labels[:6])
    return index


def lead_sentence(txt, name):
    """First descriptive sentence of a creature's prose section, if any."""
    # find "## <name>" (exact-ish) then its first non-empty paragraph
    pat = re.compile(r"\n##+ " + re.escape(name) + r"\s*\n(.*?)(?=\n##+ |\Z)",
                     re.DOTALL)
    m = pat.search("\n" + txt)
    if not m:
        return None
    body = m.group(1)
    for para in body.split("\n\n"):
        p = clean(para)
        if p and not p.startswith("**") and not p.startswith("-") \
                and not p.startswith("|") and len(p) > 20:
            # first sentence only, capped
            sent = re.split(r"(?<=[.!?])\s", p)[0]
            return sent[:200]
    return None


def make_notes(name, defer, footnote, ability_idx, txt):
    """Compose a concise notes string from: defer marker, footnote legend,
    bolded ability names, then a lead sentence fallback."""
    bits = []
    if defer:
        # defer marker reads like "As Imperator" / "As Type" -> "Defers to ...".
        d = defer.strip()
        d = re.sub(r"^As\s+", "", d)
        bits.append(f"Defers to: {d} (use that entry's statline)")
    if footnote:
        bits.append(footnote)
    # ability names keyed by the creature's own name, else by its group word
    key = name.lower()
    abil = ability_idx.get(key)
    if not abil:
        # try the creature's last word (e.g. "Glass Spider" -> "spider"?) — too
        # loose; instead try the first word as a group key ("Dwarven X" etc.)
        first = key.split()[0]
        abil = ability_idx.get(first)
    if abil:
        bits.append("Abilities: " + abil)
    if not bits:
        lead = lead_sentence(txt, name)
        if lead:
            bits.append(lead)
    note = " | ".join(b for b in bits if b)
    # keep concise
    return note[:300] if note else ""


# ---------------------------------------------------------------------------
# Build orchestration.
# ---------------------------------------------------------------------------
def build(quiet=False):
    os.makedirs(OUT_DIR, exist_ok=True)

    wwn_src = "book/Worlds Without Number Deluxe/09 - Creatures of A Far Age.md"
    atlas_src = "book/The Atlas of the Latter Earth/03 - Beasts and Fell Things.md"

    records = {}
    for path, src in ((WWN_FILE, wwn_src), (ATLAS_FILE, atlas_src)):
        part = _parse_file(path, src)
        for k, v in part.items():
            key = k
            if key in records:
                # disambiguate cross-source name clashes (e.g. "Wraith Lord")
                tag = "atlas" if "Atlas" in src else "wwn"
                key = f"{k} ({tag})"
            records[key] = v

    doc = {
        "id": "wwn.bestiary",
        "kind": "lookup",
        "category": "monster",
        "key": "name",
        "source": "WWN Deluxe ch.09 + Atlas of the Latter Earth ch.03",
        "fields": FIELDS,
        "records": records,
    }

    path = os.path.join(OUT_DIR, "bestiary.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
        f.write("\n")

    issues = verify(records)
    n = len(records)
    if quiet:
        print(f"bestiary.json: {n} creatures  "
              f"({'OK' if not issues else str(len(issues)) + ' issues'})")
    else:
        print("=" * 60)
        print(f"WWN bestiary build  ->  {path}")
        print("=" * 60)
        print(f"  creatures parsed : {n}")
        print(f"  from WWN 09      : "
              f"{sum(1 for v in records.values() if '09 - Creatures' in v['source'])}")
        print(f"  from Atlas 03    : "
              f"{sum(1 for v in records.values() if 'Beasts and Fell' in v['source'])}")
        if issues:
            print(f"  WARNINGS ({len(issues)}):")
            for p in issues[:25]:
                print("   !", p)
        else:
            print("  verification     : OK (every record has all 10 fields)")
    return doc


def _parse_file(path, src):
    """Parse one file with its source label baked into anchors."""
    txt = open(path, encoding="utf-8").read()
    lines = txt.splitlines()
    ability_idx = harvest_ability_index(txt)
    records = {}
    i = 0
    while i < len(lines):
        line = lines[i]
        if _is_header_line(line):
            # Skip the three generic example-statline tables (templates, not
            # creatures); they belong in the GM card.
            if _header_group_word(line) in GENERIC_TEMPLATE_GROUPS:
                # advance past this table to avoid re-detecting its rows
                if line.strip().startswith("|"):
                    _, nxt = extract_pipe_table(lines, i)
                else:
                    _, nxt = extract_whitespace_table(lines, i)
                i = nxt
                continue
            if line.strip().startswith("|"):
                rows, nxt = extract_pipe_table(lines, i)
                footnote = None
            else:
                rows, nxt = extract_whitespace_table(lines, i)
                footnote = find_footnote(lines, nxt)
            for (name, rec, _) in rows:
                defer = rec.pop("_defer", None)
                if rec.get("ac"):
                    rec["ac"] = rec["ac"].replace("*", "")
                out = {}
                for f in FIELDS:
                    v = rec.get(f)
                    out[f] = "" if v in (None, "") else v
                out["notes"] = make_notes(name, defer, footnote,
                                          ability_idx, txt)
                out["source"] = f"{src}#L{i + 1}"
                key = name
                if key in records:
                    key = f"{name} (2)"
                records[key] = out
            i = nxt
        else:
            i += 1
    return records


def verify(records):
    """Light verification: every record has all 10 fields; HD is numeric unless
    the row legitimately defers ('As <X>' captured into notes with empty HD).
    Returns a list of warning strings."""
    problems = []
    for name, rec in records.items():
        for f in FIELDS:
            if f not in rec:
                problems.append(f"{name}: missing field '{f}'")
        hd = rec.get("hd", "")
        deferred = hd == "" and rec.get("notes", "").startswith("Defers")
        if hd and not re.match(r"^\d", hd):
            problems.append(f"{name}: non-numeric HD '{hd}'")
        if not hd and not deferred:
            problems.append(f"{name}: empty HD (not a recognized defer row)")
    return problems


if __name__ == "__main__":
    build(quiet="--quiet" in sys.argv[1:])
