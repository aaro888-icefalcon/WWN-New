# Worldgen — build the world at Session Zero, grow it on demand

> Use this when: you need to **build the campaign world** (the Session-Zero scope dialog) or **expand it at the frontier** — the PC travels somewhere new, or play *names* a place (a Fate Question / Random Event). Never pre-build the map; detail only the starting region and grow the rest as play reaches it.

All randomness routes through **`scripts/worldgen.py`** (honest, shown dice; reuses `gen.py`'s tags/recipes). Dice print to STDERR; the committable **DRAFT CANON** markdown prints to STDOUT.

## 1 · The Session-Zero scope dialog
Before drafting, ask the player four things and record the answers:

| Ask | Options |
|---|---|
| **Scope** | single **region** ▸ a **few nations** ▸ a **kingdom** ▸ a whole **continent** |
| **Tone** | how grim / weird / heroic; any content lines |
| **Magic level** | rare-and-feared (default Latter Earth) ▸ common ▸ other (also set by the content profile) |
| **World source** | one of the **four** below |

**The four world sources:**
1. **Default Latter Earth** (the Gyre / `setting-canon.md`) — generate seeded from existing canon; hooks attach to canon NPCs/factions. The out-of-the-box start.
2. **Fresh world** (`--fresh`) — names & history rolled from scratch; **replaces `setting-canon.md` wholesale**.
3. **Provided setting** — the player supplies their own setting (their homebrew, another book, a pitch). The GM **ingests the provided text into `setting-canon.md`** (premise, powers, named NPCs, content lines, a name/place seed-pool), then generates places/factions seeded from *that* canon (not Latter Earth, not random) — hooks attach to the provided world. Use the provided proper nouns as the name pool instead of the Latter-Earth list.
4. **Guided / Modified Latter Earth** — start from Latter Earth canon, but the player **specifies the themes or gameplay for one (or more) region(s)** (e.g. "make the starting march a plague-haunted naval frontier; lean Mystery+Tension"). The GM keeps the Latter-Earth backdrop but **biases that region's generation** — its terrain/community/ruin tag picks, its faction goals/projects, and its scene themes — toward the stated direction, recording the guidance in `setting-canon.md`. The rest of the world stays default Latter Earth.

Scope sets the command (below). Sources 1 & 4 seed from Latter-Earth canon; 2 rolls fresh; 3 seeds from the player's provided canon. In every case the **frontier rule** still holds — detail only the starting region/kingdom and grow the rest on demand.

**Factions are generated as part of world building** (every nation becomes a faction on `campaign/factions.md` via the `--campaign DIR` option), and **faction moves fire every scene** at bookkeeping (`faction_turn.py --move auto`), with new factions generated whenever play surfaces an untracked power. See `SETUP-GUIDE.md`.

## 2 · The draft → feedback → commit loop
1. **Generate at scope** — run the matching command; show the player the DRAFT CANON block (it is a *proposal*, clearly labeled, never yet canon).
2. **Player feedback** — keep / **reroll** (`--seed N`) / **adjust** (edit a line) / **hand-author** (write their own). Iterate cheaply; the dice are reproducible per seed.
3. **Commit** the approved, edited version:
   - paste it into **`bridge/setting-canon.md`** (the live source of truth);
   - seed the engine's **Threads List** with one thread per hook, and the **Characters List** with each named figure;
   - put each nation on the **faction board** (`bridge/seeds.md` sources / the Faction Turn sheet).
   **Only the starting region is built in detail.** Everything else stays a sketch (or unwritten) until play arrives.

## 3 · Lazy expansion (the frontier rule)
Do **not** over-build ahead of play. When the PC enters somewhere new, or an oracle/Fate Question establishes a place that doesn't exist yet:
- call `worldgen.py` for **just that place** (a `settlement` / `court` / `ruin` / `wilderness`, or a fresh `region` / `nation` if they cross a border);
- fold the approved result back into **`setting-canon.md`** under the matching section (it is now ground truth, overriding recollection), and add its hooks/figures to the Lists.
This is the same generate-on-demand frontier `setting-canon.md` describes — keep that file the single live canon.

## 4 · Which command for which need

| Need | Command |
|---|---|
| A town/village just got named or entered | `python3 scripts/worldgen.py settlement [--seed N]` |
| A ruling court / noble house appears | `python3 scripts/worldgen.py court [--seed N]` |
| A ruin / Deep / site is entered | `python3 scripts/worldgen.py ruin [--seed N]` |
| A wild region / terrain is generated | `python3 scripts/worldgen.py wilderness [--seed N]` |
| A faction-ready **nation** brief (problems = hooks, court, figure, tension) | `python3 scripts/worldgen.py nation [--fresh] [--seed N]` |
| A detailed **starting region** (terrain + 1–2 settlements + a ruin + 2–3 hooks) | `python3 scripts/worldgen.py region [--fresh] [--seed N]` |
| The book's **region SKELETON** (oceanic frame · ~6 features · 1d4+2 rivers · 1–3 lakes · 6 nations on natural borders) | `python3 scripts/worldgen.py geography --scale region [--fresh] [--seed N] [--campaign DIR]` |
| The book's **detailed kingdom** (demographics · capital-on-water then cities clockwise · 2 Community + 2 Court tags per city) | `python3 scripts/worldgen.py geography --scale kingdom [--fresh] [--seed N] [--campaign DIR]` |
| **~6 famous ruins** in a kingdom's wilderness gaps (type + 2 Ruin Tags + a line each) | `python3 scripts/worldgen.py ruins --kingdom <name> [--fresh] [--seed N] [--campaign DIR]` |
| **Scaffold the world** at Session Zero | `python3 scripts/worldgen.py world --scope <region\|few-nations\|continent\|kingdom> [--fresh] [--seed N] [--campaign DIR]` |

Scopes: `region` = 1 detailed region · `few-nations` = 2–4 nation briefs + a shared tension + a start region · `continent` = a sketch (4–6 one-line nations + a relations map; then detail one region before play) · `kingdom` = a region **skeleton** + the one **detailed** kingdom inside it (+ its ~6 ruins) — the book's two-map start. `--fresh` rolls names/origins from scratch; omit it to seed from Latter-Earth canon. Capture just the canon text with `… > draft.md` (dice go to STDERR).

Each generated place is deliberately **short** — a frontier sketch, not a novel. For a single sub-table or tag in isolation, prefer `gen.py` / `lookup.py`; `worldgen.py` is for composed, committable world-pieces.

## 5 · The two-map hierarchy (skeleton vs. fill)

The `geography` commands implement the book's **two maps** (Geography Construction pp.124–127): a **regional** map of the campaign backdrop and a **kingdom** map of where the first sessions happen. They own **geometry & adjacency only** — every node's *content* defers to the existing tag recipes (`community`/`court`/`ruin`/`wilderness` tags), so there is no duplicated place flavor. Region scope fires **rarely** (only when the PC leaves the detailed region); kingdom/site scope is the common border/new-town case.

**Key book numbers encoded** (`bridge/generators/geography_construction.json`):
- **Region:** decide oceanic sides (1–2 coastline / 3 peninsula / 4 island); ~6 significant terrain features (d20); **1d4+2** major rivers (each ≤¼ the max map dimension; split *downstream only* — once a river splits it never rejoins); 1–3 lakes (≥1 river in, ≤1 out); **6 nations** coterminous with natural barriers. **No cities or ruins at region scale.**
- **Kingdom:** 60 people/sq mi (2,000 per 6-mile hex); ~10% urban → ⅓ in the capital, ¼ of the remainder in the 2nd city; **capital on water**, then place cities **clockwise from a random cardinal**; tag each city with **2 Community + 2 Court** tags.
- **Ruins:** ~6 famous ruins per kingdom, placed in the **wilderness gaps between trade routes**; each = a type roll (Latter-Earth d12 / General d20) + **2 Ruin Tags** + 1–2 sentences. Sketch nodes — flesh one out only on PC commitment.
- **One-roll terrain detail dice** (used on the kingdom's dominant feature): d4 populated · d6 dangerous · d8 use · d10 last event · d12 antagonists · d20 quirk.

**Three synchronized artifacts per run** (the scene system reads canon + Lists + the graph, never a raw map):
1. **Canon block** → DRAFT CANON markdown on STDOUT; on approval append to `setting-canon.md`.
2. **`places.json` graph** → with `--campaign DIR`, each place is appended as a node carrying its **FULL** tag (summary + all five sub-tables), `adjacency`, `travel_days`, `status` (`sketch`/`detailed`), shared Thread/Character `id`s, and a `canon_anchor`. Without `--campaign`, the nodes print as a fenced JSON block to save by hand. This graph is the **machine** output — its job is **proximity**, which powers the scene-weighting (PC's region > adjacent > distant). **Re-entry is a lookup of this file, not a reroll.**
3. **List + seed cards** → each place also emits a machine-readable **place card** header — `- [PLACE site:<kind> id=<id> region=… kingdom=… near=… w=N]` — that the scene framer parses for proximity/weight; the prose under it is narrated. Hooks → Threads, figures → Characters, nations → the faction board.

## 6 · Frontier wiring — generate as play explores

A new region/kingdom is generated **the moment play reaches or names it**, then folded into canon so it persists. Two integration points keep this symmetric:

- **Front of the Turn (scene-framing).** When the GM frames a scene and the PC is entering somewhere **not yet in `setting-canon.md`** (or an oracle/Fate Question *names* a place that doesn't exist): classify the destination (new **site** → `settlement`/`court`/`ruin`/`wilderness`; new **kingdom** → `geography --scale kingdom` + `ruins`; new **region** → `geography --scale region`, then detail the entered kingdom), **generate just-in-time** at the smallest scope the PC can perceive this scene, show the DRAFT CANON, let the player keep/reroll/adjust, **then** describe the scene and ask "What do you do?".
- **Back of the Turn (bookkeeping).** `bridge/subsystems.md` carries a **Frontier expansion** row (surfaced by `tick.py`), and `bookkeep.py` prints a **FRONTIER step** (between LISTS and SELF-AUDIT): if the scene reached the edge of charted canon or named a new region/kingdom, **queue** the right-scope `worldgen.py` call for next framing and, on approval, fold the result into `setting-canon.md`, seed its hooks as Threads and figures as Characters, put any new nation on the faction board, and write its nodes to `places.json --campaign <dir>`.

**Anti-flood.** Region scope is a rare, once-per-arc event; distant new content enters the Lists/seeds at **low weight (≤1)** so it never crowds the scene in front of the PC, and the `places.json` adjacency lets near content always outweigh it. Un-recorded new places are a soft scene — the world must persist what play discovered.

Source: `book/Worlds-Without-Number-Deluxe/07-Creating-Your-Campaign/` — Building Your Backdrop (pp. 121–123), Geography Construction (pp. 124–127), Nation Construction (pp. 128–131), Society Construction (pp. 132–135), Government Construction (pp. 136–139), History Construction (pp. 140–143), Religion Construction (pp. 144–149), Placing Ruins & Points of Interest (p. 150). Tag tables: `…/11–15 (Location/Community/Court/Ruin/Wilderness Tags)`.
