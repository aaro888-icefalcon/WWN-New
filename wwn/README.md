# wwn

A **companion skill for the `mythic-gm` engine** that runs a challenging, tactical solo / GM-less campaign in **Worlds Without Number** (Kevin Crawford / Sine Nomine) and the **Latter Earth** setting.

mythic-gm owns the scene loop, the Mythic oracle, honest scripted dice, and the no-softening discipline. This pack supplies the **world**: WWN's rules, tactical combat, magic, the native Faction Turn and domain subsystems, a full generator suite, an on-demand **worldgen** subroutine, and the Latter Earth gazetteer.

## Requirements
- The **mythic-gm** skill must be enabled alongside this one.

## Layout
- `SKILL.md` — entry point: first actions, the oracle ladder, WWN Session Zero, the reference-loading guide.
- `bridge/` — the engine hooks: `system-profile` (resolution), `interpretation`, `chaos-tendency`, `theme-weights`, `subsystems` (world-tick), `seeds`, `setting-canon`, `generators/*.json` + `registry.md`, `adventures/`.
- `references/rules/` & `references/gm/` — lean, page-cited play-cards (read on demand).
- `book/` — the complete WWN rulebook + Atlas of the Latter Earth, verbatim (preservation + deep lookup).
- `scripts/` — thin honest helpers (chargen, worldgen, faction turn, monster, lookup, gen); every die wraps `mythic-gm/scripts/dice.py`.
- `assets/templates/` — live-state files that extend the engine's `campaign-state.md`.

## Quick start
1. Enable `mythic-gm` and `wwn`.
2. Say "run a Worlds Without Number game." Session Zero will define the world (default: Latter Earth), roll up a character, and open the first scene.

*Content is reproduced from Worlds Without Number and The Atlas of the Latter Earth for personal play; not for redistribution.*
