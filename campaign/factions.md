# Faction Board — Kingdom of Auragne

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

<!-- The three throne-claimants + the lost-empire remnant + the Arrival + the chief foreign meddler.
     The seven counts are Characters (characters.json) + canon; their levies appear as Assets under
     whichever claimant they back, and any count can be promoted to a full faction when play makes
     them central. Honest C/F/W rolled by worldgen.py faction; names/goals re-skinned to the fiction. -->

---

## Faction: The Lord Protector's Party
- Tags: Imperialist
- Force: 3   Cunning: 5   Wealth: 2
- HP: 15 / 15
- Treasure: 0
- Goal: Cement the Regency (Difficulty 2)
- Project: Make the Regency Permanent — clock 2/8
- Stance: schemer
- Actor: Nobles and Gentry
### Assets
- Aurholt | Base of Influence | HP 15/15 | base
- Aurholt | Mercenary Captains | HP 4/4

## Faction: The Dragon Throne
- Tags: Rooted
- Force: 5   Cunning: 2   Wealth: 2
- HP: 13 / 13
- Treasure: 1
- Goal: Crown the True King (Difficulty 1)
- Project: Free and Crown Phillipe — clock 0/8
- Stance: aggressive
- Actor: Warlords and Warband Chiefs
### Assets
- Aurholt | Base of Influence | HP 13/13 | base
- Aurholt | Dragon-blood Huscarls | HP 4/4

## Faction: The Mauressac Claim
- Tags: Rich
- Force: 2   Cunning: 3   Wealth: 5
- HP: 15 / 15
- Treasure: 0
- Goal: Press the Claim (Difficulty 1)
- Project: Press the Mauressac Claim — clock 3/8
- Stance: builder
- Actor: Merchants and Oligarchs
### Assets
- Mauressac | Base of Influence | HP 15/15 | base
- Mauressac | Guild Factors | HP 4/4

## Faction: The Worm-Cult of Vael
- Tags: Zealot
- Force: 4   Cunning: 1   Wealth: 1
- HP: 8 / 8
- Treasure: 1
- Goal: Wake the Crowned Worm (Difficulty 2)
- Project: Wake the Crowned Worm — clock 4/8
- Stance: aggressive
- Actor: Sorcerers and Magic-Users
### Assets
- Vörniss' Crown | Base of Influence | HP 8/8 | base

## Faction: The Arrival
- Tags: Supported
- Force: 3   Cunning: 2   Wealth: 4
- HP: 12 / 12
- Treasure: 0
- Goal: Carve a Place to Stand (Difficulty 1)
- Project: Find a Foothold (or the Way Home) — clock 1/8
- Stance: builder
- Actor: Demagogues and Religious Zealots
### Assets
- Aurholt | Base of Influence | HP 12/12 | base
- Aurholt | The Displaced Multitude | HP 4/4

## Faction: Mishar's Hand
- Tags: Rich, Supported
- Force: 3   Cunning: 4   Wealth: 3
- HP: 14 / 14
- Treasure: 3
- Goal: Vassalize Auragne (Difficulty 2)
- Project: Vassalize Auragne — clock 0/8
- Stance: schemer
- Actor: Nobles and Gentry
### Assets
- Aurholt | Base of Influence | HP 14/14 | base
- Auragne | Bought Counts | HP 2/2 | stealth
