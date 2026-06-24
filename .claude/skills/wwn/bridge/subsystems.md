# World Subsystems — Worlds Without Number   (hook: world-tick; fired by tick.py at bookkeeping)

## Operative
FIRE `python3 scripts/bookkeep.py <campaign> <scene#>` (which runs the engine's `tick.py`) AT EVERY
scene end — not "when relevant." The Latter Earth moves whether or not the PC looks: advance the clocks
below, run a due Faction Turn (`faction_turn.py`), tick Major-Project clocks, refresh Effort, recover or
charge System Strain, spend supplies, and roll wandering/naval checks honestly. A filled clock is never
silent — telegraph it now and fire it next beat as a Random Event (Close a Thread) or a Turning Point
(Conclusion). If a subsystem stalls for several scenes, the world has drifted; tick is mandatory.

# tick.py reads the cadence column: 'every scene' | 'every N scenes' | 'on trigger: …'
| subsystem | cadence | advance by |
|---|---|---|
| Faction Turn | every ~week of in-world time (≈ every 4–6 scenes) | run `scripts/faction_turn.py <faction-sheet>`: each faction earns Treasure, pays upkeep, takes ONE action (opposed 1d10+attr), advances its goal. Apply results to the Threads/Characters Lists (`world-model.md`). |
| Major-Project clocks | per faction turn | +1 (or +2 if the faction/party worked it this turn); a filled clock concludes its project → Renown / a world-change. |
| Effort refresh | scene / day | for-the-scene Effort returns at scene end; for-the-day at a night's rest; indefinite stays committed. |
| System Strain recovery | per night's rest | −1 Strain and recover level/HD HP if fed and rested; Frail recover neither. |
| Wealth / upkeep & taxes | per in-world interval | net holding income vs hireling/soldier/upkeep costs; unrest or lost assets if unpaid. |
| Wandering encounters | per watch/turn while exploring | roll the region's encounter check; on a hit, draw `wilderness_tags`/`monster_gen` + a Reaction (2d6). |
| Supplies & privation | per day in the field | spend food/water/light; on a shortfall, Physical saves + System Strain (`references/rules/saves.md`). |
| Naval ship-crisis | per day at sea | roll `naval` (Seafaring Event / Ship Crisis) honestly. |

# SURFACING: advancing a clock is not enough — surface it. When tick.py advances or fills a clock,
# convert it per world-model.md §3: show a visible sign now (telegraph), and fire a FILLED clock on the
# next beat as a Random Event (Close a Thread) or a Turning Point (Conclusion). Never let a clock fill silently.
#
# Campaign-specific clocks (a siege, a sorcerer's working, an Outsider incursion, a Major Project) are
# seeded into campaign-state.md at session zero and tracked there as Threads (world-model.md §2), not
# hard-listed in this registry.
