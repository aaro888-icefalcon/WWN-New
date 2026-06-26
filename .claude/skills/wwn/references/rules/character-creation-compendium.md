# WWN Character-Creation Compendium

> **Single-document reference** for running character creation in play. Compiles everything the
> GM needs at the table: the dice/rolling rules, the full skill list, **all 20 backgrounds** (with
> Growth/Learning tables), **all 4 classes** + the 4 Adventurer combos, **all 33 Foci**, and **all 11
> mage traditions / magic-using partial classes**. Faithful to *Worlds Without Number Deluxe*
> (Character Creation pp. 8–35; Magic pp. 60–97; Arts of the Gyre pp. 348–359).
>
> This is a play-card digest, not a replacement for the book. Where exact spell/art text matters,
> pull it verbatim: `python3 scripts/lookup.py spell <name>` / `lookup.py focus <name>`.
> The script `scripts/chargen.py` automates the build with honest, shown dice.

---

## 0 · The order of creation (do these in order, in play)

1. **Attributes** — roll 3d6 in order (Str, Dex, Con, Int, Wis, Cha); may set one to 14.
2. **Background** — d20 or pick; free skill + (Quick / pick-two-Learning / roll-three).
3. **Class** — Warrior / Expert / Mage / Adventurer (two partials). Mages pick a tradition.
4. **Foci** — 1 free (any) + the class's combat/non-combat pick(s).
5. **Final touches** — free skill, HP, AC, attack bonus, saves, Effort/spells, gear, name/goal/ties.

> In *solo step-by-step play*, the GM rolls each die through the scripts and **stops at every choice**
> (which attribute → 14, background, skill mode, class, each focus, tradition, spells, package, goal)
> to let the player decide before moving on. Never batch-resolve a creation the player hasn't chosen.

---

## 1 · Rules for rolling (the dice that matter at creation & in play)

### Attribute modifiers (p.9)
| Score | 3 | 4–7 | 8–13 | 14–17 | 18 |
|---|---|---|---|---|---|
| Mod | −2 | −1 | 0 | +1 | +2 |

### Generating attributes (p.9)
- **Roll:** 3d6 six times, **assigned in order** Str→Cha. Then you **may change one score to 14**.
  *(Clement GMs may let rolls be assigned freely; strict tables keep them in order.)*
- **Array (no free 14):** assign 14, 12, 11, 10, 9, 7 as you wish.

### Skill checks (p.10, resolution)
`2d6 + skill level + best applicable attribute mod` vs **difficulty**. Meet-or-beat = success.

| Diff | 6 | 8 | 10 | 12 | 14+ |
|---|---|---|---|---|---|
| Meaning | tricky for a layman | real challenge | only a skilled expert | only a master reliable | even a master likely fails |

- **Untrained** (no level-0): **−1**, and some esoteric skills can't be attempted at all.
- **Circumstance/tool modifiers** cap at **±2** total; a peripheral-but-plausible skill = **+2 difficulty**.
- **Aiding:** helper rolls vs same difficulty; success = **+1** to the actor (max +1 total).
- **Opposed:** all roll `2d6 + mod`; **highest wins, ties to the PC**.
- Skills rated **0–4**; **no novice exceeds level-1** at creation.

### Combat to-hit (p.28)
`d20 + base attack bonus (class) + combat skill (Stab/Shoot/Punch) + attribute mod` ≥ target AC.
Untrained weapon = **−2**. Damage = weapon die + attribute mod (Punch also adds Punch skill).
**Shock** = listed N/AC: on a miss vs a target of that AC or lower, still deal N damage.

### Saving throws (roll d20 ≥ target; higher is better)
| Save | Attribute used | Target |
|---|---|---|
| Physical | best of Str/Con | **16 − level − mod** |
| Evasion | best of Int/Dex | **16 − level − mod** |
| Mental | best of Wis/Cha | **16 − level − mod** |
| Luck | none | **16 − level** |

*(At level 1 this equals "15 − mod" / "15"; saves improve by 1 per level.)*
Monsters/NPCs use one save = **15 − ½ HD** (round down).

### Hit points, AC, initiative, Effort, Strain
- **HP (max):** roll class hit die **+ Con mod**, minimum **1**.
- **AC:** unarmored 10; else armor value **+ Dex mod**. Shield: **+1 if you already wear equal/better
  armor**, otherwise the held shield **sets** the base (13 small / 14 large) before Dex.
