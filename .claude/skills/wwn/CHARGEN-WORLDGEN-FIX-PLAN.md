# Fix Plan — Character Creation & Worldgen (WWN skill)

> Review of `scripts/chargen.py` and `scripts/worldgen.py` against the book, plus a plan to make both
> support **step-by-step, player-in-the-loop generation in play** and to incorporate the book's
> **map-creation / country→region→location** guidance. Companion to
> `references/rules/character-creation-compendium.md` (the compiled rules digest).

---

## A · Character creation — review findings

### A1. Issues to fix (chargen.py)

| # | Severity | Issue | Detail |
|---|---|---|---|
| 1 | **High** | **No interactive / step-by-step mode** | `chargen.py` resolves *every* choice itself (random or class-biased heuristics). For in-play creation the player must choose attribute→14, background, skill mode, class, each focus, tradition, spells, package, goal. Today there's no "roll this step, stop, ask, continue" flow. |
| 2 | **High** | **Magic traditions incomplete** | `_setup_tradition` only offers High Mage / Necromancer / Elementalist, chosen at random, with `# TODO verify spell lists`. **Missing:** Healer, Vowed, Adunic Invoker, Darian Skinshifter, Kistian Duelist, Llaigisan Beastmaster, Sarulite Blood Priest, Vothite Thought Noble. |
| 3 | **High** | **Effort formula wrong for special traditions** | Code always uses `1 + Magic + better Int/Cha`. But Healer uses **Heal**, Vowed uses the **order skill + best mod**, Skinshifter/Beastmaster **Survive**, Duelist **Stab**, Blood Priest **Pray**, Thought Noble **Notice**, each with its own attribute pair. |
| 4 | **Med** | **Spells/arts are placeholders** | `step_final` emits `<1st-level spell N>` strings even though `spells.json` holds real High Magic / Elementalist / Necromancer / Healer / Vowed lists. Starting spells/arts should be pulled (and let the player pick). |
| 5 | **Med** | **`--roll-wealth` print bug** | Line 791: `print("  Starting wealth: %d sp (rolled; buy gear individually).")` has **no `% sp`** — prints the literal `%d`. |
| 6 | **Low** | **Focus page numbers wrong** | Many foci hard-coded to `p.28` (Specialist, Spirit Familiar, Trapmaster, Unarmed Combatant, Valiant Defender, Well Met, Whirlwind Assault, Xenoblooded…) regardless of real page. Cosmetic but misleading for `lookup`. |
| 7 | **Low** | **HP folding logic is fragile** | `ch.hp_max = ch.hp_max - 1 + hp if ch.hp_max != 1 else hp` — works for Die Hard today but is brittle; should track `focus_hp_bonus` explicitly and add it to the rolled HP. |
| 8 | **Low** | **"Roll three" randomizes the split** | Book lets the player choose how to split 3 rolls across Growth/Learning; code rolls `1d2` per roll. Fine for full-random, wrong for interactive (player should choose the split). |
| 9 | **Low** | **Non-human origins not enumerated** | `Special Origin` / `Xenoblooded` are notes only; no list of origin foci from the bestiary (p.280). Acceptable to leave manual, but flag it. |
| 10 | **Verify** | **Saves formula** | Code & references both use `16 − level − mod` (= `15 − mod` at L1, improving 1/level). Matches the book's L1 value; the per-level slope should be spot-checked against `04-The-Rules-of-the-Game.md` advancement, but is internally consistent. |

### A2. What is already correct (keep)
- Attribute mods, 3d6-in-order + free-14 rule, the array option.
- All 20 backgrounds with faithful Growth/Learning tables.
- Skill stacking (0 → 1 → swap), the no-novice-above-1 cap.
- Class HD/attack-bonus tables incl. the 4 Adventurer combos.
- All 33 foci present with correct bonus skills and the combat/non-combat eligibility gate.
- Equipment packages verbatim; AC/shield/saves/initiative math.
- Honest, shown, seedable dice via `roll()`.

---

## B · The in-play step-by-step creation flow (how the GM runs it)

Goal: the player **generates scores and makes every choice live**, with honest dice shown. Two ways to
deliver this — recommend doing **both** (script support + a GM script-of-play):

