# Worlds Without Number — Character Creation Compendium

> A single-file reference for rolling up a WWN PC in the Latter Earth: the dice rules,
> the full creation procedure, every skill, every background, every class (core + Heroic
> + Atlas optional), every Focus, and every mage tradition.
>
> Sources: `book/Worlds-Without-Number-Deluxe/02-Character-Creation.md`,
> `05-Magic.md`, `12-Heroic-Classes.md`; `book/The-Atlas-of-the-Latter-Earth/04-Optional-Rules-and-Classes.md`;
> the skill references and `bridge/generators/foci.json`.
> Pull anything verbatim with `python3 .claude/skills/wwn/scripts/lookup.py focus|spell|monster <name>`.

---

## 1. Rules for Rolling

**Every die is rolled through the scripts and shown — never invent a number.**
`python3 .claude/skills/mythic-gm/scripts/dice.py roll <NdM±K>` for an ad-hoc roll;
`python3 .claude/skills/wwn/scripts/check.py …` for a resolved PC action;
`python3 .claude/skills/wwn/scripts/chargen.py …` to build/validate a whole sheet.

### Attributes
- **Roll 3d6 six times in order:** Strength, Dexterity, Constitution, Intelligence, Wisdom, Charisma.
- **After rolling you may set ONE score to 14** (your hero is unusually good at *something*).
- **OR** take the array **14, 12, 11, 10, 9, 7** assigned freely — but then you get **no free 14**.
- Clement GMs may let rolled scores be assigned in any order instead of strictly in order.

| Score | 3 | 4–7 | 8–13 | 14–17 | 18 |
|---|---|---|---|---|---|
| **Modifier** | −2 | −1 | 0 | +1 | +2 |

| Attribute | Governs |
|---|---|
| **Strength** | Lifting, breaking, melee combat, carrying gear |
| **Dexterity** | Speed, evasion, manual dexterity, reaction time, initiative |
| **Constitution** | Hardiness, enduring injury, resisting poison, privation |
| **Intelligence** | Memory, reasoning, intellectual skills, education |
| **Wisdom** | Noticing things, judgment, reading situations, intuition |
| **Charisma** | Force of character, charm, attention, loyalty |