- **Initiative:** `1d8 + Dex mod`.
- **System Strain:** current 0, **max = Con score**.
- **Effort (casters):** default `1 + Magic skill level + better of Int/Cha mod`; **Partial Mage −1** (min 1).
  *Several traditions override the skill/attribute used — see §5.*
- **Time:** Round = 6 s · Turn = 10 min · Scene = one activity/place (most durations = "1 scene").

### Starting languages (p.29)
Native + Trade Cant + 1 tongue per Connect/Know at **level-0**, **2** each at level-1.

---

## 2 · The skill list (p.10)

Rated 0–4. Combat skills are **Stab, Shoot, Punch**; everything else is non-combat. *Magic* gates
Arts/spells (non-casters get only scholarly use).

| Skill | Covers |
|---|---|
| **Administer** | run an org, scribe, logistics, audit records, spot incompetence/treachery |
| **Connect** | find useful people, make ties, call on org resources, get favors |
| **Convince** | persuade a listener something is true |
| **Craft** | make/repair goods & tech appropriate to background |
| **Exert** | run, swim, climb, jump, throw, sustained physical labor |
| **Heal** | wounds, disease, poison, stabilize the Mortally Wounded |
| **Know** | history, geography, natural science, academic fields |
| **Lead** | inspire & manage followers, keep loyalty under pressure |
| **Magic** | cast/analyze magic; know mages & magical events (gate for Arts/spells) |
| **Notice** | spot details, ambushes, hidden things; read emotional state |
| **Perform** | sing, act, dance, orate; compose works |
| **Pray** | rites, gods/demons/taboos, religious hierarchy & iconography |
| **Punch** | unarmed/natural-weapon fighting (reliably non-lethal) |
| **Ride** | ride/drive land transport; mount care & cart repair |
| **Sail** | sail/repair ships, navigate, manage crew |
| **Shoot** | bows, crossbows, hurled weapons; fletch |
| **Sneak** | stealth, hide, pick pockets/locks, disguise, defeat traps |
| **Stab** | melee weapons, thrown weapons; maintain/identify weaponry |
| **Survive** | hunt, fish, navigate, mitigate hazards, shelter |
| **Trade** | buy/sell at profit, appraise, black markets, smuggling law |
| **Work** | catch-all profession (painter, lawyer, farmer, herdsman…) |

**Skill stacking (p.11):** 1st time gained = level-0 · 2nd = level-1 · 3rd time (or forced) = pick **any
other** skill below level-1. **No novice skill exceeds level-1.**
**Attribute growth tokens:** `+1 Any` = +1 to any one stat. `+2 Physical` = +2 to one of Str/Dex/Con
or +1 to two of them; `+2 Mental` likewise for Int/Wis/Cha. (Cap 18.)

---

## 3 · Backgrounds (pp.11–17)

**d20 table:** 1 Artisan · 2 Barbarian · 3 Carter · 4 Courtesan · 5 Criminal · 6 Hunter · 7 Laborer ·
8 Merchant · 9 Noble · 10 Nomad · 11 Peasant · 12 Performer · 13 Physician · 14 Priest · 15 Sailor ·
16 Scholar · 17 Slave · 18 Soldier · 19 Thug · 20 Wanderer.

**After the free skill, choose ONE:** (a) take the **Quick Skills** (level-0); (b) **pick two** from the
**Learning** table (not "Any Skill"); (c) **roll three times**, split as you like across **Growth** & **Learning**
(the only path to attribute bumps or a 3rd skill). "Any Combat" = Stab/Shoot/Punch.

