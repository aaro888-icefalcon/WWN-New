# Implementation Plan #1 — Character Creation & Dynamic Worldgen

> The **buildable** version of `CHARGEN-WORLDGEN-FIX-PLAN.md`: file-by-file, function-by-function work
> items with acceptance criteria. Extends the original plan with (a) **Atlas of the Latter Earth**
> content folded *into character creation*, and (b) **kingdom/region generation wired into scene-setting
> and end-of-scene bookkeeping**, so new regions generate **dynamically as the PC explores them**.
>
> Companion docs: `references/rules/character-creation-compendium.md` (the rules digest),
> `CHARGEN-WORLDGEN-FIX-PLAN.md` (the review this expands).

---

## Part 0 · Conventions & guardrails (apply to every item)

- **Honest dice, shown.** Every new roll goes through the existing `roll()` (chargen) / `gen.Roller`
  (worldgen) so dice print in the `NdM -> [...] = K` format and stay seed-reproducible.
- **Player-in-the-loop.** New interactive paths *stop at each choice*; `--random` keeps auto-resolving.
- **Frontier rule preserved.** Only the starting region/kingdom is detailed; everything else is a
  one-line sketch grown on demand. No pre-building the map.
- **Std-lib only, Python 3.6+.** No new dependencies.
- **Data, not code, for content.** New game content (classes, foci, tags, terrain tables) goes in
  `bridge/generators/*.json` and is *read*, so `lookup.py`/`gen.py` see it too — not hard-coded.

---

## Part 1 · chargen.py — the reviewed fixes (expanded to implementation)

