#!/usr/bin/env python3
"""
worldgen.py — build & grow a WORLDS WITHOUT NUMBER world with HONEST, SHOWN dice.

This is the Session-Zero WORLDGEN subroutine and the on-demand frontier grower.
It does NOT re-implement any generator data or dice logic: it imports the tag /
recipe primitives from gen.py (same scripts/ folder) — the same Roller, table
loaders, tag rollers and pickers gen.py's own recipes use — and composes the
rolled pieces into a clean markdown **DRAFT CANON** block the agent shows the
player and — once they approve — pastes into `bridge/setting-canon.md` and seeds
into the engine Lists.  (gen.py can equally be shelled as `gen.py settlement`
etc.; we import so the rolled fields can be folded straight into canon.)

Every die is printed transparently to STDERR while rolling, e.g.

    1d100 -> [42] = 42

so the result can be audited.  Nothing is fudged.  Reproduce a run with --seed.
The DRAFT CANON block itself is printed to STDOUT (so `worldgen.py … > x.md`
captures just the committable text); the honest dice trace goes to STDERR.

If env MYTHIC_GM_DICE is set, gen.py's banner notes the engine roller is
available; rolls remain honest and reproducible either way (we reuse gen.py's
Roller, which already honours that contract).

USAGE
  python3 scripts/worldgen.py <command> [--fresh] [--seed N]

  settlement | court | ruin | wilderness
        A fully-expanded place — the same tag + its 5 d3 sub-tables gen.py's
        recipes roll (via the shared gen.py primitives), reframed as a short
        DRAFT CANON place stub.

  nation [--fresh] [--seed N]
        A faction-ready nation brief: nation_construction (2 problems = hooks,
        1 good thing, 1 theme, 1 tension) + a ruling court (court tag) + a
        notable figure (NPC) + a name flavor.  --fresh rolls an origin from
        history_construction; default seeds the name from Latter-Earth canon.

  region [--fresh] [--seed N]
        A starting region as committable draft canon: a wilderness/terrain tag
        + 1-2 settlements + a nearby ruin + 2-3 hooks (fractal_seeds).

  world --scope <region|few-nations|continent> [--fresh] [--seed N]
        Scaffold a world at the chosen scope by composing the above:
          region       = 1 detailed region (== `region`).
          few-nations  = 2-4 nation briefs + 1 shared tension + a start region.
          continent    = a sketch: 4-6 one-line nations + a relations map.
        --fresh generates names/history from scratch (history_construction);
        without it, assume Latter-Earth seeding (hooks left to attach to canon).

Keep every generated place SHORT — this is a frontier sketch, not a novel.
Only the starting region should be built in detail; grow the rest on demand.

Std-lib only; Python 3.6+.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(HERE)

# Reuse gen.py's data + dice logic wholesale (no duplication): we import its
# Roller, table loaders, tag rollers and pickers and call them directly.  gen.py
# prints its dice to STDOUT; we redirect that to STDERR so STDOUT stays clean
# markdown.  (gen.py can also be shelled as `gen.py <recipe>` for the same
# place recipes; importing lets us structure the rolled pieces into canon.)
sys.path.insert(0, HERE)
import gen  # noqa: E402  (Roller, load, roll_tag, roll_tag_subtables, roll_table, pick, die_of, recipe_*)


# ---------------------------------------------------------------------------
# Latter-Earth seed flavor (default, non-fresh).  Names/places to draw on so a
# default brief reads as the Gyre rather than generic fantasy.  --fresh ignores
# these and rolls history_construction instead.
# ---------------------------------------------------------------------------
LE_NATION_NAMES = [
    "Emed-Kist", "Ka-Adun", "Llaigis", "New Voth", "Sarul", "Thur",
    "Emed-Dar", "Gathis", "Veshtun", "Old Korl", "Hadeb", "Iskerine",
]
LE_PLACE_PREFIX = [
    "Kor", "Vesh", "Adun", "Tel", "Mesh", "Sar", "Vael", "Ond", "Gyr", "Hul",
    "Bras", "Lath", "Emed", "Iss", "Nuru", "Cael",
]
LE_PLACE_SUFFIX = [
    "-keb", "-hold", "-gate", "-reach", "-mere", "-fall", "-watch", "-spur",
    "-dun", "-vault", "-march", "-strand", "-deep", "-rest", "-burh", "-tor",
]
LE_RULER_TITLE = [
    "Reaping-Marquis", "Legate", "Great King", "Censor", "Warlord",
    "Hierarch", "Senator-Prince", "Gentry-Master", "Beggar-Prince", "Margrave",
]
FRESH_PLACE_SUFFIX = LE_PLACE_SUFFIX  # same shapes work for fresh worlds


def _name(roller, prefix_pool, suffix_pool, label):
    """Honest two-roll name: a prefix + a suffix, dice shown via the Roller."""
    pi = roller.roll(len(prefix_pool), f"{label} name pt.1 (d{len(prefix_pool)})")
    si = roller.roll(len(suffix_pool), f"{label} name pt.2 (d{len(suffix_pool)})")
    return prefix_pool[pi - 1] + suffix_pool[si - 1]


def _seen(roller):
    """Per-run set of names already used, so a single world/cluster draft does
    not repeat a nation/place name.  Lives on the Roller; dice stay honest."""
    if not hasattr(roller, "_used_names"):
        roller._used_names = set()
    return roller._used_names


def _unique(roller, make, tries=6):
    """Call make() (which rolls dice) until it yields an unused name, bounded.
    Every attempt's dice are shown honestly; we just skip a name we already
    placed in this draft and keep the first novel one (or the last if all clash)."""
    seen = _seen(roller)
    name = make()
    n = 1
    while name in seen and n < tries:
        name = make()
        n += 1
    seen.add(name)
    return name


def nation_name(roller, fresh):
    if fresh:
        return _unique(roller,
                       lambda: _name(roller, LE_PLACE_PREFIX, FRESH_PLACE_SUFFIX,
                                     "nation"))
    def pick_le():
        i = roller.roll(len(LE_NATION_NAMES),
                        f"nation name (d{len(LE_NATION_NAMES)})")
        return LE_NATION_NAMES[i - 1]
    return _unique(roller, pick_le)


def place_name(roller, fresh=True):
    return _unique(roller,
                   lambda: _name(roller, LE_PLACE_PREFIX, LE_PLACE_SUFFIX,
                                 "place"))


def ruler_title(roller):
    i = roller.roll(len(LE_RULER_TITLE), f"ruler title (d{len(LE_RULER_TITLE)})")
    return LE_RULER_TITLE[i - 1]


# ---------------------------------------------------------------------------
# Reuse helpers built on gen.py primitives.  All dice come from gen.py's Roller.
# ---------------------------------------------------------------------------
def roll_bundle_table(roller, bundle_slug, table_name, label):
    """Roll one named table inside a construction bundle, via gen.py.load + dice."""
    doc = gen.load(gen.BUNDLE_FILES[bundle_slug])
    return gen.roll_table(roller, doc["tables"][table_name], label)


def roll_location_tag(roller, family):
    """A location tag + its 5 d3 sub-tables, exactly as gen.py rolls them.
    Returns (tag_name, {label: value})."""
    name, detail = gen.roll_tag(roller, family, full=True)
    subs = gen.roll_tag_subtables(roller, detail, name)
    return name, subs


def short_npc(roller):
    """A one-line notable figure: class/role + twist + an Ambition, reusing
    gen.py's npc_quickgen + character_tags data.  Kept SHORT (no appearance)."""
    nq = gen.load("npc_quickgen.json")
    cd = gen.load("character_tags_detail.json")
    classes = ["Underclass", "Commoners", "Gentry"]
    c = roller.roll(3, "figure class (d3)")
    cls = classes[c - 1]
    role = gen.roll_table(roller, nq["tables"][f"Random NPC ({cls})"],
                          f"figure role · {cls} (d100)")
    twist = gen.roll_table(roller, nq["tables"]["Characteristic Twists"],
                           "figure twist (d12)")
    r = roller.roll(100, "figure character tag (d100)")
    ctag = gen.pick(gen.load("character_tags.json"), r)
    amb = cd["tags"][ctag]["subtables"]["Ambitions"]
    a = roller.roll(3, "figure Ambition (d3)")
    ambition = amb[min(a, len(amb)) - 1]
    return f"{role} ({cls}); {twist}; ambition — {ambition.rstrip('.')}"


