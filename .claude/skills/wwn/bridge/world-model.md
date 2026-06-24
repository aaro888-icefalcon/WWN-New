# World Model — WWN clocks, factions & threats → the engine   (supports: world-tick, seeds, meaning)

The Latter Earth is a living world: factions pursue Cunning/Force/Wealth goals, Major-Project and threat clocks tick, and ruins and Outsiders stir whether or not the PC acts. This file feeds that live world **into the engine**, so it surfaces as the engine's own Random Events, Turning Points, scene elements, and seeds — not as an inert ledger.

## 1. The world ledger (lives in `campaign-state.md`)
- **Factions** — Cunning/Force/Wealth, HP, assets, a **Major-Project clock**, attitude to the PC. Advanced by the Faction Turn (`scripts/faction_turn.py`).
- **Clocks** — project/threat/deadline countdowns (n/N): each carries what advances it and where/whom it touches.
- **Threats** — a ruin waking, an Outsider incursion, a sorcerer's working; each owns a clock.
- **NPCs** — each with written wants/fears.
- **Holdings** — domains the PC or a faction holds (income/upkeep).

## 2. The ledger IS the engine's Lists (no parallel bookkeeping)
Map it onto the engine's **Threads** and **Characters** Lists so it surfaces automatically:

| World object | Engine List | Represented as |
|---|---|---|
| a clock / faction goal / open quest | **Threads** | the looming change ("Sarul's legion masses on the Gyre border") |
| a threat with no clear thread yet | **Threads** (the menace) + **Adventure Features** (its site/hazard) | a danger to be discovered |
| a faction + its project | **Threads** (the agenda) + **Characters** (the faction / its agent) | who is pushing it |
| an NPC | **Characters** | acts on written wants |
| a threat's site / signature hazard | **Adventure Features** | a place or menace a scene can land on |

At bookkeeping: a new clock/faction/threat → add the matching List entry (weight ≤3); a concluded one → remove it.

## 3. Four ways the world surfaces
**a. → Random Event.** When `oracle.py event --campaign <dir>` rolls a Focus that invokes a List:
- *Move/Close a Thread* → roll the **Threads** (the clocks/projects); the drawn clock **advances** (Toward +1, hard +2; **Close** = it fills/concludes now). Narrate the visible sign.
- *NPC Action / ±* → roll the **Characters** (factions/NPCs); the drawn actor takes its next move on its written want — a faction resolves it through the **Faction Turn**.
- A **filled** clock always takes priority as a Close.

**b. → Turning Point.** On an Altered/Interrupt scene, when `adventure_crafter.py turning-point --campaign <dir>` invokes a **Thread**, **prefer a due clock or faction project**. A filled clock → engineer its **Conclusion** plot point and remove the Thread.

**c. → Scene framing.** After `tick.py` advances a clock, show a **visible sign now** in the framing — a refugee column, a sorcerous omen, a new banner over a keep, frost in the wrong season. Always telegraph before a clock fires (`interpretation.md`).

**d. → Seeds.** Every active clock, faction-with-a-project, and threat is a **seed candidate** — the steady channel that keeps the world present even when no event fires (`seeds.md`).

## 4. Bookkeeping procedure (each scene end)
1. `python3 <mythic-gm>/scripts/tick.py ./bridge <scene#>` → advance the due subsystems (faction-turn cadence, clocks, supplies); roll their tables honestly.
2. Apply ledger changes to the **Lists** (add/remove Threads & Characters; weight ≤3).
3. If any clock **filled**, queue it to fire **next beat** as a Random Event (Close) or Turning Point (Conclusion) — never silently.
4. Refresh the seed deck from the ledger (`seeds.md`).
5. Record the updated ledger to `campaign-state.md`.

## 5. Weighting (proximity + urgency + visibility)
When the engine picks among open world objects (a List invoke or a seed draw), bias by: **proximity** (the PC's region > adjacent > distant), **urgency** (a clock ≥75% full, or one that ticked this scene, outweighs a quiet one), **visibility** (something the PC has seen a sign of outweighs a secret). Let the dice choose **within** the weighted set; never hand-pick the convenient one. **Player ≠ PC knowledge:** an un-earned secret may seed a *sign*, never the reveal. This is how the Latter Earth drives play through the engine instead of around it.