### B1. Add an interactive mode to `chargen.py` (`--interactive`)
Drive the existing step functions but **pause at each decision**, printing the rolled dice and the menu,
reading the player's choice, then proceeding. Concretely:

1. **Attributes** — roll 3d6 ×6 in order (shown). Present the six scores; ask **which one to set to 14**
   (or decline / use the array). Show final mods.
2. **Background** — offer "roll d20 or pick"; on roll, show it. Then ask **skill mode** (Quick / pick-two
   / roll-three). For *roll-three*, ask the player the **split** before each roll; show each die.
3. **Class** — menu of Warrior / Expert / Mage / the 4 Adventurer combos. Show what it grants.
4. **Foci** — for each granted slot (combat / non-combat / any), present the **eligible** focus list
   (filtered by class/attr rules), let the player pick; apply bonus skill / HP / AC / mod.
5. **Tradition & spells** (if caster) — menu of the **full set** of traditions (see B2); set the correct
   **Effort formula** for that tradition; then present the tradition's **starting spell/art list** from
   `spells.json` and let the player pick the right number (4 full / 2 partial / 2 miracles for Blood Priest, etc.).
6. **Final touches** — free skill pick (menu); roll HP (shown); choose package or roll wealth; compute
   AC/saves/attack lines; prompt **name, goal, ties**; write the sheet.

Keep `--random` and the current flags working unchanged; `--interactive` is additive.

### B2. Make the tradition layer complete & data-driven
- Add a `TRADITIONS` table keyed by name with: `caster` (spells / spell-points / arts-only),
  `effort_skill` (Magic / Heal / Pray / Survive / Stab / Notice / order-choice),
  `effort_attrs` (the pair), `spell_lists` (which `spells.json` lists), `free_arts`, `starting_known`.
