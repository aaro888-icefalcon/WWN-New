# Seed Sources — Worlds Without Number   (hook: seeds)

## Operative
Refresh the seed deck (30–40 cards) EVERY bookkeeping, after `tick.py`, from the sources below; consume
a seed when a scene framing, Turning Point, or Random Event uses it. Weight by proximity · urgency ·
visibility, but let honest dice choose *within* the weighted set — never hand-pick the convenient seed.
An un-earned secret seeds a *sign*, never the reveal (Player ≠ PC knowledge). A stale deck = the world
stops offering hooks.

# Sources & mechanics (deck size 30–40; refresh each bookkeeping):
- deck size: 35            # 30–40
- refresh: each bookkeeping (after `tick.py`; see `world-model.md` §4)
- weighting: proximity · urgency · visibility (`world-model.md` §5) — let the dice choose *within* the weighted set
- sources (priority order):
  - **setting-canon near the PC** — `bridge/setting-canon.md` + the committed-canon frontier
  - **the live world ledger** — active clocks, faction Major-Projects, revealed regions, faction standings (`campaign-state.md`)
  - **the engine's Threads & Characters Lists** — the ledger *is* the Lists (`world-model.md` §2)
  - **random novelty rolls** on WWN generators, for fresh texture:
    - `python3 scripts/gen.py hook`          # a fractal adventure seed (Enemy/Friend/Complication/Thing/Place)
    - `python3 scripts/gen.py npc`           # a quick NPC (role + twist + ambition)
    - `python3 scripts/dice.py table bridge/generators/fractal_seeds.json`
    - `python3 scripts/worldgen.py region|nation`   # only when the frontier is actually reached
- consumed when a seed is invoked by a scene framing, a Turning Point, or a Random Event; refill to size each bookkeeping.
- commit: when a seed becomes a beat, add it to the Lists as **JSON** — `state.py thread|char add <campaign> …` (never a Markdown list).
- discipline: a seed is a **candidate**, surfaced only by contextual relevance and honest dice — never hand-pick the convenient one. An un-earned secret seeds a *sign*, never the reveal (Player ≠ PC knowledge).
