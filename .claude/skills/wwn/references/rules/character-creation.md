# Character Creation

> Use this when: rolling up a new WWN PC (or a named NPC of class), or checking how attributes, backgrounds, classes, foci, HP, saves, Effort, or starting gear are built. `scripts/chargen.py` automates all of this with honest, shown dice.

**Run it:** `python3 scripts/chargen.py --random --seed N` (full random) or `--class pm/pw --tradition healer --background physician --set14 Int --focus "One Point Strike Style" --out sheet.md`. Use `--tradition <name>` for any of the 15 traditions (core 5 + 6 Gyre + 4 Atlas: Accursed/Bard/Mageslayer/Wise) and `--art <name>` to pick tradition Arts. Pull any focus or spell verbatim with `python3 scripts/lookup.py focus <name>` / `lookup.py spell <name>`.

**Full data reference** (every skill, all 20 backgrounds, all classes & the Adventurer partial system, all 15 traditions, and every focus — core + the Atlas Maqqatban/Godblood/Arcane-Secret/Origin sets): `references/rules/character-creation-compendium.md`.

WWN is lethal and tactical — a level-1 hero can die to one good spear-thrust. Build honestly.

## The procedure (in order)

1. **Attributes** — roll **3d6 in order** for Str, Dex, Con, Int, Wis, Cha. *After rolling, you may set ONE score to 14.* (Or take the array 14, 12, 11, 10, 9, 7 — but then no free 14.) Mods: 3 = −2 · 4–7 = −1 · 8–13 = 0 · 14–17 = +1 · 18 = +2.
2. **Background** (d20 or pick) — gain its **free skill** at level-0, then ONE of:
   - take the listed **Quick Skills** (level-0), or
   - **pick two** from the Learning table (not "Any Skill"), or
   - **roll three times**, split as you like across the **Growth** and **Learning** tables (the only way to gain attribute bumps or a 3rd skill).
   - *Skill stacking:* 1st time = level-0, 2nd = level-1, 3rd = pick any other skill below level-1. **No novice skill exceeds level-1.** "+2 Physical/Mental" = +2 to one of Str/Dex/Con (resp. Int/Wis/Cha) or +1 to two.
3. **Class** — Warrior / Expert / Mage, or **Adventurer** (pick two partials). Sets hit die, attack bonus, and focus picks (table below). Mages/Partial Mages pick a **tradition** (Magic ch.).
4. **Foci** — every PC gets **1 free** focus (any kind). A Warrior/Partial Warrior adds **1 combat** focus; an Expert/Partial Expert adds **1 non-combat** focus (both levels may stack on one focus → start at level 2). Many foci grant a bonus skill; some give flat HP, AC, or a modifier. (`lookup.py focus <name>` for the full text.)
5. **Final touches** —
   - **Free skill:** pick one more skill at level-0.
   - **HP (max):** roll the class hit die **+ Con mod**, minimum **1**. (Warrior **1d6+2**, Expert **1d6**, Mage **1d6−1**; per level. Die Hard adds +2/level.)
   - **AC:** unarmored 10; else armor value (**+1 if a shield and you already wear equal/better armor**, else the shield sets base 13/14) **+ Dex mod**.
   - **Attack bonus:** from the class table. **Hit = d20 + attack bonus + combat-skill (Stab/Shoot/Punch) + attribute mod**; untrained weapon = −2.
   - **Saves** (roll d20 ≥ target): **Physical** 16 − level − best Str/Con · **Evasion** 16 − level − best Int/Dex · **Mental** 16 − level − best Wis/Cha · **Luck** 16 − level (no attr).
   - **Effort** (casters only): **1 + Magic skill level + better of Int/Cha mod** (Partial Mage −1, min 1); each tradition has its own pool. Full Mage knows **4** first-level spells, Partial **2** (dual-partial 4).
   - **System Strain:** current 0, **max = Con score**. **Initiative:** 1d8 + Dex mod.
6. **Gear** — pick an **equipment package** (below) *or* roll **3d6 × 10** starting silver and buy from the gear/armor/weapon tables. Note each weapon's damage + attribute mod and its **Shock N/AC** (Punch also adds Punch skill to damage).
7. **Name, goal, ties** — every hero needs an active **goal** worth risking death for and a reason to trust the party. Also: native language + Trade Cant + 1 tongue per Connect/Know at level-0 (2 each at level-1).

## Class summary (level-1 line)

| Class | Hit die (L1) | Attack bonus | Foci at L1 | Signature ability |
|---|---|---|---|---|
| Warrior | 1d6+2 | +1 | 1 combat + 1 any | Veteran's Luck; Killing Blow (+½ level dmg & Shock) |
| Expert | 1d6 | +0 | 1 non-combat + 1 any | Masterful Expertise (1/scene reroll); Quick Learner |
| Mage | 1d6−1 | +0 | 1 any | Arcane Tradition (full caster) |
| Adv. Pe/Pw | 1d6+2 | +1 | 1 combat + 1 non-combat + 1 any | Quick Learner only |
| Adv. Pe/Pm | 1d6 | +0 | 1 non-combat + 1 any | Quick Learner; partial caster |
| Adv. Pm/Pw | 1d6+2 | +1 | 1 combat + 1 any | partial caster; improved HD/attack |
| Adv. Pm/Pm | 1d6−1 | +0 | 1 any | two partial traditions |

*Adventurer partials lack the full class's strongest ability (no Masterful Expertise / Veteran's Luck / Killing Blow; weaker magic), but gain an extra focus pick at L1.*

## Equipment packages (pick one; p.29)
Adventuring Peasant · Ranger or Archer · Armored Warrior · Gentry Wayfarer · Mage/Healer/Scholar · Roguish Wanderer. Each lists armor, shield, weapons (with damage + Shock), gear, and any cash. The script picks a class-appropriate package by default, or `--package <id>` / `--roll-wealth`.

The filled sheet goes to `assets/templates/character-sheet.md` (stored per-PC in the campaign folder).

Source: `book/Worlds-Without-Number-Deluxe/02-Character-Creation.md` (attributes L103–134; backgrounds L222–402; classes L404–590; foci L592–905; final touches L906–953; packages L954–991) and `03 - Equipment, Armor, and Weaponry.md` (armor L196–238; weapons L250–354).
