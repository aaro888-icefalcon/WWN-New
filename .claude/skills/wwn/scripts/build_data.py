#!/usr/bin/env python3
"""
build_data.py — Generator-layer data builder for the Worlds Without Number
companion that rides on the mythic-gm engine.

It parses WWN's random tables from two trusted, on-disk sources:

  A) the installed `wwn-worldbuilder` skill references (uniform, WWN-accurate
     markdown): the five tag families, npc_quickgen, adventure_seeds,
     religion/nation/history construction.
  B) the WWN book chapters bundled with this skill: Placing Treasures,
     Additional GM Tools (One-Roll Characterization depth + architecture),
     Creatures of A Far Age (monster generation), Naval Adventuring, and the
     Atlas optional rules (maiming wounds, alchemical accidents).

Output: verified JSON in ../bridge/generators/, in exactly the three shapes the
engine's dice scripts can consume (flat table / bundle / tag detail), plus a
manifest.json with a verification report.

Re-runnable / idempotent: it rewrites every target file from source each run.

Std-lib only; Python 3.6+.

USAGE
  python3 scripts/build_data.py            # build + verify, print manifest summary
  python3 scripts/build_data.py --quiet    # build, print only PASSED/FAILED line
"""
import json
import os
import re
import sys
import unicodedata
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# Paths.  Resolve relative to this file so the script runs from anywhere.
# ---------------------------------------------------------------------------
HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(HERE)
OUT_DIR = os.path.join(SKILL_ROOT, "bridge", "generators")

# Source A: the installed wwn-worldbuilder skill references.  Search a couple of
# plausible locations so the build works on the user machine and in the
# Linux workspace where folders are mounted under a session path.
def _find_wb_refs():
    cands = [
        os.path.join(SKILL_ROOT, "..", "..", ".claude", "skills",
                     "wwn-worldbuilder", "references"),
        "/sessions/quirky-keen-clarke/mnt/.claude/skills/wwn-worldbuilder/references",
        os.path.expanduser("~/.claude/skills/wwn-worldbuilder/references"),
    ]
    # Also: walk up from SKILL_ROOT looking for a sibling .claude/skills tree.
    p = SKILL_ROOT
    for _ in range(8):
        p = os.path.dirname(p)
        cands.append(os.path.join(p, ".claude", "skills",
                                  "wwn-worldbuilder", "references"))
    for c in cands:
        c = os.path.normpath(c)
        if os.path.isdir(c):
            return c
    return cands[0]

WB = _find_wb_refs()
BOOK_WWN = os.path.join(SKILL_ROOT, "book", "Worlds Without Number Deluxe")
BOOK_ATLAS = os.path.join(SKILL_ROOT, "book", "The Atlas of the Latter Earth")

ATTRIB = ("Worlds Without Number by Kevin Crawford / Sine Nomine Publishing")

# ---------------------------------------------------------------------------
# Text hygiene.  The sources mix curly quotes, en-dashes, OCR noise (stray
# single digits dropped mid-sentence, a few mis-scanned words).  Normalize.
# ---------------------------------------------------------------------------
SMART = {
    "’": "'", "‘": "'", "“": '"', "”": '"',
    "–": "-", "—": "-", "…": "...", " ": " ",
    "′": "'", "″": '"',
}

# Known OCR word fixes seen in the book scans (book is the only place these
# occur; the wwn-worldbuilder references are clean).
OCR_WORDS = {
    "futtery": "fluttery",
    "effcient": "efficient",
    "Offcer": "Officer",
    "Piscene": "Piscine",
    "an particular": "a particular",
    " in ability": " inability",
}


def clean(s):
    """Normalize smart punctuation; collapse internal whitespace; trim."""
    if s is None:
        return s
    for k, v in SMART.items():
        s = s.replace(k, v)
    s = unicodedata.normalize("NFC", s)
    s = re.sub(r"[ \t]+", " ", s).strip()
    for k, v in OCR_WORDS.items():
        s = s.replace(k, v)
    return s


def scrub_seed(s):
    """The Fractal Adventure Seeds in wwn-worldbuilder carry OCR debris: stray
    standalone digits (column-gutter page numbers) and a couple of half-words
    (' Th') dropped into the middle of sentences.  Remove them without touching
    the legitimate 'Complication 3' style references that name a sub-table row.

    Strategy: only strip a bare number when it is clearly orphaned -- i.e. it
    sits between two lowercase words or before a lone capital, not when it
    directly follows a component keyword (Enemy/Friend/Complication/Thing/
    Place)."""
    s = clean(s)
    # remove orphan ' Th' fragment
    s = re.sub(r"\bTh\b(?=\s+[a-z])", "", s)
    # 'Complication 3' / 'Thing 4' immediately after a keyword: drop the digit,
    # it is OCR bleed, the keywords are placeholders not numbered sub-rows here.
    s = re.sub(r"\b(Enemy|Friend|Complication|Thing|Place)\s+\d+\b", r"\1", s)
    # orphan digit floating between two words: "process the" got "process 3 the"
    s = re.sub(r"(?<=[a-z,]) \d+ (?=[a-z])", " ", s)
    # orphan digit right before end of sentence: "...threatening a Friend. 1"
    s = re.sub(r"\.\s+\d+\s*$", ".", s)
    # orphan digit hugging a capitalized word start: "from 4 an Enemy"
    s = re.sub(r"\s\d+ (?=[A-Z][a-z])", " ", s)
    s = re.sub(r"[ \t]+", " ", s).strip()
    return s


# ---------------------------------------------------------------------------
# Range helpers.  WWN d100 master tables write '1-2' and '99-00' (00 == 100).
# ---------------------------------------------------------------------------
def parse_range(token, die):
    """Return (min,max) ints from a token like '1', '1-4', '99-00', '97-00'."""
    token = clean(token).replace("–", "-").replace("—", "-")
    token = token.strip()
    if "-" in token:
        lo_s, hi_s = token.split("-", 1)
        lo, hi = int(lo_s), int(hi_s)
        if hi == 0:                    # '99-00' -> 99..100 on a d100
            hi = die
        if lo == 0:
            lo = die
        return lo, hi
    n = int(token)
    if n == 0:
        n = die
    return n, n


def flat(slug, title, source, die, entries):
    """Assemble a flat table record.  `entries` is a list of (lo,hi,value)."""
    return {
        "id": f"wwn.{slug}",
        "title": title,
        "source": source,
        "type": f"list_d{die}",
        "dice": f"1d{die}",
        "entries": [
            {"min": lo, "max": hi, "value": clean(v)}
            for (lo, hi, v) in entries
        ],
    }


