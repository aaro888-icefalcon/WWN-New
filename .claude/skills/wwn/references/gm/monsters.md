# Monsters — statting & generating foes

> Use this when: you need a creature's stats, want to stat a foe fast, or generate a monstrous concept. Foes **act to win** — stat them honestly, then play their Instinct and Morale.

## The statblock
`HD · AC · Atk · Dmg · Shock · Move · ML · Instinct · Skill · Save`
- **HD** hit dice (HP ≈ HD × 4.5). **AC** ascending (an `a` suffix = naturally armored). **Atk** hit bonus (`×N` = N attacks/round). **Dmg** weapon die + mods. **Shock N/AC** (deals N even on a miss vs that AC). **Move** ft/round. **ML** Morale (roll 2d6 vs it). **Instinct** what it does when undirected (1–8 + a behavior). **Skill** generic skill bonus. **Save** = `15 − ½HD` (one number).

## Stat a foe fast  (`scripts/monster.py --hd N`)
HP = roll **Nd8**; Atk ≈ **+N** (cap ~+10); Save **15 − N//2**; AC **12** (weak) / **13** / **15** (tough); Damage **1d6 / 1d8 / 1d10** by size; Morale 8 default. The script prints a ready baseline — tune AC/damage/abilities to the concept.

## Generate a concept  (`scripts/monster.py --context`)
Rolls the **One-Roll Monstrous Context** (basic body plan, animal resemblance, how it hunts, why it isn't dead yet, a Monstrous Drive) from `monster_gen.json`. Layer one **Uncanny Power** (damage / movement / debilitating / augmenting / intrinsic) to give it a signature threat worth a tactical answer.

## Bestiary lookup  (`scripts/lookup.py monster <name>`)
**137** statblocks parsed from WWN ch.9 + the Atlas's Beasts & Fell Things — pull one without loading the chapter.

## Reaction · Morale · Instinct
First contact (if not obviously hostile): **Reaction 2d6** (hostile ↔ friendly). In a losing fight or after a fright: **Morale 2d6 vs ML** → flee, surrender, or parley. Undirected, a creature acts on its **Instinct**. Intelligent foes use cover, focus fire, screen, retreat, and bargain — never play them dumb to spare the PC (engine Creed).

Source: `book/Worlds-Without-Number-Deluxe/09-Creatures-of-A-Far-Age.md`; `book/The-Atlas-of-the-Latter-Earth/03-Beasts-and-Fell-Things.md`. (Data: `bridge/generators/monster_gen.json`, `bestiary.json`.)
