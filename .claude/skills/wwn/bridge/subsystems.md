# World Subsystems — Worlds Without Number   (hook: world-tick; fired by tick.py at bookkeeping)

## Operative
FIRE `python3 scripts/bookkeep.py <campaign> <scene#>` (which runs the engine's `tick.py`) AT EVERY
scene end — not "when relevant." The Latter Earth moves whether or not the PC looks: advance the clocks
below, fire a **Faction move EVERY scene** (`faction_turn.py --move auto`) and the full Faction Turn at
the weekly cadence, generating a **new faction** for any power play surfaces, tick Major-Project clocks,
refresh Effort, recover or charge System Strain, spend supplies, and roll wandering/naval checks
honestly. A filled clock is never
silent — telegraph it now and fire it next beat as a Random Event (Close a Thread) or a Turning Point
(Conclusion). If a subsystem stalls for several scenes, the world has drifted; tick is mandatory.

# tick.py reads the cadence column: 'every scene' | 'every N scenes' | 'on trigger: …'
| subsystem | cadence | advance by |
|---|---|---|
| Faction move | every scene | run `scripts/faction_turn.py <faction-sheet> --move auto`: ONE faction takes ONE action (opposed 1d10+attr) and advances its Major-Project clock — no economy. The world's powers act EVERY beat. Surface the move as a sign/seed next scene; a FILLED clock fires as a Random Event/Turning Point. If this scene revealed a power not on the board, **generate a new faction** (`scripts/worldgen.py faction --name <X> --campaign <dir>`) and add it. |
| Faction Turn (full economy) | every ~week of in-world time (≈ every 4–6 scenes) | run `scripts/faction_turn.py <faction-sheet>`: every faction earns Treasure, pays upkeep, takes an action, advances its goal/clock. Apply results to the Threads/Characters Lists (`world-model.md`). |
| Major-Project clocks | per faction turn | +1 (or +2 if the faction/party worked it this turn); a filled clock concludes its project → Renown / a world-change. |
| Effort refresh | scene / day | for-the-scene Effort returns at scene end; for-the-day at a night's rest; indefinite stays committed. |
| System Strain recovery | per night's rest | −1 Strain and recover level/HD HP if fed and rested; Frail recover neither. |
| Wealth / upkeep & taxes | per in-world interval | net holding income vs hireling/soldier/upkeep costs; unrest or lost assets if unpaid. |
| Wandering encounters | per watch/turn while exploring | roll the region's encounter check; on a hit, draw `wilderness_tags`/`monster_gen` + a Reaction (2d6). |
| Supplies & privation | per day in the field | spend food/water/light; on a shortfall, Physical saves + System Strain (`references/rules/saves.md`). |
| Naval ship-crisis | per day at sea | roll `naval` (Seafaring Event / Ship Crisis) honestly. |
| Frontier expansion | on trigger: PC approaches/names an uncharted region or kingdom | generate it with `scripts/worldgen.py` at the smallest covering scope (`settlement\|court\|ruin\|wilderness` for a new site, `geography --scale kingdom` (+ `ruins --kingdom <name>`) for a new kingdom, `geography --scale region` for a new region) BEFORE the next scene; show the DRAFT CANON, then on approval append it to `setting-canon.md`, add its hooks as Threads and named figures as Characters (`state.py`), put any new nation on the faction board, and write a node per place to `places.json` (`worldgen.py … --campaign <dir>`). Distant content enters the Lists/seeds at low weight (≤1) so it never crowds the scene in front of the PC; re-entry is a lookup of `places.json`, not a reroll. |

# SURFACING: advancing a clock is not enough — surface it. When tick.py advances or fills a clock,
# convert it per world-model.md §3: show a visible sign now (telegraph), and fire a FILLED clock on the
# next beat as a Random Event (Close a Thread) or a Turning Point (Conclusion). Never let a clock fill silently.
#
# Campaign-specific clocks (a siege, a sorcerer's working, an Outsider incursion, a Major Project) are
# seeded into campaign-state.md at session zero and tracked there as Threads (world-model.md §2), not
# hard-listed in this registry.
