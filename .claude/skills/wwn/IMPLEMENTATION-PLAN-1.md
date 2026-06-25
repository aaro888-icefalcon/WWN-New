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

The Atlas adds creation-time content that should be selectable in chargen (gated by a campaign
**content profile**, since much of it is optional/setting-toned). Source: `04-Optional-Rules-and-Classes.md`,
`05-Character-Tags.md`, plus Latter-Earth origins in the Deluxe `06-The-World-of-the-Latter-Earth.md`.

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

### 2.3 Character Tags as a creation step (Atlas ch. 05)
`character_tags.json` / `character_tags_detail.json` already exist but chargen ignores them. Add an
**optional creation step** (after background, before/after foci): offer to **roll or pick 1 Character Tag**
(Baneful Success, Bitter Grudge, Hidden Origins, …) to seed the PC's dramatic hook — and record its
**Ambition** into the sheet's Goal/Ties and as a starting **Thread** for the engine Lists. This directly
serves the "goal worth dying for" requirement and gives Session Zero a built-in hook.

### 2.4 Latter-Earth origins & languages
- **Origins:** enumerate the Latter-Earth playable origins (human default; **Blighted/Anakim** and any
  Deluxe bestiary origins) as `Special Origin` sub-options with their mechanical notes, gated by GM
  permission (a content-profile flag).
- **Languages:** at "Record starting languages", offer the **Gyre tongues** list
  (Deluxe p.107 / setting-canon) so a Latter-Earth PC picks real languages, not placeholders.

### 2.5 Campaign content profile (gates all of the above)
New `campaign/content-profile.json` (written at Session Zero, read by chargen):
```
{ "magic_level": "default|low|no",   // low/no-magic class & focus restrictions (Atlas ch.04)
  "allow_atlas_classes": true, "allow_gyre_arts": true,
  "allow_nonhuman_origins": false, "optional_rules": ["maiming","slow_healing", ...] }
```
- `magic_level: low` → no full Mages/dual partials, no Healers, Wise becomes the main caster.
- `magic_level: no` → only Warrior/Expert/Pe-Pw; strike supernatural foci (Nullifier, Lucky, Spirit
  Familiar, …) per the Atlas list.
chargen filters the class/focus/tradition menus against this profile so the player is only offered what
the campaign allows. **Conclusion of creation:** the chosen optional rules (maiming, slow healing, more
System Strain) are written into `campaign/campaign-state.md` so play and bookkeeping honor them.

**Acceptance:** with `magic_level: no` the tradition step is skipped and supernatural foci are hidden;
with Atlas enabled, Bard/Mageslayer/Wise/Accursed and the Maqqatban styles appear in the menus; a chosen
Character Tag lands in the sheet's Goal and as a starting Thread.

---

## Part 3 · worldgen.py — the map / country→region→location pipeline

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
- **seed deck** ← refreshed to 30–40 from the new canon.
These are the same `state.py`/`seeds` calls bookkeeping already runs, so the wiring is additive.

### 4.4 Cadence & "don't over-generate"
- **Region scope** is generated **rarely** (only when the PC leaves the detailed region) — a once-per-arc
  event, fully player-approved.
- **Kingdom/site scope** is the common case at a border or a new town.
- Everything beyond what the scene needs stays a **one-line sketch**; deeper detail waits for the PC to
  commit (ruins fleshed out only on entry). The bookkeeping FRONTIER step explicitly warns against
  pre-building.

**Acceptance:** travelling into an uncharted kingdom triggers (a) a generated, player-approved kingdom at
scene-framing, narrated before "What do you do?", and (b) a bookkeeping FRONTIER entry that appends it to
`setting-canon.md` and seeds the Lists/faction board — so re-entering it later reads from canon, not a
re-roll.

---

## Part 5 · Sequencing & acceptance

1. **Part 1.1** quick wins → 2. **Part 1.2** tradition layer + spells → 3. **Part 2.5 + 2.1–2.4** Atlas
   content gated by the content profile → 4. **Part 1.3** interactive chargen (now offers the full,
   profile-filtered menus) → 5. **Part 3** worldgen geography data + commands → 6. **Part 4** scene /
   bookkeeping wiring + doc updates → 7. **Part 1.5 / 3 stretch** encode Gyre & Atlas arts and ruin tables.

Every step keeps honest-shown dice, the player-in-the-loop contract, and the frontier rule. Docs to
update alongside code: `SKILL.md` (play loop + Session Zero), `references/gm/worldgen.md`,
`references/rules/character-creation.md`, `bridge/subsystems.md`, `scripts/bookkeep.py`.

**Definition of done for the headline goals:**
- *In-play creation:* `chargen.py --interactive` walks every step, shows every die, offers all
  book + Atlas options the content profile allows, and writes a complete sheet incl. a Character-Tag goal.
- *Dynamic worlds:* crossing into uncharted land generates the region/kingdom at framing, narrates it,
  and bookkeeping persists it to `setting-canon.md` + the Lists — new regions appear *because the PC
  explored them*, and stay.