| Background | Free skill | Quick skills | d6 Growth (1–6) | d8 Learning (1–8) |
|---|---|---|---|---|
| **Artisan** | Craft | Trade, Connect | +1 Any · +2 Phys · +2 Phys · +2 Ment · Exert · Any Skill | Connect · Convince · Craft · Craft · Exert · Know · Notice · Trade |
| **Barbarian** | Survive | Any Combat, Notice | +1 Any · +2 Phys · +2 Phys · +2 Ment · Exert · Any Skill | Any Combat · Connect · Exert · Lead · Notice · Punch · Sneak · Survive |
| **Carter** | Ride | Connect, Any Combat | +1 Any · +2 Phys · +2 Phys · +2 Ment · Connect · Any Skill | Any Combat · Connect · Craft · Exert · Notice · Ride · Survive · Trade |
| **Courtesan** | Perform | Notice, Connect | +1 Any · +2 Ment · +2 Ment · +2 Phys · Connect · Any Skill | Any Combat · Connect · Convince · Exert · Notice · Perform · Survive · Trade |
| **Criminal** | Sneak | Connect, Convince | +1 Any · +2 Ment · +2 Phys · +2 Ment · Connect · Any Skill | Administer · Any Combat · Connect · Convince · Exert · Notice · Sneak · Trade |
| **Hunter** | Shoot | Survive, Sneak | +1 Any · +2 Phys · +2 Phys · +2 Ment · Exert · Any Skill | Any Combat · Exert · Heal · Notice · Ride · Shoot · Sneak · Survive |
| **Laborer** | Work | Connect, Exert | +1 Any · +1 Any · +1 Any · +1 Any · Exert · Any Skill | Administer · Any Skill · Connect · Convince · Craft · Exert · Ride · Work |
| **Merchant** | Trade | Convince, Connect | +1 Any · +2 Ment · +2 Ment · +2 Ment · Connect · Any Skill | Administer · Any Combat · Connect · Convince · Craft · Know · Notice · Trade |
| **Noble** | Lead | Connect, Administer | +1 Any · +2 Ment · +2 Ment · +2 Ment · Connect · Any Skill | Administer · Any Combat · Connect · Convince · Know · Lead · Notice · Ride |
| **Nomad** | Ride | Survive, Any Combat | +1 Any · +2 Phys · +2 Phys · +2 Ment · Exert · Any Skill | Any Combat · Connect · Exert · Lead · Notice · Ride · Survive · Trade |
| **Peasant** | Exert | Sneak, Survive | +1 Any · +2 Phys · +2 Phys · +2 Phys · Exert · Any Skill | Connect · Exert · Craft · Notice · Sneak · Survive · Trade · Work |
| **Performer** | Perform | Convince, Connect | +1 Any · +2 Ment · +2 Phys · +2 Phys · Connect · Any Skill | Any Combat · Connect · Exert · Notice · Perform · Perform · Sneak · Convince |
| **Physician** | Heal | Know, Notice | +1 Any · +2 Phys · +2 Ment · +2 Ment · Connect · Any Skill | Administer · Connect · Craft · Heal · Know · Notice · Convince · Trade |
| **Priest** | Pray | Convince, Know | +1 Any · +2 Ment · +2 Phys · +2 Ment · Connect · Any Skill | Administer · Connect · Know · Lead · Heal · Convince · Pray · Pray |
| **Sailor** | Sail | Exert, Notice | +1 Any · +2 Phys · +2 Phys · +2 Ment · Exert · Any Skill | Any Combat · Connect · Craft · Exert · Heal · Notice · Perform · Sail |
| **Scholar** | Know | Heal, Administer | +1 Any · +2 Ment · +2 Ment · +2 Ment · Connect · Any Skill | Administer · Heal · Craft · Know · Notice · Perform · Pray · Convince |
| **Slave** | Sneak | Survive, Exert | +1 Any · +2 Phys · +2 Phys · +2 Ment · Exert · Any Skill | Administer · Any Combat · Any Skill · Convince · Exert · Sneak · Survive · Work |
| **Soldier** | Any Combat | Exert, Survive | +1 Any · +2 Phys · +2 Phys · +2 Phys · Exert · Any Skill | Any Combat · Any Combat · Exert · Lead · Notice · Ride · Sneak · Survive |
| **Thug** | Any Combat | Convince, Connect | +1 Any · +2 Ment · +2 Phys · +2 Phys · Connect · Any Skill | Any Combat · Any Combat · Connect · Convince · Exert · Notice · Sneak · Survive |
| **Wanderer** | Survive | Sneak, Notice | +1 Any · +2 Phys · +2 Phys · +2 Ment · Exert · Any Skill | Any Combat · Connect · Notice · Perform · Ride · Sneak · Survive · Work |

---

## 4 · Classes (pp.18–21)

Every PC gets **1 free focus (any kind)** plus the class's pick(s). Hit die rolled at **each level**.

| Class | Hit die (per level) | Attack bonus (L1→L10) | Foci at L1 | Signature ability |
|---|---|---|---|---|
| **Warrior** | 1d6+2 | +1,2,3,4,5,6,7,8,9,10 | 1 combat + 1 any | **Veteran's Luck** (1/scene turn a miss→hit or a hit-on-you→miss); **Killing Blow** (+½ level, round up, to damage **and** Shock) |
| **Expert** | 1d6 | +0,1,1,2,2,3,3,4,4,5 | 1 non-combat + 1 any | **Masterful Expertise** (1/scene reroll a non-combat check, Instant); **Quick Learner** (extra non-combat/attribute skill point per level) |
| **Mage** | 1d6−1 | +0,0,0,0,1,1,1,1,1,2 | 1 any | **Arcane Tradition** (pick a tradition; full caster) |