def numbered_entries(rows):
    """rows = list of value strings in roll order, 1..N -> contiguous singles."""
    return [(i + 1, i + 1, v) for i, v in enumerate(rows)]


# ===========================================================================
# PARSER 1 -- the five tag families (tag detail + flat companion).
# ===========================================================================
TAG_LABELS = {
    "character": ["Ambitions", "Powers", "Dreads"],
    "community": ["Enemies", "Friends", "Complications", "Things", "Places"],
    "court": ["Enemies", "Friends", "Complications", "Things", "Places"],
    "ruin": ["Enemies", "Friends", "Complications", "Things", "Places"],
    "wilderness": ["Enemies", "Friends", "Complications", "Things", "Places"],
}


def parse_tag_family(family):
    """Parse one *_tags.md from wwn-worldbuilder into (detail, flat)."""
    path = os.path.join(WB, f"{family}_tags.md")
    txt = open(path, encoding="utf-8").read()
    labels = TAG_LABELS[family]

    # --- d100 master table -> name + d100 range -------------------------------
    mt = re.search(r"## d100 Master Table\s*(.*?)\n---", txt, re.DOTALL)
    if not mt:
        raise ValueError(f"{family}: no master table")
    order = []            # [(lo,hi,name)] in roll order
    name_range = {}       # name -> (lo,hi)
    for line in mt.group(1).splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        # header / separator rows
        if not cells or cells[0].lower() in ("roll", "") or set(cells[0]) <= set("-: "):
            continue
        # two (Roll, Tag) pairs per row
        for i in range(0, len(cells) - 1, 2):
            rng, name = cells[i], cells[i + 1]
            if not re.match(r"^\d", rng):
                continue
            lo, hi = parse_range(rng, 100)
            name = clean(name)
            order.append((lo, hi, name))
            name_range[name] = (lo, hi)
    order.sort(key=lambda t: t[0])

    # --- per-tag sections -----------------------------------------------------
    # Split on H2 headers; keep only those whose title is a known tag name.
    tags = {}
    sections = re.split(r"\n## ", "\n" + txt)
    for sec in sections:
        head, _, body = sec.partition("\n")
        name = clean(head)
        if name not in name_range:
            continue
        summary = ""
        for para in body.split("\n\n"):
            p = para.strip()
            if p and not p.startswith("**") and not re.match(r"^\d+\.", p):
                summary = clean(p)
                break
        subtables = {}
        for label in labels:
            m = re.search(
                r"\*\*%s \(d3\):\*\*\s*(.*?)(?=\n\*\*|\n---|\Z)" % re.escape(label),
                body, re.DOTALL)
            opts = []
            if m:
                for ln in m.group(1).splitlines():
                    mm = re.match(r"\s*([123])\.\s+(.*)$", ln)
                    if mm:
                        opts.append(clean(mm.group(2)))
            subtables[label] = opts
        tags[name] = {
            "d100": list(name_range[name]),
            "summary": summary,
            "subtables": subtables,
        }

    detail = {
        "id": f"wwn.{family}_tags_detail",
        "title": f"{family.capitalize()} Tags",
        "source": "wwn-worldbuilder",
        "kind": "tag_detail",
        "subtable_dice": "1d3",
        "labels": labels,
        "tags": tags,
    }
    flat_tbl = flat(
        f"{family}_tags", f"{family.capitalize()} Tags (d100)",
        "wwn-worldbuilder", 100,
        [(lo, hi, name) for (lo, hi, name) in order],
    )
    return detail, flat_tbl


# ===========================================================================
# Generic markdown-table parsers used by several sources.
# ===========================================================================
def parse_pipe_table(block, die, col=1, roll_col=0):
    """A standard | Roll | Value | pipe table -> [(lo,hi,value)].
    `col` selects the value column index; `roll_col` the roll column."""
    out = []
    for line in block.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) <= max(col, roll_col):
            continue
        if set("".join(cells)) <= set("-:| ") or cells[roll_col].lower() in ("roll", "d100", "d20", "d12", "d10", "d8", "d6", "d4"):
            continue
        if not re.match(r"^\d", cells[roll_col]):
            continue
        lo, hi = parse_range(cells[roll_col], die)
        out.append((lo, hi, cells[col]))
    return out


def parse_loose_table(lines, die):
    """A 'loose' (non-pipe) table where each entry is 'N value' or 'N-M value'
    on its own line.  Handles wrapped continuation lines and the book's
    occasional 'label then number' inversion.  Returns [(lo,hi,value)]."""
    rows = []          # [(lo,hi,[parts])]
    pending_text = None
    for raw in lines:
        ln = clean(raw)
        if not ln:
            continue
        m = re.match(r"^(\d+(?:\s*[-–]\s*\d+)?)\s+(.*)$", ln)
        if m:
            lo, hi = parse_range(m.group(1).replace(" ", ""), die)
            rest = m.group(2).strip()
            if rest:
                rows.append([lo, hi, [rest]])
                pending_text = None
            else:
                # number on its own; value is the line we stashed (book quirk)
                if pending_text is not None:
                    rows.append([lo, hi, [pending_text]])
                    pending_text = None
                else:
                    rows.append([lo, hi, []])
        else:
            # continuation / inverted-label line
            if rows and rows[-1][2] is not None and not _looks_label_first(ln):
                rows[-1][2].append(ln)
            else:
                pending_text = ln
    return [(lo, hi, clean(" ".join(parts))) for lo, hi, parts in rows if parts]


def _looks_label_first(ln):
    return False


# ===========================================================================
# PARSER 2 -- npc_quickgen (multi-column d100 + many d12 + characterization).
# ===========================================================================
def parse_npc_quickgen():
    path = os.path.join(WB, "npc_quickgen.md")
    txt = open(path, encoding="utf-8").read()
    tables = {}

    # d12 NPC Characteristic Twists
    blk = _section(txt, "## d12 NPC Characteristic Twists")
    tables["Characteristic Twists"] = _mini(parse_pipe_table(blk, 12), 12)

    # d100 Random NPC Types -> three flat tables (one per social class column)
    blk = _section(txt, "## d100 Random NPC Types")
    for ci, cls in ((1, "Underclass"), (2, "Commoners"), (3, "Gentry")):
        tables[f"Random NPC ({cls})"] = _mini(
            parse_pipe_table(blk, 100, col=ci), 100)

    # specific d12 role tables (### headers)
    for label, head in (
        ("Specific Criminals", "### Specific Criminals"),
        ("Specific Merchants", "### Specific Merchants"),
        ("Specific Nobility", "### Specific Nobility"),
        ("Specific Tribals", "### Specific Tribals"),
        ("Specific Villagers", "### Specific Villagers"),
        ("Specific Warriors", "### Specific Warriors"),
    ):
        blk = _section(txt, head)
        tables[label] = _mini(parse_pipe_table(blk, 12), 12)

    # characterization d4/d6/d8/d12/d20 (clean wwn-worldbuilder versions)
    for label, head, die in (
        ("Physical Build", "### d4 General Physical Build", 4),
        ("Way They Move", "### d6 The Way They Move", 6),
        ("Clothing", "### d8 Clothing Idiosyncrasies", 8),
        ("How They Differ", "### d12 One Way They Differ From Expectations", 12),
        ("Visible Mannerisms", "### d20 Visible Mannerisms or Traits", 20),
    ):
        blk = _section(txt, head)
        tables[label] = _mini(parse_pipe_table(blk, die), die)

    return bundle("npc_quickgen", "NPC Quickgen",
                  "wwn-worldbuilder (WWN NPC Quickgen)", tables)


