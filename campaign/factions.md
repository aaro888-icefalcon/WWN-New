# Faction Board — <campaign name>

> Use this when: this file is the campaign's **live faction board** — the roster of the 3-4 (max ~6) factions whose Cunning/Force/Wealth struggles drive the living world. It is the file `scripts/faction_turn.py <this file> --seed N` runs ONE WWN faction turn off (`--out same` writes the new numbers back). Session Zero copies this template in; **`scripts/worldgen.py` APPENDS** a generated faction block here for every nation it rolls (`worldgen.py faction`, `nation`, `world`, `geography` with `--campaign <dir>`). Keep it in sync with the faction board in `wwn-campaign-state.md`. Faithful to *Worlds Without Number* ch.10.

**Format rules (the parser reads these exactly — keep them when hand-editing):**
- One block per faction, headed `## Faction: <Name>`.
- Attributes on one line: `- Force: N   Cunning: N   Wealth: N` (1-8 each).
- `- HP: cur / max` — **max = sum of the three attributes' HP values** (rating 1=1, 2=2, 3=4, 4=6, 5=9, 6=12, 7=16, 8=20).
- `- Treasure: N` (points).
- `- Goal: <name> (Difficulty X)` — the goal the faction is pursuing for XP.
- `- Project: <name> — clock n/N` *(optional Major-Project clock the faction advances)*.
- `- Tags: <tag>, <tag>` *(optional; e.g. Martial, Rich, Rooted)*.
- `- Stance: aggressive | defensive | builder | schemer` *(optional AI hint for the script)*.
- `- Actor: <type>` *(optional background-actor type: Adventuring Parties / Demagogues / Nobles / Merchants / Warlords / Sorcerers — the script rolls one event/turn; omit for the generic d20)*.
- Then `### Assets`, one per line: `- <Location> | <AssetName> | HP a/b | [stealth] [base]`.
  - The HQ line is the `Base of Influence` flagged `base`; its max HP equals the faction maximum.
  - `stealth` marks a Stealthed Asset (can't be targeted until it acts or is revealed).

<!-- worldgen appends generated faction blocks below this line. Each block is
     already in the exact format above and runs through faction_turn.py as-is.
     Remove this placeholder note once real factions exist if you like. -->

---

## Faction: Sarul
- Tags: Rooted
- Force: 3   Cunning: 4   Wealth: 3
- HP: 14 / 14
- Treasure: 0
- Goal: Peaceable Kingdom (Difficulty 1)
- Project: A recurring plant plague is causing hunger — clock 0/8
- Stance: schemer
- Actor: Demagogues
### Assets
- Sarul | Base of Influence | HP 14/14 | base
- Sarul | Smugglers | HP 4/4
