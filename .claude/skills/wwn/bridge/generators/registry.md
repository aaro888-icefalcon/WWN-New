# Generator Index — Worlds Without Number   (hooks: generate:*)

## Operative
When a generation need below is triggered, ROLL its registered WWN table
(`python3 <mythic-gm>/scripts/dice.py table <abs path>/bridge/generators/<x>.json`, or the `scripts/gen.py`
/ `scripts/lookup.py` wrappers) — don't free-form what a table exists for. NEW CHARACTERS auto-fire the
character generator (the AC Character Crafter **in conjunction** with `npc_role.json` / `npc_quickgen`);
keep `--bridge <this-skill>/bridge` on the roller calls so this index's overrides apply. Flesh every NPC as a
Latter Earth native, tied to a setting-canon faction and the current region. Anything not listed below
falls through to the Mythic/AC engine default.

# Routing index — need · when called · table(s) · mode (replace | conjunction | default):
The routing index the engine/agent consults whenever a generate:* hook fires.
For each need: when it triggers, which generator table(s) to roll, and the
**mode** that decides how the result relates to the engine's own Mythic/AC
output:

- **replace** — use the WWN generator instead of the Mythic/AC default.
- **conjunction** — roll BOTH the engine default and the WWN table, then read
  them together (the WWN table adds WWN-specific texture).
- **default** — no WWN table; fall through to the Mythic/AC engine default.

| need                        | when called                                        | table(s)                                                        | mode        |
|-----------------------------|----------------------------------------------------|-----------------------------------------------------------------|-------------|
| generic NPC                 | any new throwaway/scene Character is invoked       | Mythic Character Crafter  +  `npc_quickgen` (role + twist + appearance) | conjunction |
| faction leader / major NPC  | a named antagonist, ally, or faction-level theme   | `character_tags` (→ detail: Ambitions / Powers / Dreads)        | replace     |
| faction / organization (full) | a new power needs Cunning/Force/Wealth + assets  | `worldgen.py nation\|court` + `faction.json` (tags · C/F/W assets) + `character_tags` (leader) | conjunction |
| settlement / community      | an unnamed or fresh town/village is introduced     | `community_tags` (→ 5 d3 sub-tables)                            | replace     |
| court / noble house         | a ruling court, household, or power-circle appears | `court_tags` (→ 5 d3 sub-tables)                               | replace     |
| ruin / site / dungeon       | a ruin, Deep, or point of interest is entered      | `ruin_tags` (→ 5 d3 sub-tables)  +  `monster_gen` (resident)    | replace     |
| wilderness / region         | a fresh region, hex, or wild area is generated     | `wilderness_tags` (→ 5 d3 sub-tables)                          | replace     |
| adventure hook              | a new hook/premise is needed                       | `adventure_seeds` (Bait d10, Intro d20)  +  `fractal_seeds` (d100) | replace     |
| treasure                    | loot must be placed for a site or foe              | `treasure` (silver matrix 2d6 · magic-count 1d20 · flavor)      | replace     |
| monster / fell creature     | a creature's shape, drive, or context is needed    | `monster_gen` (shape · drive · One-Roll Context · uncanny powers) | replace    |
| naval event                 | a sea-travel day, ship sighting, or ship crisis    | `naval` (Seafaring Event d10 · Ship Encounter d10 · Ship Crisis d12) | replace |
| NPC depth (recurring)       | a running antagonist/ally needs history & texture  | `npc_depth` (Burning Ambition · Tragedy · Friendship · Romance) | conjunction |
| architecture / civ flavor   | a culture's buildings or a ruin's style is needed  | `architecture` (7 × d8 style generators)                        | replace     |
| religion / god              | a faith or deity is built                          | `religion_construction` (origin · matter · want · function · portfolio · requirement) | replace |
| nation                      | a nation's problems, ties, or theme are set        | `nation_construction` (Problems · Good Things · Disputes · Ties · Themes) | replace |
| geography / terrain         | a region/kingdom's land, features, or ruins are placed | `geography_construction` (Significant Terrain Features d20 · How Populated d4 · How Dangerous d6 · What Use d8 · Last Event d10 · Common Antagonists d12 · Optional Quirk d20 · General Places of Adventure d20 · Latter-Earth Places d12) — composed by `worldgen.py geography\|ruins\|world` | replace |
| history                     | a group's origin/rise/peak/fall is built           | `history_construction`  +  `historical_crises` (d100)  +  `historical_events` (d100) | replace |
| wound / mishap              | a Mortal Wound maims, or an alchemy lab fails      | `wounds` (Maiming Wound d12 · Alchemical Accident d6)           | replace     |
| generic inspiration         | Discover Meaning with no WWN-specific need         | Mythic Elements (Meaning Tables)                                | default     |

Anything not listed above falls through to the Mythic/AC engine default.

**Lookups (not rolls):** pull one record without loading a chapter —
`python3 scripts/lookup.py focus|spell|monster <name>` (from `foci.json` / `spells.json` / `bestiary.json`),
and `lookup.py tag <name>` for any tag family.

## Rolling these tables

**Flat tables** are `list_d100` JSON in this folder, rolled directly by the engine:

    python3 <mythic-gm>/scripts/dice.py table <abs path>/bridge/generators/community_tags.json

Flat companions exist for every tag family (`character_tags`, `community_tags`,
`court_tags`, `ruin_tags`, `wilderness_tags` → d100 tag name), plus
`fractal_seeds`, `historical_crises`, `historical_events`.

**Bundles** (`kind: "bundle"`) hold several related tables in one file
(`npc_quickgen`, `adventure_seeds`, `treasure`, `monster_gen`, `naval`,
`wounds`, `npc_depth`, `architecture`, the three construction files). Roll a
named table inside one with the companion script:

    python3 scripts/gen.py naval/"Ship Encounter"

**Tag detail** (`kind: "tag_detail"`, the five `*_tags_detail.json`) is for
lookup and composition, not a flat roll. Expand it with:

    python3 scripts/lookup.py tag "Blood Feud"        # summary + d3 sub-tables
    python3 scripts/gen.py settlement --seed 1         # tag + all 5 sub-tables rolled
    python3 scripts/gen.py hook                        # a fractal seed filled live

All of `scripts/gen.py`'s dice are honest and shown (`1d100 -> [N] = N`) and
reproducible with `--seed`; `scripts/build_data.py` (re)builds and verifies
every file here (`manifest.json` carries the verification result).