# ===========================================================================
# PARSER 3 -- adventure_seeds (d10 Bait, d20 Intro, d100 Fractal Seeds).
# ===========================================================================
def parse_adventure_seeds():
    path = os.path.join(WB, "adventure_seeds.md")
    txt = open(path, encoding="utf-8").read()
    tables = {}

    blk = _section(txt, "## d10 Bait for Adventure Hooks")
    tables["Bait"] = _mini(parse_pipe_table(blk, 10), 10)

    blk = _section(txt, "## d20 Ways of Introducing an Adventure Hook")
    tables["Introduction"] = _mini(parse_pipe_table(blk, 20), 20)

    # Fractal seeds: numbered '1.' lines across 5 sub-headed groups.  These hold
    # OCR debris, so scrub each.  Output one d100 flat table, grouped 1-100.
    seeds = {}
    for m in re.finditer(r"^\s*(\d{1,3})\.\s+(.*)$", txt, re.MULTILINE):
        n = int(m.group(1))
        if 1 <= n <= 100:
            seeds[n] = scrub_seed(m.group(2))
    entries = [(n, n, seeds[n]) for n in sorted(seeds)]
    fractal = flat("fractal_seeds", "Fractal Adventure Seeds (d100)",
                   "wwn-worldbuilder (WWN Fractal Adventure Seeds)", 100,
                   entries)

    seed_bundle = bundle(
        "adventure_seeds", "Adventure Seeds",
        "wwn-worldbuilder (WWN Adventure Seeds)", tables)
    return seed_bundle, fractal


# ===========================================================================
# PARSER 4 -- the three construction files.
# ===========================================================================
def parse_religion():
    txt = open(os.path.join(WB, "religion_construction.md"), encoding="utf-8").read()
    tables = {}
    specs = [
        ("Where Did The God Come From", "## d12 Where Did The God Come From?", 12, 1),
        ("Why Does The Faith Matter", "## d10 Why Does The Faith Matter?", 10, 1),
        ("What Does The Faith Want", "## d12 What Does The Faith Want?", 12, 1),
        ("What This God Does in Society", "## d20 What Does This God Do in Society?", 20, 1),
        ("Particular Religious Requirement", "## d20 Particular Religious Requirements", 20, 1),
    ]
    for label, head, die, col in specs:
        blk = _section(txt, head)
        tables[label] = _mini(parse_pipe_table(blk, die, col=col), die)
    # paired portfolio table: one roll -> both columns
    blk = _section(txt, "## d20 Human Concern + Natural Principle (paired)")
    concern = parse_pipe_table(blk, 20, col=1)
    principle = parse_pipe_table(blk, 20, col=2)
    tables["Human Concern"] = _mini(concern, 20)
    tables["Natural Principle"] = _mini(principle, 20)
    return bundle("religion_construction", "Religion Construction",
                  "wwn-worldbuilder (WWN Religion Construction)", tables)


def parse_nation():
    txt = open(os.path.join(WB, "nation_construction.md"), encoding="utf-8").read()
    tables = {}
    specs = [
        ("Current National Problems", "## d20 Current National Problems", 20),
        ("Good Things Happening Now", "## d20 Good Things Happening Right Now", 20),
        ("Disputes With a Neighbor", "## d20 Disputes With a Neighboring State", 20),
        ("Positive Ties With a Neighbor", "## d20 Positive Ties With a Neighboring State", 20),
        ("Nation Themes", "## d20 Nation Themes", 20),
    ]
    for label, head, die in specs:
        blk = _section(txt, head)
        tables[label] = _mini(parse_pipe_table(blk, die), die)
    return bundle("nation_construction", "Nation Construction",
                  "wwn-worldbuilder (WWN Nation Construction)", tables)


def parse_history():
    """History: bundle of small tables + two big d100 flat companions."""
    txt = open(os.path.join(WB, "history_construction.md"), encoding="utf-8").read()
    tables = {}
    small = [
        ("How Did They Originate", "## d8 How Did They Originate?", 8),
        ("Original Inhabitants", "## d10 What Became of the Original Inhabitants?", 10),
        ("How They Overcame the Crisis", "## d10 How Did They Overcome the Crisis?", 10),
        ("Great About Its Peak", "## d12 What Was Great About Its Peak?", 12),
        ("Why It Failed", "## d12 Why Did It Fail At the Final Crisis?", 12),
        ("Unabsorbed Survivors", "## d12 What Became of the Unabsorbed Survivors?", 12),
    ]
    for label, head, die in small:
        blk = _section(txt, head)
        tables[label] = _mini(parse_pipe_table(blk, die), die)

    blk = _section(txt, "## d100 Historical Crises")
    crises = flat("historical_crises", "Historical Crises (d100)",
                  "wwn-worldbuilder (WWN History Construction)", 100,
                  parse_pipe_table(blk, 100))
    blk = _section(txt, "## d100 Historical Events")
    events = flat("historical_events", "Historical Events (d100)",
                  "wwn-worldbuilder (WWN History Construction)", 100,
                  parse_pipe_table(blk, 100))

    hb = bundle("history_construction", "History Construction",
                "wwn-worldbuilder (WWN History Construction)", tables)
    return hb, crises, events


