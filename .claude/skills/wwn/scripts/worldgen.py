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

  geography --scale <region|kingdom> [--fresh] [--seed N] [--campaign DIR]
        The book's two-map system (Geography Construction pp.124-127).  This is
        the SKELETON layer — geometry & adjacency only; every node's content
        comes from the existing tag recipes (no reinvented place flavor).
          region   = oceanic frame -> ~6 terrain features -> 1d4+2 rivers (split
                     downstream only, <=1/4 map) -> 1-3 lakes -> 6 nations on
                     natural borders.  NO cities/ruins.  Relational sketch +
                     coordinate hints.
          kingdom  = small-scale terrain -> demographics (60/sq mi; ~10% urban,
                     1/3 capital, 1/4 of remainder in 2nd city) -> capital on
                     water then cities CLOCKWISE from a random cardinal -> each
                     city tagged 2 Community + 2 Court.

  ruins --kingdom <name> [--fresh] [--seed N] [--campaign DIR]
        ~6 famous ruins (Placing Ruins p.150) in the wilderness gaps between
        trade routes; each = a ruin-type roll (Latter-Earth d12 / General d20)
        + 2 Ruin Tags + a line.  Sketch nodes — flesh out on PC commitment.

  world --scope <region|few-nations|continent|kingdom> [--fresh] [--seed N] [--campaign DIR]
        Scaffold a world at the chosen scope by composing the above:
          region       = 1 detailed region (== `region`).
          few-nations  = 2-4 nation briefs + 1 shared tension + a start region.
          continent    = a sketch: 4-6 one-line nations + a relations map.
          kingdom      = a region SKELETON + the one detailed kingdom inside it
                         (+ its ~6 ruins) — the two-map start of a campaign.
        --fresh generates names/history from scratch (history_construction);
        without it, assume Latter-Earth seeding (hooks left to attach to canon).

  --campaign DIR  on the geography/ruins/world commands: append the generated
        place nodes (each carrying its FULL tag, adjacency, status, ids) to
        DIR/places.json — the machine graph the scene system reads for proximity.
        Without it, the node JSON is printed in a fenced block in the draft.

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
    Returns (tag_name, summary, {label: value}) so the FULL tag — its book
    summary paragraph AND all five sub-tables — can be surfaced into the
    committed canon (and the saved place record), not just the tag name."""
    name, detail = gen.roll_tag(roller, family, full=True)
    summary = ""
    if detail and name in detail["tags"]:
        summary = detail["tags"][name].get("summary", "")
    subs = gen.roll_tag_subtables(roller, detail, name)
    return name, summary, subs


# Plural -> singular label used when rendering a tag's sub-tables.
_TAG_SINGULAR = {"Enemies": "Enemy", "Friends": "Friend",
                 "Complications": "Complication", "Things": "Thing",
                 "Places": "Place"}


def full_tag_block(title, name, summary, subs, indent=""):
    """Render a tag's COMPLETE information — summary + all five sub-tables — as
    markdown lines, so the saved site carries the full meaning of its tag."""
    lines = [f"{indent}- **{title} — {name}**"]
    if summary:
        lines.append(f"{indent}  - *{summary}*")
    for label in ("Enemies", "Friends", "Complications", "Things", "Places"):
        if label in subs:
            lines.append(f"{indent}  - {_TAG_SINGULAR[label]}: {subs[label]}")
    return lines


# ---------------------------------------------------------------------------
# Geography Construction data (the book's terrain / detail / ruin tables).
# Loaded directly via gen.load (not reimplemented); rolled with gen.roll_table.
# ---------------------------------------------------------------------------
GEO_FILE = "geography_construction.json"


def _geo(roller, table_name, label):
    """Roll one table inside geography_construction.json via the shared dice."""
    doc = gen.load(GEO_FILE)
    return gen.roll_table(roller, doc["tables"][table_name], label)


def roll_terrain_feature(roller, label="terrain feature (d20)"):
    return _geo(roller, "Significant Terrain Features", label)


def roll_terrain_details(roller):
    """The six one-roll detail dice for a terrain feature."""
    return {
        "Populated": _geo(roller, "How Populated", "how populated (d4)"),
        "Dangerous": _geo(roller, "How Dangerous", "how dangerous (d6)"),
        "Use": _geo(roller, "What Use", "what use (d8)"),
        "LastEvent": _geo(roller, "Last Event", "last event (d10)"),
        "Antagonists": _geo(roller, "Common Antagonists", "common antagonists (d12)"),
        "Quirk": _geo(roller, "Optional Quirk", "optional quirk (d20)"),
    }


def roll_ruin_type(roller, latter_earth=True):
    """A ruin type from the General (d20) or Latter-Earth (d12) place table."""
    if latter_earth:
        return _geo(roller, "Latter-Earth Places", "ruin type · Latter-Earth (d12)")
    return _geo(roller, "General Places of Adventure", "ruin type · general (d20)")


# ---------------------------------------------------------------------------
# Relational-map geometry (the book's "loose scrawls" — geometry only, the tag
# subsystem owns all place content).  Honest dice via the shared Roller.
# ---------------------------------------------------------------------------
CARDINALS = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
EDGES = ["north edge", "east edge", "south edge", "west edge"]
OCEANIC = {1: "1 oceanic side — a curving coastline",
           2: "2 oceanic sides — a peninsula / land bridge off two edges",
           3: "3 oceanic sides — a self-contained peninsula",
           4: "4 oceanic sides — the region is an island"}


def roll_oceanic_sides(roller):
    n = roller.roll(4, "oceanic sides (d4)")
    return n, OCEANIC[n]


def roll_cardinal(roller, label="cardinal (d8)"):
    i = roller.roll(8, label)
    return CARDINALS[i - 1]


# ---------------------------------------------------------------------------
# places.json persistence — the machine graph (Part 3.0 Pillar 4).  Its job is
# proximity/adjacency so the scene system can weight near vs. distant content.
# Each node carries the FULL rolled tag (summary + sub-tables), shared ids, and
# a canon anchor.  Re-entry is a lookup of this file, not a reroll.
# ---------------------------------------------------------------------------
def _places_path(campaign):
    return os.path.join(campaign, "places.json")


def load_places(campaign):
    p = _places_path(campaign)
    if not os.path.exists(p):
        return {"nodes": []}
    import json
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def _next_id(doc, prefix):
    """Next free id with a kind-prefix: R-/K-/S-/C-/U-/W- + zero-padded count."""
    n = sum(1 for nd in doc["nodes"] if nd.get("id", "").startswith(prefix + "-"))
    return f"{prefix}-{n + 1:02d}"


KIND_PREFIX = {"region": "RG", "kingdom": "K", "settlement": "S",
               "court": "CT", "ruin": "R", "wilderness": "W"}


def make_node(doc, name, kind, tag_name="", summary="", subs=None,
              parent=None, adjacency=None, travel_days=None,
              status="sketch", threads=None, characters=None,
              canon_anchor=None, node_id=None):
    """Build a Pillar-4 place node carrying its FULL tag (summary + sub-tables)."""
    nid = node_id or _next_id(doc, KIND_PREFIX.get(kind, "P"))
    return {
        "id": nid,
        "name": name,
        "kind": kind,
        "parent": parent,
        "adjacency": adjacency or [],
        "travel_days": travel_days,
        "status": status,
        "tag": {"name": tag_name, "summary": summary, "subtables": subs or {}},
        "threads": threads or [],
        "characters": characters or [],
        "canon_anchor": canon_anchor or f"setting-canon.md#{name.lower().replace(' ', '-')}",
    }


def write_places(campaign, nodes):
    """Append nodes to campaign/places.json (creating it if absent).  Returns the
    full doc so callers can report the assigned ids."""
    import json
    doc = load_places(campaign)
    doc["nodes"].extend(nodes)
    os.makedirs(campaign, exist_ok=True)
    with open(_places_path(campaign), "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return doc


def place_card(node, near=None, weight=1, extra=""):
    """The machine-readable place card header the scene framer eats (Pillar 3):
       - [PLACE site:<kind> id=<id> region=.. kingdom=.. near=.. w=N] <name> — <tag>; <summary>
    The bracket header is parsed for proximity/weight; the prose is narrated."""
    tag = node["tag"]
    region = node.get("_region", "")
    kingdom = node.get("parent") or node.get("_kingdom", "")
    bits = [f"site:{node['kind']}", f"id={node['id']}"]
    if region:
        bits.append(f"region={region}")
    if kingdom:
        bits.append(f"kingdom={kingdom}")
    if near:
        bits.append(f"near={near}")
    bits.append(f"w={weight}")
    head = f"- [PLACE {' '.join(bits)}]"
    summ = tag.get("summary", "")
    name = node["name"]
    tagname = tag.get("name", "")
    line = f"  {name} — {node['kind']}"
    if tagname:
        line += f"; {tagname}"
    if summ:
        line += f". {summ}"
    if extra:
        line += f" {extra}"
    return head + "\n" + line


def nodes_to_json_block(nodes):
    """Render nodes as a fenced JSON block for the draft when no --campaign DIR
    is given (so the player can still see / save the machine graph)."""
    import json
    return ("```json places.json (append these nodes)\n"
            + json.dumps({"nodes": nodes}, ensure_ascii=False, indent=2)
            + "\n```")


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
    # Surface the character tag's full meaning (name + summary), not just the
    # rolled ambition, so the NPC's drama reaches context (Mythic/NPC adjunct).
    csumm = cd["tags"].get(ctag, {}).get("summary", "")
    line = f"{role} ({cls}); {twist}; tag *{ctag}*; ambition — {ambition.rstrip('.')}"
    if csumm:
        line += f"\n    - *{csumm}*"
    return line


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
    name, summary, subs = roll_location_tag(roller, family)
    # Surface the FULL tag — its summary paragraph and all five sub-tables —
    # so the saved site carries its complete meaning into later scene framing.
    lines = full_tag_block(f"{family.capitalize()} tag", name, summary, subs)
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
    # Ruling court flavor (a court tag — keep its full summary with the nation)
    court_name, court_detail = gen.roll_tag(roller, "court", full=True)
    court_summary = ""
    if court_detail and court_name in court_detail["tags"]:
        court_summary = court_detail["tags"][court_name].get("summary", "")
    figure = short_npc(roller)

    origin = None
    if fresh:
        origin = roll_bundle_table(roller, "history_construction",
                                   "How Did They Originate", "origin (d8)")

    L = [f"### Nation — {name}",
         f"- **Government / theme:** ruled by a {title}; national mood is "
         f"*{gov_theme.split(',')[0].lower()}*.",
         f"- **Ruling court:** {court_name}."
         + (f"\n  - *{court_summary}*" if court_summary else ""),
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

    wild_name, wild_summary, wild_subs = roll_location_tag(roller, "wilderness")

    settles = []
    for i in range(nsettle):
        sn = place_name(roller)
        tag, summary, subs = roll_location_tag(roller, "community")
        comp = subs.get("Complications", "")
        settles.append((sn, tag, comp, summary, subs))

    rn = place_name(roller)
    ruin_tag, ruin_summary, ruin_subs = roll_location_tag(roller, "ruin")
    ruin_thing = ruin_subs.get("Things", "")

    nh = roller.roll(2, "hook count base (d2)") + 1  # 2 or 3
    hooks = [short_hook(roller) for _ in range(nh)]

    L = [f"### Region — {rname}",
         f"- **Terrain / wilderness tag:** {wild_name} "
         f"(complication: {wild_subs.get('Complications', '—')}).",
         f"- **Settlements:**"]
    for sn, tag, comp, _summary, _subs in settles:
        L.append(f"  - **{sn}** — {tag}; current trouble: {comp}.")
    L.append(f"- **Nearby ruin:** **{rn}** — {ruin_tag}; holds: {ruin_thing}.")
    L.append(f"- **Hooks (seeds to attach to canon):**")
    for h in hooks:
        L.append(f"  - {h}.")
    # FULL tag fidelity: keep every rolled tag's summary + all five sub-tables
    # with the saved region, so re-entry reads the complete site, not a one-liner.
    L.append(f"- **Place details (full rolled tags — save with the site):**")
    L += full_tag_block("Terrain", wild_name, wild_summary, wild_subs, indent="  ")
    for sn, tag, comp, summary, subs in settles:
        L += full_tag_block(sn, tag, summary, subs, indent="  ")
    L += full_tag_block(rn, ruin_tag, ruin_summary, ruin_subs, indent="  ")
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
# Geography composers (Part 3) — geometry & adjacency ONLY.  Every node's
# *content* comes from the existing tag recipes (roll_location_tag /
# full_tag_block); the geography layer just places & indexes.  Each composer
# returns (title, body_markdown, [place_node...]) so the caller can persist the
# nodes to places.json and emit the machine place cards.
# ---------------------------------------------------------------------------
def compose_geography_region(roller, fresh, campaign=None):
    """Region scale: oceanic sides -> ~6 terrain features -> 1d4+2 rivers
    (split downstream only, <=1/4 map) -> 1-3 lakes -> 6 nations on natural
    borders.  NO cities/ruins at region scale (book p.124-127).  Relational
    sketch + a simple coordinate table.  Wilderness gets a full tag; nations
    reuse compose_continent_line-style briefs but bounded by named barriers."""
    rname = place_name(roller) + " Reach"
    doc = load_places(campaign) if campaign else {"nodes": []}
    nodes = []

    n_oce, oce_desc = roll_oceanic_sides(roller)
    sea_edges = [EDGES[i] for i in
                 sorted(roller.roll(4, f"oceanic edge {k+1} (d4)") - 1
                        for k in range(n_oce))]
    sea_edges = sorted(set(sea_edges))

    # ~6 significant terrain features, each placed at a cardinal/edge hint.
    nfeat = 6
    feats = []
    for i in range(nfeat):
        feat = roll_terrain_feature(roller, f"feature {i+1} (d20)")
        card = roll_cardinal(roller, f"feature {i+1} placement (d8)")
        feats.append((feat, card))

    # rivers: 1d4+2, each from a highland -> sea/lake; split downstream only.
    nriv = roller.roll(4, "river count (1d4)") + 2
    highlands = [f for (f, _c) in feats
                 if any(w in f.lower() for w in
                        ("mountain", "hills", "canyon", "volcano"))]
    rivers = []
    for i in range(nriv):
        src = (highlands[(i) % len(highlands)].split(" — ")[0]
               if highlands else "the central highlands")
        sink = "the sea" if sea_edges else "an inland lake"
        rivers.append((src, sink))

    # 1-3 lakes; each >=1 river in, <=1 out.
    nlake = roller.roll(3, "lake count (d3)")
    lakes = []
    for i in range(nlake):
        card = roll_cardinal(roller, f"lake {i+1} placement (d8)")
        lakes.append(card)

    # 6 nations on natural borders (the named barriers above bound them).
    barriers = [f.split(" — ")[0] for (f, _c) in feats] + \
               [f"river from {s}" for (s, _k) in rivers]
    nations = []
    for i in range(6):
        nm = nation_name(roller, fresh)
        theme = roll_bundle_table(roller, "nation_construction", "Nation Themes",
                                  f"{nm} theme (d20)")
        b1 = barriers[(2 * i) % len(barriers)]
        b2 = barriers[(2 * i + 1) % len(barriers)]
        nations.append((nm, theme.split(",")[0].lower(), b1, b2))

    # one full wilderness tag for the region's defining wild (content layer).
    wild_name, wild_summary, wild_subs = roll_location_tag(roller, "wilderness")

    # ---- place node: the region itself (full wilderness tag) ----------------
    region_node = make_node(doc, rname, "region",
                            tag_name=wild_name, summary=wild_summary,
                            subs=wild_subs, status="detailed")
    region_node["_region"] = rname
    nodes.append(region_node)
    doc["nodes"].append(region_node)

    # ---- draft body ---------------------------------------------------------
    L = [f"### Region — {rname}",
         f"- **Oceanic frame:** {oce_desc}"
         + (f" (seas on the {', '.join(sea_edges)})." if sea_edges else "."),
         f"- **Significant terrain (~6 features):**"]
    for feat, card in feats:
        L.append(f"  - {card}: {feat}.")
    L.append(f"- **Major rivers ({nriv} = 1d4+2; each ≤¼ map, split downstream only):**")
    for src, sink in rivers:
        L.append(f"  - from {src} → {sink}.")
    if lakes:
        L.append(f"- **Lakes ({nlake}; ≥1 river in, ≤1 out each):** "
                 + ", ".join(lakes) + ".")
    else:
        L.append("- **Lakes:** none.")
    L.append("- **Nations (6, on natural borders — no cities/ruins at this scale):**")
    for nm, theme, b1, b2 in nations:
        L.append(f"  - **{nm}** — *{theme}*; bounded by {b1} and {b2}.")
    # relational sketch / coordinate hint table
    L.append("- **Relational sketch (hand-draw from this):**")
    L.append("  | feature | rough position |")
    L.append("  |---|---|")
    for feat, card in feats:
        L.append(f"  | {feat.split(' — ')[0]} | {card} |")
    L.append("- **Defining wilderness tag (full, save with the region):**")
    L += full_tag_block("Wilderness", wild_name, wild_summary, wild_subs, indent="  ")
    L.append("- **Place card (machine-readable header):**")
    L.append(place_card(region_node, weight=1))

    return rname, "\n".join(L), nodes


def compose_geography_kingdom(roller, fresh, campaign=None, region_name=None):
    """Kingdom scale: small-scale terrain -> demographics (60/sq mi; ~10% urban,
    ⅓ in capital, ¼ of remainder in 2nd city) -> capital on water then cities
    CLOCKWISE from a random cardinal -> tag each city (2 Community + 2 Court)."""
    kname = nation_name(roller, fresh)
    doc = load_places(campaign) if campaign else {"nodes": []}
    nodes = []

    # kingdom node (parent for its cities/ruins)
    kingdom_node = make_node(doc, kname, "kingdom", status="detailed",
                             parent=region_name)
    kingdom_node["_region"] = region_name or ""
    nodes.append(kingdom_node)
    doc["nodes"].append(kingdom_node)

    # one obtruding terrain feature riffed for the whole landscape (book p.49).
    feat = roll_terrain_feature(roller, "kingdom terrain (d20)")
    details = roll_terrain_details(roller)

    # demographics: pick a map size in 6-mile hexes (honest), derive population.
    hexes = roller.roll(20, "kingdom span in 6-mile hexes (d20)") + 10  # 11..30
    pop = hexes * 2000                       # 2000 people / 6-mile hex
    urban = pop // 10                        # ~10% urban
    capital_pop = urban // 3                 # ⅓ of urban in the capital
    second_pop = (urban - capital_pop) // 4  # ¼ of the remainder in 2nd city
    # how many cities total (capital + 1-2 more), placed clockwise.
    ncity = roller.roll(2, "extra cities (d2)") + 1  # 2 or 3 cities total

    start_dir = roll_cardinal(roller, "first city bearing from capital (d8)")
    start_i = CARDINALS.index(start_dir)

    cities = []
    for i in range(ncity):
        cn = place_name(roller)
        # 2 Community + 2 Court tags per city (reuse the tag recipes).
        comm1 = roll_location_tag(roller, "community")
        comm2 = roll_location_tag(roller, "community")
        court1 = roll_location_tag(roller, "court")
        court2 = roll_location_tag(roller, "court")
        if i == 0:
            bearing = "on water (capital)"
            cpop = capital_pop
            kind_label = "capital"
        else:
            bearing = CARDINALS[(start_i + (i - 1) * 2) % 8] + " of the capital (clockwise)"
            cpop = second_pop if i == 1 else max(1, second_pop // 2)
            kind_label = "city"
        cities.append((cn, kind_label, bearing, cpop,
                       comm1, comm2, court1, court2))

    # ---- place nodes: each city carries its FULL community tag --------------
    prev_id = kingdom_node["id"]
    for cn, kind_label, bearing, cpop, comm1, comm2, court1, court2 in cities:
        cname, csumm, csubs = comm1
        node = make_node(doc, cn, "settlement",
                         tag_name=cname, summary=csumm, subs=csubs,
                         parent=kingdom_node["id"], adjacency=[prev_id],
                         status="detailed")
        node["_region"] = region_name or ""
        node["_kingdom"] = kname
        nodes.append(node)
        doc["nodes"].append(node)
        prev_id = node["id"]

    # ---- draft body ---------------------------------------------------------
    L = [f"### Kingdom — {kname}",
         f"- **Dominant terrain:** {feat}.",
         f"  - *populated:* {details['Populated']}; *danger:* {details['Dangerous']}; "
         f"*use:* {details['Use']}.",
         f"  - *last event:* {details['LastEvent']}; *antagonists:* {details['Antagonists']}; "
         f"*quirk:* {details['Quirk']}.",
         f"- **Demographics:** ≈{hexes} six-mile hexes ⇒ ~{pop:,} people "
         f"(60/sq mi); ~{urban:,} urban (10%). Capital ≈{capital_pop:,}; "
         f"2nd city ≈{second_pop:,}.",
         f"- **Cities ({ncity}; capital on water, the rest CLOCKWISE from "
         f"{start_dir}):**"]
    for cn, kind_label, bearing, cpop, comm1, comm2, court1, court2 in cities:
        L.append(f"  - **{cn}** ({kind_label}, {bearing}; ≈{cpop:,}) — "
                 f"Community: *{comm1[0]}*, *{comm2[0]}*; "
                 f"Court: *{court1[0]}*, *{court2[0]}*.")
    L.append("- **City tags (full, save with each city):**")
    for cn, kind_label, bearing, cpop, comm1, comm2, court1, court2 in cities:
        L += full_tag_block(f"{cn} · Community", comm1[0], comm1[1], comm1[2], indent="  ")
        L += full_tag_block(f"{cn} · Community", comm2[0], comm2[1], comm2[2], indent="  ")
        L += full_tag_block(f"{cn} · Court", court1[0], court1[1], court1[2], indent="  ")
        L += full_tag_block(f"{cn} · Court", court2[0], court2[1], court2[2], indent="  ")
    L.append("- **Place cards (machine-readable headers):**")
    for node in nodes:
        if node["kind"] == "settlement":
            L.append(place_card(node, near="cap", weight=2))
    L.append("> **Next:** place ~6 famous ruins in the wilderness gaps "
             "(`worldgen.py ruins --kingdom " + kname + "`).")

    return kname, "\n".join(L), nodes


def compose_ruins(roller, kingdom_name, campaign=None, n=6, latter_earth=True):
    """~6 famous ruins per kingdom, placed in the wilderness gaps between trade
    routes; each = a ruin-type roll + 2 Ruin Tags + 1-2 sentences (book p.150)."""
    doc = load_places(campaign) if campaign else {"nodes": []}
    nodes = []
    L = [f"### Ruins of {kingdom_name} (~{n}, in the wilderness gaps between trade routes)"]
    for i in range(n):
        rname = place_name(roller)
        rtype = roll_ruin_type(roller, latter_earth=latter_earth)
        # 2 Ruin Tags give it character (full tags, saved with the node).
        tag1 = roll_location_tag(roller, "ruin")
        tag2 = roll_location_tag(roller, "ruin")
        gap = roll_cardinal(roller, f"ruin {i+1} gap bearing (d8)")
        node = make_node(doc, rname, "ruin",
                         tag_name=tag1[0], summary=tag1[1], subs=tag1[2],
                         parent="K-" + kingdom_name, status="sketch")
        node["_kingdom"] = kingdom_name
        node["_ruin_type"] = rtype
        node["_second_tag"] = {"name": tag2[0], "summary": tag2[1],
                               "subtables": tag2[2]}
        nodes.append(node)
        doc["nodes"].append(node)
        thing = tag1[2].get("Things", "—")
        L.append(f"- **{rname}** ({gap} gap) — *{rtype}*; tags *{tag1[0]}* + "
                 f"*{tag2[0]}*; holds: {thing}.")
    L.append("- **Ruin tags (full, save with each ruin):**")
    for node in nodes:
        L += full_tag_block(node["name"] + " · tag 1", node["tag"]["name"],
                            node["tag"]["summary"], node["tag"]["subtables"],
                            indent="  ")
        st = node["_second_tag"]
        L += full_tag_block(node["name"] + " · tag 2", st["name"],
                            st["summary"], st["subtables"], indent="  ")
    L.append("- **Place cards (machine-readable headers):**")
    for node in nodes:
        L.append(place_card(node, near="cap+2d", weight=1))
    return kingdom_name, "\n".join(L), nodes


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


def _strip_internal(node):
    """Drop the transient _region/_kingdom hints before persisting (they're
    derived from parent and only used to render place cards)."""
    return {k: v for k, v in node.items() if not k.startswith("_")}


def persist_note(campaign, nodes):
    """Either write nodes to campaign/places.json and report the ids, or — when
    no --campaign DIR is given — return a fenced JSON block of the nodes so the
    player can still save the machine graph by hand."""
    clean = [_strip_internal(n) for n in nodes]
    if campaign:
        write_places(campaign, clean)
        ids = ", ".join(n["id"] for n in clean)
        return (f"\n> **places.json:** appended {len(clean)} node(s) "
                f"[{ids}] to `{os.path.join(campaign, 'places.json')}` "
                f"(each carries its FULL tag + adjacency; re-entry is a lookup, "
                f"not a reroll).")
    return ("\n> **places.json (no --campaign DIR given):** append these nodes "
            "to the campaign's `places.json` on approval —\n\n"
            + nodes_to_json_block(clean))


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


def cmd_world(roller, scope, fresh, seed, campaign=None):
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

    if scope == "kingdom":
        # region skeleton + the one detailed kingdom inside it + its ruins.
        rname, rbody, rnodes = compose_geography_region(roller, fresh, campaign)
        kname, kbody, knodes = compose_geography_kingdom(roller, fresh, campaign,
                                                         region_name=rname)
        _kk, ruinbody, ruinnodes = compose_ruins(roller, kname, campaign,
                                                 latter_earth=not fresh)
        body = rbody + "\n\n" + kbody + "\n\n" + ruinbody
        body += persist_note(campaign, rnodes + knodes + ruinnodes)
        note = ("Scope = a region SKELETON + the one detailed kingdom inside it "
                "(+ ~6 ruins). Geometry & adjacency only; all place content comes "
                "from the tag recipes. Grow the rest on demand.")
        return draft_block(f"World (kingdom scope): {kname} in {rname}",
                           body, seed, note)

    sys.exit(f"Unknown scope '{scope}'. Use "
             "region | few-nations | continent | kingdom.")


def cmd_geography(roller, scale, fresh, seed, campaign=None):
    if scale == "region":
        name, body, nodes = compose_geography_region(roller, fresh, campaign)
        body += persist_note(campaign, nodes)
        note = ("Region SKELETON (book pp.124-127): oceanic frame, ~6 terrain "
                "features, 1d4+2 rivers, 1-3 lakes, 6 nations on natural borders. "
                "NO cities or ruins at this scale — geometry & adjacency only.")
        return draft_block(f"Geography — Region: {name}", body, seed, note)
    if scale == "kingdom":
        name, body, nodes = compose_geography_kingdom(roller, fresh, campaign)
        body += persist_note(campaign, nodes)
        note = ("Kingdom DETAIL (book pp.124-127 + p.49): small-scale terrain, "
                "demographics (60/sq mi, ~10% urban), capital on water then "
                "cities clockwise; each city carries 2 Community + 2 Court tags. "
                "Next: `worldgen.py ruins --kingdom " + name + "`.")
        return draft_block(f"Geography — Kingdom: {name}", body, seed, note)
    sys.exit(f"Unknown scale '{scale}'. Use region | kingdom.")


def cmd_ruins(roller, kingdom, fresh, seed, campaign=None):
    name, body, nodes = compose_ruins(roller, kingdom, campaign,
                                      latter_earth=not fresh)
    body += persist_note(campaign, nodes)
    note = ("~6 famous ruins (book p.150) placed in the wilderness gaps between "
            "trade routes; each = a ruin-type roll + 2 Ruin Tags + a line. "
            "These are sketch nodes — flesh one out only when the PC commits.")
    return draft_block(f"Ruins — {kingdom}", body, seed, note)


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
    scale = None
    if "--scale" in args:
        scale = args[args.index("--scale") + 1]
    kingdom = None
    if "--kingdom" in args:
        kingdom = args[args.index("--kingdom") + 1]
    campaign = None
    if "--campaign" in args:
        campaign = args[args.index("--campaign") + 1]

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
        elif cmd == "geography":
            if not scale:
                sys.stdout = real_stdout
                sys.exit("geography needs --scale <region|kingdom>.")
            block = cmd_geography(roller, scale, fresh, seed, campaign)
        elif cmd == "ruins":
            if not kingdom:
                sys.stdout = real_stdout
                sys.exit("ruins needs --kingdom <name>.")
            block = cmd_ruins(roller, kingdom, fresh, seed, campaign)
        elif cmd == "world":
            if not scope:
                sys.stdout = real_stdout
                sys.exit("world needs --scope "
                         "<region|few-nations|continent|kingdom>.")
            block = cmd_world(roller, scope, fresh, seed, campaign)
        else:
            sys.stdout = real_stdout
            sys.exit(f"Unknown command '{cmd}'. See --help.")
    finally:
        sys.stdout = real_stdout

    # Committable DRAFT CANON markdown -> STDOUT.
    print(block)


if __name__ == "__main__":
    main()
