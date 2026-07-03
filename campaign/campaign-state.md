# Campaign State — WWN   (extends the engine's campaign-state.md)

> Use this when: this is the campaign's **source of truth** — overwrite it at each scene end (engine bookkeeping). It EXTENDS mythic-gm's `campaign-state.md` with WWN fields. The engine reads the Engine block; WWN reads the rest. See `bridge/world-model.md` for how the ledger feeds the engine's Lists.

## Engine block (mythic-gm)
*Lists are stored canonically as `threads.json` / `characters.json` (engine `state.py thread|char` / `lists.py`); the lines below mirror them for reading. `state.py init <campaign>` scaffolds the JSON; pass `--campaign <dir>` to the engine's List / Fate / Turning-Point scripts.*

- **Chaos Factor:** 5
- **Adventure mode:** Pure Mythic | Adventure Crafter | Prepared
- **Threads & Characters Lists:** canonical in `threads.json` / `characters.json` — view with `state.py thread show` / `char show`. **Do not copy them here.**
- **Adventure Features:** …  *(if a prepared/ingested adventure)*
- **Last scene recap (2–3 sentences):** …
- **Open canon answers (Fate Questions made true):** …

## Party & PCs
- **<PC name>** — class/level · HP cur/max · AC · System Strain cur/max · Effort cur/max · key foci · condition (Frail? Mortally Wounded?). *Full sheet: a `character-sheet.md` per PC.*
- **Shared:** light & supplies · mounts/vehicles · wealth · marching order · current party goal.

## Effort & Strain  (per caster / PC)
- **<PC>:** Effort committed — scene: … · day: … · indefinite: … ; **System Strain** …/Con.

## Faction board  (summary; full board: `faction-sheet.md`)
- **<Faction>** — C/F/W · HP cur/max · Major-Project clock n/N · attitude to PC. *Run `faction_turn.py` at the world-tick cadence.*

## World ledger — clocks & threats  (see `world-model.md`)
- **<Clock / threat name>** n/N — advances by … — touches (where/whom) …

## Domains / holdings
- **<Holding>** — income vs upkeep net per interval; unrest …

## World-tick clocks
- **Supplies:** days remaining … · **Wandering-encounter:** per watch/turn while exploring · **Days at sea:** …

## Committed-canon frontier  (worldgen)
- **Detailed now:** <starting region / nations>.
- **Generate on demand:** everything else — call `scripts/worldgen.py` when play reaches it, then fold the result here and into the Lists.

*Overwrite each scene end. Run the engine SELF-AUDIT before sending a scene: did dice decide every uncertain outcome, were stakes pre-committed, did the world act to win, did a clock/List/Chaos move?*