# ===========================================================================
# PARSER 5 -- Placing Treasures (book).  Silver-value matrix + flavor + magic.
# ===========================================================================
def parse_treasure():
    path = os.path.join(BOOK_WWN, "08 - Creating Adventures",
                        "10 - Placing Treasures.md")
    txt = open(path, encoding="utf-8").read()
    src = "WWN Deluxe, Placing Treasures (pp. 260-261)"

    # --- silver-value matrix: each row is a site type, 5 columns by 2d6 band ---
    # Format lines: "<Site Type> <c1> <c2> <c3> <c4> <c5>" where each cell is a
    # dice expression possibly containing 'x N,NNN'.  Parse from the marked block.
    band_labels = ["2-3", "4-5", "6-8", "9-10", "11-12"]
    silver_rows = []
    start = txt.index("Silver Piece Value of the Site's Contents".replace("'", "’")) \
        if "Silver Piece Value of the Site" in txt.replace("’", "'") else None
    # robust: find header line then read until blank/next header
    region = txt.split("Silver Piece Value", 1)[1]
    region = region.split("|||Chance for Magic", 1)[0]
    cell_re = re.compile(r"\d+d\d+(?:\s*x\s*[\d,]+)?")
    for raw in region.splitlines():
        ln = clean(raw)
        if not ln or ln.startswith("Type of Site") or ln.startswith("Silver"):
            continue
        cells = cell_re.findall(ln)
        if len(cells) != 5:
            continue
        # site name is everything before the first dice cell
        first = cell_re.search(ln)
        name = ln[:first.start()].strip()
        if not name:
            continue
        silver_rows.append((name, [c.replace(" ", "") for c in cells]))

    # --- magic-item count matrix (1d20) ---------------------------------------
    # The block is a wide pipe table with <br>-joined owner rows and per-column
    # ranges.  Reconstruct owners and the four count-columns.
    magic_block = txt.split("|||Chance for Magic", 1)[1].split("d8 Types of Jewelry", 1)[0]
    owners, no_i, one_i, two_i, three_i = [], [], [], [], []
    for line in magic_block.splitlines():
        if "<br>" in line and "|" in line:
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) >= 5 and "N/A" in line or "1–" in line or "1-" in line:
                owners = [clean(x) for x in cells[0].split("<br>")]
                no_i = [clean(x) for x in cells[1].split("<br>")]
                one_i = [clean(x) for x in cells[2].split("<br>")]
                two_i = [clean(x) for x in cells[3].split("<br>")]
                three_i = [clean(x) for x in cells[4].split("<br>")]
                break

    # --- flavor flat tables (d8 / d20) ----------------------------------------
    def loose(head, die):
        blk = _book_loose(txt, head)
        return _mini(parse_loose_table(blk, die), die)

    tables = {}
    tables["Types of Jewelry"] = loose("d8 Types of Jewelry", 8)
    tables["Magic Item Type"] = loose("d20 Type of Magic Item Found", 20)
    tables["Why Object Is Valuable"] = loose("d20 Why is the Object Particularly Valuable?", 20)
    tables["Valuable Objects"] = loose("d20 Valuable Objects or Precious Goods", 20)

    # Encode the silver matrix and magic-count matrix as structured (non-roll)
    # helper blocks the GM/gen.py can drive: pick a row, then roll 2d6 / 1d20.
    silver_matrix = {
        "roll": "2d6",
        "bands": band_labels,
        "rows": {name: dict(zip(band_labels, cells))
                 for name, cells in silver_rows},
    }
    magic_matrix = {
        "roll": "1d20",
        "columns": ["No Items", "One Item", "Two Items", "Three or More"],
        "rows": {owners[i]: {
            "No Items": no_i[i] if i < len(no_i) else "N/A",
            "One Item": one_i[i] if i < len(one_i) else "N/A",
            "Two Items": two_i[i] if i < len(two_i) else "N/A",
            "Three or More": three_i[i] if i < len(three_i) else "N/A",
        } for i in range(len(owners))},
        "item_count_dice": "1d20",
        "magic_item_distribution_table": "Magic Item Type",
    }

    b = bundle("treasure", "Treasure Generation", src, tables)
    b["silver_value_matrix"] = silver_matrix
    b["magic_item_matrix"] = magic_matrix
    b["notes"] = ("Pick the site row, roll 2d6 to choose the column, then roll "
                  "that cell's dice for the trove's silver value. For magic, "
                  "pick the owner row and roll 1d20 for the item count, then "
                  "roll on Magic Item Type per item.")
    return b


# ===========================================================================
# PARSER 6 -- monster_gen (book: shapes/drives + One-Roll Context + powers).
# ===========================================================================
def parse_monster_gen():
    path = os.path.join(BOOK_WWN, "09 - Creatures of A Far Age.md")
    txt = open(path, encoding="utf-8").read()
    src = "WWN Deluxe, Creatures of A Far Age"
    tables = {}

    # --- Monster Shapes -------------------------------------------------------
    tables["Animal Resemblance"] = _mini(
        _loose_split(_book_loose(txt, "d12 What Kind of Animal Is It Most Like?"), 12),
        12)
    tables["How It Hunts"] = _mini(
        parse_loose_table(_book_loose(txt, "d10 How Does It Usually Hunt?"), 10), 10)

    # Basic body plan (d8 with ranged rows 1 / 2-3 / 4-7 / 8) lives in a pipe-ish
    # block; build it explicitly from the known ranges to stay faithful.
    body = [
        (1, 1, "Limbless, amorphous, or a tentacular mass"),
        (2, 3, "Bipedal, generally upright"),
        (4, 7, "Quadrupedal, perhaps able to rear up"),
        (8, 8, "Sexapedal, perhaps with wings and legs"),
    ]
    tables["Basic Body Plan"] = {"type": "list_d8", "dice": "1d8",
                                 "entries": [{"min": a, "max": b, "value": clean(c)}
                                             for a, b, c in body]}
    why = [
        (1, 1, "It requires very little food for survival"),
        (2, 2, "It's poisonous and repels its predators"),
        (3, 3, "It eats something other creatures can't"),
        (4, 4, "It's newly introduced in the area"),
        (5, 5, "It doesn't need food in a normal sense"),
        (6, 6, "It exists in symbiosis with something else"),
    ]
    tables["Why Isn't It Dead Yet"] = {"type": "list_d6", "dice": "1d6",
                                       "entries": [{"min": a, "max": b, "value": clean(c)}
                                                   for a, b, c in why]}

    # --- Monstrous Drives (d12; value = the bold drive NAME) ------------------
    drives = []
    dblock = txt.split("Monstrous Drives", 2)[-1].split("## Uncanny Powers", 1)[0]
    for m in re.finditer(r"^- (\d{1,2})\s+\*\*([A-Za-z]+)\*\*", dblock, re.MULTILINE):
        drives.append((int(m.group(1)), int(m.group(1)), m.group(2)))
    drives.sort()
    tables["Monstrous Drive"] = _mini(drives, 12)

    # --- One-Roll Monstrous Context ------------------------------------------
    tables["How It Arose"] = _mini(
        parse_loose_table(_book_loose(txt, "d4 How Did the Monster Arise?"), 4), 4)
    tables["Connection With the Past"] = _mini(
        parse_loose_table(_book_loose(txt, "d12 What Is Its Connection With the Past?"), 12), 12)
    tables["Local Contact"] = _mini(
        _inline_list(txt, "d6 How Much Local Contact Does It Have?", 6), 6)
    tables["Local Reaction"] = _mini(
        parse_loose_table(_book_loose(txt, "d8 How Do the Locals React To Its Drive?"), 8), 8)
    tables["Scars Left Here"] = _mini(
        parse_loose_table(_book_loose(txt, "d10 What Scars Has It Left Here?"), 10), 10)
    tables["Twist To Its Activities"] = _mini(
        parse_loose_table(_book_loose(txt, "d20 A Twist To Its Activities"), 20), 20)

    # --- Uncanny Powers: pick-lists (not dice).  Capture options + point cost. -
    powers = _parse_power_lists(txt)

    b = bundle("monster_gen", "Monster Generation", src, tables)
    b["uncanny_powers"] = powers
    b["degree_of_power"] = _parse_degree(txt)
    b["notes"] = ("Roll Animal Resemblance, Basic Body Plan, How It Hunts, then "
                  "a Monstrous Drive; optionally a full One-Roll Monstrous "
                  "Context. Uncanny powers are GM pick-lists (point-costed), not "
                  "die rolls -- choose 1-3 to fit the drive. Statblock assembly "
                  "(HD/AC/attacks) is out of scope for this generator.")
    return b