def short_hook(roller):
    """One fractal seed filled from a freshly-rolled community tag's pools.
    Mirrors gen.py.recipe_hook's fill logic but returns a single SHORT string."""
    import re
    seeds = gen.load("fractal_seeds.json")
    name, detail = gen.roll_tag(roller, "community", full=False)
    pools = gen.roll_tag_subtables(roller, detail, name)
    plural = {"Enemy": "Enemies", "Friend": "Friends",
              "Complication": "Complications", "Thing": "Things",
              "Place": "Places"}
    s = roller.roll(100, "fractal seed (d100)")
    seed = gen.pick(seeds, s)
    filled = seed
    for singular, pl in plural.items():
        val = pools.get(pl)
        if val:
            filled = re.sub(rf"\b{singular}\b", f"{singular} [{val}]",
                            filled, count=99)
    return filled.rstrip(".")


# ---------------------------------------------------------------------------
# Composers — each returns a markdown DRAFT CANON fragment (string).  Dice are
# rolled (and shown) as a side effect via the shared Roller.
# ---------------------------------------------------------------------------
PLACE_RECIPE_TITLE = {
    "settlement": "SETTLEMENT", "court": "COURT",
    "ruin": "RUIN", "wilderness": "WILDERNESS",
}


def compose_place(roller, cmd):
    """settlement/court/ruin/wilderness via roll_location_tag, as a short stub.
    Map the command to the tag family the way gen.py does (settlement ->
    community), so we reuse the same flat/detail files gen.py reads."""
    family = gen.TAG_DETAIL[cmd]  # settlement->community, ruin->ruin, ...
    name, subs = roll_location_tag(roller, family)
    singular = {"Enemies": "Enemy", "Friends": "Friend",
                "Complications": "Complication", "Things": "Thing",
                "Places": "Place"}
    lines = [f"**{family.capitalize()} tag — {name}**"]
    for label in ("Enemies", "Friends", "Complications", "Things", "Places"):
        if label in subs:
            lines.append(f"- {singular[label]}: {subs[label]}")
    return name, "\n".join(lines)


