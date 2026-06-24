# The Faction Turn — WWN factions, projects, domains

> Use this when: running the strategic layer — factions acting between scenes, a Major Project, or a domain's income. Fires at the world-tick cadence (`bridge/subsystems.md`); run it with `python3 scripts/faction_turn.py <faction-sheet> --seed N`. Factions pursue their goals whether or not the PC is present, and they **act to win**.

## A faction
- **Attributes** Cunning / Force / Wealth (1–8). **Max HP** = the sum of each attribute's HP-by-rating: `1→1, 2→2, 3→4, 4→6, 5→9, 6→12, 7→16, 8→20`. (So Force 5 / Cunning 2 / Wealth 3 = 9 + 2 + 4 = **15 HP**.)
- **Tags** grant special powers (e.g. Martial, Rich, Rooted, Machiavellian). A **Base of Influence** roots a faction in a place; **damage to a Base also reduces faction HP**.
- **Assets** are bought with the matching attribute (and need that rating): each has a cost, HP, attack, counterattack, and sometimes an ability. Catalogs are in `bridge/generators/faction.json` (Cunning / Force / Wealth asset lists).

## The Faction Turn  (`scripts/faction_turn.py`)
1. **Initiative** — every faction rolls **1d8**, high → low (GM breaks ties).
2. **Earn Treasure** = **½ Wealth + ¼ (Force + Cunning)**, rounded up.
3. **Pay upkeep** — asset upkeep + **1 Treasure per asset over its attribute's rating**; unpaid excess assets are lost (cheapest first).
4. **Free asset abilities** trigger (movement, profit, etc.).
5. **One Action** — every qualifying owned asset performs it:
   - **Attack** — opposed **1d10 + attribute** (the attacking asset's Cunning/Force/Wealth vs the defender's); the attacker wins **only on a strictly higher** total. Hit → the defender takes the attacker's **attack** damage; miss → the attacker takes the defender's **counter**.
   - **Move Asset** · **Repair Asset/HP** · **Expand Influence** (found a new Base via an attribute check) · **Buy / Sell Asset** · **Use Asset Ability** · **Seize a holding**.
6. **Goal check** — goal met → take its XP and choose a new goal; otherwise continue (or abandon it at the cost of next turn's action + abilities).
7. **Advance the Major-Project clock** (+1, or +2 if the faction worked it) and roll **one Background Actor event** (d20 general, or a typed d12: Adventuring Parties / Demagogues / Nobles / Merchants / Warlords / Sorcerers).

## Major Projects, Renown & the party
A **Major Project** is a multi-turn goal tracked as a clock; completing one grants **Renown** and a world-change. A **PC party is a small faction** — it buys assets and runs projects the same way; this is how heroes graduate from delvers to powers.

## Domains & holdings
A Base/holding produces income and demands upkeep (property taxes, hireling & soldier wages, construction). Net it each interval; neglect breeds unrest and lost assets. Surface every faction move through the engine's Lists — see `bridge/world-model.md`.

Source: `book/Worlds-Without-Number-Deluxe/10-Factions-and-Major-Projects.md`; `08 - Creating Adventures/11 - Land Ownership and Domains.md`. (Live rules data: `bridge/generators/faction.json`.)