def _parse_power_lists(txt):
    """Capture the five point-costed power pick-lists.  Each row is
    'Points  Power text' (text may wrap).  Keep the cost token + description."""
    out = {}
    spans = [
        ("Damage Infliction", "Points Damage Infliction", "## Movement Powers"),
        ("Movement", "Points Movement Powers", "## Debilitating Powers"),
        ("Debilitating", "Points Debilitating Power", "## Augmenting Powers"),
        ("Augmenting", "Points Augmenting Power", "## Intrinsic Powers"),
        ("Intrinsic", "Points Intrinsic Power", "Spellcasting monsters"),
    ]
    for label, start, end in spans:
        if start not in txt:
            continue
        seg = txt.split(start, 1)[1].split(end, 1)[0]
        items = []
        cur = None
        for raw in seg.splitlines():
            ln = clean(raw)
            if not ln:
                continue
            m = re.match(r"^(x?[-+]?\d+(?:/\d+)?|x\d/\d|x1/2|N/A)\s+(.*)$", ln)
            if m and re.match(r"^(x?[-+]?\d|N/A)", m.group(1)):
                if cur:
                    items.append(cur)
                cur = {"cost": m.group(1), "power": m.group(2)}
            elif cur is not None:
                cur["power"] = clean(cur["power"] + " " + ln)
        if cur:
            items.append(cur)
        out[label] = items
    return out


def _parse_degree(txt):
    seg = txt.split("Total The Creature's Degree of Power".replace("'", "’"), 1)
    if len(seg) < 2:
        seg = txt.split("Degree of Power", 1)
    body = seg[1].split("Even perfectly normal", 1)[0]
    rows = []
    for raw in body.splitlines():
        ln = clean(raw)
        m = re.match(r"^(\d+)\s+(.+)$", ln)
        if m:
            rows.append({"points": int(m.group(1)), "tier": m.group(2)})
    return rows


# ===========================================================================
# PARSER 7 -- Naval Adventuring (Atlas): Seafaring Event, Ship Encounter, Crisis.
# ===========================================================================
def parse_naval():
    path = os.path.join(BOOK_ATLAS, "06 - Naval Adventuring.md")
    txt = open(path, encoding="utf-8").read()
    src = "Atlas of the Latter Earth, Naval Adventuring"
    tables = {}

    # Seafaring Event d10: entries scattered as '- d10 Seafaring Event 1-3 X',
    # then '- 4 X', etc., with a nested '- 10 Crippled Ship' belonging to the
    # Ship Encounter; the standalone Seafaring rows are 1-3,4,5,6,7,8,9,10.
    sea = {}
    # first row carries the header inline
    m = re.search(r"d10 Seafaring Event\s+1-3\s+\*\*(.*?)\*\*\s*:?\s*(.*)", txt)
    if m:
        sea[(1, 3)] = clean(f"{m.group(1)}: {m.group(2)}").strip(": ")
    for m in re.finditer(r"^- (\d{1,2})\s+\*\*(.*?)\*\*\s*:?\s*(.*)$", txt, re.MULTILINE):
        n = int(m.group(1))
        label, desc = clean(m.group(2)), clean(m.group(3))
        val = f"{label}: {desc}".strip(": ")
        # Seafaring events are 4..10 (10 'Damaged Fitting'); the '10 Crippled
        # Ship' line is indented (3 leading spaces) and belongs to Encounter.
        if 4 <= n <= 10 and "Crippled Ship" not in label:
            sea[(n, n)] = val
    sea_entries = [(lo, hi, sea[(lo, hi)]) for (lo, hi) in sorted(sea)]
    tables["Seafaring Event"] = _mini(sea_entries, 10)

    # Ship Encounter d10: a loose block '1-3 Local Trader : ...' through '9 ...'
    # then '- 10 Crippled Ship : Roll again...'.  In the source the Seafaring
    # Event rows 8/9 ('- 8 **Damaged Cargo**' ...) are interleaved *after* the
    # encounter list; cut the block at the first of those bold bullets, then
    # re-attach only the genuine '- 10 Crippled Ship' encounter row.
    enc_region = txt.split("d10 Ship Encounter", 1)[1].split("Buying Ships", 1)[0]
    enc_main = enc_region.split("- 8 **", 1)[0]
    m_crip = re.search(r"- 10\s+\*\*Crippled Ship\*\*\s*:\s*(.*)", enc_region)
    enc = _parse_encounter(enc_main)
    if m_crip:
        enc.append((10, 10, "Crippled Ship: " + clean(m_crip.group(1))))
    tables["Ship Encounter"] = _mini(enc, 10)

    # Ship Crisis d12 (the compact type table)
    crisis_block = txt.split("d12 Ship Crisis Type", 1)[1].split("## ", 1)[0]
    crisis = []
    for raw in crisis_block.splitlines():
        ln = clean(raw)
        m = re.match(r"^(\d+(?:-\d+)?)\s+(.+?)(?:\s+(Acute|Continuing|-))?$", ln)
        if m and re.match(r"^\d", ln):
            lo, hi = parse_range(m.group(1), 12)
            kind = m.group(3) or ""
            val = m.group(2).strip()
            if kind and kind != "-":
                val = f"{val} ({kind})"
            crisis.append((lo, hi, val))
    tables["Ship Crisis"] = _mini(crisis, 12)

    return bundle("naval", "Naval Adventuring", src, tables)


