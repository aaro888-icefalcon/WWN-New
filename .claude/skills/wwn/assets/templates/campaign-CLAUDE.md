# Campaign GM directives — Worlds Without Number   (ALWAYS-ON)

> Session Zero copies this file to `<campaign>/CLAUDE.md` so it loads every turn. It carries the
> operative rules that must be present **at the moment of action** — not pointed to, present.
> Engine: mythic-gm · Companion: wwn (paths below = the installed skill).

## RESOLVE — rung 1 is the WWN check, NOT a Fate Question
When a PC **attempts to do something**, resolve it with the WWN system via `scripts/check.py` (honest dice), never the oracle:

| The PC… | Run |
|---|---|
| attacks / strikes / shoots | `check.py attack <hitBonus> --ac <AC>`  (Shock applies on a miss vs low AC) |
| uses a skill (climb, sneak, persuade, lockpick, recall, heal…) | `check.py skill <skill+attr> --vs <6\|8\|10\|12\|14>` |
| resists poison / spell / blast / fall / fear | `check.py save <target>`  (target = 16−level−attr; Luck 16−level) |
| contests another (sneak vs notice, arm-wrestle, duel of wits) | `check.py opposed <pcMod> <foeMod>`  (ties → PC) |
| deals damage / Shock / hits 0 HP | resolve per `references/rules/combat.md` + `healing-and-strain.md` |
| casts / commits Effort | `references/rules/magic-and-effort.md` |

**`dice.py fate` (Fate Question) is ONLY for world facts the rules don't cover** — is the gate guarded? is the lord amenable? does it rain? **Never for anything a PC *does*.** Before any Fate Question, ask: *"is this a PC task / attack / save / contest?"* → if yes, stop and use `check.py`.

## BOOKKEEP — every scene end, run the tool
`python3 <skill>/scripts/bookkeep.py <campaign> <scene#>` and do what it prints: Chaos ±1 · world-tick (`tick.py` → faction turn if due, clocks, supplies) · Effort refresh · System Strain · update the Lists (JSON) · self-audit. **A scene sent without bookkeeping is incomplete.**

## STATE — one source of truth (JSON)
The Threads & Characters Lists live in `threads.json` / `characters.json` (engine `state.py`). They are the **source of truth**. **Never hand-maintain a Markdown copy of the Lists.** Read them with `state.py thread show` / `char show`; edit with `state.py thread|char add|weight|remove`. `campaign-state.md` holds only WWN fields (party, Effort, Strain, faction board, world ledger, frontier) — it does not re-list the Threads/Characters.

## SELF-AUDIT — gate before sending a scene
- A PC task resolved by a **Fate Question instead of a WWN check** = FAIL → redo it with `check.py`.
- A scene with **no honest roll, no stake moved, no clock/List/Chaos change** = soft → add an edge.
- **NPCs and factions act to win.** Roll before you narrate; show the dice. Death and ruin are real.
