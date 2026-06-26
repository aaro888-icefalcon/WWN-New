#!/usr/bin/env python3
"""
gen.py — roll the WWN generators with HONEST, SHOWN dice.

Every random draw is printed transparently, e.g.

    1d100 -> [42] = 42

so a reader can audit the result.  Dice never decide silently and nothing is
fudged.  Reproduce any run with --seed N.

By default an internal roller is used so the script is fully standalone.  If the
env var MYTHIC_GM_DICE is set (to the engine's dice.py or just any truthy
value), gen.py prints a one-line note that the engine roller is available; the
honest roll itself is still produced and shown here in the same format, so
behaviour and reproducibility are unchanged.

USAGE
  python3 scripts/gen.py <generator> [--full] [--seed N]

  <generator> may be:
    * any flat table id/slug, e.g.  community_tags  fractal_seeds
      historical_crises  wilderness_tags
    * a bundle table, addressed as  <bundle>/<Table Name>, e.g.
      naval/"Ship Encounter"   monster_gen/"Monstrous Drive"
      npc_quickgen/"Random NPC (Gentry)"
    * a composed recipe:
        settlement   community tag + its 5 d3 sub-tables
        court        court tag + its 5 d3 sub-tables
        ruin         ruin tag (+ a monster_gen drive/shape) + 5 sub-tables
        wilderness   wilderness tag + its 5 d3 sub-tables
        npc          quickgen role + d12 twist + appearance + a character Ambition
        hook         one fractal seed filled with Enemy/Friend/Complication/
                     Thing/Place drawn live from a freshly-rolled location tag

  --full   when rolling a flat *_tags table or a recipe, also expand the
           rolled tag's d3 sub-tables (recipes already expand; --full adds the
           tag summary text).
  --seed N reproducible dice.

Std-lib only; Python 3.6+.
"""
import json
import os
import random
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(HERE)
GEN = os.path.join(SKILL_ROOT, "bridge", "generators")


# ---------------------------------------------------------------------------
# Honest dice.  Format: "1d100 -> [42] = 42",  "1d3 -> [2] = 2".
# ---------------------------------------------------------------------------
class Roller:
    def __init__(self, seed=None):
        self.rng = random.Random(seed)
        self.engine = os.environ.get("MYTHIC_GM_DICE")
        self.log = []

    def roll(self, sides, label=None):
        n = self.rng.randint(1, sides)
        line = f"1d{sides} -> [{n}] = {n}"
        if label:
            line = f"{label}: {line}"
        print("   " + line)
        self.log.append(line)
        return n

    def banner(self):
        if self.engine:
            print(f"[dice] engine roller available at MYTHIC_GM_DICE="
                  f"{self.engine}; rolls shown below are honest and reproducible.")


# ---------------------------------------------------------------------------
# Data access.
# ---------------------------------------------------------------------------
def load(fname):
    p = os.path.join(GEN, fname)
    if not os.path.exists(p):
        return None
    return json.load(open(p, encoding="utf-8"))


def die_of(tbl):
    m = re.match(r"list_d(\d+)", tbl.get("type", ""))
    return int(m.group(1)) if m else None


def pick(tbl, r):
    for e in tbl["entries"]:
        if e["min"] <= r <= e["max"]:
            return e["value"]
    return None


def roll_table(roller, tbl, label=None):
    """Roll one flat/in-bundle table dict; return its value, dice shown."""
    die = die_of(tbl)
    r = roller.roll(die, label)
    return pick(tbl, r)


# Map a flat-table slug -> filename (for direct `gen.py <slug>`).
FLAT_FILES = {
    "character_tags": "character_tags.json",
    "community_tags": "community_tags.json",
    "court_tags": "court_tags.json",
    "ruin_tags": "ruin_tags.json",
    "wilderness_tags": "wilderness_tags.json",
    "fractal_seeds": "fractal_seeds.json",
    "historical_crises": "historical_crises.json",
    "historical_events": "historical_events.json",
}

BUNDLE_FILES = {
    "npc_quickgen": "npc_quickgen.json",
    "adventure_seeds": "adventure_seeds.json",
    "religion_construction": "religion_construction.json",
    "nation_construction": "nation_construction.json",
    "history_construction": "history_construction.json",
    "treasure": "treasure.json",
    "monster_gen": "monster_gen.json",
    "naval": "naval.json",
    "wounds": "wounds.json",
    "npc_depth": "npc_depth.json",
    "architecture": "architecture.json",
}

TAG_DETAIL = {
    "settlement": "community",
    "community": "community",
    "court": "court",
    "ruin": "ruin",
    "wilderness": "wilderness",
    "character": "character",
}


def load_tag_detail(family):
    return load(f"{family}_tags_detail.json")