def _parse_encounter(block):
    rows = []
    pending = None
    for raw in block.splitlines():
        ln = clean(raw).lstrip("- ")
        if not ln:
            continue
        m = re.match(r"^(\d+(?:-\d+)?)\s+(.+?)\s*:\s*(.*)$", ln)
        if m:
            lo, hi = parse_range(m.group(1), 10)
            rows.append([lo, hi, clean(m.group(2)), clean(m.group(3))])
        elif rows and not re.match(r"^\d", ln):
            rows[-1][3] = clean(rows[-1][3] + " " + ln)
    return [(lo, hi, (f"{name}: {desc}".strip(": ")))
            for lo, hi, name, desc in rows]


# ===========================================================================
# PARSER 8 -- wounds (Atlas optional): Maiming Wounds d12, Alchemical Accident d6.
# ===========================================================================
def parse_wounds():
    path = os.path.join(BOOK_ATLAS, "04 - Optional Rules and Classes.md")
    txt = open(path, encoding="utf-8").read()
    src = "Atlas of the Latter Earth, Optional Rules"
    tables = {}

    # Maiming Wounds d12 -- the book renders this as a two-column table flattened
    # by OCR: some rows are inline ('4 Lamed : ...'); others put the label first
    # then the number on its own line ('Leg loss : ...' / '7' / 'prosthesis').
    mw_block = txt.split("d12 Maiming Wound", 1)[1].split("A repeated result", 1)[0]
    tables["Maiming Wound"] = _mini(_parse_maiming(mw_block), 12)

    # Alchemical Accident d6 -- bulleted, number-on-second-line inversion:
    #   - **Explosion** : suffer ...,
    #   - 1 double for a greater work. Lab destroyed.
    acc = _parse_alchemical(txt)
    tables["Alchemical Accident"] = _mini(acc, 6)

    return bundle("wounds", "Wounds and Mishaps", src, tables)


def _parse_maiming(block):
    """Reconstruct the d12 Maiming Wound two-column scan.  Walk the lines,
    maintaining a 'current entry' that the bare-number lines bind to and the
    continuation lines extend.

      '4 Lamed : ...'        -> entry 4, label inline
      'Ugly scar : -1 ...'   -> a fresh label awaiting its number
      '5'                    -> bind the pending label to entry 5
      'skill checks'         -> continuation of entry 5
    """
    entries = {}            # n -> value
    pending_label = None    # text of a label seen before its number
    last_n = None           # most recently completed number (for continuations)
    for raw in block.splitlines():
        ln = clean(raw)
        if not ln:
            continue
        m_inline = re.match(r"^(\d{1,2})\s+(.+)$", ln)
        m_bare = re.match(r"^(\d{1,2})$", ln)
        if m_bare:
            n = int(m_bare.group(1))
            entries[n] = pending_label or ""
            pending_label = None
            last_n = n
        elif m_inline:
            n = int(m_inline.group(1))
            entries[n] = clean(m_inline.group(2))
            pending_label = None
            last_n = n
        else:
            # a label-first line (has ' : ') starts a new pending entry;
            # a plain fragment continues whichever entry is open.
            if " : " in ln and pending_label is None and (
                    last_n is None or entries.get(last_n)):
                pending_label = ln
            elif pending_label is not None:
                pending_label = clean(pending_label + " " + ln)
            elif last_n is not None:
                entries[last_n] = clean(entries[last_n] + " " + ln)
    # normalize ' : ' -> ': '
    out = []
    for n in sorted(entries):
        val = re.sub(r"\s*:\s*", ": ", entries[n], count=1).strip()
        out.append((n, n, val))
    return out


def _parse_alchemical(block_txt):
    """Reconstruct the d6 Alchemical Accident two-column scan.

      '- **Explosion** : suffer ...,'        -> label + pre-text for next number
      '- 1 double for a greater work. ...'   -> entry 1 = label + pre + tail
      '- 4 unusable ... **Broken Tool** : ..'-> entry 4 tail AND entry 5 label
    """
    block = block_txt.split("d6 Alchemical Accident", 1)[1].split(
        "## Using Alchemical", 1)[0]
    items = {}
    cur_label = None
    cur_pre = ""
    for raw in block.splitlines():
        ln = clean(raw).lstrip("- ").strip()
        if not ln:
            continue
        mn = re.match(r"^(\d)\s+(.*)$", ln)
        if mn:
            n = int(mn.group(1))
            tail = mn.group(2)
            # a number-line may also embed the NEXT entry's '**Label** :' tail
            split = re.split(r"\*\*(.+?)\*\*\s*:?\s*", tail, maxsplit=1)
            if len(split) == 3:
                tail_here, next_label, next_pre = split
            else:
                tail_here, next_label, next_pre = tail, None, ""
            desc = clean((cur_pre + " " + tail_here).strip())
            # leading stray digit from OCR ('3 3 System Strain') -> drop one
            desc = re.sub(r"^(\d)\s+(?=[A-Za-z])", "", desc)
            items[n] = f"{cur_label}: {desc}".strip(": ") if cur_label else desc
            if next_label:
                cur_label = clean(next_label)
                cur_pre = clean(next_pre)
            else:
                cur_label = None
                cur_pre = ""
        else:
            ml = re.match(r"^\*\*(.+?)\*\*\s*:?\s*(.*)$", ln)
            if ml:
                cur_label = clean(ml.group(1))
                cur_pre = clean(ml.group(2))
            elif cur_label:
                cur_pre = clean(cur_pre + " " + ln)
    return [(n, n, items[n]) for n in sorted(items)]