def compose_nation(roller, fresh):
    """A faction-ready nation brief."""
    name = nation_name(roller, fresh)
    title = ruler_title(roller)
    gov_theme = roll_bundle_table(roller, "nation_construction", "Nation Themes",
                                  "national theme (d20)")
    prob1 = roll_bundle_table(roller, "nation_construction",
                              "Current National Problems", "problem 1 (d20)")
    prob2 = roll_bundle_table(roller, "nation_construction",
                              "Current National Problems", "problem 2 (d20)")
    good = roll_bundle_table(roller, "nation_construction",
                             "Good Things Happening Now", "good thing (d20)")
    tension = roll_bundle_table(roller, "nation_construction",
                                "Disputes With a Neighbor", "tension (d20)")
    # Ruling court flavor (a court tag, summary only — short)
    court_name, court_detail = gen.roll_tag(roller, "court", full=True)
    figure = short_npc(roller)

    origin = None
    if fresh:
        origin = roll_bundle_table(roller, "history_construction",
                                   "How Did They Originate", "origin (d8)")

    L = [f"### Nation — {name}",
         f"- **Government / theme:** ruled by a {title}; national mood is "
         f"*{gov_theme.split(',')[0].lower()}*.",
         f"- **Ruling court:** {court_name}.",
         f"- **Problems (= adventure hooks):**",
         f"  1. {prob1}.",
         f"  2. {prob2}.",
         f"- **A good thing:** {good}.",
         f"- **Notable figure:** {figure}.",
         f"- **Tension with a neighbor:** {tension}."]
    if origin:
        L.insert(1, f"- **Origin (fresh):** {origin}.")
    return name, "\n".join(L), tension