def roll_tag_subtables(roller, detail, tag_name):
    """Roll d3 on each sub-table of one tag; print and return {label: value}."""
    rec = detail["tags"][tag_name]
    out = {}
    for label in detail["labels"]:
        opts = rec["subtables"].get(label, [])
        if not opts:
            continue
        r = roller.roll(3, f"{label} (d3)")
        idx = min(r, len(opts)) - 1
        val = opts[idx]
        out[label] = val
        print(f"     -> {label}: {val}")
    return out


def roll_tag(roller, family, full=False):
    """Roll the d100 tag for a family off its flat companion, returning the
    tag name plus the detail record (so callers can expand sub-tables)."""
    flat = load(f"{family}_tags.json")
    detail = load_tag_detail(family)
    r = roller.roll(100, f"{family} tag (d100)")
    name = pick(flat, r)
    print(f"     -> {family.capitalize()} tag: {name}")
    if full and detail and name in detail["tags"]:
        print(f"        {detail['tags'][name]['summary']}")
    return name, detail


# ---------------------------------------------------------------------------
# Recipes.
# ---------------------------------------------------------------------------
def recipe_location(roller, family, title, full=False, extra=None):
    """settlement / court / ruin / wilderness: a tag + its 5 d3 sub-tables."""
    print(f"=== {title} ===")
    name, detail = roll_tag(roller, family, full=True)
    if extra:
        extra(roller)
    print(f"   {family} tag sub-tables:")
    subs = roll_tag_subtables(roller, detail, name)
    print()
    print(f"RESULT — {title}: {name}")
    summ = detail["tags"].get(name, {}).get("summary") if detail else None
    if summ:
        print(f"  {summ}")
    for label in detail["labels"]:
        if label in subs:
            print(f"  {label}: {subs[label]}")
    return name, subs


def _ruin_monster(roller):
    """Ruins get a monstrous flavor: shape + drive from monster_gen."""
    mg = load("monster_gen.json")
    if not mg:
        return
    print("   resident threat (monster_gen):")
    shape = roll_table(roller, mg["tables"]["Animal Resemblance"], "animal (d12)")
    print(f"     -> resembles: {shape}")
    drive = roll_table(roller, mg["tables"]["Monstrous Drive"], "drive (d12)")
    print(f"     -> drive: {drive}")


def recipe_npc(roller, full=False):
    """quickgen role + d12 twist + an appearance + a character-tag Ambition."""
    print("=== NPC ===")
    nq = load("npc_quickgen.json")
    cd = load("character_tags_detail.json")

    # social class: roll d3 to choose Underclass/Commoners/Gentry honestly
    classes = ["Underclass", "Commoners", "Gentry"]
    c = roller.roll(3, "social class (d3)")
    cls = classes[c - 1]
    role = roll_table(roller, nq["tables"][f"Random NPC ({cls})"],
                      f"role · {cls} (d100)")
    print(f"     -> role: {role}")

    twist = roll_table(roller, nq["tables"]["Characteristic Twists"], "twist (d12)")
    print(f"     -> twist: {twist}")

    build = roll_table(roller, nq["tables"]["Physical Build"], "build (d4)")
    move = roll_table(roller, nq["tables"]["Way They Move"], "movement (d6)")
    manner = roll_table(roller, nq["tables"]["Visible Mannerisms"], "mannerism (d20)")
    print(f"     -> appearance: {build}; {move}; {manner}")

    # a character-tag Ambition (gives the NPC a drive)
    r = roller.roll(100, "character tag (d100)")
    ctag = pick(load("character_tags.json"), r)
    print(f"     -> character tag: {ctag}")
    amb_opts = cd["tags"][ctag]["subtables"]["Ambitions"]
    a = roller.roll(3, "Ambition (d3)")
    ambition = amb_opts[min(a, len(amb_opts)) - 1]
    print(f"     -> Ambition: {ambition}")

    print()
    print("RESULT — NPC")
    print(f"  Class/Role : {cls} — {role}")
    print(f"  Twist      : {twist}")
    print(f"  Appearance : {build}; {move}; {manner}")
    print(f"  Tag        : {ctag}")
    print(f"  Ambition   : {ambition}")
    if full and cd["tags"][ctag].get("summary"):
        print(f"  (tag) {cd['tags'][ctag]['summary']}")