# ===========================================================================
# PARSER 9 -- npc_depth (book One-Roll Characterization depth + architecture).
# Unique book content not present in wwn-worldbuilder.
# ===========================================================================
def parse_npc_depth():
    path = os.path.join(BOOK_WWN, "15 - Additional GM Tools.md")
    txt = open(path, encoding="utf-8").read()
    src = "WWN Deluxe, Additional GM Tools"

    # d10 The First Thing Noticed (book-only; complements npc_quickgen)
    tables = {}
    tables["First Thing Noticed"] = _mini(
        parse_loose_table(_book_loose(txt, "d10 The First Thing Noticed"), 10), 10)

    # Burning Ambitions
    tables["Ambition Form"] = _mini(
        parse_loose_table(_book_loose(txt, "d10 What's the Basic Ambition's Form?".replace("'", "’")), 10), 10)
    tables["Ambition Obstacle"] = _mini(
        parse_loose_table(_book_loose(txt, "d12 What's the Biggest Immediate Obstacle?".replace("'", "’")), 12), 12)
    tables["Ambition Help or Hinder"] = _mini(
        parse_loose_table(_book_loose(txt, "d20 Things to Help or Hinder the Ambition"), 20), 20)
    tables["Ambition Who Knows"] = _mini(_inline_list(txt, "d6 Who Knows or Has Been Involved in It?", 6), 6)
    tables["Ambition Tools Used"] = _mini(_inline_list(txt, "d8 What Tools Are Used to Advance It?", 8), 8)

    # Personal Tragedies
    tables["Tragedy Form"] = _mini(
        parse_loose_table(_book_loose(txt, "d10 What Was Its Basic Form?"), 10), 10)
    tables["Tragedy Coping"] = _mini(
        parse_loose_table(_book_loose(txt, "d8 How Did They Try to Cope With It?"), 8), 8)
    tables["Tragedy Consequences"] = _mini(
        parse_loose_table(_book_loose(txt, "d12 What Ugly Consequences Followed?"), 12), 12)
    tables["Tragedy Scars"] = _mini(
        parse_loose_table(_book_loose(txt, "d20 What Scars Do They Have From It?"), 20), 20)

    # Close Friendships
    tables["Friendship What Done Together"] = _mini(
        parse_loose_table(_book_loose(txt, "d8 What Have They Done Together?"), 8), 8)
    tables["Friendship Harmonizing Tie"] = _mini(
        parse_loose_table(_book_loose(txt, "d10 What Tie Harmonizes Their Differences?"), 10), 10)
    tables["Friendship What Divides"] = _mini(
        parse_loose_table(_book_loose(txt, "d12 What Threatens to Divide Them?"), 12), 12)
    tables["Friendship Things Between"] = _mini(
        parse_loose_table(_book_loose(txt, "d20 Things Between Friends"), 20), 20)

    # Troubled Romances
    tables["Romance Spark"] = _mini(
        parse_loose_table(_book_loose(txt, "d8 What Sparked the Romance?"), 8), 8)
    tables["Romance Problem"] = _mini(
        parse_loose_table(_book_loose(txt, "d10 What Problem Does One or Both Have?"), 10), 10)
    tables["Romance Current Issue"] = _mini(
        parse_loose_table(_book_loose(txt, "d12 What's the Current Issue They Face?".replace("'", "’")), 12), 12)
    tables["Romance Quirks"] = _mini(
        parse_loose_table(_book_loose(txt, "d20 Quirks or Traits of the Relationship"), 20), 20)

    return bundle("npc_depth", "NPC One-Roll Characterization (Depth)", src, tables)


def parse_architecture():
    path = os.path.join(BOOK_WWN, "15 - Additional GM Tools.md")
    txt = open(path, encoding="utf-8").read()
    src = "WWN Deluxe, Additional GM Tools (Architectural Style Generators)"
    tables = {}
    for label, head in (
        ("Architectural Adjectives", "d8 Architectural Adjectives"),
        ("Favorite Materials", "d8 Favorite Materials"),
        ("Favorite Color Schemes", "d8 Favorite Color Schemes"),
        ("Common Visual Motifs", "d8 Common Visual Motifs"),
        ("Structure Adornment", "d8 Structure Adornment"),
        ("Favorite Structural Features", "d8 Favorite Structural Features"),
        ("Settlement Design Patterns", "d8 Settlement Design Patterns"),
    ):
        tables[label] = _mini(parse_loose_table(_book_loose(txt, head), 8), 8)
    return bundle("architecture", "Architectural Style Generators", src, tables)


# ===========================================================================
# Small shared helpers.
# ===========================================================================
def _section(txt, header):
    """Slice from a markdown header to the next '## ' / '### ' / EOF."""
    idx = txt.find(header)
    if idx < 0:
        raise ValueError(f"section not found: {header!r}")
    after = txt[idx + len(header):]
    # stop at the next header of equal-or-higher level
    nxt = re.search(r"\n#{2,3} ", after)
    return after[:nxt.start()] if nxt else after


def _book_loose(txt, header):
    """Return the lines of a non-pipe ('loose') book table that begins right
    after a `dNN <Title>` header line, up to a blank line / next 'dNN ' header
    / next '## ' header."""
    idx = txt.find(header)
    if idx < 0:
        raise ValueError(f"loose table not found: {header!r}")
    rest = txt[idx + len(header):]
    out = []
    for raw in rest.splitlines():
        ln = raw.rstrip()
        s = clean(ln)
        if out and (not s or re.match(r"^d\d+\s+[A-Z]", s) or s.startswith("## ")
                    or s.startswith("|")):
            break
        if s and not re.match(r"^d\d+\s+[A-Z]", s):
            out.append(ln)
    return out


def _inline_list(txt, header, die):
    """Book quirk: some tables are crammed onto one line as
    '- dN Title 1 a 2 b 3 c ...'.  Split into rows on ' N '."""
    idx = txt.find(header)
    if idx < 0:
        raise ValueError(f"inline list not found: {header!r}")
    line = clean(txt[idx + len(header):].splitlines()[0])
    # parse leading number-delimited segments
    pairs = re.findall(r"(\d+)\s+(.*?)(?=\s+\d+\s+|$)", line)
    out = []
    for n, val in pairs:
        n = int(n)
        if 1 <= n <= die:
            out.append((n, n, clean(val)))
    return out


def _loose_split(lines, die):
    """Variant of parse_loose_table for 'N Label : description' rows where we
    want 'Label: description' as the value."""
    out = []
    for raw in lines:
        ln = clean(raw)
        m = re.match(r"^(\d+(?:-\d+)?)\s+(.*?)\s*:\s*(.*)$", ln)
        if m:
            lo, hi = parse_range(m.group(1), die)
            out.append((lo, hi, f"{m.group(2)}: {m.group(3)}".strip(": ")))
        else:
            m2 = re.match(r"^(\d+(?:-\d+)?)\s+(.+)$", ln)
            if m2:
                lo, hi = parse_range(m2.group(1), die)
                out.append((lo, hi, m2.group(2)))
    return out


def _mini(entries, die):
    """Wrap (lo,hi,value) rows into the in-bundle table shape."""
    return {
        "type": f"list_d{die}",
        "dice": f"1d{die}",
        "entries": [{"min": lo, "max": hi, "value": clean(v)}
                    for (lo, hi, v) in entries],
    }