def compose_region(roller, fresh):
    """A starting region: terrain + 1-2 settlements + a nearby ruin + 2-3 hooks."""
    rname = place_name(roller) + " March"
    # how many settlements (1-2) — honest d2-ish via d3 capped
    sc = roller.roll(2, "settlement count (d2)")
    nsettle = sc  # 1 or 2

    wild_name, wild_subs = roll_location_tag(roller, "wilderness")

    settles = []
    for i in range(nsettle):
        sn = place_name(roller)
        tag, subs = roll_location_tag(roller, "community")
        comp = subs.get("Complications", "")
        settles.append((sn, tag, comp))

    rn = place_name(roller)
    ruin_tag, ruin_subs = roll_location_tag(roller, "ruin")
    ruin_thing = ruin_subs.get("Things", "")

    nh = roller.roll(2, "hook count base (d2)") + 1  # 2 or 3
    hooks = [short_hook(roller) for _ in range(nh)]

    L = [f"### Region — {rname}",
         f"- **Terrain / wilderness tag:** {wild_name} "
         f"(complication: {wild_subs.get('Complications', '—')}).",
         f"- **Settlements:**"]
    for sn, tag, comp in settles:
        L.append(f"  - **{sn}** — {tag}; current trouble: {comp}.")
    L.append(f"- **Nearby ruin:** **{rn}** — {ruin_tag}; holds: {ruin_thing}.")
    L.append(f"- **Hooks (seeds to attach to canon):**")
    for h in hooks:
        L.append(f"  - {h}.")
    return rname, "\n".join(L)


def compose_continent_line(roller, fresh):
    """One nation as a single line for the continent sketch."""
    name = nation_name(roller, fresh)
    theme = roll_bundle_table(roller, "nation_construction", "Nation Themes",
                              f"{name} theme (d20)")
    prob = roll_bundle_table(roller, "nation_construction",
                             "Current National Problems", f"{name} hook (d20)")
    return name, f"**{name}** — *{theme.split(',')[0].lower()}*; hook: {prob.lower()}."


# ---------------------------------------------------------------------------
# DRAFT-CANON wrappers.
# ---------------------------------------------------------------------------
HEADER = (
    "<!-- DRAFT CANON — generated proposal; NOT yet canon. "
    "Show the player, let them keep / reroll / adjust / hand-author, THEN edit "
    "and paste the approved version into bridge/setting-canon.md and seed the "
    "engine Threads/Characters Lists + faction board. Keep it SHORT. -->")


def draft_block(title, body, seed, scope_note=None):
    seedline = f"_seed: {seed}_  " if seed is not None else ""
    parts = [HEADER, "", f"# DRAFT CANON — {title}", ""]
    if scope_note:
        parts += [f"> {scope_note}", ""]
    if seedline:
        parts += [seedline.strip(), ""]
    parts.append(body)
    parts += ["",
              "> **Next:** approve / reroll (`--seed N`) / hand-author. On "
              "approval, fold into `bridge/setting-canon.md`, add Threads for "
              "each hook, add Characters for each named figure, and put each "
              "nation on the faction board. Build the rest **on demand** as "
              "play travels — never pre-build the map."]
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Commands.
# ---------------------------------------------------------------------------
def cmd_place(roller, family, seed):
    name, body = compose_place(roller, family)
    return draft_block(f"{family.capitalize()}: {name}", body, seed)


def cmd_nation(roller, fresh, seed):
    name, body, _ = compose_nation(roller, fresh)
    note = ("Fresh world: name & origin rolled from scratch." if fresh
            else "Latter-Earth seeding: name drawn from Gyre canon; attach "
                 "hooks to existing setting-canon.md entries.")
    return draft_block(f"Nation: {name}", body, seed, note)


def cmd_region(roller, fresh, seed):
    name, body = compose_region(roller, fresh)
    note = ("Fresh world: names rolled from scratch." if fresh
            else "Latter-Earth seeding: this is the detailed starting region; "
                 "leave hooks to attach to canon NPCs/factions.")
    return draft_block(f"Starting Region: {name}", body, seed, note)