**Adventurer** = pick **two** partial classes. The extra L1 focus matters most at low levels; partials
lack the full class's strongest ability.

| Adventurer combo | Hit die | Attack bonus (L1→L10) | Foci at L1 |
|---|---|---|---|
| **Partial Expert / Partial Warrior** | 1d6+2 | +1,2,2,3,4,5,5,6,6,7 | 1 expert + 1 warrior + 1 any |
| **Partial Expert / Partial Mage** | 1d6 | +0,1,1,2,2,3,3,4,4,5 | 1 expert + 1 any |
| **Partial Mage / Partial Warrior** | 1d6+2 | +1,2,2,3,4,5,5,6,6,7 | 1 warrior + 1 any |
| **Partial Mage / Partial Mage** | 1d6−1 | +0,0,0,0,1,1,1,1,1,2 | 1 any (two partial traditions) |

- **Partial Expert:** keeps *Quick Learner*, loses *Masterful Expertise*.
- **Partial Warrior:** improved HD & attack, loses *Veteran's Luck* & *Killing Blow*.
- **Partial Mage:** gains *Arcane Tradition* at reduced power (Effort −1); may be taken **twice** for two
  traditions (use the dual-partial spell table, p.64).

> **Class focus eligibility:** a *combat* focus is one usable in a fight (combat-tagged); a *non-combat*
> focus is the reverse. Some foci are usable as either — the GM rules in ambiguous cases.

---

## 5 · Mage traditions & magic-using partial classes (pp.60–97; 348–359)

**Shared:** Spells are ranked 1–5, prepared after rest, cast a limited number/day (Main Action, free
hand, vocalized; taking damage that round spoils the cast). **Arts** are Effort-fueled tradition powers
(committed for the scene / day / indefinitely). **Casting & most arts are barred in armor or with a
shield** unless the **Armored Magic** focus is taken — *except* the non-spellcasting classes noted below,
whose powers work while armored. **Full Mage knows 4 first-level spells at L1; Partial Mage knows 2;
dual-partial knows 4.**

### Full spellcasting traditions

| Tradition | Spell lists | Effort = | L1 free arts | L1 cast / prepare (full · partial) |
|---|---|---|---|---|
| **High Mage** | High Magic | Magic + better Int/Cha | 2 (1 partial); arts manipulate spells | 1/3 · 1/2 |
| **Elementalist** | High Magic + Elementalist | Magic + better Int/Cha | *Elemental Resilience* + *Elemental Sparks* + 1 chosen | 1/3 · 1/2 |
| **Necromancer** | High Magic + Necromancer | Magic + better Int/Cha | 1 chosen | 1/3 · 1/2 |
| **Adunic Invoker** | High Magic via **spell points** | — (no arts by default) | none | spell pts 1+Int / prep 2+Int (1+Int / 1+Int partial) |

- **High Mage:** the orthodox wizard; +2 new High Magic spells each level. No casting in armor.
- **Elementalist:** earth/fire/wind/water specialist; learns Elementalist New Magic (only this class can).
- **Necromancer:** death/undeath; widely outlawed and feared (social hazard, not a stat).
- **Adunic Invoker:** spell-point caster (repeats minor spells, no top-end arts). **Cannot mix with any
  other spellcasting partial.** Its unique **Traditional Education** focus is the only way it gains a
  tradition's arts (Effort = Magic skill, min 1).

### Non-spellcasting partial classes (arts/miracles only — **work while armored**)

| Class | Type | Effort = | L1 free | Notes |
|---|---|---|---|---|
| **Healer** | partial only | **Heal** + better Int/Cha (min 1) | *Healing Touch* + 1 | heal 2d6+Heal as Main Action (+1 Strain). Limb-restore/revive need L8+ |
| **Vowed** | partial only | **order's chosen skill** + **best** mod (min 1) | 3 free arts + 1 | monk: Martial Style, Unarmed Might (1d6→scaling), Unarmored Defense (AC 13+½ level) |
| **Darian Skinshifter** | Gyre, partial | **Survive** + Con/Cha | *Change Form* + 1 | masters 1 alt form/level; ≤3 arts per form |
| **Kistian Duelist** | Gyre, partial | **Stab** + Dex/Int | *Favored Weapon* + 1 | no arts in medium/heavy armor or large shield; Pw/Duelist uses **1d6 HD** (Flaw of Fragility) |
| **Llaigisan Beastmaster** | Gyre, partial | **Survive** + Wis/Cha | *Bind Companion* + 1 | one animal companion HD ≤ level+1; arts buff the bond |
| **Sarulite Blood Priest** | Gyre, partial | **Pray** + Wis/Cha | **2 miracles** | fighting-cleric; miracles need no gestures/free hand, just a prayer |
| **Vothite Thought Noble** | Gyre, partial | **Notice** + Int/Wis | *Open Mind* + 1 | psychic; gains a new art **every** level L1–10 |