def bundle(slug, title, source, tables):
    return {
        "id": f"wwn.{slug}",
        "title": title,
        "source": source,
        "kind": "bundle",
        "tables": tables,
    }


# ===========================================================================
# Verification.
# ===========================================================================
def verify_flat_entries(entries, die):
    """Return list of problem strings for one table's entries vs its die."""
    problems = []
    rows = sorted(entries, key=lambda e: e["min"])
    expect = 1
    for e in rows:
        if e["min"] > e["max"]:
            problems.append(f"inverted range {e['min']}-{e['max']}")
        if e["min"] != expect:
            problems.append(f"gap/overlap: expected {expect}, got {e['min']}")
        expect = e["max"] + 1
    if expect - 1 != die:
        problems.append(f"covers 1..{expect-1}, expected 1..{die}")
    return problems


def die_of(table):
    t = table.get("type", "")
    m = re.match(r"list_d(\d+)", t)
    return int(m.group(1)) if m else None


def verify_record(rec):
    """Verify one emitted JSON record; return list of issue strings."""
    issues = []
    rid = rec.get("id", "?")
    kind = rec.get("kind")
    if kind == "tag_detail":
        # companion flat table is verified separately; here check sub-table
        # presence and d100 coverage of the tag set.
        ranges = [tuple(v["d100"]) for v in rec["tags"].values()]
        ents = [{"min": a, "max": b} for a, b in ranges]
        for p in verify_flat_entries(ents, 100):
            issues.append(f"{rid} (tag d100): {p}")
        for name, v in rec["tags"].items():
            for label in rec["labels"]:
                opts = v["subtables"].get(label, [])
                if len(opts) != 3:
                    issues.append(f"{rid}: tag '{name}' {label} has {len(opts)} (want 3)")
            if not v.get("summary"):
                issues.append(f"{rid}: tag '{name}' missing summary")
    elif kind == "bundle":
        for tname, tbl in rec["tables"].items():
            die = die_of(tbl)
            if die is None:
                issues.append(f"{rid}/{tname}: no list_dN type")
                continue
            for p in verify_flat_entries(tbl["entries"], die):
                issues.append(f"{rid}/{tname}: {p}")
    else:
        die = die_of(rec)
        if die is None:
            issues.append(f"{rid}: not a flat list table")
        else:
            for p in verify_flat_entries(rec["entries"], die):
                issues.append(f"{rid}: {p}")
    return issues


def count_entries(rec):
    if rec.get("kind") == "tag_detail":
        return len(rec["tags"])
    if rec.get("kind") == "bundle":
        return sum(len(t["entries"]) for t in rec["tables"].values())
    return len(rec.get("entries", []))


# ===========================================================================
# Build orchestration.
# ===========================================================================
def write_json(name, obj):
    path = os.path.join(OUT_DIR, name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return path


def build(quiet=False):
    os.makedirs(OUT_DIR, exist_ok=True)
    records = []          # (filename, record)

    # 1) tag families -> detail + flat companion
    for fam in ("character", "community", "court", "ruin", "wilderness"):
        detail, flat_tbl = parse_tag_family(fam)
        records.append((f"{fam}_tags_detail.json", detail))
        records.append((f"{fam}_tags.json", flat_tbl))

    # 2) npc quickgen bundle
    records.append(("npc_quickgen.json", parse_npc_quickgen()))

    # 3) adventure seeds bundle + fractal seeds flat
    seed_bundle, fractal = parse_adventure_seeds()
    records.append(("adventure_seeds.json", seed_bundle))
    records.append(("fractal_seeds.json", fractal))

    # 4) construction
    records.append(("religion_construction.json", parse_religion()))
    records.append(("nation_construction.json", parse_nation()))
    hist_bundle, crises, events = parse_history()
    records.append(("history_construction.json", hist_bundle))
    records.append(("historical_crises.json", crises))
    records.append(("historical_events.json", events))

    # 5-8) book Tier-1
    records.append(("treasure.json", parse_treasure()))
    records.append(("monster_gen.json", parse_monster_gen()))
    records.append(("naval.json", parse_naval()))
    records.append(("wounds.json", parse_wounds()))

    # 9) book unique extras
    records.append(("npc_depth.json", parse_npc_depth()))
    records.append(("architecture.json", parse_architecture()))

    # verify + write
    all_issues = []
    manifest_gens = []
    for fname, rec in records:
        issues = verify_record(rec)
        all_issues.extend(issues)
        path = write_json(fname, rec)
        manifest_gens.append({
            "id": rec["id"],
            "file": f"generators/{fname}",
            "type": rec.get("kind", rec.get("type", "?")),
            "entries": count_entries(rec),
        })

    # Fold in HAND-AUTHORED generators (not built from source here, e.g.
    # geography_construction.json) so a rebuild doesn't silently drop them from
    # the manifest. Any generators/*.json not written above is treated as
    # hand-authored and preserved in the manifest.
    import glob as _glob
    generated = {fname for fname, _ in records} | {"manifest.json"}
    for _p in sorted(_glob.glob(os.path.join(OUT_DIR, "*.json"))):
        _fn = os.path.basename(_p)
        if _fn in generated:
            continue
        try:
            _rec = json.load(open(_p, encoding="utf-8"))
        except Exception:
            continue
        manifest_gens.append({
            "id": _rec.get("id", _fn) if isinstance(_rec, dict) else _fn,
            "file": f"generators/{_fn}",
            "type": (_rec.get("kind", _rec.get("type", "hand-authored"))
                     if isinstance(_rec, dict) else "hand-authored"),
            "entries": count_entries(_rec) if isinstance(_rec, dict) else 0,
            "hand_authored": True,
        })

    verification = "PASSED" if not all_issues else "FAILED"
    manifest = {
        "built": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source_wwn_worldbuilder": WB,
        "source_book": SKILL_ROOT,
        "generators": manifest_gens,
        "verification": verification,
        "issues": all_issues,
    }
    write_json("manifest.json", manifest)

    if quiet:
        print(f"verification: {verification}  ({len(manifest_gens)} files, "
              f"{len(all_issues)} issues)")
    else:
        print("=" * 64)
        print(f"WWN generator build  ->  {OUT_DIR}")
        print("=" * 64)
        for g in manifest_gens:
            print(f"  {g['type']:11}  {g['entries']:>4}  {g['file']}")
        print("-" * 64)
        print(f"  files: {len(manifest_gens)}   verification: {verification}")
        if all_issues:
            print(f"  ISSUES ({len(all_issues)}):")
            for p in all_issues[:40]:
                print("   X", p)
    return manifest


if __name__ == "__main__":
    build(quiet="--quiet" in sys.argv[1:])
