# Revision Options — Collaborative / Partial Generation (worldgen & chargen)

> Design discussion (not yet built). The user wants both generators to support **partial insertion**
> (the player supplies some facts; the generator fills the gaps and *brings up* the remaining details to
> decide), and **collaborative, step-by-step** generation. Both already have the bones for this — the
> worldgen DRAFT-CANON keep/reroll/adjust loop and `places.json` sketch→detailed promotion; chargen's
> `--interactive` and explicit `--class/--background/--focus` flags. Below are concrete options to extend
> them, with trade-offs and a recommendation. The unifying pattern is **mixed-initiative "seed → fill →
> zoom"**: lock what's given, generate the gaps, elaborate any node on demand.

---

## Part A · WORLDGEN

### A1. Partial insertion — "seed-and-fill" (recommended)
The player supplies any subset of facts; the generator treats them as **locked canon** and rolls only the
gaps. Two entry points:

- **Structured `--given`:** `worldgen.py geography --scale kingdom --given "coast=south; ruler=mad
  sorcerer-priest; terrain=drowned marsh; offshore=a sunken Deep"`. The composer skips rolling any slot
  that's supplied, tags it `[authored]` in the DRAFT CANON, and rolls the rest. `places.json` records
  per-field provenance (`authored` vs `rolled`) so a later reroll never overwrites an authored fact.
- **Free-text concept:** the GM parses a player's prose ("a poor coastal margravate that worships a
  drowned god") into the structured slots, locks them, generates the remainder. Works today as a GM
  procedure; the `--given` flag makes it honest and durable (the lock is recorded, not just remembered).

*Trade-off:* needs a slot vocabulary per scale (coast/terrain/ruler/tension/…). Modest; the slots already
exist implicitly in the composers.

### A2. Progressive disclosure — "zoom / bring up details" (recommended)
Generate a **headline** first, then elaborate any node on demand — the "have details brought up" ask. This
extends the existing frontier rule (sketch nodes, lazy detail) into an explicit verb:

- **`worldgen.py expand <node-id> --campaign DIR`** — reads a `sketch` node from `places.json` and
  generates the *next* level only: a kingdom → its cities + trade-mesh; a city → its court + 2 districts +
  a hook; a ruin → its first level + a guardian. Promotes `status: sketch → detailed`, appends the new
  child nodes (each itself a `sketch`), and surfaces the next decision ("expand which city?").
- This makes the world a **tree you walk**, never a wall of text: the player always sees a short summary
  and chooses where to drill. Pairs with A1 — you can `--given` facts at any expansion step.

*Trade-off:* requires the `places.json` graph (already specced in Plan #1 Part 3) to be live. Low risk.

### A3. Collaborative stepwise — `worldgen.py --interactive` (recommended)
Mirror chargen's `--interactive` for the world: a guided session that walks **world → region → kingdom →
cities → ruins**, pausing at each layer with **keep / reroll / adjust / hand-author**, and accepting
`--given` partial input at each pause. This unifies A1+A2 into one Session-Zero flow. The DRAFT-CANON
loop already does keep/reroll/adjust per block; `--interactive` just sequences it and stops for input.

### A4. Mixed-initiative "propose & re-derive" (optional / stretch)
When the player edits a generated line, re-derive downstream facts that depended on it (change a kingdom's
terrain to desert → re-roll its cities' water siting; change the ruler to a theocrat → re-bias its court
tags). Needs a light dependency map (which fields feed which). Highest power, highest complexity — defer
until A1–A3 are in play.

### Recommended worldgen path
**A1 `--given` + A2 `expand <node>` + A3 `--interactive`**, all writing provenance into `places.json`.
That delivers "partially insert + bring up details + collaborate in steps" with modest, additive code and
no change to the honest-dice / frontier contracts. A4 is a later luxury.

---

## Part B · CHARGEN

Same shape; chargen is further along (it has `--interactive` and explicit flags), so the work is smaller.

### B1. Partial insertion — concept-first / `--given` (recommended)
- **Already partial:** `--class`, `--background`, `--focus` (repeatable), `--name`, `--set14`,
  `--skill-mode` already let you lock pieces and auto-fill the rest.
- **Add `--concept "<prose>"`:** the GM maps a one-line concept ("a disgraced Sarulite blood-priest,
  frail but silver-tongued") to locked choices (class = partial-X/Sarulite Blood Priest, background =
  Priest or Noble, bias Con low / Cha high) and generates the remainder, showing what it inferred so the
  player can correct. A structured `--given "con<=8; cha>=14; tradition=Vowed"` is the explicit form.
- **Provenance:** the sheet marks each line `authored` vs `rolled`, so a reroll of "the rest" never
  disturbs a locked choice.

### B2. Progressive disclosure — explain / defer / zoom (recommended)
- **Explain at each step:** in `--interactive`, show the *consequence* of each option inline (pick Mage →
  "frail 1d6−1 HP, +0 attack, but Effort + arts"; pick Kistian Duelist → "Flaw of Fragility: 1d6 HD with
  Partial Warrior"). Turns the menu into a teaching tool.
- **Defer / "surprise me":** let the player postpone any choice ("decide later"); the generator rolls a
  placeholder and flags it for revisit, so momentum never stalls on an unfamiliar pick.
- **Zoom / re-open:** `chargen.py revise <sheet.md> --step foci` re-opens exactly one step on a finished
  sheet (re-pick foci, swap tradition, reroll HP) without rebuilding the character — the "bring up that
  detail again" ask.

### B3. Collaborative stepwise — already `--interactive` (enhance)
`--interactive` is this loop. Enhancements: a **back/undo** at each step, and a **running summary** of the
character so far (attributes → mods → skills → foci) shown above each prompt, so the player always sees
the whole build while deciding the next piece.

### B4. Concept → mechanics inversion (optional)
Invert the flow: start from a concept and have the generator *propose a complete legal build that fits*,
which the player then tweaks — instead of mechanics-first. This is B1's `--concept` taken to its end
(generate a full sheet, not just fill gaps). Good for new players; pairs with B2's explain so they learn
the system from a working example.

### Recommended chargen path
**B1 `--concept`/`--given` + B2 explain/defer/`revise` + B3 running-summary/undo.** Small additions atop
the existing `--interactive`; B4 is a nice on-ramp once B1 exists.

---

## Cross-cutting principles (apply to both)
1. **Lock-and-fill with provenance.** Every fact is `authored` or `rolled`; rerolls touch only `rolled`.
   This is the single mechanism behind "partially insert the world/character."
2. **Headline → drill.** Always present a short summary and let the player choose where to elaborate; never
   dump the full tree. (`expand <node>` / `revise --step`.)
3. **One guided loop.** A single `--interactive` per generator sequences the steps with
   keep/reroll/adjust/hand-author and accepts partial input at every pause.
4. **Honest dice + the frontier rule are untouched.** Authored facts replace a roll (shown as
   `[authored]`); generated facts still roll openly; the world still grows only as far as play (or the
   player's stated input) reaches.
5. **Provenance persists.** `places.json` nodes and the character sheet store authored-vs-rolled, so a
   campaign resumed later still knows what the player decided versus what the dice gave.

### Suggested build order (if pursued)
1. Provenance fields (`authored`/`rolled`) in `places.json` + the sheet — the foundation for everything.
2. chargen `--concept`/`--given` + `revise --step` (smallest, highest player value).
3. worldgen `--given` + `expand <node>`.
4. Unify each under `--interactive` (worldgen gains it; chargen enhances it with explain/undo/summary).
5. Optional: A4/B4 mixed-initiative re-derivation and concept-first full proposals.
