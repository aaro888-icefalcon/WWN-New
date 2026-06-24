# System Profile — Worlds Without Number   (hook: resolve)

> Use this when: every session, to know what WWN resolves vs. what defers to the engine's Fate Question, and how to express any WWN roll. This is the seam.

**Precedence:** this profile + the WWN cards + `book/` **>** model memory. **All dice route through `mythic-gm/scripts/dice.py`** (shown, never invented).

## Operative
WWN RESOLVES PC ACTIONS — a Fate Question NEVER does. Rung 1 of the oracle ladder: if a PC *does*
something with real stakes, roll the WWN check via `scripts/check.py` (honest dice), never the oracle.
Use the WWN system WHEN the PC:
- attacks / strikes / shoots → `check.py attack <hitBonus> --ac <AC>` (Shock lands on a miss vs low AC)
- uses a skill (climb, sneak, persuade, lockpick, heal, recall…) → `check.py skill <skill+attr> --vs <6|8|10|12|14>`
- resists poison / spell / blast / fall / fear → `check.py save <target>` (PC target 16−level−attr; Luck 16−level)
- contests another (sneak vs notice, duel, arm-wrestle) → `check.py opposed <pcMod> <foeMod>` (ties → PC)
- deals damage / drops to 0 HP / casts or commits Effort → resolve per the combat & magic cards (Shock; mortal wounds; Effort)
A Fate Question is ONLY for world facts the rules don't cover (is the gate guarded? does it rain?).
Before any `dice.py fate`, ask "is this a PC task / attack / save / contest?" — if yes, drop to rung 1.

## Dice convention
- Express a skill check as: `dice.py roll 2d6+<skill+attr+mods>`
- Express an attack as: `dice.py roll 1d20+<hit bonus>` · a save as: `dice.py roll 1d20` (compare to target) · damage as `dice.py roll <weaponDie>+<mods>`
- Advantage/disadvantage where a rule grants a reroll-style edge: `dice.py roll 2d6+N adv|dis`.

## Core resolution (the three rolls)
- **Skill check** — `2d6 + skill level + attribute mod` **vs difficulty 6 / 8 / 10 / 12 / 14** (routine → legendary). Untrained (no level-0) = **−1**. Success = meet-or-beat. Failure = no progress *or* progress at a cost (GM picks). Situational mods cap at **±2**. Peripheral-skill use raises difficulty by **+2**.
- **Opposed check** — both roll relevant `2d6+mod`; **highest wins, ties to the PC**. NPCs add their listed skill bonus when the role fits, else roll flat 2d6.
- **Saving throw** — `d20`, roll **≥** target. PC targets = **16 − level − best relevant attribute mod** (Luck = 16 − level, no attr). Monster/NPC save = **15 − ½ HD**. Four PC saves: **Physical** (Str/Con), **Evasion** (Int/Dex), **Mental** (Wis/Cha), **Luck** (none).
- **Degrees of success?** No graded tiers in the core (success/fail). In **rule-mode Fate Questions**, collapse Exceptional → ±maximal (treat as crit/fumble); never grant "yes, and" mechanical bonuses the system doesn't define.

## Stats & skills
- **Attributes (3d6):** Str, Dex, Con, Int, Wis, Cha → mods (−2…+2 typical). **Skills** rated 0–4, rolled as `2d6 + level + attr`. Full skill list & the 2d6 check: `references/rules/resolution.md`.
- **Class** sets attack-bonus growth and HP: Warrior (full attack bonus + Veteran's Luck + Killing Blow), Expert (skills + Quick Learner), Mage (Arts/spells), Adventurer/partials. **Foci** are the feat layer (`scripts/lookup.py focus <name>`).

## Defenses & health
- **Armor Class** is ascending; unarmored = 10; AC = armor value (+shield +1) + Dex mod. Higher is better.
- **Hit Points** by class/level + Con mod. **System Strain** ≤ Con caps forced healing/exertion.
- **Death is real:** at 0 HP, unnamed NPCs die; PCs & named NPCs are **Mortally Wounded** (die at end of the 6th round unless stabilized; instant death on further damage). See `references/rules/healing-and-strain.md`.

## Combat (full card: `references/rules/combat.md`)
- **Initiative:** each side `1d8 + best Dex mod`; PCs win ties. (Optional individual init.)
- **Attack:** `1d20 + combat-skill + class attack bonus + attribute mod` vs target **AC**; untrained weapon = −2.
- **Shock:** weapons list **Shock N/AC** — on a *miss* vs a target whose AC ≤ that value, deal N anyway (+attr & magic). A hit never deals less than its Shock. The tactical floor: attacks rarely do nothing.
- **Action economy:** one **Main**, one **Move**, free **On-Turn**, any number of **Instant** (incl. off-turn). Signature tactical actions: Swarm Attack (mob, +2/+1 each, max +6/+3, Shock always lands), Screen an Ally, Total Defense (Shock-immune, +2 AC), Fighting Withdrawal, Snap Attack (−4 Instant), Execution Attack, Shatter Shield, Charge.
- **Morale:** `2d6` vs Morale score; fail → flee/parley. NPCs act to win and break realistically.

## NPC stat units (stat on the fly)
A WWN foe = **HD · AC · Atk bonus · Damage die(+Shock N/AC) · Move · Morale (2d6) · Instinct · Save (15−½HD) · Skill bonus**. To improvise an NPC's quality: decide the expected value → a Fate Question → read `oracle.py answer npc_statistics <key>` (Yes = as expected; Exc Yes +25%; No −25%; Exc No −50% to the relevant number). Full statting / generation: `references/gm/monsters.md`, `scripts/monster.py`.

## Routing default (the oracle ladder)
- **WWN resolves (anything a PC *does*):** combat, skill checks, saving throws, magic/Effort, healing/strain, character & monster stats, faction turns, treasure, worldgen. **Front-door: `scripts/check.py skill|attack|save|opposed`** (rung 1). A PC task / attack / save / contest is **never** a Fate Question.
- **Defer to a Fate Question:** world questions the rules are silent on (does the patrol pass? is the door unlocked? is the duke amenable?). `dice.py fate <odds> <CF>`; `--mode rule` when standing in for a missing mechanic.
- **Subsystems as procedures (not bare Fate Questions):** the Faction Turn, Major Projects, worldgen, and naval combat each run their own steps — see `bridge/subsystems.md` and the `references/gm/` cards.

Source: `book/Worlds-Without-Number-Deluxe/04-The-Rules-of-the-Game.md` (L51–453); character & class detail in `02 - Character Creation.md`.
