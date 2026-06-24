# <Character Name>

> Use this when: this file is a player character's full record, stored in the campaign folder and updated as the PC changes. It **extends the engine's campaign character record** (`assets/templates/_engine-character-sheet.reference.md`) with WWN's specific fields. `scripts/chargen.py --out <path>` fills this for a new PC.

- **Level / Class:** <1>  <Warrior | Expert | Mage | Adventurer (Pe/Pw, …)>
- **Background:** <Soldier, …>
- **Goal:** <the active goal this PC will risk death for — required>
- **Ties:** <why this PC trusts and adventures with the party>

## Attributes
| Str | Dex | Con | Int | Wis | Cha |
|-----|-----|-----|-----|-----|-----|
| <10 (+0)> | <10 (+0)> | <10 (+0)> | <10 (+0)> | <10 (+0)> | <10 (+0)> |

_Mods: 3 = −2 · 4–7 = −1 · 8–13 = 0 · 14–17 = +1 · 18 = +2_

## Defenses & Health
- **AC:** <10>  (<armor +shield>, Dex <+0>)   — ascending; higher is better
- **HP:** <max> / <max>   ·   **System Strain:** 0 / <Con score> (max = Con)
- **Attack bonus:** <+0>   ·   **Initiative:** 1d8 <+Dex mod>
- **Saving throws** (roll d20 ≥ target):
  - **Physical** <15>  (16 − level − best Str/Con)
  - **Evasion** <15>  (16 − level − best Int/Dex)
  - **Mental** <15>  (16 − level − best Wis/Cha)
  - **Luck** <15>  (16 − level)

## Skills
_Check = `2d6 + skill level + attribute mod` vs difficulty 6/8/10/12/14._

- <Skill>-<level>
- <Skill>-<level>

## Foci
- **<Focus Name>** (level <1>, p.<##>) — <effect; bonus skill / +HP / +AC if any>
- **<Focus Name>** (level <1>, p.<##>) — <effect>

## Magic  _(casters only — delete if not a Mage/Partial Mage)_
- **Tradition:** <High Mage | Necromancer | Elementalist | …>
- **Effort:** <N> / <N>  (1 + Magic level + better Int/Cha mod; Partial Mage −1)
- **Prepared spells:** <spell>, <spell>, <spell>, <spell>
- **Arts:** <art name — Commit Effort for scene/day/indefinitely>

## Weapons
_Hit = attack bonus + combat-skill (Stab/Shoot/Punch) + attr mod; untrained = −2. Damage & Shock add the attr mod; Punch also adds Punch skill._

| Weapon | Hit | Damage | Shock | Attr / Notes |
|--------|-----|--------|-------|--------------|
| <Short Sword> | <+0> | <1d6> | <2/AC15> | <Str/Dex> |
| <Dagger> | <+0> | <1d4> | <1/AC15> | <Str/Dex, thrown 30/60> |

## Armor & Gear
- **Armor:** <type (AC)>   ·   **Shield:** <type | none>
- **Gear:** <pack contents; Readied vs Stowed if tracking Encumbrance>
- **Cash / wealth:** <N> sp
- **Languages:** native + Trade Cant + <1 per Connect/Know lvl-0, 2 per lvl-1>

## Record-keeping
- **XP:** 0
- **Conditions / injuries:** none   _(Mortally Wounded? Frail? track here)_
- **Notes:** <henchmen, mounts, contacts, focus reminders, # TODO verify items>

_Rules: Character Creation (book pp.8–35) and Equipment (pp.36–41). Resolve every roll with `mythic-gm/scripts/dice.py` and show it._
