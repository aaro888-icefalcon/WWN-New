# GM Tools — the generator bank, indexed

> Use this when: you're stuck for a name, a face, a building, a twist, or a premise, and want the WWN table that fills the gap. This is the index; the full routing table (with replace/conjunction modes) lives in `bridge/generators/registry.md`.

**How to roll:** named tables inside a bundle → `python3 scripts/gen.py <bundle>/"<Table>"`; one record without loading a file → `python3 scripts/lookup.py <kind> "<name>"`; flat `d100` files → `python3 mythic-gm/scripts/dice.py table bridge/generators/<file>.json`. All `gen.py` dice are honest, shown, and `--seed`-reproducible. Plain dice via `mythic-gm/scripts/dice.py roll <NdM>`.

## Oracular adventure adjustments — un-stick your own ideas
When a concept feels *almost* right, roll one of these (book L45–116; not yet in a bundle — roll by hand) and bend, don't railroad:
- **Idea affirmation/negation** `dice.py roll 1d4` — 1 No/opposite · 2 No/related · 3 Yes but an assumption is wrong · 4 Yes, push it farther.
- **Change this NPC** `1d12` · **This mistake twists the adventure** `1d6` · **Theme informs it** `1d8` · **Reality intrudes** `1d10` · **Throw this event in** `1d20`.
Adventure-hook *delivery* (`1d20`) and **Bait** (`1d10`) also live here → `gen.py adventure_seeds/"Bait"` and `/"Introduction"`.

## Architecture generators — a civilization's look
Give a culture (or a ruin's builders) a consistent visual identity; recognizing it later rewards player attention. Bundle `architecture.json` — seven `d8` tables, all via `gen.py architecture/"<Table>"`:
**Architectural Adjectives · Favorite Materials · Favorite Color Schemes · Common Visual Motifs · Structure Adornment · Favorite Structural Features · Settlement Design Patterns.** (`gen.py architecture` alone rolls all seven.)

## Fractal adventure seeds — a premise in a few rolls
Get a handful of **Enemies / Friends / Complications / Things / Places**, roll **`dice.py roll 1d100`** on `fractal_seeds.json` for a structural premise ("A *Thing* is in a dangerous *Place*, and a *Friend* knows how to get it"), and plug the components in. Keep complicating by rolling a `d20` sub-seed on one component and nesting it. The engine does all of this for you: **`python3 scripts/gen.py hook`** draws a location tag, rolls its five component sub-tables, fills a fractal seed, and adds Bait + Introduction. (See `references/gm/creating-adventures.md`.)

## NPC types & twists — someone for the scene
Need a face fast: `gen.py npc` (role + `d12` twist + appearance + an Ambition), or pull a specific flavor from bundle `npc_quickgen.json`:
- **By class:** `npc_quickgen/"Random NPC (Underclass)"`, `(Commoners)`, `(Gentry)`.
- **By type:** Specific **Criminals / Merchants / Nobility / Tribals / Villagers / Warriors**.
- **Spin:** `npc_quickgen/"Characteristic Twists"` (`d12` — secret identity, looming disaster, a useful odd friend…).
- **Appearance:** Physical Build · Way They Move · Clothing · How They Differ · Visible Mannerisms.
Court tags (`gen.py court`) add a target's social context, minions, and resources.

## One-Roll Characterization — depth for a recurring NPC
For a running antagonist, lasting ally, or VIP who needs more than a function. Bundle `npc_depth.json` (use `gen.py npc_depth/"<Table>"`, or `gen.py npc_depth` for the lot); these are *suggestions* — overrule the dice freely. Each strand should give the PCs a **lever**, or it's just padding:
- **First Thing Noticed** — the visual hook.
- **Burning Ambition** — Form · Obstacle · Help-or-Hinder · Who Knows · Tools Used (the NPC's drive; PCs can exploit it).
- **Personal Tragedy** — Form · Coping · Consequences · Scars (sympathetic fuel).
- **Close Friendship** — What Done Together · Harmonizing Tie · What Divides · Things Between.
- **Troubled Romance** — Spark · Problem · Current Issue · Quirks.

Source: `book/Worlds-Without-Number-Deluxe/15-Additional-GM-Tools.md` (oracular L45–116; architecture L118–225; fractal seeds L226–465; NPC types L466–597; One-Roll Characterization L598–981). Routing & modes: `bridge/generators/registry.md`.
