# Faction Board — <campaign name>

> Use this when: this file is the campaign's **faction board** — the live roster of the 3-4 (max 6) factions whose Cunning/Force/Wealth struggles drive the living world. `scripts/faction_turn.py <this file> --seed N` runs one WWN faction turn off it; `--out same` writes the new numbers back. Keep it in sync with the faction board in `wwn-campaign-state.md`. Faithful to *Worlds Without Number* ch.10.

**Format rules (the parser reads these exactly):**
- One block per faction, headed `## Faction: <Name>`.
- Attributes on one line: `- Force: N   Cunning: N   Wealth: N` (1-8 each).
- `- HP: cur / max` (max = sum of the three attributes' HP values; see the card).
- `- Treasure: N` (points).
- `- Goal: <name> (Difficulty X)` — the goal the faction is pursuing for XP.
- `- Project: <name> — clock n/N` *(optional Major-Project clock the faction advances)*.
- `- Tags: <tag>, <tag>` *(optional; e.g. Martial, Rooted, Rich)*.
- `- Stance: aggressive | defensive | builder | schemer` *(optional AI hint for the script)*.
- `- Actor: <type>` *(optional background-actor type: Adventuring Parties / Demagogues / Nobles / Merchants / Warlords / Sorcerers — the script rolls one event/turn; omit for the generic d20)*.
- Then `### Assets`, one per line: `- <Location> | <AssetName> | HP a/b | [stealth] [base]`.
  - The HQ line is the `Base of Influence` flagged `base`; its max HP equals the faction maximum.
  - `stealth` marks a Stealthed Asset (can't be targeted until it acts or is revealed).

---

## Faction: <Faction One>
- Tags: <Martial>
- Force: 5   Cunning: 2   Wealth: 3
- HP: 15 / 15
- Treasure: 4
- Goal: Blood the Enemy (Difficulty 2)
- Project: <Fortify the frontier> — clock 0/6
- Stance: aggressive
- Actor: Warlords
### Assets
- <HQ Location> | Base of Influence | HP 15/15 | base
- <HQ Location> | Infantry | HP 6/6
- <Contested Town> | Scouts | HP 5/5

## Faction: <Faction Two>
- Tags: <Rich>
- Force: 2   Cunning: 4   Wealth: 5
- HP: 17 / 17
- Treasure: 6
- Goal: Inside Enemy Territory (Difficulty 2)
- Project: <Buy the council> — clock 1/8
- Stance: schemer
### Assets
- <HQ Location> | Base of Influence | HP 17/17 | base
- <Contested Town> | Spymaster | HP 4/4
- <Contested Town> | Blackmail | HP 4/4