### 1.1 Quick wins (low risk, do first)
| Item | File · location | Change |
|---|---|---|
| Roll-wealth print bug (#5) | `chargen.py` `step_final` L791 | `print("  Starting wealth: %d sp ..." % sp)` — add the missing `% sp`. |
| Focus page numbers (#6) | `chargen.py` `FOCI` dict | Correct each `"page"` to the real book page (Alert 22 … Whirlwind 28 etc.). Source pages already in the compendium/`02-Character-Creation.md`. |
| HP folding (#7) | `chargen.py` `Character` + `step_final` | Add `self.focus_hp_bonus = 0`; foci add to it; `step_final` sets `ch.hp_max = max(1, base + con) + ch.focus_hp_bonus`. Remove the brittle `hp_max - 1 + hp` expression. |

**Acceptance:** `chargen.py --roll-wealth` prints the silver value; `lookup.py focus <x>` shows correct
pages; a Die Hard build's HP = rolled + Con + 2/level exactly.

### 1.2 Data-driven tradition layer (#2, #3, #4) — the high-value fix
**New data file `bridge/generators/traditions.json`** — one record per tradition:
```
{ "name": "Healer", "kind": "arts",            // spells | spellpoints | arts
  "full_or_partial": "partial",                 // full | partial | both
  "effort_skill": "Heal",                       // Magic|Heal|Pray|Survive|Stab|Notice|order
  "effort_attrs": ["Int","Cha"],                // pair; Vowed = "best"
  "spell_lists": [],                            // which spells.json lists it draws
  "free_arts": ["Healing Touch"], "chosen_arts_L1": 1,
  "known_spells_full": 0, "known_spells_partial": 0,
  "notes": "works in armor; Limb/Revive need L8+", "page": 80 }
```
Populate all 11: High Mage, Elementalist, Necromancer, Adunic Invoker, Healer, Vowed, Darian
Skinshifter, Kistian Duelist, Llaigisan Beastmaster, Sarulite Blood Priest, Vothite Thought Noble
(values from the compendium §5).

**chargen.py changes:**
- Load `traditions.json` into a `TRADITIONS` dict at import (with a small fallback if the file is absent).
- Replace `_setup_tradition`: present the **full menu** (filtered by `full_or_partial` vs the chosen
  class), let the player pick (or auto-pick under `--random`). Store `ch.tradition_rec`.
- Replace the Effort block in `step_final` to compute from the record:
  `effort = base_skill_level + attr_term` where `base_skill_level` = the level of `effort_skill`
  (Magic/Heal/Pray/Survive/Stab/Notice), `attr_term` = `max(mods of effort_attrs)` or `best of all mods`
  for Vowed; apply the `1 +`/partial `−1`/`min 1` rules per `kind`. Adunic Invoker uses the spell-point
  line instead (`pts = 1 + Int mod` scaling).
- **Wire starting spells/arts (#4):** for `kind in (spells, spellpoints)` pull the tradition's first-level
  spell names from `spells.json` and present them; for `kind == arts` present the art names. Pick the
  right count (`known_spells_full/partial`, `free_arts` + `chosen_arts_L1`, Blood Priest = 2 chosen).
  For the six Gyre classes still **lacking encoded arts**, fall back to a cited pointer
  (`11-Arts-of-the-Gyre.md`) until those arts are added to `spells.json` (Part 1.5).

**Acceptance:** `chargen.py --class mage --interactive` lets you pick any of the 11 traditions; a Healer's
Effort uses Heal; a Blood Priest's uses Pray; starting spells/arts are real names from `spells.json`
(or a clear pointer for un-encoded Gyre arts).

### 1.3 Interactive step-by-step mode (#1, #8) — the headline feature
Add `--interactive` (additive; `--random` and explicit flags unchanged). A thin `ask()` helper
(`input()` with a numbered menu + default) drives the existing step functions, **pausing at every
decision** in book order:
1. `step_attributes` — roll 3d6×6 shown → ask which score → 14 (or decline / array).
2. `step_background` — roll-or-pick d20 → ask skill mode → for *roll-three*, ask the Growth/Learning
   **split per roll** (fixes #8) → show each die.
3. `step_class` — menu Warrior/Expert/Mage/4 Adventurer combos (+ Atlas classes from Part 2).
4. `step_foci` — per slot, present the **eligible** focus list, pick; apply effects.
5. tradition + spells (Part 1.2).
6. `step_final` — free skill menu; roll HP; package-or-wealth; prompt name/goal/ties; write sheet.

**Acceptance:** a full PC can be built end-to-end by answering prompts, every die shown, no auto-picks;
piping a fixed answer file reproduces a known sheet with `--seed`.

### 1.4 Engine-roller integration (optional polish)
`roll()` already supports `MYTHIC_GM_DICE`. Leave as-is, but confirm the interactive prompts also echo
through `LOG` so a transcript captures the build.

### 1.5 Stretch — encode Gyre arts
Extend `build_magic.py` / `spells.json` with the arts for Adunic Invoker, Skinshifter, Duelist,
Beastmaster, Blood Priest, Thought Noble (from `11-Arts-of-the-Gyre.md`). Then the tradition picker shows
real options for **all 11** traditions and `lookup.py spell <art>` resolves them.

---

## Part 2 · Atlas of the Latter Earth — folded *into* character creation

The Atlas adds creation-time content. **Default = all classes available** — core (Warrior/Expert/Mage +
the four Adventurer combos), all Gyre traditions, and the four Atlas partials are *all* on the menu by
default. The content profile (2.5) is an **opt-out** for tone-restricted games, not an opt-in.
Source: `04-Optional-Rules-and-Classes.md`, plus Latter-Earth origins in the Deluxe
`06-The-World-of-the-Latter-Earth.md`. **Character Tags are NOT a creation step** — see 2.3.

### 2.1 Four new partial classes (Atlas ch. 04)
Add to `CLASSES` (and `traditions.json` where they grant arts):
- **The Accursed** — partial; cursed/supernatural, has *Accursed Arts* (Effort-fuelled). Treat like a
  Gyre arts-class record.
- **The Bard** — partial; *Bard Arts*; social/inspiration magic.
- **The Mageslayer** — partial; anti-magic warrior; *Mageslayer Arts*; has Pw/Mageslayer and
  Pe/Mageslayer combos (add the two attack-bonus rows).
- **The Wise** — partial; subtle magic for low/no-magic settings; *General + Divination Arts*,
  Curses & Blessings.

Each needs: HD/attack-bonus contribution, Effort skill+attrs, free/chosen arts at L1, and the legal
Adventurer pairings. Encode arts in `spells.json` (or pointer-fallback initially).

### 2.2 New Foci (Atlas ch. 04)
Add to `FOCI` (with correct pages) and `foci.json`:
- **Mundane Alchemist** (Focus; brew alchemical Lesser/Greater Works).
- **Maqqatban Knight styles** — Ghost Archer, All Directions Edge, One Point Strike, Pyre of Heaven,
  Catalytic Soul, Wrathful Mountain, Righteous Iron, World Tree Lance (martial style foci).
- **Amundi Godblood Foci** — bloodline powers.
Mark each `combat`/eligibility and any class restriction so `_focus_ok_for` filters them correctly.

### 2.3 Character Tags are an NPC adjunct — NOT a PC creation step
`character_tags.json` / `character_tags_detail.json` are an **NPC/Mythic tool, not a chargen step.**
chargen does **not** offer them to the player. They belong to the world-generation side, as an adjunct to
the Mythic emulator and The Adventure Crafter:
- They already drive `worldgen.short_npc()` (role + characteristic twist + **Ambition** + now the tag's
  full summary — see the tag-fidelity fix).
- When the oracle **spawns or deepens an NPC** (a Random Event "NPC Action", an Adventure Crafter
  Character/plot-point, a Fate Question that names someone), roll/assign a Character Tag for drama and let
  its **Ambition become that NPC's Thread** on the engine Lists.
- The PC's own goal/ties stay a deliberate player choice at "name, goal, ties" (compendium §8), unaided by
  a tag roll.

This keeps tags surfacing *the world* (NPCs the engine introduces) and out of the player's build.

### 2.4 Latter-Earth origins & languages
- **Origins:** enumerate the Latter-Earth playable origins (human default; **Blighted/Anakim** and any
  Deluxe bestiary origins) as `Special Origin` sub-options with their mechanical notes, gated by GM
  permission (a content-profile flag).
- **Languages:** at "Record starting languages", offer the **Gyre tongues** list
  (Deluxe p.107 / setting-canon) so a Latter-Earth PC picks real languages, not placeholders.

### 2.5 Campaign content profile (an OPT-OUT; default = everything on)
New `campaign/content-profile.json` (written at Session Zero, read by chargen). **Defaults enable all
content;** the profile only ever *removes* options for a tone-restricted game.
```
{ "magic_level": "default",          // default | low | no   (default = full menu)
  "allow_atlas_classes": true,        // Accursed / Bard / Mageslayer / Wise
  "allow_gyre_arts": true,            // the six Gyre arts-classes
  "allow_nonhuman_origins": true,     // Blighted/Anakim & bestiary origins
  "optional_rules": [] }              // e.g. "maiming","slow_healing","more_strain"
```
- `magic_level: default` (the default) → **every class/tradition/focus is offered.**
- `magic_level: low` → opt-out: no full Mages/dual partials, no Healers, Wise becomes the main caster.
- `magic_level: no` → opt-out: only Warrior/Expert/Pe-Pw; strike supernatural foci (Nullifier, Lucky,
  Spirit Familiar, …) per the Atlas list.
chargen filters the menus against this profile, but with defaults the player sees the **full** roster.
**Conclusion of creation:** any chosen optional rules (maiming, slow healing, more System Strain) are
written into `campaign/campaign-state.md` so play and bookkeeping honor them.

**Acceptance:** a default campaign offers **all** classes — core + 4 Adventurer combos + 11 traditions +
the 4 Atlas partials + Maqqatban/Amundi/Alchemist foci. Setting `magic_level: no` removes casters and
supernatural foci. No step ever asks the player to roll a Character Tag.

---

## Part 3 · worldgen.py — the map / country→region→location pipeline

### 3.0 Design contract (why this stays legible to Mythic)

**Pillar 1 — separate the skeleton from the fill.** The two-map system owns **geometry & adjacency only**.
It never invents place content: every node it places (settlement/court/ruin/wilderness) gets its character
by **deferring to the existing tag subsystem** (`gen.py`'s recipes + `*_tags(_detail).json`), which
`worldgen.py` already imports. The map says *where*; the tag recipe says *what*. No duplicated content.

**Pillar 2 — three synchronized artifacts per run** (the scene system reads canon + Lists + seeds, never a
raw map):
1. **Canon block** → prose appended to `setting-canon.md` (human ground truth).
2. **Location graph** → `campaign/places.json` nodes (the *machine* output; its job is **proximity**, which
   powers the `world-model.md` §5 weighting — "PC's region > adjacent > distant", "close enough to show a sign").
3. **List + seed cards** → each hook → **Thread**, each figure → **Character**, each site/hazard →
   **Adventure Feature** (via `state.py`), each nation → faction board (the `world-model.md` §2 mapping).

**Pillar 3 — the structured card the scene framer already eats.** Per-place output is a short, typed card
matching the existing fractal-seed shape (no new parser needed):
```
- [PLACE site:ruin id=R-07 region=Veshmarch kingdom=Emed-Kist near=cap+2d w=1]
  Korvault — ruin; <full tag summary + 5 sub-tables>. → Thread: "what woke in Korvault" (w2)
```
The bracket header is machine-parsed (proximity/weight); the prose is narrated. Graph node and card share
the `id`, so they stay in sync. Tag fidelity (Part 4.3) applies: the card carries the **full** tag.

**Pillar 4 — `places.json` schema** (the persistent graph; one node per region/kingdom/site):
```
{ "id": "R-07", "name": "Korvault", "kind": "ruin",     // region|kingdom|settlement|court|ruin|wilderness
  "parent": "K-Emed-Kist", "adjacency": ["S-03","W-02"], // graph edges (neighbours)
  "travel_days": 2, "status": "sketch",                  // sketch | detailed
  "tag": { "name": "...", "summary": "...", "subtables": {Enemies..Places} },  // FULL tag, not a stub
  "threads": ["T-12"], "characters": ["C-09"], "canon_anchor": "setting-canon.md#korvault" }
```

### 3.1 New data: `bridge/generators/geography_construction.json`
Encode the book's tables (Geography Construction ch.04; Placing Ruins ch.10):
- `Significant Terrain Features` (d20) + one-roll detail dice (d4 populated · d6 dangerous · d8 use ·
  d10 last event · d12 antagonists · d20 quirk).
- `General Places of Adventure` (d20) and `Latter-Earth Places` (d12) for ruin types.
Register in `registry.md` and `manifest.json`; verify with `gen.py`/`lookup.py`.

### 3.2 New commands / scopes (compose with honest dice; emit DRAFT CANON)
| Command | Book procedure encoded |
|---|---|
| `worldgen.py geography --scale region` | oceanic sides → ~6 terrain features (detailed) → `1d4+2` rivers (split-downstream-only, ≤¼ map) → 1–3 lakes → 6 nations on natural borders. **No cities/ruins yet.** Relational sketch + coordinate hints. |
| `worldgen.py geography --scale kingdom` | small-scale terrain → demographics (60/sq mi; 10% urban, ⅓ capital, ¼ second city) → capital then cities **clockwise from a random cardinal** → tag each city (2 Community + 2 Court tags). |
| `worldgen.py ruins --kingdom <name>` | trade-route mesh → wilderness gaps → **6 ruins**, each = type roll + 2 Ruin Tags + 1 line. |
| `world --scope kingdom` (new) | region + the one detailed kingdom inside it. |

### 3.3 Map representation
Emit a **relational sketch** (the book wants "loose scrawls," two maps, optional 6-mile hexes) — a feature
list with cardinal/edge hints, rivers as "from <highland> → <sea/lake>", nations bounded by named
barriers, and an optional ASCII grid / coordinate table the player can hand-draw from. No pixel art.

**Acceptance:** `geography --scale region` yields a committable DRAFT CANON block with 6 features, 1d4+2
rivers, ≤3 lakes, 6 bordered nations, and a sketch; `ruins --kingdom` places 6 tagged ruins in the gaps.

---

## Part 4 · Dynamic region generation — wired into scene-setting & bookkeeping

The point: **a new region/kingdom is generated the moment play reaches or names it**, then folded into
canon so it persists. Two integration points — the **front** of the Turn (framing a scene) and the
**back** (end-of-scene bookkeeping) — plus the canon write that links them.

### 4.1 Scene-setting hook (front of the Turn) — *generate before you describe*
When the GM frames the next scene and the PC is **entering somewhere not yet in `setting-canon.md`**:

1. **Detect the frontier.** Classify the destination:
   - new **site** in a known kingdom (town/court/ruin/wilderness) → existing
     `worldgen.py settlement|court|ruin|wilderness`;
   - new **kingdom** (crossed a border) → `worldgen.py geography --scale kingdom` (+ `ruins`);
   - new **region** (travelled off the edge of the detailed region) → `worldgen.py geography --scale
     region` then detail the entered kingdom.
2. **Generate just-in-time** at the smallest scope that covers what the PC can perceive this scene
   (don't over-build ahead of play — the frontier rule).
3. **Show the DRAFT CANON**, let the player keep/reroll/adjust, **then describe the scene** from the
   approved result and ask "What do you do?".

This is added to the **SKILL.md play loop** ("Framing a scene") and `references/gm/worldgen.md §3 Lazy
expansion` as an explicit *new-region* branch (today it only covers single places). The trigger also
fires when an **oracle / Fate Question names a place that doesn't exist** — same flow, generate then narrate.

### 4.2 End-of-scene bookkeeping hook (back of the Turn) — *record & queue*
Add a **frontier subsystem row** to `bridge/subsystems.md` so `tick.py` surfaces it every scene:

```
| Frontier expansion | on trigger: PC approaches/names an uncharted region or kingdom | generate it
  with worldgen.py at the right scope BEFORE the next scene; append the approved DRAFT CANON to
  setting-canon.md; add its hooks as Threads, named figures as Characters, and put any new nation on
  the faction board. |
```
And add a **frontier step** to the `bookkeep.py` checklist (between LISTS and SELF-AUDIT):

```
N. FRONTIER: did this scene reach the edge of charted canon, or name a new region/kingdom? If yes →
   queue `worldgen.py geography --scale <region|kingdom>` for next framing; fold the approved result
   into setting-canon.md and seed Threads/Characters/faction board. Un-recorded new places are a soft
   scene — the world must persist what play discovered.
```

So the loop is symmetric: **bookkeeping flags & queues** the expansion and writes discovered facts to
canon; **scene-setting consumes the queue**, generating and narrating the new region next beat.

### 4.3 The canon write (what makes it persist)
On approval (either hook), the generated region/kingdom is **appended to `setting-canon.md`** under the
matching section — it becomes ground truth, overriding recollection (exactly as the file's
"Generate-on-demand frontier" section already prescribes). Concretely, per new region/kingdom:
- paste the geography sketch + nation/kingdom briefs into `setting-canon.md`;
- **Threads List** ← one thread per generated hook (`state.py thread add`);
- **Characters List** ← each named figure (`state.py char add`);
- **faction board** ← each new nation (faction sheet / `seeds.md`);
- **seed deck** ← refreshed to 30–40 from the new canon;
- **`places.json`** ← a node per place (Pillar 4 schema), holding the **full tag**, adjacency, `status`,
  and the shared `id`s of its Threads/Characters + a `canon_anchor` back into `setting-canon.md`.
These are the same `state.py`/`seeds` calls bookkeeping already runs, plus the one new `places.json` write,
so the wiring is additive.

**Re-entry is a lookup, not a reroll (Pillar 6).** Because each node persists with its rolled tag and
links, returning to a place reads its saved character; the generator is called **only** when a node is
absent or being promoted `sketch → detailed`. Shared `id`s let a resolving Thread find and update the exact
node — no orphaned prose, no duplicate towns.

**Tag fidelity (hard rule).** Whenever a place/figure is generated from a tag, the **full** tag must be
surfaced and saved — its **summary paragraph AND all five sub-tables** (Enemies/Friends/Complications/
Things/Places), and for character tags the summary + Ambition — never just the tag name or one sub-table.
This is now enforced in the generators (`gen.py` RESULT, `worldgen.py` place/region/nation/NPC composers
via `full_tag_block`); the `places.json` node must store the same complete tag so re-entry re-surfaces it
to context rather than re-rolling or reading a thin stub.

### 4.4 Cadence & anti-flood (Pillar 5 — called in context, without gumming up Mythic)
Three governors keep generation from swamping the emulator:
- **Scope ladder + smallest-covering-scope.** Site < kingdom < region. The frontier hook generates only
  what the PC can perceive this scene. **Region scope fires rarely** (only when the PC leaves the detailed
  region) — a once-per-arc, player-approved event; **kingdom/site scope** is the common border/new-town case.
- **Proximity-graded entry into the Lists/seeds.** A whole new kingdom generated at a border must **not**
  crowd out the scene in front of the PC. New **distant** content enters the deck at **low weight (≤1)**;
  the `places.json` adjacency feeds `world-model.md` §5 so near content always outweighs it — distant hooks
  sit dormant until proximity rises. This is the anti-flood mechanism.
- **Two fixed call sites, never speculative.** Invoked only from the scene-framing frontier hook (4.1) and
  the bookkeeping FRONTIER step (4.2, surfaced by `tick.py` via the subsystem row). Everything beyond
  scene-need stays a **one-line `sketch`** node; ruins flesh out only on PC commitment.

**Acceptance:** travelling into an uncharted kingdom triggers (a) a generated, player-approved kingdom at
scene-framing, narrated before "What do you do?", and (b) a bookkeeping FRONTIER entry that appends it to
`setting-canon.md` and seeds the Lists/faction board — so re-entering it later reads from canon, not a
re-roll.

---

## Part 5 · Sequencing & acceptance

1. **Part 1.1** quick wins → 2. **Part 1.2** tradition layer + spells → 3. **Part 2.1–2.2, 2.4–2.5** Atlas
   classes/foci/origins + the all-on-by-default content profile → 4. **Part 1.3** interactive chargen (now
   offers the full default roster) → 5. **Part 3** worldgen geography data + commands + `places.json` →
   6. **Part 4** scene / bookkeeping wiring + doc updates → 7. **Part 1.5 / 3 stretch** encode Gyre & Atlas
   arts and ruin tables. *(2.3 is a no-op for chargen — tags stay an NPC/worldgen adjunct.)*

Every step keeps honest-shown dice, the player-in-the-loop contract, and the frontier rule. Docs to
update alongside code: `SKILL.md` (play loop + Session Zero), `references/gm/worldgen.md`,
`references/rules/character-creation.md`, `bridge/subsystems.md`, `scripts/bookkeep.py`.

**Definition of done for the headline goals:**
- *In-play creation:* `chargen.py --interactive` walks every step, shows every die, offers the **full
  default roster** (all classes/traditions/foci unless the campaign opted out), and writes a complete
  sheet whose goal/ties are the player's own choice (no tag roll).
- *Dynamic worlds:* crossing into uncharted land generates the region/kingdom at framing, narrates it,
  and bookkeeping persists it to `setting-canon.md` + `places.json` + the Lists — new regions appear
  *because the PC explored them*, carry their full tags, and re-entry is a lookup, not a reroll.