def recipe_hook(roller, full=False):
    """One fractal seed filled with Enemy/Friend/Complication/Thing/Place drawn
    LIVE from a freshly-rolled location tag's sub-tables, plus Bait + Intro."""
    print("=== ADVENTURE HOOK ===")
    seeds = load("fractal_seeds.json")
    seedsb = load("adventure_seeds.json")

    # 1) draw a location tag and roll its 5 component sub-tables -> the pools
    #    a hook fills from.  Use community tags as the default location flavor.
    print("   location tag (provides Enemy/Friend/Complication/Thing/Place):")
    name, detail = roll_tag(roller, "community", full=True)
    pools = roll_tag_subtables(roller, detail, name)
    # detail labels are Enemies/Friends/Complications/Things/Places (plural);
    # the seed placeholders are singular.  Map them.
    plural = {"Enemy": "Enemies", "Friend": "Friends",
              "Complication": "Complications", "Thing": "Things",
              "Place": "Places"}

    # 2) roll the structural seed
    print("   structural premise:")
    s = roller.roll(100, "fractal seed (d100)")
    seed = pick(seeds, s)
    print(f"     -> seed {s}: {seed}")

    # 3) fill singular placeholders with the rolled component (case-insensitive
    #    whole-word replace; the seed text uses 'Enemy', 'Friend', ...).
    filled = seed
    for singular, pl in plural.items():
        val = pools.get(pl)
        if not val:
            continue
        filled = re.sub(rf"\b{singular}\b", f"{singular} [{val}]", filled, count=99)

    # 4) bait + introduction
    print("   bait & introduction:")
    bait = roll_table(roller, seedsb["tables"]["Bait"], "bait (d10)")
    print(f"     -> bait: {bait}")
    intro = roll_table(roller, seedsb["tables"]["Introduction"], "introduction (d20)")
    print(f"     -> introduction: {intro}")

    print()
    print("RESULT — HOOK")
    print(f"  Location tag : {name}")
    print(f"  Components    :")
    for singular, pl in plural.items():
        if pools.get(pl):
            print(f"    {singular}: {pools[pl]}")
    print(f"  Seed (filled) : {filled}")
    print(f"  Bait          : {bait}")
    print(f"  Introduction  : {intro}")


RECIPES = {
    "settlement": lambda r, full: recipe_location(r, "community", "SETTLEMENT", full),
    "court": lambda r, full: recipe_location(r, "court", "COURT", full),
    "ruin": lambda r, full: recipe_location(r, "ruin", "RUIN", full, extra=_ruin_monster),
    "wilderness": lambda r, full: recipe_location(r, "wilderness", "WILDERNESS", full),
    "npc": recipe_npc,
    "hook": recipe_hook,
}


# ---------------------------------------------------------------------------
# Dispatch.
# ---------------------------------------------------------------------------
def run_flat(roller, slug, full):
    fname = FLAT_FILES[slug]
    tbl = load(fname)
    print(f"=== {tbl['title']} ===")
    die = die_of(tbl)
    r = roller.roll(die, slug)
    val = pick(tbl, r)
    print(f"RESULT: {val}")
    # --full on a *_tags flat table -> expand its sub-tables
    if full and slug.endswith("_tags"):
        fam = slug[:-5]
        detail = load_tag_detail(fam)
        if detail and val in detail["tags"]:
            rec = detail["tags"][val]
            print(f"  {rec['summary']}")
            for label in detail["labels"]:
                opts = rec["subtables"].get(label, [])
                rr = roller.roll(3, f"{label} (d3)")
                print(f"    {label}: {opts[min(rr,len(opts))-1]}")


def run_bundle_table(roller, bundle_slug, table_name):
    doc = load(BUNDLE_FILES[bundle_slug])
    if not doc:
        sys.exit(f"No bundle '{bundle_slug}'.")
    tables = doc["tables"]
    if table_name not in tables:
        # fuzzy-ish: case-insensitive match
        low = {k.lower(): k for k in tables}
        key = low.get(table_name.lower())
        if not key:
            sys.exit(f"Bundle '{bundle_slug}' has no table '{table_name}'. "
                     f"Tables: {', '.join(tables)}")
        table_name = key
    print(f"=== {doc['title']} :: {table_name} ===")
    val = roll_table(roller, tables[table_name], table_name)
    print(f"RESULT: {val}")


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return
    full = "--full" in args
    seed = None
    if "--seed" in args:
        seed = int(args[args.index("--seed") + 1])
    pos = [a for i, a in enumerate(args)
           if not a.startswith("--") and not (i > 0 and args[i - 1] == "--seed")]
    if not pos:
        sys.exit("Need a generator name. See --help.")
    target = pos[0]

    roller = Roller(seed)
    roller.banner()

    if target in RECIPES:
        RECIPES[target](roller, full)
    elif "/" in target:
        b, t = target.split("/", 1)
        run_bundle_table(roller, b, t)
    elif target in FLAT_FILES:
        run_flat(roller, target, full)
    elif target in BUNDLE_FILES:
        # rolling a whole bundle by name: roll every table once
        doc = load(BUNDLE_FILES[target])
        print(f"=== {doc['title']} (all tables) ===")
        for tname, tbl in doc["tables"].items():
            val = roll_table(roller, tbl, tname)
            print(f"   RESULT {tname}: {val}")
    else:
        sys.exit(f"Unknown generator '{target}'.\n"
                 f"Recipes: {', '.join(RECIPES)}\n"
                 f"Flat: {', '.join(FLAT_FILES)}\n"
                 f"Bundles (use <bundle>/<Table>): {', '.join(BUNDLE_FILES)}")


if __name__ == "__main__":
    main()