- Replace `_setup_tradition` / the Effort block in `step_final` to read from this table.
- Wire **starting spells/arts** to `lookup.py` / `spells.json` so the player picks real options; for the
  six Gyre arts-classes without encoded data, fall back to a pointer (cite `11-Arts-of-the-Gyre.md`)
  until those arts are added to `spells.json` (see A2 of the worldgen plan's "data" note).

### B3. GM procedure (works even without code changes)
When running creation in chat, the GM walks §0 of the compendium, calling the scripts for **every die**:
`chargen.py` for the batch, or `dice.py roll 3d6` per attribute + manual choices, and
`lookup.py focus|spell <name>` to show exact text before the player commits. Stop at each choice; never
auto-pick. This is the fallback until `--interactive` lands.

---

## C · Worldgen — review & the map / country→region→location plan

### C1. Findings (worldgen.py)
- **Implements:** `settlement | court | ruin | wilderness` stubs (via gen.py tags), `nation` brief,
  `region` (terrain tag + 1–2 settlements + ruin + hooks), and `world --scope region|few-nations|continent`.
- **Missing the book's actual map pipeline.** None of the *Geography Construction / Building Your Backdrop*
  machinery exists:
  - No **kingdom scope** (the book wants **two maps**: a ~200-mi **region** and a ~60-mi **kingdom**).
  - No **Significant Terrain Features** table (d20), no **rivers** (`1d4+2`, ≤¼ map dimension), no
    **lakes** (1–3, ≥1 river in / ≤1 out), no **oceanic-sides** step, no **climate** check.
  - No **city placement** procedure (capital on water → clockwise from a random cardinal; 10% urban,
    ⅓ capital / ¼ second city; 60 people/sq mi, 2,000/6-mi-hex).
  - No **trade-route mesh → wilderness gaps → ruin placement** (the book's method for *where* ruins go).
  - No data file: there is **no `geography_construction.json`** (only `nation_construction`, `history_construction`,
    `religion_construction`). The terrain/river/feature-detail tables are unencoded.

### C2. Plan — add the country→region→location map process

**1. New generator data: `bridge/generators/geography_construction.json`** with the book's tables:
- `Significant Terrain Features` (d20) + the one-roll detail dice (d4 populated / d6 dangerous / d8 use /
  d10 last event / d12 antagonists / d20 quirk).
- `General Places of Adventure` (d20) and `Latter-Earth Places` (d12) for ruins (may live here or in a
  `ruin_placement` block).
- Register in `registry.md` and `manifest.json`.

**2. New worldgen commands / scopes** (compose with honest dice, emit DRAFT CANON):

| Command | Produces (book procedure) |
|---|---|
| `worldgen.py geography --scale region` | oceanic sides → ~6 terrain features (each detailed) → `1d4+2` rivers (split-downstream-only, ≤¼ map) → 1–3 lakes → place 6 nations on natural borders. **No cities/ruins yet.** A text "map sketch" (relational, ASCII/coordinate hints). |
| `worldgen.py geography --scale kingdom` | repeat at ~60-mi scale: 1 main terrain + spice → rivers → demographics (60/sq mi; 10% urban, ⅓ capital, ¼ second city) → place capital then cities **clockwise from a random cardinal** → tag each city (2 Community + 2 Court tags). |
| `worldgen.py ruins --kingdom <name>` | identify trade-route gaps → place **6 famous ruins** in the gaps → each = type roll (d20/d12) + **2 Ruin Tags** + a one-line description. |
| extend `world --scope` | add a **`kingdom`** scope between region and continent; have `continent`/`few-nations` defer to `geography` for the *one* detailed region+kingdom. |

**3. Map representation.** The book is explicit that **no artistic/global map is needed** — "loose
scrawls and crude symbols" suffice, two maps total (region + kingdom), optional 6-mile hexes
(Hexographer) only for a hexcrawl. So the script should emit a **relational sketch**, not pixel art:
- a compact list of features with rough relative positions (cardinal/edge hints from the oceanic-sides
  + clockwise-placement rolls),
- rivers as "from <highland feature> → <sea/lake>",
- nations bounded by named natural barriers,
- optionally a simple ASCII grid or a coordinate table the player can hand-draw from.

**4. Keep the frontier rule.** Detail **one** starting kingdom/region in full; everything else stays a
one-line sketch and is grown on demand with the existing `settlement|court|ruin|wilderness` commands —
exactly as the book and `setting-canon.md` prescribe. The new geography commands are for **Session Zero**
and for crossing into a genuinely new kingdom, not for pre-building the world.

**5. Update docs.** Extend `references/gm/worldgen.md` (and the SKILL.md worldgen step) to add the
two-map hierarchy, the load-bearing numbers (6-mile hex / 2,000 per hex / 60 per sq mi; `1d4+2` rivers
≤¼ map; 1–3 lakes; 6 nations / 6 features / 6 ruins; 10% urban → ⅓ capital, ¼ second city; 2 history
events/group + 3–4 at kingdom; 1d10 vs 1d10+10 negative/positive themes), and the new commands.

### C3. The country→region→location hierarchy (what each level holds)
- **World (minimal):** name + physics + 1–2 distant empires (two sentences each). Defer gods.
- **Region (~200-mi square, one only):** 6 features, `1d4+2` rivers, 6 nations on natural borders,
  regional gods, 2 history events/nation, relationships, 3–4 active factions. **No cities/ruins yet.**
- **Kingdom (~60-mi, equal effort to a whole region):** small-scale geography, rulers + enemies +
  problems, ethnic/demihuman placement, society, local gods, demographics, capital-then-clockwise cities.
- **Locations / POIs:** ~6 famous ruins in the wilderness gaps, each = type roll + 2 Ruin Tags + 1–2
  sentences; flesh out fully only when the PCs commit to going.

---

## D · Suggested implementation order

1. **Quick wins (low risk):** fix the `--roll-wealth` print bug (#5); correct focus page numbers (#6);
   make HP folding explicit (#7).
2. **Tradition layer (high value):** data-driven `TRADITIONS` table + correct Effort formulas (#2, #3);
   wire starting spells/arts from `spells.json` (#4).
3. **Interactive mode:** `chargen.py --interactive` step-by-step flow (#1, #8) — the headline feature for
   in-play creation.
4. **Worldgen geography:** `geography_construction.json` + `geography`/`ruins` commands + `kingdom` scope
   + doc updates (Section C).
5. **Stretch:** encode the six Gyre arts-classes' arts into `spells.json` so the tradition picker can
   show real options for all 11 traditions (#9 + Gyre data gap).

Each change keeps the **honest-dice, shown-rolls, player-in-the-loop** contract and the **frontier rule**
(detail only the starting region/kingdom; grow the rest on demand).
