# Game Setup / Start Options — WWN on the mythic-gm engine

> The full set of choices for starting (or resuming) a game, with what each does and the defaults.
> Two things determine everything: whether a campaign already exists, and the choices made at Session
> Zero. Companion docs: `references/gm/worldgen.md` (worldgen dialog), `references/rules/character-creation-compendium.md`
> (the build rules), `REVISION-OPTIONS.md` (planned partial/collaborative generation).

---

## 0 · The fork — New game vs. Continue
The system checks for `campaign/campaign-state.md`:
- **Absent → WWN SESSION ZERO** (the guided setup below; ends on the First Scene + "What do you do?").
- **Present → CONTINUE** — read `campaign-state.md` (+ that campaign's `CLAUDE.md`), recap the last beat
  in 2–3 sentences, restate the Creed, resume the Turn. No setup choices.

---

## 1 · Session Zero — the six stages

| # | Stage | What you decide |
|---|---|---|
| 1 | Hardcore contract | Confirm honest dice, real consequences, no rescues (the Creed) |
| 2 | Content profile | What classes/magic/origins/optional-rules exist |
| 3 | World scope dialog | Scope · tone · magic level · **world source (4 options)** |
| 4 | World generation | Generate → review → commit; **factions generated here too** |
| 5 | Theme & stakes | Fixed theme priority + Chaos Factor |
| 6 | Character creation | Mode + every build choice |

Then it seeds the Lists, builds the First Scene (untested), asks "What do you do?", and stops.

---

## 2 · Stage 1 — the hardcore contract
A real yes/no: do you want the no-softening game? Confirming locks the Creed — shown dice never fudged,
NPCs act to win, death/maiming/ruin are permanent, the oracle's answer stands. Softer tone is expressed
through the **content profile** and **Chaos Factor**, never by relaxing dice honesty.

---

## 3 · Stage 2 — the content profile (`campaign/content-profile.json`)
**An opt-out: defaults enable everything.**
- **`magic_level`** — `default` (full roster: core + 4 Adventurer combos + 11 traditions + 4 Atlas
  partials) · `low` (no full Mages/dual-partials/Healers; Wise is the main caster) · `no` (only
  Warrior/Expert/Pe-Pw; supernatural foci struck).
- **`allow_atlas_classes`** / **`allow_gyre_arts`** / **`allow_nonhuman_origins`** — independent toggles.
- **`optional_rules`** — e.g. `maiming`, `slow_healing`, `more_strain`; written into `campaign-state.md`
  so play & bookkeeping honor them.
The profile filters the chargen menus (Stage 6).

---

## 4 · Stage 3 — the world scope dialog (four questions)

| Question | Options |
|---|---|
| **Scope** | **region** ▸ **few nations** ▸ **kingdom** ▸ **continent** |
| **Tone** | grim / weird / heroic; hard content lines (recorded in canon) |
| **Magic level** | rare-and-feared (default) ▸ common ▸ other |
| **World source** | the **four** options below |

### The four world sources
1. **Default Latter Earth** — the Gyre and its six successor-states from `setting-canon.md`; generation
   seeds from canon, hooks attach to it. The out-of-the-box start.
2. **Fresh world** (`--fresh`) — names & history rolled from scratch; **replaces `setting-canon.md`**.
3. **Provided setting** *(new)* — you supply your own setting (homebrew, another book, a pitch). The GM
   **ingests it into `setting-canon.md`** (premise, powers, named NPCs, content lines, and a proper-noun
   seed-pool), then generates places/factions seeded from *that* canon — hooks attach to your world. Your
   names become the generation name-pool instead of the Latter-Earth list.
4. **Guided / Modified Latter Earth** *(new)* — keep the Latter-Earth backdrop, but **specify the themes
   or gameplay for one (or more) region(s)** (e.g. "the starting march is a plague-haunted naval frontier;
   lean Mystery + Tension"). The GM **biases that region's generation** — terrain/community/ruin tag picks,
   faction goals/projects, and scene themes — toward your direction, recording the guidance in canon. The
   rest of the world stays default Latter Earth.

All four obey the **frontier rule**: only the starting region/kingdom is detailed; the rest grows on demand.

---

## 5 · Stage 4 — world generation (incl. factions)

Scope picks the command; all use **honest, shown dice** and a **draft → feedback → commit** loop (every
block is a labeled DRAFT CANON *proposal* you keep / reroll `--seed N` / adjust / hand-author before it
folds into `setting-canon.md`).

| Command | Builds |
|---|---|
| `region` | a light ~200-mi region: terrain tag + 1–2 settlements + a ruin + hooks |
| `geography --scale region` | map 1: oceanic frame → ~6 terrain features → `1d4+2` rivers → 1–3 lakes → 6 bordered nations (no cities/ruins) |
| `geography --scale kingdom` | map 2: demographics → capital-then-clockwise cities (2 Community + 2 Court tags each) |
| `ruins --kingdom <name>` | ~6 ruins in the wilderness gaps, each type-roll + 2 Ruin Tags |
| `world --scope <region\|few-nations\|kingdom\|continent>` | scaffolds the chosen scope at once |
| `faction [--name N]` | a single faction stat block (Force/Cunning/Wealth, Goal, Project clock, assets) |

Key properties:
- **Full tag fidelity** — every place keeps its summary paragraph + all five sub-tables.
- **`places.json`** (with `--campaign DIR`) — each place is a node (full tag, adjacency, status, ids); the
  proximity graph the scene system reads. New regions then generate **as you explore them** and persist.
- **Factions are generated as part of world building** *(new)* — with `--campaign DIR`, every generated
  nation becomes a faction on `campaign/factions.md` (Force/Cunning/Wealth, a Goal, a Major-Project clock
  seeded from the nation's problem, a Base of Influence + assets). The board is live from scene one.

---

## 6 · Stage 5 — theme & stakes
- **Theme priority is fixed** for WWN: every adventure rolls **Action ▸ Social ▸ Tension ▸ Personal ▸
  Mystery** (`adventure_crafter.py themes --style wwn`). Deterministic, not a weighted draw.
- **Chaos Factor = 5** at start — the in-play dial: it rises when the world is in control, falls when the
  PC is, biasing how often scenes get interrupted/altered. (Honesty never relaxes; *consequence* scales.)

---

## 7 · Stage 6 — character creation
**Modes** (combinable): `--random` (all rolled, seed-reproducible) · `--interactive` (step-by-step, pauses
at every choice) · flag-driven partial lock (`--class --background --focus --set14 --skill-mode --level
--name --package/--roll-wealth --out`) · `--content-profile PATH` (applies the Stage-2 allow-list).

**Choices:** attributes (3d6-in-order +14, or the array) → background (d20/pick; Quick/pick-two/roll-three)
→ class (the profile-allowed roster) → tradition (all **15** offer real pickable arts/spells, each with its
own Effort skill; the Wise use no Effort) → foci → final touches (HP, AC, saves, Effort/spells, equipment,
languages, and a **goal + ties** — your own choice; Character Tags are an NPC tool, not a PC step).

---

## 8 · The handoff & the living world
Session Zero seeds the **Threads & Characters Lists** + **faction board**, refreshes the **seed deck**,
frames the **First Scene** (described, not tested), and stops on "What do you do?".

From then on, **every scene's end-of-scene bookkeeping** (`bookkeep.py`) fires the world-tick, including:
- a **Faction move every scene** *(new)* — `faction_turn.py <campaign>/factions.md --move auto` advances
  one faction's action + Major-Project clock (the world's powers act every beat; the full economic Faction
  Turn still batches at the ~weekly cadence);
- **new-faction generation** *(new)* — if the scene surfaced a power not on the board, `worldgen.py
  faction --campaign <dir>` adds it;
- the **Frontier** step — new regions/kingdoms generate and persist as play reaches or names them;
- Chaos judgment, Effort/Strain, supplies, and the List/seed refresh.

---

## 9 · Planned setup options (not yet built — see `REVISION-OPTIONS.md`)
- **Partial insertion** (`--given` / `--concept`) — supply some world/character facts in prose; lock them
  as `[authored]`, generate only the gaps.
- **`expand <node>` / `revise --step`** — elaborate one place or one character step on demand.
- A unified **`worldgen --interactive`** Session-Zero loop matching chargen's.

---

### Quick reference — start a default game
1. `python3 .claude/skills/mythic-gm/scripts/state.py init campaign` (scaffold)
2. Copy templates: `campaign-CLAUDE.md`, `wwn-campaign-state.md`, `content-profile.json`, `factions.md`
3. `python3 scripts/worldgen.py world --scope kingdom --campaign campaign` (world + factions; review/commit)
4. `python3 .claude/skills/mythic-gm/scripts/adventure_crafter.py themes --style wwn --campaign campaign`
5. `python3 scripts/chargen.py --interactive --content-profile campaign/content-profile.json --out campaign/character-sheet.md`
6. Seed the Lists, frame the First Scene, ask "What do you do?", stop.