> **Encoded vs. not:** `spells.json` holds **High Magic (52), Elementalist (15 + 12 arts), Necromancer
> (16 + 12 arts), Healer (14 arts), Vowed (16 arts)**. The **Adunic Invoker** and the **five other Gyre
> classes have no art data in the skill** — pull their miracles/arts from `11-Arts-of-the-Gyre.md`.

---

## 6 · Foci (pp.22–28) — all 33

Each focus has up to two levels; many grant a **bonus skill** (level-0, or +1 if already held; else any
non-Magic skill). The **free** focus is any kind; a Warrior/Partial Warrior adds a **combat** focus, an
Expert/Partial Expert a **non-combat** focus — both levels may stack on one focus (start at level 2).

| Focus | Bonus skill | Combat? | Level 1 → Level 2 |
|---|---|---|---|
| **Alert** | Notice | combat | Can't be surprised / no Execution on you; +1 side-init or roll init twice → always act first |
| **Armored Magic** | — | non-combat | Cast in armor Enc ≤2 (+shield if other hand free) → cast in any armor, hands full |
| **Armsmaster** | Stab | combat | Add Stab to melee/thrown dmg & Shock; Ready stowed as Instant → melee Shock treats AC 10; +1 hit |
| **Artisan** | Craft | non-combat | Craft +1 for mods, −1 salvage; craft any profession → first mod free Maintenance & half cost; auto-masterwork |
| **Assassin** | Sneak | combat | Conceal a knife; surprise point-blank can't miss → Move on the same round as an Execution Attack |
| **Authority** | Lead | non-combat | 1/day Cha/Lead vs Morale to compel a non-hostile NPC → followers gain Morale/hit/+1 checks |
| **Close Combatant** | Any Combat | combat | Ignore melee Shock; knife-throw in melee → melee Shock treats AC 10; free Fighting Withdrawal |
| **Connected** | Connect | non-combat | Web of contacts, 1 favor/day after a week → 1/session meet a useful acquaintance |
| **Cultured** | Connect | non-combat | Speak regional languages; 1 minor favor/day → 1/session reroll a failed social check |
| **Deadeye** | Shoot | combat | Add Shoot to ranged dmg; Ready ranged as Instant; bow-in-melee at −4 → reload as On Turn; auto-hit inanimate |
| **Dealmaker** | Trade | non-combat | Find any buyer/seller in ½ hour → 1/session compel a non-hostile to bargain |
| **Developed Attribute** | — | either | Chosen attribute's **modifier +1** (max +3). **Not for Mages.** (Repeatable for different attrs) |
| **Diplomatic Grace** | Convince | non-combat | Speak regional languages; reroll 1s on negotiation → 1/day magically bind a bargain (Mental save to break) |
| **Die Hard** | — | either | **+2 max HP/level**; auto-stabilize if Mortally Wounded → 1/day survive a killing blow at 1 HP |
| **Gifted Chirurgeon** | Heal | non-combat | Heal rolls 3d6 drop lowest; double first-aid HP → magical heal 1d6+Heal as Main Action (+1 Strain) |
| **Henchkeeper** | Lead | non-combat | Recruit loyal henchmen (1 per 3 levels) → henchmen fight as Veteran Soldiers |
| **Impervious Defense** | — | combat | **Innate AC 15 + ½ level** (no stack w/ armor) → 1/day shrug off one weapon attack |
| **Impostor** | Perform/Sneak | non-combat | 1/scene reroll a disguise check; one flawless false identity → 3 swappable appearances; new IDs per city |
| **Lucky** | — | either | **Needs an attr mod ≤ −1.** 1/week a lethal blow fails → 1/session roll 1d6 for a lucky break (1 = worse) |
| **Nullifier** | — | either | +2 saves vs magic (allies w/in 20'); sense magic; negate 1st failed save/day. **Not for Mages.** → 1/day full immunity |
| **Poisoner** | Heal | non-combat | Brew toxins (2d6+level, Phys save half); reroll saves vs poison → poison-immune; toxins as Execution Attack |
| **Polymath** | Any | non-combat | **Experts only.** Treat all non-combat skills as ≥ level-0 → as ≥ level-1 |
| **Rider** | Ride | either | Steeds Morale 12, use your AC, +50% travel → negate an attack on your steed; telepathic bond |
| **Shocking Assault** | Punch/Stab | combat | Melee Shock treats all targets as AC 10 → +2 Shock rating to melee/unarmed |
| **Sniper's Eye** | Shoot | combat | Ranged Execution/target checks roll 3d6 drop lowest → don't miss ranged Executions; −4 to target's save |
| **Special Origin** | — | either | Non-human origin (bestiary). GM permission. Mechanics per the chosen species |
| **Specialist** | Any non-Magic | non-combat | Chosen skill rolls 3d6 drop lowest → 4d6 drop two. Repeatable for different skills |
| **Spirit Familiar** | — | either | A loyal minor spirit (summon/dismiss as Main Action); refreshes 1 Effort/day → pick 2 upgrades (HP, attack, fly…) |
| **Trapmaster** | Notice | either | 1/scene reroll a trap check; improvise traps (1d6+2×level) → counts as *Extirpate Arcana* vs magical traps |
| **Unarmed Combatant** | Punch | combat | Unarmed scales: Punch-0 1d6 · -1 1d8 · -2 1d10 · -3 1d12 · -4 1d12+1; Shock = Punch vs AC15 → 1d6 even on a miss |
| **Unique Gift** | — | either | GM-defined special power (balanced with the GM) |
| **Valiant Defender** | Stab/Punch | combat | +2 Screen Ally; screen one extra attacker; screen vs spells/AoE → first Screen each round auto-succeeds; +2 AC |
| **Well Met** | — | non-combat | +1 reaction rolls while present; foes give a round to parley → 1/session a subject becomes maximally friendly |
| **Whirlwind Assault** | Stab | combat | 1/scene apply Shock to all foes in melee range → on a kill, gain a second attack |
| **Xenoblooded** | — | either | Pick one alien adaptation (heat immunity / water-breathing / gravity build / no-eat-sleep-breathe) → — |

---

## 7 · Equipment packages (p.29)

Pick a package, **or** roll **3d6 × 10** starting silver and buy individually.

| Package | Armor | Shield | Weapons | Cash |
|---|---|---|---|---|
| **Adventuring Peasant** | War Shirt (AC 11) | Large (14) | Light Spear, Dagger | + mule & cart |
| **Ranger or Archer** | Buff Coat (AC 12) | — | Large Bow, 20 arrows, Dagger, Hand Axe | 20 sp |
| **Armored Warrior** | Pieced Armor (AC 14) | Large (+1) | Short Sword, Dagger | — |
| **Gentry Wayfarer** | Buff Coat (AC 12) | Small (13) | Short Sword | 20 sp |
| **Mage / Healer / Scholar** | Buff Coat (AC 12) | Small (13) | Short Sword, 5 Throwing Blades | — |
| **Roguish Wanderer** | none (AC 10) | — | 2 Daggers, Staff | 80 sp |

Each package also lists a backpack, rations, light source, etc. — see the book/`chargen.py` output.

---

## 8 · Final touches checklist (pp.28–29)

- [ ] **Free skill** — one more skill at level-0 (or +1 if already 0).
- [ ] **HP** — class die + Con mod, min 1 (+ Die Hard if taken).
- [ ] **AC** — armor + Dex (+shield).
- [ ] **Attack bonus** — from class table; compute each weapon's hit & damage lines.
- [ ] **Saves** — Physical / Evasion / Mental / Luck (16 − level − mod).
- [ ] **Effort & spells** (casters) — Effort by tradition; pick starting spells/arts.
- [ ] **System Strain** 0 / Con · **Initiative** 1d8 + Dex.
- [ ] **Languages** — native + Trade Cant + Connect/Know bonuses.
- [ ] **Gear** — package or rolled silver.
- [ ] **Name, goal, ties** — an active goal worth dying for, and a reason to trust the party.

---

*Reproduced from Worlds Without Number Deluxe / The Atlas of the Latter Earth for personal solo play;
not for redistribution. Verbatim spell/focus text: `scripts/lookup.py`. Automated build: `scripts/chargen.py`.*