def cmd_world(roller, scope, fresh, seed):
    if scope == "region":
        name, body = compose_region(roller, fresh)
        note = "Scope = single region (only the starting region is detailed)."
        return draft_block(f"World (region scope): {name}", body, seed, note)

    if scope == "few-nations":
        nn = roller.roll(3, "nation count base (d3)") + 1  # 2..4
        blocks, names, tensions = [], [], []
        for _ in range(nn):
            nm, body, tension = compose_nation(roller, fresh)
            names.append(nm)
            tensions.append(tension)
            blocks.append(body)
        # one shared tension binding the cluster
        shared = roll_bundle_table(roller, "nation_construction",
                                   "Disputes With a Neighbor",
                                   "SHARED regional tension (d20)")
        # a starting region inside the cluster
        rname, rbody = compose_region(roller, fresh)
        body = "\n\n".join(blocks)
        body += (f"\n\n### Shared tension (binds the cluster)\n"
                 f"- All of {', '.join(names)} are entangled by: {shared}.\n")
        body += f"\n{rbody}"
        note = (f"Scope = a few neighboring nations ({nn}); only the starting "
                f"region below is detailed — grow the rest on demand.")
        return draft_block("World (few-nations scope)", body, seed, note)

    if scope == "continent":
        cn = roller.roll(3, "continent nation count base (d3)") + 3  # 4..6
        lines, names = [], []
        for _ in range(cn):
            nm, line = compose_continent_line(roller, fresh)
            names.append(nm)
            lines.append(f"- {line}")
        # relations map: pair each nation with the next via a dispute/tie
        rel = ["", "### Map of relations"]
        for i in range(len(names)):
            a = names[i]
            b = names[(i + 1) % len(names)]
            kind = roll_bundle_table(
                roller, "nation_construction",
                "Disputes With a Neighbor" if roller.roll(2, f"{a}/{b} sign (d2)") == 1
                else "Positive Ties With a Neighbor",
                f"{a} ↔ {b} (d20)")
            rel.append(f"- **{a} ↔ {b}:** {kind}.")
        body = "### Nations (one line each)\n" + "\n".join(lines) + "\n" + "\n".join(rel)
        note = (f"Scope = whole continent ({cn} nations) — a SKETCH only. "
                f"Detail a single starting region (`worldgen.py region`) before "
                f"play; grow everything else on demand.")
        return draft_block("World (continent scope)", body, seed, note)

    sys.exit(f"Unknown scope '{scope}'. Use region | few-nations | continent.")


# ---------------------------------------------------------------------------
# Entry.
# ---------------------------------------------------------------------------
def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return

    cmd = args[0]
    fresh = "--fresh" in args
    seed = None
    if "--seed" in args:
        seed = int(args[args.index("--seed") + 1])
    scope = None
    if "--scope" in args:
        scope = args[args.index("--scope") + 1]

    # Build a Roller from gen.py so the dice contract (honest, shown, seeded,
    # MYTHIC_GM_DICE-aware) is identical to gen.py's.  Redirect its STDOUT dice
    # chatter to STDERR so STDOUT carries only the committable markdown.
    roller = gen.Roller(seed)
    real_stdout = sys.stdout
    sys.stdout = sys.stderr  # gen.py's Roller.print() -> STDERR (audit trail)
    print(f"=== worldgen: {cmd}{' --fresh' if fresh else ''}"
          f"{(' --scope ' + scope) if scope else ''}"
          f"{(' --seed ' + str(seed)) if seed is not None else ''} ===")
    roller.banner()

    try:
        if cmd in PLACE_RECIPE_TITLE:
            block = cmd_place(roller, cmd, seed)
        elif cmd == "nation":
            block = cmd_nation(roller, fresh, seed)
        elif cmd == "region":
            block = cmd_region(roller, fresh, seed)
        elif cmd == "world":
            if not scope:
                sys.stdout = real_stdout
                sys.exit("world needs --scope <region|few-nations|continent>.")
            block = cmd_world(roller, scope, fresh, seed)
        else:
            sys.stdout = real_stdout
            sys.exit(f"Unknown command '{cmd}'. See --help.")
    finally:
        sys.stdout = real_stdout

    # Committable DRAFT CANON markdown -> STDOUT.
    print(block)


if __name__ == "__main__":
    main()