### Skill checks
- **`2d6 + skill level + relevant attribute modifier`** vs a difficulty. **No skill at all → −1** to the roll (some esoteric tasks can't be attempted untrained).
- Difficulty ladder: **6** routine · **8** tricky · **10** hard · **12** very hard · **14** legendary.
- **Opposed check:** higher total wins; **ties go to the PC**.
- Skill levels: **0** ordinary practitioner · **1** veteran · **2** best in the city · **3** best in the kingdom · **4** best in the world. Novices cap at **level-1**.

### Saving throws
- **Roll 1d20; success = result ≥ target.** Higher is better.
- **PC target = 16 − character level − best relevant attribute modifier.** (At level 1 this is **15 − mod**.)
  - **Physical** — best of Str/Con (poison, disease, exhaustion, bodily transformation)
  - **Evasion** — best of Int/Dex (blasts, pits, hurled perils, reaction-speed dangers)
  - **Mental** — best of Wis/Cha (mind magic, illusions, willpower)
  - **Luck** — **no attribute**, target = **16 − level** (blind fortune)
- **Monsters/NPCs:** one save = **15 − ½ HD** (round down).

### Attack & damage
- **Hit roll: `1d20 + class attack bonus + combat-skill level (Stab/Shoot/Punch) + attribute modifier`** vs target **Armor Class** (ascending). Untrained weapon = **−2**.
  - *The class attack bonus already encodes martial aptitude — a Warrior's +1…+10 equals their level. Do **not** add level again on top.*
  - Weapon attribute: use the weapon's listed stat; if two are listed, use the better.
- **Damage: weapon die + attribute modifier (+ magic/Focus).** Punch weapons also add Punch skill.
- **Shock (N/AC):** on a **miss** against a target whose **AC ≤ the listed value**, still deal **N** damage (+ attribute & magic, *not* other damage bonuses). A hit never deals less than its Shock. Shields negate the **first** Shock each round.
- **0 HP:** unnamed NPC dies; PC / named NPC is **Mortally Wounded** (stabilize within rounds or die). Non-lethal intent → unconscious, revives at 1 HP in 10 min.
- **Initiative:** `1d8 + Dex modifier` (by side; PCs win ties).

### Hit points, Strain, Effort
- **Max HP = class hit die + Constitution modifier, minimum 1.** (Warrior **1d6+2**, Expert **1d6**, Mage **1d6−1**, per level; *Die Hard* adds +2/level.)
- **System Strain:** current 0, **maximum = Constitution score**.
- **Effort (casters):** see §7. Baseline = **1 + Magic-skill level + better of Int/Cha modifier**.

### Starting languages
Native tongue + **Trade Cant** + extra languages by social skill: **level-0 in Connect or Know → +1 language each; level-1 → +2 each.**

---

## 2. The Creation Procedure (in order)

1. **Attributes** — roll 3d6 in order (or take the array); set one to 14 if you rolled; note modifiers.
2. **Background** (roll d20 or pick) — gain its **free skill** at level-0, then choose ONE:
   - take the listed **Quick Skills** (level-0), **or**
   - **pick two** skills from the Learning table (not "Any Skill"), **or**
   - **roll three times**, split as you like across the **Growth** and **Learning** tables (the only route to attribute bumps or a third skill).
   - *Stacking:* 1st pick = level-0, 2nd = level-1, 3rd of the same = pick any other skill below level-1. **No novice skill above level-1.** "+2 Physical" = +2 to one of Str/Dex/Con (or +1 to two); "+2 Mental" likewise for Int/Wis/Cha. "+1 Any Stat" = +1 to any one attribute (max 18).
3. **Class** — Warrior / Expert / Mage, or **Adventurer** (two partial classes). Sets hit die, attack bonus, and Focus picks. Mages/Partial Mages pick a **tradition** (§7).
4. **Foci** — every PC gets **1 free Focus** (any kind). A **Warrior/Partial Warrior** adds **1 combat** Focus; an **Expert/Partial Expert** adds **1 non-combat** Focus. (Both of a class's picks may stack on one Focus → start it at level 2.) Many Foci grant a bonus skill (level-0, or level-1 if already 0; if already 1, pick any non-Magic skill).
5. **Final touches:**
   - **Free skill:** pick one more skill at level-0.
   - **Hit points:** roll the class die + Con mod (min 1).
   - **Saving throws:** record all four (§1).
   - **Base attack bonus:** from the class table.
   - **Mages:** choose starting spells — full Mage **4**, Partial Mage **2**, dual-Partial-Mage **4** — from a 1st-level list available to your tradition; record Arts (§7).
   - **Languages:** native + Trade Cant + by Connect/Know.
   - **Armor Class, weapons, Shock, damage, Initiative, System Strain.**
6. **Equipment** — pick a package (§8) *or* roll **3d6 × 10** starting silver and buy gear.
7. **Name, goal, ties** — every hero needs an **active goal** worth risking death for and a reason to trust the party.

---

## 3. Skills (the 21)

| Skill | Use |
|---|---|
| **Administer** | Run an organization, scribe, logistics, spot incompetence/treachery, analyze records |
| **Connect** | Find/know useful people, make ties, call on organizations' help |
| **Convince** | Persuade a listener something is true |
| **Craft** | Make/repair goods & technology appropriate to your background |
| **Exert** | Run, swim, climb, jump, labor, throw — physical exertion |
| **Heal** | Treat wounds, cure disease, neutralize poison, stabilize the Mortally Wounded |
| **Know** | History, geography, natural science, scholarship |
| **Lead** | Inspire followers, manage subordinates, keep morale |
| **Magic** | Cast/analyze magic; know mages & magical events (non-casters get only scholarly benefit) |
| **Notice** | Spot details, ambushes, hidden things; read emotional state |
| **Perform** | Sing, act, dance, orate; compose |
| **Pray** | Religious rites; know gods, demons, taboos, hierarchies |
| **Punch** | Unarmed/natural-weapon fighting (non-lethal by default) |
| **Ride** | Ride animals, drive carts, tend mounts |
| **Sail** | Sail/repair ships, navigate, manage sailors |
| **Shoot** | Bows, crossbows, hurled weapons; maintenance/fletching |
| **Sneak** | Move silently, hide, pick pockets/locks, disguise, defeat traps |
| **Stab** | Melee weapons (and thrown); maintain/identify weaponry |
| **Survive** | Hunt, fish, navigate, mitigate hazards, shelter |
| **Trade** | Buy/sell at profit, appraise, black markets, smuggling law |
| **Work** | Catch-all profession skill (painter, lawyer, farmer, herdsman…) |

Combat skills = **Stab, Shoot, Punch**. All others are non-combat.

---

## 4. Backgrounds (the 20)

Each gives a **Free skill** (level-0). Then choose Quick Skills, two Learning picks, or three Growth/Learning rolls.
**"Any Combat"** = Stab/Shoot/Punch; **"Any Skill"** = any skill (can't be a Learning *pick*, only a roll).

| d20 | Background | Free | Quick Skills |
|---|---|---|---|
| 1 | **Artisan** (smith, tanner, carpenter) | Craft | Trade, Connect |
| 2 | **Barbarian** (savage, wild man) | Survive | Any Combat, Notice |
| 3 | **Carter** (hauler, post-rider) | Ride | Connect, Any Combat |
| 4 | **Courtesan** (companion, artist) | Perform | Notice, Connect |
| 5 | **Criminal** (thief, con man, burglar) | Sneak | Connect, Convince |
| 6 | **Hunter** (trapper, recluse) | Shoot | Survive, Sneak |
| 7 | **Laborer** (urban worker) | Work | Connect, Exert |
| 8 | **Merchant** (trader, peddler) | Trade | Convince, Connect |
| 9 | **Noble** (exile, black sheep) | Lead | Connect, Administer |
| 10 | **Nomad** (raider, wanderer) | Ride | Survive, Any Combat |
| 11 | **Peasant** (farmer, serf) | Exert | Sneak, Survive |
| 12 | **Performer** (bard, dancer) | Perform | Convince, Connect |
| 13 | **Physician** (healer, healer-monk) | Heal | Know, Notice |
| 14 | **Priest** (monk, holy hermit) | Pray | Convince, Know |
| 15 | **Sailor** (bargeman, fisher, pirate) | Sail | Exert, Notice |
| 16 | **Scholar** (sage, apprentice mage) | Know | Heal, Administer |
| 17 | **Slave** (indentured, runaway) | Sneak | Survive, Exert |
| 18 | **Soldier** (mercenary, guardsman) | Any Combat | Exert, Survive |
| 19 | **Thug** (ruffian, bandit, enforcer) | Any Combat | Convince, Connect |
| 20 | **Wanderer** (exile, explorer) | Survive | Sneak, Notice |

### Growth (d6) and Learning (d8) tables

| Background | d6 Growth | d8 Learning |
|---|---|---|
| **Artisan** | +1 Any, +2 Phys, +2 Phys, +2 Mental, Exert, Any Skill | Connect, Convince, Craft, Craft, Exert, Know, Notice, Trade |
| **Barbarian** | +1 Any, +2 Phys, +2 Phys, +2 Mental, Exert, Any Skill | Any Combat, Connect, Exert, Lead, Notice, Punch, Sneak, Survive |
| **Carter** | +1 Any, +2 Phys, +2 Phys, +2 Mental, Connect, Any Skill | Any Combat, Connect, Craft, Exert, Notice, Ride, Survive, Trade |
| **Courtesan** | +1 Any, +2 Mental, +2 Mental, +2 Phys, Connect, Any Skill | Any Combat, Connect, Convince, Exert, Notice, Perform, Survive, Trade |
| **Criminal** | +1 Any, +2 Mental, +2 Phys, +2 Mental, Connect, Any Skill | Administer, Any Combat, Connect, Convince, Exert, Notice, Sneak, Trade |
| **Hunter** | +1 Any, +2 Phys, +2 Phys, +2 Mental, Exert, Any Skill | Any Combat, Exert, Heal, Notice, Ride, Shoot, Sneak, Survive |
| **Laborer** | +1 Any, +1 Any, +1 Any, +1 Any, Exert, Any Skill | Administer, Any Skill, Connect, Convince, Craft, Exert, Ride, Work |
| **Merchant** | +1 Any, +2 Mental, +2 Mental, +2 Mental, Connect, Any Skill | Administer, Any Combat, Connect, Convince, Craft, Know, Notice, Trade |
| **Noble** | +1 Any, +2 Mental, +2 Mental, +2 Mental, Connect, Any Skill | Administer, Any Combat, Connect, Convince, Know, Lead, Notice, Ride |
| **Nomad** | +1 Any, +2 Phys, +2 Phys, +2 Mental, Exert, Any Skill | Any Combat, Connect, Exert, Lead, Notice, Ride, Survive, Trade |
| **Peasant** | +1 Any, +2 Phys, +2 Phys, +2 Phys, Exert, Any Skill | Connect, Exert, Craft, Notice, Sneak, Survive, Trade, Work |
| **Performer** | +1 Any, +2 Mental, +2 Phys, +2 Phys, Connect, Any Skill | Any Combat, Connect, Exert, Notice, Perform, Perform, Sneak, Convince |
| **Physician** | +1 Any, +2 Phys, +2 Mental, +2 Mental, Connect, Any Skill | Administer, Connect, Craft, Heal, Know, Notice, Convince, Trade |
| **Priest** | +1 Any, +2 Mental, +2 Phys, +2 Mental, Connect, Any Skill | Administer, Connect, Know, Lead, Heal, Convince, Pray, Pray |
| **Sailor** | +1 Any, +2 Phys, +2 Phys, +2 Mental, Exert, Any Skill | Any Combat, Connect, Craft, Exert, Heal, Notice, Perform, Sail |
| **Scholar** | +1 Any, +2 Mental, +2 Mental, +2 Mental, Connect, Any Skill | Administer, Heal, Craft, Know, Notice, Perform, Pray, Convince |
| **Slave** | +1 Any, +2 Phys, +2 Phys, +2 Mental, Exert, Any Skill | Administer, Any Combat, Any Skill, Convince, Exert, Sneak, Survive, Work |
| **Soldier** | +1 Any, +2 Phys, +2 Phys, +2 Phys, Exert, Any Skill | Any Combat, Any Combat, Exert, Lead, Notice, Ride, Sneak, Survive |
| **Thug** | +1 Any, +2 Mental, +2 Phys, +2 Phys, Connect, Any Skill | Any Combat, Any Combat, Connect, Convince, Exert, Notice, Sneak, Survive |
| **Wanderer** | +1 Any, +2 Phys, +2 Phys, +2 Mental, Exert, Any Skill | Any Combat, Connect, Notice, Perform, Ride, Sneak, Survive, Work |

---

## 5. Classes

A class sets your **hit die**, **attack bonus**, **Focus picks**, and signature ability. Pick the tools you want, not what "fits" the background. **Adventurers** pick two partial classes.

### Core classes — level 1

| Class | Hit die | Attack bonus | Foci at L1 | Signature ability |
|---|---|---|---|---|
| **Warrior** | 1d6+2 | +1 | 1 combat + 1 any | **Veteran's Luck** (1/scene turn a miss→hit or a hit-on-you→miss); **Killing Blow** (+½ level rounded up to damage *and* Shock) |
| **Expert** | 1d6 | +0 | 1 non-combat + 1 any | **Masterful Expertise** (1/scene reroll a non-combat check, Instant); **Quick Learner** (extra non-combat/attribute skill point per level) |
| **Mage** | 1d6−1 | +0 | 1 any | **Arcane Tradition** (full caster — pick a tradition) |
| **Adventurer** | — | — | varies | two partials (see below) — never the full class's strongest ability, but an extra Focus at L1 |

### Adventurer partial combinations — level 1

| Combo | Hit die | Attack bonus | Foci at L1 | Notes |
|---|---|---|---|---|
| **Partial Expert / Partial Warrior** | 1d6+2 | +1 | 1 Expert + 1 Warrior + 1 any | Quick Learner only (no Masterful Expertise / Veteran's Luck / Killing Blow) |
| **Partial Expert / Partial Mage** | 1d6 | +0 | 1 Expert + 1 any | Quick Learner; partial caster (2 spells) |
| **Partial Mage / Partial Warrior** | 1d6+2 | +1 | 1 Warrior + 1 any | partial caster; improved HD/attack (no Veteran's Luck/Killing Blow) |
| **Partial Mage / Partial Mage** | 1d6−1 | +0 | 1 any (Free) | two partial traditions, two Effort pools (4 spells; uses the dual-caster table) |

*Partial Healer and Partial Vowed are non-spellcasting Mage partials — combine them with another partial (e.g. Partial Warrior/Partial Healer = combat medic; Partial Warrior/Partial Vowed = warrior-monk). See §7.*

### Attack-bonus progression (levels 1–10)

| Class | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| Warrior | +1 | +2 | +3 | +4 | +5 | +6 | +7 | +8 | +9 | +10 |
| Expert | +0 | +1 | +1 | +2 | +2 | +3 | +3 | +4 | +4 | +5 |
| Mage / Pm-Pm | +0 | +0 | +0 | +0 | +1 | +1 | +1 | +1 | +1 | +2 |
| Pe/Pw & Pm/Pw | +1 | +2 | +2 | +3 | +4 | +5 | +5 | +6 | +6 | +7 |
| Pe/Pm | +0 | +1 | +1 | +2 | +2 | +3 | +3 | +4 | +4 | +5 |

Hit dice scale per level (e.g. L3 Warrior = 3d6+6). **Foci picks** are gained at **levels 1, 2, 5, 7, and 10** (plus the class's bonus L1 combat/non-combat pick for Warrior/Expert).

### Heroic classes (optional high-fantasy tone, ch. 12)

Used from campaign start for larger-than-life heroes. All Heroic PCs also get **Heroic Resilience** (+12 max HP), **Heroic Reflexes** (always win initiative unless ambushed), and **Heroic Determination** (1/scene accept 1 Strain to heal 1d8 + level, even from Mortally Wounded).

- **Heroic Warrior** — full Warrior + **Slayer** (auto-hit anything with HD ≤ your level), **Unbroken** (1/day negate a 0-HP/hostile-magic effect, drop to 1 HP), **Heroic Warrior's Fray** (1/round On Turn, 1d8 + level to one weaker target in reach).
- **Heroic Expert** — full Expert (Quick Learner) but **Legendary Expertise** replaces Masterful Expertise (1/scene auto-succeed a non-combat check ≤ 12, or reroll an opposed check), plus **Heroic Skill** (set one non-combat/non-Magic skill to level-4) and **Heroic Expert's Fray** (1d8 + ½ level to a weaker target in reach).
- **Heroic Mage** — three partial casters, or one full + one partial (all spellcasting); uses the Heroic Mage spell table; **Heroic Mage's Fray** (1/round, 1d4 + ½ level to any target within 60 ft).
- **Heroic Adventurer** — one full + one partial, or three partials; free bonus Focus; picks one Fray ability matching a class it has.

### Atlas optional classes (ch. 4)

All four are **partial classes** taken by an Adventurer alongside a second partial. Their arts are **non-magical / pact-based and work in armor** (except where noted), and don't count as magic for dispel/detect. `chargen.py` builds them all — e.g. `--class "partial-warrior/accursed"`, `"partial-expert/bard"`, `"necromancer/accursed"`, `"partial-warrior/mageslayer"`, `"partial-expert/wise"`.

**The Accursed** — pacted with an Outsider; a **partial Mage** class. Gains **Magic-0**. **Effort = Magic + better Int/Cha** (min 1). At L1 take **Accursed Blade or Accursed Bolt + one more art**. *Foci like Armsmaster/Deadeye read "Magic" for the Blade/Bolt.* HD/attack: Warrior pairing 1d6+2 / partial-warrior AB; Expert 1d6 / Pe-Pm AB; Mage 1d6−1 / Mage AB.
- **Blade** (On Turn): 1d8 one-hand or 2d6 two-hand, + Magic to damage, Shock 2/15, attack with Magic + best of Str/Dex/Int/Cha. **Bolt**: as Blade but 200' ranged (1d8 + Magic).
- Arts: Bewitching Distraction · Compelling Shriek · Devil's Bargain · Dire Pact · Lying Face · Night-Black Eyes · Pacted Protection · Rob Vitality · Scourging Curse · Shadowed Steps · Snaring Speech · Sorcerous Battery · Soul Consumption · Tendrils of Night · Unseen Steps · Weight of Sin · Weeping Wounds.

**The Bard** — Legacy-charged performer; a **partial Expert** variant (no Quick Learner / bonus Expert focus from the Bard side). Gains **Perform-0**. **Effort = Perform + Cha** (min 1). Auto **A Thousand Tongues** + 1 art. HD/attack: Warrior 1d6+2 / partial-warrior AB; Expert or Mage 1d6 / Pe-Pm AB.
- Arts: Battle Cry · Cursed Tune · Deft Fingers · Entangle Incantation · Evoke Emotion · Inspire Dread · Keen Senses · Liberating Song · Rally · Soothe the Savage · Soothing Graces · Swift Misdirection.

**The Mageslayer** — mage-killer; a **partial Warrior** variant (no +2 HP/die or bonus combat focus from the Mageslayer side; **no Mage pairing allowed**). Gains **Magic-0**. **Effort = Magic + best of Int/Con** (min 1). **Fixed art progression:** Antimage + Magebane (L1), Witchfinder + Spellshield (L2), Disrupt Sorcery (L3), Know Your Prey (L4), Share the Pain (L5), Dispel Enchantment (L6), Ward Ally (L7), Immaculate Body (L8), Immaculate Mind (L9), Absolute Negation (L10). HD/attack: Partial Warrior/Mageslayer 1d6+2 / **full-Warrior AB**; Partial Expert/Mageslayer 1d6 / partial-warrior AB.

**The Wise** — low/no-magic priest, witch, or seer; a **partial Expert** variant (no Quick Learner / bonus Expert focus from the Wise side). Gains a **concept skill** (Pray/Know/Survive…). **No Effort** — arts are always-on or limited-use. Picks arts by concept from three lists. HD/attack as a partial Expert.
- **General:** Dread Awe · Elite Ties · Erudite · Folk-Friend · Healer · Holy Sanctity · Personal Impunity · Skilled.
- **Divination:** Compel Truth · Deliver Oracle · Find Object · Read Omens.
- **Curses & Blessings:** Auspicious Undertaking · Evil Eye · Ill Fate · Luck Blessing · War Curse.

---

## 6. Foci

Every Focus has two levels (take it once for L1, again for L2). Many grant a **bonus skill**. Combat Foci can satisfy a Warrior pick; non-combat Foci an Expert pick (GM rules ambiguous cases).

| Focus | Req. | Level 1 | Level 2 |
|---|---|---|---|
| **Alert** | — | Gain Notice. Can't be surprised or hit by Execution Attacks; +1 side initiative (or roll individual init twice). | Always act first unless another is equally Alert. |
| **Armored Magic** | Mage/Partial Mage | Cast/use arts in armor of Enc ≤ 2; shield OK if a hand is free. | Cast in any armor, even with both hands full. |
| **Armsmaster** | — | Gain Stab. Ready stowed melee/thrown as Instant; add Stab to melee/thrown damage or Shock. | Melee Shock treats targets as AC 10; +1 to hit thrown/melee. |
| **Artisan** | — | Gain Craft. Craft counts +1 (max 5) for mods; mods cost 1 less salvage; craft any profession's wares. | First mod free of Maintenance & half-cost; auto-succeed masterwork; monthly extra salvage cut. |
| **Assassin** | — | Gain Sneak. Conceal & draw a knife On Turn; surprise point-blank attacks can't miss. | Move on the same round as an Execution Attack, splittable, without alerting the victim. |
| **Authority** | — | Gain Lead. 1/day Cha/Lead vs an NPC's Morale to compel a not-harmful request. | Led NPCs gain +Lead to Morale/hit and +1 skill checks; followers won't betray you. |
| **Close Combatant** | — | Gain any combat skill. Use knife-thrown in melee; ignore melee Shock (disrupts your casting that round). | Melee Shock treats all targets as AC 10; Fighting Withdrawal is a free On Turn action. |
| **Connected** | — | Gain Connect. After a week somewhere, contacts for mildly-illegal favors — 1/game day. | 1/session, plausibly run into someone you know for a modest favor. |
| **Cultured** | — | Gain Connect. Speak all regional languages; learn one in a week; 1/day a minor no-cost favor. | 1/session, reroll a failed social check. |
| **Deadeye** | — | Gain Shoot. Ready stowed ranged as Instant; use a bow in melee at −4; add Shoot to ranged damage. | Reload slow weapons On Turn; ranged in melee freely; 1/scene auto-hit an inanimate target. |
| **Dealmaker** | — | Gain Trade. In half an hour find any buyer/seller in the community, legal or not. | 1/session, get a non-hostile sentient to deal for a price or favor. |
| **Developed Attribute** | Not Mage/Partial Mage | Raise one attribute's **modifier** by +1 (max +3); score unchanged. Repeatable for different attributes. | *(no L2 — repeatable instead)* |
| **Diplomatic Grace** | — | Gain Convince. Speak regional languages; reroll 1s on negotiation/diplomacy dice. | 1/day consecrate a bargain; the other must Mental save to break it. |
| **Die Hard** | — | +2 max HP per level (retroactive); auto-stabilize when Mortally Wounded unless torn apart. | 1/day, the first injury that would drop you to 0 HP leaves you at 1 HP. |
| **Gifted Chirurgeon** | — | Gain Heal. Stabilize one adjacent Mortally Wounded/round On Turn; Heal checks 3d6-drop-lowest; double post-battle first aid. | Healing counts as magical: heal 1d6 + Heal to an adjacent ally as a Main action (+1 Strain), no Frailty. |
| **Henchkeeper** | — | Gain Lead. Recruit loyal henchmen (1 per 3 levels); they escort/risk danger but won't fight except to survive. | Henchmen fight as Veteran Soldiers; capable NPCs can become henchmen if you've earned it. |
| **Impervious Defense** | — | Innate AC = **15 + half level** (round up); doesn't stack with armor, but Dex/shield apply. | 1/day, Instant, shrug off a single weapon attack or physical trauma (not environmental/falling). |
| **Impostor** | — | Gain Perform or Sneak. 1/scene reroll a disguise check; one flawless minor false identity. | Swap among three appearances with a Main action; new false identity per community. |
| **Lucky** | An attribute mod ≤ −1 | 1/week a killing/disabling blow simply fails; roll games of chance twice, take the better. | 1/session in peril, roll 1d6: 2+ something fortunate; 1 things get much worse. |
| **Nullifier** | Not Mage/Partial Mage | You + allies within 20' get +2 saves vs magic; sense magic On Turn; first failed save vs magic/day becomes a success. | 1/day, Instant, be unaffected by an unwanted magical/monstrous effect, even one with no save. |
| **Poisoner** | — | Gain Heal. Reroll failed saves vs poison; brew toxins (1 dose/level) for 2d6 + level, Physical save half. | Immune to poison; universal antidote; −Heal to detect/save vs your poisons; ingested = Execution Attack. |
| **Polymath** | Expert/Partial Expert | Gain any one skill. Treat all non-combat skills as ≥ level-0 for checks. | Treat all non-combat skills as ≥ level-1. |
| **Rider** | — | Gain Ride. Steeds count as Morale 12, use your AC if better, travel +50%/day; intuitively communicate. | 1/scene negate an attack on your steed; reroll a Ride check; telepathic link with a bonded steed within 200'. |
| **Shocking Assault** | — | Gain Punch or Stab. Your weapon's Shock treats all targets as AC 10 (if it can harm them). | +2 to the Shock rating of all melee/unarmed attacks that do Shock. |
| **Sniper's Eye** | — | Gain Shoot. On a ranged Execution/target-shoot, roll 3d6-drop-lowest. | Don't miss ranged Execution Attacks; target takes −4 on the Physical save and double damage even on a success. |
| **Special Origin** | GM permission | Take a species origin Focus (bestiary) to play a non-human kind, gaining its listed benefits. | *(varies by origin)* |
| **Specialist** | — | Gain any skill (not Magic/Stab/Shoot/Punch). Roll 3d6-drop-lowest for it. Repeatable for other skills. | Roll 4d6-drop-two-lowest for that skill. |
| **Spirit Familiar** | — | A loyal familiar (cat- to human-sized) with Evoked Servitor stats, summon/dismiss as a Main action; 1/day refresh one Committed Effort. | Pick two upgrades (extra HP, an attack, a skill, a second shape, flight, or speech). Repeatable. |
| **Trapmaster** | — | Gain Notice. 1/scene reroll a trap save/check; improvise a trap (non-lethal lose-a-round or 1d6 + 2× level) in 5 min. | 1/scene, your efforts count as Extirpate Arcana (as a Mage of 2× your level) vs a magical trap. |
| **Unarmed Combatant** | — | Gain Punch. Unarmed damage scales (1d6 @ L0 → 1d12+1 @ L4); Shock = Punch skill vs AC 15; bind ranged-weapon foes. | Even on a missed Punch, deal an unmodified 1d6 plus any Shock. |
| **Unique Gift** | GM agreement | A catch-all special power defined with the GM, worth one Focus pick; revisable. | *(as agreed)* |
| **Valiant Defender** | — | Gain Stab or Punch. +2 Screen Ally; screen one more attacker; 1/round screen even spells/area effects. | First Screen Ally each round auto-succeeds; +2 AC while screening; screen ogre-/ox-sized foes. |
| **Well Met** | — | +1 reaction rolls while present; even hostiles usually grant a round of parley. Works once per target. | 1/session, make a subject as friendly/helpful as plausibly possible on a reaction roll. |
| **Whirlwind Assault** | — | Gain Stab. 1/scene, On Turn, apply your Shock to all foes in melee range susceptible to it. | First time you kill someone in a round with a normal attack, instantly gain a second attack. |
| **Xenoblooded** | GM permission | Pick one alien-heritage benefit (heat/smoke immunity; water-adaptation; gravity attribute shift; or no food/sleep/air + see in the dark). | *(single heritage benefit — no L2)* |

### Atlas optional & setting Foci (ch. 4)

All selectable in `chargen.py` and via `lookup.py focus <name>`. Each `Level 1 // Level 2`.

**Mundane Alchemy** *(Experts/Partial Experts only)*

| Focus | Level 1 // Level 2 |
|---|---|
| **Mundane Alchemist** | Gain Alchemy-0 (only this Focus raises Alchemy); all lesser-work formulae; jury-rig a lesser lab. // All greater-work formulae; a week of lab work yields level×25 sp of components. |

**Maqqatban Knight styles** *(Warriors/Partial Warriors only; only ONE style ever)*

| Style | Level 1 // Level 2 |
|---|---|
| **Ghost Archer** | Gain Shoot; manifest spirit-copies of bows you've fired (no enc, self-ammo, fire in melee); −4 with non-bows. // 1/scene teleport to where your arrow lands (+1 Strain). |
| **All Directions Edge** | Hit die −2/level. Gain a combat skill; On Turn extra non-grappling attack 1/round (extra/day cost 1 Strain). // 1/day attack every enemy in range. |
| **One Point Strike** | Gain a combat skill; attacks use better of Int/Wis; Main Action auto-15-to-hit but minimum damage. // 1/scene maximize a melee hit (Instant). |
| **Pyre of Heaven** | Gain a combat skill; ignore first 5 fire/heat dmg; ignite weapon for +level+2 dmg & Shock (1 Strain, once/foe/scene). // Fire/smoke immunity; full-body ignite; first ignite/scene burns melee foes 1d6 per 3 levels. |
| **Catalytic Soul** | Gain Shoot; ranged attacks pass through allies; route a melee ally's Shock onto your target (no-Shock ranged only). // Boosted hit can heal you or the ally 2d6+target level (1 Strain). |
| **Wrathful Mountain** | Gain Stab/Punch; manifest a 0-enc magic large shield; 1/round Instant retaliation vs meleers of a Screened ally. // Retaliate vs ranged attackers too; 1 Strain to hit all attackers of your ward. |
| **Righteous Iron** | Gain Exert; worn armor +1 AC, no enc, no Sneak/Exert penalty, sleep in it; free 750sp armor at L1. // Armored: no need to eat/drink/sleep/breathe, climate-immune; AC bonus +2. Heavy armor only. |
| **World Tree Lance** | Gain Stab; spear 0 enc, returns when thrown, +1 hit/dmg & magic. // Reach 10'+level; allies don't block. Spears/polearms only. |

**Amundi Godblood Foci** *(Experts only; only ONE; the +1 modifier caps at +2)*

| Focus | Level 1 // Level 2 |
|---|---|
| **Master Tracker** | Gain Survive; follow any trail (1 day city / 1 week wild), read numbers & condition. // +1 Wis; ID people by tracks; reconstruct a recent scene. |
| **Night Walker** | Gain Sneak; see in all but pitch black; sleep as wakefulness. // +1 Dex; invisible in dim light until you act. |
| **Danger Sense** | Gain Notice; sense Execution Attacks; 1/day avert a trap/ambush. // +1 Wis; 1/day intuit the best escape from peril. |
| **Pack Beast** | Gain Exert; Str counts as 18 (22 if already 18) for encumbrance. // +1 Str; 1/scene carry up to 1000 lb briefly. |
| **Folie à Deux** | Gain Convince; lies read as sincere to magic; 1/day be believed sincere. // +1 Cha; 1/day a bald-faced lie forces a Mental save (−Convince). |
| **Provident Crafter** | Gain Craft; Str +4 for enc; needed items count as Readied. // +1 Dex; 1/day "happen to have" a Stowed item (pay cost). |
| **Wildtongue** | Gain Survive; talk with animals (minor favors). // +1 Cha; 1/day command an animal for a scene. |
| **Walk Like Wind** | Gain Exert; +10' move; move on vertical surfaces. // +1 Dex; leap 20'/10'; 1/scene bonus Move. |

**Arcane Secret Foci** *(Mages/Partial Mages only; only ONE; single level)*

| Focus | Effect |
|---|---|
| **Atlantean Divination** | Gain Know; 1/day ritual asks a one-sentence question about the next week (Int/Know vs 9; +1 Strain). |
| **Iteral Pacting** | Gain Pray; pick a patron portfolio; 1/day (+1 Strain) +4 hit, or +1 skill, or cast a related 1st-level spell w/o a slot; −1 social. |
| **Nagadi Hemomancy** | Gain Heal; 1/day after a helpful spell, take 1d4/spell-level so it doesn't count against daily casts (+1 Strain). |
| **Old Empire Sigilism** | Embed a spell in a personal token (10 min/level + a slot); cast w/o vocal/gesture, undisruptable; one token at a time. |
| **Vothite Mind-Sorcery** | Cast w/o vocal/gesture (still Main Action/armor-limited); spells untraceable to you — but you can't deal non-mental HP damage. |

**Non-Human Origin Foci** *(GM permission; usually the free/any pick; modifiers cap at ±2 — the GM applies them)*

Choeru Beastfolk (capybara: Convince/Connect, +1 Cha, +reaction) · Ghoul (Sneak, +1 Str/Dex, must eat flesh) · !Man (algorithmic: any skill, mind-immune) · Guer Beastfolk (fox: Notice/Sneak, +1 Wis/Cha, +10' move) · Accipiter Anak (winged: Flight, +1 Dex/−1 Con) · Harbinger Anak (face-shift: +1 Cha/−1 Con) · Aristoi Anak (ruler: Lead+skill, +1 Wis, Wis for any weapon) · Hua Beastfolk (bull: +1 Str/−1 Dex, +Strain) · Kitsune Beastfolk (fox: +1 Cha, Elemental Sparks) · Deepfolk (dark-vision, ½ needs, raise a physical to 14; sun harms) · Manu Beastfolk (lizard: swim, breath-hold, −1 Shock) · Nahu Beastfolk (cat: claws=daggers, low-light) · Oni (+1 Str/−1 Wis, −2 Mental saves) · Pichi Beastfolk (rat: blindsense 10') · Piren Beastfolk (wolf: grant an ally a bonus Main) · Still Cities Undead (no needs, auto-stabilize, immune poison/disease) · Sui Beastfolk (pig: poison-immune, act 1 round at 0 HP) · Tanuki Beastfolk (climb, 1/day shapeshift) · Tengu Beastfolk (crow: fly outdoors) · Usagi Beastfolk (rabbit: +1 all saves, double move) · Zakathi (Con→14/18, +Strain, must labor).

---

## 7. Mage Traditions

A Mage (or Partial Mage) picks one tradition. **Spells** are mighty Vancian High Magic (circles 1–5) plus tradition New Magic; **Arts** are lesser, repeatable tricks fueled by **Effort** (a separate pool per tradition). Spellcasters **cannot cast/use arts in armor or with a shield** (the *Armored Magic* Focus lifts this) — **except Healers**, whose arts work freely in armor.

**Effort** (committed for the **scene**, the **day**, or **indefinitely**):
- High Mage / Elementalist / Necromancer: **1 + Magic level + better Int/Cha mod** (Partial: −1, min 1).
- **Healer: Heal level + better Int/Cha mod** (min 1; *no +1*).
- **Vowed: order-skill level + best attribute mod** (min 1; *no +1*).

**Spells/Arts at level 1:** full caster prepares **3**, casts **1/day**, max circle **1**, starts with **4** spells; partial caster prepares **2**, casts **1/day**, **2** spells; dual-Partial-Mage prepares **3**, casts **1/day**, **4** spells.

All casters of a spell tradition gain **Magic** as a bonus skill (level-0, or level-1 if already 0). Healers gain **Heal**; Vowed gain a non-combat skill of their order (Exert/Know/Pray/Magic, etc.).

### High Mage *(full or partial)*
The orthodox wizard; masters inherited High Magic. **Gains Magic** as a bonus skill; each level-up learns **two** High Magic spells castable by them. At L1 a full High Mage picks **two** arts, a partial **one**.
**Arts:** Arcane Lexicon · Counter Magic · Empowered Sorcery · Hang Sorcery · Inexorable Effect · Iron Resolution · Preparatory Countermagic · Psychic Conversion · Restrained Casting · Retain Sorcery · Sense Magic · Suppress Magic · Swift Casting · Ward Allies · Wizard's Grandeur.

### Elementalist *(full or partial)*
Masters earth/fire/wind/water; casts High Magic **+ Elementalist New Magic**. **Gains Magic.** Auto-gains **Elemental Resilience** and **Elemental Sparks**, plus one chosen art at L1.
**Other arts:** Beckoned Deluge · Earthsight · Elemental Blast · Flamesight · Pavis of Elements · Petrifying Stare · Rune of Destruction · Steps of Air · Stunning Shock · Thermal Shield.
*New Magic spells (Elementalist-only):* Aqueous Harmony, The Burrower Below, Flame Scrying, Flame Without End, Elemental Favor, Pact of Stone and Sea, Elemental Spy, Elemental Vallation, Boreal Wings, Like the Stones, Wind Walking, Calcifying Scourge, Elemental Guardian, Fury of the Elements, Tremors of the Depths.

### Necromancer *(full or partial)*
Broker of life and death; casts High Magic **+ Necromancer New Magic**; raises/commands the dead. **Gains Magic.** Picks one art at L1.
**Arts:** Bonetalker · Cold Flesh · Consume Life Energy · False Death · Gravesight · Keeper of the Gate · Life Bridge · Master of Bones · Red Harvest · Unaging · Uncanny Ichor · Unliving Persistence.

### Healer *(partial-class only)*
Magical mender; **no spells**, only healing arts; **works in armor**. **Gains Heal.** Effort uses **Heal**. Auto-gains **Healing Touch** and picks one more art at L1.
**Other arts:** Empowered Healer · Facile Healer · Far Healer · Final Repose · Healer's Eye · Limb Restoration *(L8+)* · Purge Ailment · Refined Restoration · Revive the Fallen *(L8+)* · Swift Healer · The Healer's Knife · Tireless Vigor · Vital Furnace.

### Vowed *(partial-class only)*
Body-adept / martial monk; **no spells**, only inner-power arts. Hit die can't be worse than 1d6/level. **Gains a non-combat order-skill.** Effort uses that order's skill. Auto-gains **Martial Style**, **Unarmed Might**, **Unarmored Defense** (base AC 13 + ½ level unarmored), plus one chosen art at L1.
**Other arts:** Brutal Counter · Faultless Awareness · Hurling Throw · The Inward Eye · Leap of the Heavens · Master's Vigor · Mob Justice · Nimble Ascent · Purified Body · Revivifying Breath · Shattering Strike · Style Weaponry · Unobtrusive Step.

### High Magic — 1st-circle spell list (new full Mages pick 4, partials 2)

| Spell | Effect |
|---|---|
| Apprehending the Arcane Form | See magic 15 min/level, also see in the dark |
| Cognitive Supersession of the Inferior Orders | Telepathically bond with an animal (obeys, won't fight) |
| The Coruscating Coffin | 1d8/level to a visible target, save for half; 1-HD foes die |
| Damnation of the Sense | Seize one sense of a target for a scene on a failed save |
| Decree of Ligneous Dissolution | Destroy all non-magic plant matter in the area |
| The Excellent Transpicuous Transformation | Turn one target/level invisible for an hour/level |
| Imperceptible Cerebral Divulgence | Detect surface thoughts; ask memory questions |
| Ineluctable Shackles of Volition | Enslave a target's mind, leaving them dazed but obedient |
| The Long Amber Moment | Put a willing creature into invulnerable stasis |
| Phantasmal Mimesis | Create an independent, functional illusion |
| Velocitous Imbuement | Augment one target/level's movement |
| Wardpact Invocation | Make a target weapon-immune or a weapon useless |
| The Wind of the Final Repose | Sleep living targets of ≤ 4 HD in the area |

*Higher circles (2–5) and full New Magic / spell descriptions: `lookup.py spell <name>` or `book/Worlds-Without-Number-Deluxe/05-Magic.md`.*

### Other traditions (pointers)
- **Gyre traditions** (ch. 11): Adunic Invoker · Darian Skinshifter · Kistian Duelist *(non-caster martial)* · Llaigisan Beastmaster · Sarulite Blood Priest · Vothite Thought Noble.
- **Legate Writs** (ch. 13): Might / Skill / Sorcery / Mastery on Legate Effort — endgame tier.
- **Atlas casters** (ch. 4): The Accursed, The Bard, The Mageslayer, The Wise.

---

## 8. Equipment Packages (pick one, or roll 3d6 × 10 silver)

| Package | Armor | Shield | Weapons | Notable gear | Cash |
|---|---|---|---|---|---|
| **Adventuring Peasant** | War Shirt (AC 11) | Large (AC 14 held) | Light Spear (1d6, Shock 2/13), Dagger (1d4, 1/15) | Backpack, 1 wk rations, mule & cart, tinderbox + 3 torches | — |
| **Ranger or Archer** | Buff Coat (AC 12) | — | Large Bow (1d8, no Shock) + 20 arrows, Dagger (1d4, 1/15), Hand Axe (1d6, 1/15) | Backpack, cooking kit + 1 wk rations, waterskin, tinderbox + 3 torches | 20 sp |
| **Armored Warrior** | Pieced Armor (AC 14) | Large (+1 when armored) | Short Sword (1d6, Shock 2/15), Dagger (1d4, 1/15) | Backpack, tinderbox + 3 torches | — |
| **Gentry Wayfarer** | Buff Coat (AC 12) | Small (AC 13 held) | Short Sword (1d6, Shock 2/15) | Backpack, 1 wk rations, waterskin, fine clothes, writing kit + paper | 20 sp |
| **Mage / Healer / Scholar** | Buff Coat (AC 12) | Small (AC 13 held) | Short Sword (1d6, Shock 2/15), 5 Throwing Blades (1d4, no Shock) | Backpack, 1 wk rations, waterskin, tinderbox + 3 torches, grappling hook + 50' rope | — |
| **Roguish Wanderer** | none (AC 10) | — | 2 Daggers (1d4, 1/15), Staff (1d6, 1/13) | Backpack, lantern + tinderbox + 2 oil flasks, writing kit + paper, 1 wk rations, waterskin, healer's pouch | 80 sp |

*Shield rule:* a shield gives **+1 AC if your worn armor's AC ≥ the shield's held value**; otherwise the shield **sets** the base AC (Small 13 / Large 14). Add Dex either way.

---

*Content reproduced from Worlds Without Number / The Atlas of the Latter Earth (Kevin Crawford / Sine Nomine) for personal solo play; not for redistribution.*
