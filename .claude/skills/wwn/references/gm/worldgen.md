# Worldgen — build the world at Session Zero, grow it on demand

> Use this when: you need to **build the campaign world** (the Session-Zero scope dialog) or **expand it at the frontier** — the PC travels somewhere new, or play *names* a place (a Fate Question / Random Event). Never pre-build the map; detail only the starting region and grow the rest as play reaches it.

All randomness routes through **`scripts/worldgen.py`** (honest, shown dice; reuses `gen.py`'s tags/recipes). Dice print to STDERR; the committable **DRAFT CANON** markdown prints to STDOUT.

## 1 · The Session-Zero scope dialog
Before drafting, ask the player four things and record the answers:

| Ask | Options |
|---|---|
| **Scope** | single **region** ▸ a **few nations** ▸ a whole **continent** |
| **Tone** | how grim / weird / heroic; any content lines |
| **Magic level** | rare-and-feared (default Latter Earth) ▸ common ▸ other |
| **World** | **default Latter Earth** (the Gyre / `setting-canon.md`) ▸ a **fresh** world (`--fresh`, names & history rolled from scratch) |

Scope sets the command (below). **Default = Latter Earth**: leave generated hooks to attach to existing canon NPCs/factions. **Fresh** replaces `bridge/setting-canon.md` wholesale.

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
| **Scaffold the world** at Session Zero | `python3 scripts/worldgen.py world --scope <region\|few-nations\|continent> [--fresh] [--seed N]` |

Scopes: `region` = 1 detailed region · `few-nations` = 2–4 nation briefs + a shared tension + a start region · `continent` = a sketch (4–6 one-line nations + a relations map; then detail one region before play). `--fresh` rolls names/origins from scratch; omit it to seed from Latter-Earth canon. Capture just the canon text with `… > draft.md` (dice go to STDERR).

Each generated place is deliberately **short** — a frontier sketch, not a novel. For a single sub-table or tag in isolation, prefer `gen.py` / `lookup.py`; `worldgen.py` is for composed, committable world-pieces.

Source: `book/Worlds-Without-Number-Deluxe/07-Creating-Your-Campaign/` — Building Your Backdrop (pp. 121–123), Geography Construction (pp. 124–127), Nation Construction (pp. 128–131), Society Construction (pp. 132–135), Government Construction (pp. 136–139), History Construction (pp. 140–143), Religion Construction (pp. 144–149), Placing Ruins & Points of Interest (p. 150). Tag tables: `…/11–15 (Location/Community/Court/Ruin/Wilderness Tags)`.
