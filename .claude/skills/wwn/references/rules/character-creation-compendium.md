# WWN Character Creation — Full Compendium

> Use this when: building or reviewing a Worlds Without Number PC (or a classed NPC). This is a single-file
> compilation of **how to roll**, **all skills**, **all backgrounds**, **all classes & the Adventurer partial
> system**, **all mage traditions**, and **all foci** (core + the Atlas of the Latter Earth optional sets).
> It is the companion to the lean `character-creation.md` card — that card is the quick procedure; this is the
> complete data behind it.

**Sources:** `book/Worlds-Without-Number-Deluxe/02-Character-Creation.md` (attributes, backgrounds, classes,
foci, final touches, packages), `…/05-Magic.md` (traditions, Effort, spells/Arts), `…/04-The-Rules-of-the-Game.md`
(skill checks, saves, advancement), and `book/The-Atlas-of-the-Latter-Earth/04-Optional-Rules-and-Classes.md`
(Maqqatban styles, Godblood / Arcane-Secret / Non-Human-Origin foci). Background data cross-checked against the
canonical `scripts/chargen.py` tables. The Atlas book is OCR-scrambled; reconstructed entries flagged ⚠️ note
uncertain Level-2 attributions — verify against the book before relying on them in play.

> ⚠️ **Tooling gap (see the audit):** `scripts/chargen.py` and `bridge/generators/foci.json` do **not** yet know
> the **Healer** or **Vowed** traditions or any **Atlas focus** — so a Healer/Vowed PC or a Maqqatban-style PC
> must currently be hand-built from this document. A fix plan exists in `CHARACTER-CREATION-AUDIT.md`.

---

## Contents
1. **Rolling & Resolution** — dice, skill checks, saves, attacks, Shock
2. **Character Creation** — procedure, attributes, classes, the focus-count rule, final touches, equipment
3. **Backgrounds** — all 20
4. **Mage Traditions** — High Mage · Elementalist · Healer · Necromancer · Vowed (+ Gyre pointers)
5. **Foci — Core** — the 47 base foci
6. **Foci — Atlas / Optional** — Maqqatban styles · Godblood · Arcane Secret · Non-Human Origin

---

# PART 1 — ROLLING & RESOLUTION

## Rolling & Resolution

All randomness in WWN routes through honest dice (in this campaign, the scripts). Two engines: **2d6 for skills**, **d20 for combat & saves**.

### Attribute modifiers
| Score | 3 | 4–7 | 8–13 | 14–17 | 18 |
|---|---|---|---|---|---|
| Mod | −2 | −1 | +0 | +1 | +2 |

### Skill checks (2d6)
`2d6 + skill level + best applicable attribute mod` vs a **difficulty**:

| Diff | Meaning |
|---|---|
| 6 | Tricky for a layman; below this, don't roll |
| 8 | A real challenge a pro still beats more often than not |
| 10 | Only a skilled expert; even they may fail |
| 12 | Only a master is reliable |
| 14+ | Even a master will probably fail |

- **Meet or beat** the difficulty = success.
- **Untrained** (no level-0 in the skill) = **−1**, and some esoteric skills can't be attempted untrained at all.
- **Modifiers** from circumstance/tools cap at **±2** total. Using a skill for a peripheral-but-plausible purpose raises the difficulty by **+2** instead of forbidding it.
- **Failure** = you can't do it, *or* success at a cost/complication (GM's call).
- Don't call for a check when success is routine for the PC's background, or when neither outcome is interesting.

**Aiding:** a helper describes their aid and rolls a relevant skill vs the same difficulty; success grants the acting PC **+1** (max +1 total, no matter how many helpers).

**Opposed checks:** all parties roll `2d6 + mod`; **highest wins, ties go to the PC**. An NPC adds its skill bonus when its role fits, else rolls flat 2d6. The GM picks the most applicable skill/attribute per side (e.g. Dex/Sneak vs Wis/Notice).

### The skill list (rated 0–4)
Administer · Connect · Convince · Craft · Exert · Heal · Know · Lead · Magic · Notice · Perform · Pray · **Punch · Shoot · Stab** (the three combat skills) · Ride · Sail · Sneak · Survive · Trade · Work.
*Magic gates Arts and spells. Combat skills add to hit rolls (and Punch adds to unarmed damage).*

### Attack rolls (d20)
`1d20 + combat-skill level + class attack bonus + attribute mod (+ situational)` vs the target's **Armor Class** (ascending). Untrained weapon = **−2**.
- **Damage:** weapon die **+ attribute mod + magic/Focus bonuses**, subtracted from HP. (Punch also adds Punch skill to damage.)
- **Shock:** many weapons list **Shock N/AC** — on a *miss* against a target whose AC ≤ the listed value, you still deal **N** damage. Combat is never "nothing happens."
- At **0 HP** a character is dying → **Mortal Wounds**: must be stabilized within a short window (Heal check, or it's automatic for some abilities) or die. Death is real.

### Saving throws (d20, roll ≥ target)
At level 1 the target is **15 − best relevant attribute mod** (equivalently **16 − level − mod** as you advance):
- **Physical** — best of Str/Con · **Evasion** — best of Int/Dex · **Mental** — best of Wis/Cha · **Luck** — no attribute (flat 16 − level).
- Monster save = **15 − ½ HD**.

### Time
**Round** = 6 s (combat). **Turn** = 10 min (exploration; light, torches, wandering checks). **Scene** = one activity/place — most effect durations are "1 scene."

### Advancement (summary)
PCs gain XP from adventures and pursued goals. Each level raises attack bonus (by class), HP (another hit die), save targets (16 − level − attr), skill points, and grants new foci at set levels. Gains taper past 10th. Full thresholds: `book/Worlds-Without-Number-Deluxe/04-The-Rules-of-the-Game.md` (L694–798).


---

# PART 2 — CHARACTER CREATION

> Source: `02-Character-Creation.md` (Worlds Without Number Deluxe, pp. 8–35).
> Reference line numbers are given inline so claims can be re-checked against the book.

## Character Creation Procedure

The book's "A Summary of Character Creation" (L39–101) is printed with its numbered steps
scrambled across two columns; reassembled in order, the ordered procedure is:

1. **Roll attributes** — roll 3d6 six times, assign in order to Str/Dex/Con/Int/Wis/Cha, or use
   the array (L49). If rolled, you may change one score to 14 (L49).
2. **Mark attribute modifiers** for each score (L53–55).
3. **Pick a background** (list p. 11); gain its free skill at level-0 (L59).
4. **Decide to roll or pick skills.** If you pick: two more from the background's Learning table
   (no "Any Skill" entries), no Growth-table picks; or just take the "Quick Skills" at level-0
   (L63).
5. **If rolling skills:** roll up to three times, split between Growth and Learning tables as you
   wish (L67).
6. **Choose your class** from those on p. 18 — Warrior, Expert, Mage, or Adventurer (mix two)
   (L41).
7. **Choose your Foci** — one free Focus of any kind; Expert/Partial Expert adds one non-combat
   Focus; Warrior/Partial Warrior adds one combat-related Focus; both class picks may stack on one
   Focus to start it at level 2 (L45).
8. **(Optional) Non-human PC** by spending a Focus pick on an origin Focus (L51).
9. **Pick one free skill** of your choice (L57).
10. **If Mage / Partial Mage, pick a tradition** (Magic chapter p. 60). Full High Mage / Necromancer /
    Elementalist, or partial in those, or the partial classes Healer or Vowed (L61).
11. **Mages choose starting spells** — full spellcasting Mage = 4 first-level spells; Partial Mage = 2;
    two partial spellcasting Mage classes = 4 (L65, L926–928).
12. **Roll maximum hit points** = class hit die + Con mod, min 1 (L69).
13. **Note base attack bonus** from the class table (L89).
14. **Choose an equipment package** (p. 29) or roll 3d6 × 10 starting silver (L91).
15. **Total hit bonus** = base attack bonus + Punch/Stab/Shoot skill + attribute mod (−2 if no
    level-0 combat skill) (L95).
16. **Note weapon damage** = base damage dice + attribute mod (+ Punch skill for Punch weapons)
    (L97).
17. **Record Armor Class** — unarmored = 10, + Dex mod; armor sets its own value (L101, L87).
18. **Record saving throws** — Physical, Evasion, Mental, Luck (L93).
19. **Name and goal** (L99).

(Final Touches, L906–952, restates steps 9, 12–18 as the closing record-keeping stage.)

## Attributes

- **Generation (L119–125):** Each attribute is 3–18. Roll **3d6 six times in order** for Str, Dex,
  Con, Int, Wis, Cha. After rolling, you **may change one attribute to 14** ("unusually good at
  *something*"). A clement GM may let rolls go to any attribute. Alternatively use the **standard
  array 14, 12, 11, 10, 9, 7** placed where you wish — but if you assign the array you **cannot**
  swap a score for a 14.
- **Modifier table (L127–132):**

  | Score | Modifier |
  |---|---|
  | 3 | −2 |
  | 4–7 | −1 |
  | 8–13 | +0 (no modifier) |
  | 14–17 | +1 |
  | 18 | +2 |

## Classes

There are four classes (L408). Each begins play at level 1 (first row of its table). All HP entries
below are level-1 (1 die); higher rows show the per-level progression.

### Warrior (L485–518)
- **Hit die / level:** 1d6+2 (L490; HP step also at L69/L912).
- **Attack bonus:** +1 at L1, scaling +1 per level to +10 at L10 (L489–500).
- **Foci:** 1 free (Any) + 1 Warrior (combat) at level 1 = **2 foci** (L490–491). Additional "+1
  Any" at levels 2, 5, 7, 10.
- **Class abilities:**
  - **Veteran's Luck** (L506–514): once per scene, as an Instant action, turn a missed attack into a
    hit, OR turn a successful attack against you into a miss — only one of the two per scene.
  - **Killing Blow** (L510–518): on any damage dealt (attack/spell/ability), add half character level
    rounded up to the damage; also added to Shock.

### Expert (L414–451)
- **Hit die / level:** 1d6 (L420).
- **Attack bonus:** +0 at L1, rising to +5 at L10 (L420–431).
- **Foci:** 1 free (Any) + 1 Expert (non-combat) at level 1 = **2 foci** (L421–422). Additional
  "+1 Any" at levels 2, 5, 7, 10.
- **Class abilities:**
  - **Masterful Expertise** (L445–447): once per scene, reroll any failed non-combat skill check as
    an Instant action; use the better result.
  - **Quick Learner** (L449–451): on level-up, gain an extra skill point spendable only on non-combat
    skills or raising attributes (can be saved).

### Mage (L453–483)
- **Hit die / level:** 1d6−1 (L466).
- **Attack bonus:** +0 through L4, +1 at L5–9, +2 at L10 (L466–475).
- **Foci:** 1 free (Any) at level 1 = **1 focus** — a Mage adds NO class focus (L466). Additional
  "+1 Any" at levels 2, 5, 7, 10.
- **Class ability — Arcane Tradition** (L481–483): pick one magical tradition (Magic chapter p. 60),
  granting its benefits and restrictions. Full spellcasting Mage starts with 4 first-level spells.

### Adventurer (the partial-class system) (L520–590)
An Adventurer picks **two of the three main classes** as *partial* classes, gaining some of each at
the cost of never matching a full specialist (L435, L522–528). The signature class abilities of the
full classes are mostly LOST (see each partial below). There are four legal pairings:

**Partial Expert** (L530–532): treated as a full Expert and **keeps Quick Learner**, but **loses
Masterful Expertise**.

**Partial Warrior** (L542–544): keeps the improved hit die and a somewhat improved attack bonus, but
**loses Veteran's Luck AND Killing Blow**.

**Partial Mage** (L534–540): gains **Arcane Tradition** (pick a tradition), but that tradition's
abilities are more limited than a full Mage's; a full Mage will outstrip a Partial Mage in their
tradition (L528). May be taken **twice** for two different traditions. A Partial Mage starts with 2
first-level spells (4 if two spellcasting partial-Mage classes) (L65, L538, L926–928).

#### Partial Expert / Partial Warrior (L546–560)
- **Hit die / level:** 1d6+2.
- **Attack bonus:** +1 (L1) → +7 (L10). (Slightly behind a full Warrior, which reaches +10.)
- **Foci at L1:** 1 Expert + 1 Warrior + 1 Any = **3 foci** (worked example at L526 confirms three).
- **Loses:** Masterful Expertise and Veteran's Luck + Killing Blow. Keeps Quick Learner.

#### Partial Expert / Partial Mage (L562–575)
- **Hit die / level:** 1d6.
- **Attack bonus:** +0 (L1) → +5 (L10) — same line as full Expert/Mage.
- **Foci at L1:** 1 Expert + 1 Any = **2 foci** (Mage adds none).
- **Loses:** Masterful Expertise; full-tradition power. Keeps Quick Learner + Arcane Tradition
  (limited).

#### Partial Mage / Partial Warrior (L577–590)
- **Hit die / level:** 1d6+2.
- **Attack bonus:** +1 (L1) → +7 (L10).
- **Foci at L1:** 1 Warrior + 1 Any = **2 foci** (Mage adds none).
- **Loses:** Veteran's Luck + Killing Blow; full-tradition power. Keeps Arcane Tradition (limited).

#### Partial Mage / Partial Mage (L538)
- **Hit die / attack bonus / foci:** uses the **full Mage chart** (1d6−1 HD; +0→+2 attack; **1 focus**
  at L1, the free Any only).
- Uses the spellcasting table on p. 64 if both partials cast; starts with **4 first-level spells**.
- **Loses:** the depth of any single full tradition; gains partial access to two traditions instead.

> **Note on "Healer" / "Vowed":** the partial Mage list includes the magically-gifted partial classes
> **Healer** and **Vowed** (L61). A *Partial Healer* is mechanically a *Partial Mage* (Healer is a
> Mage tradition), so any Adventurer pairing involving Healer uses the corresponding Partial-Mage
> table above.

## Foci Allocation Rule

**The underlying rule, quoted from the book:**

- "**Every PC can pick one Focus of any kind** representing past experiences or native talent. This
  free Focus doesn't necessarily have to have anything to do with your class…" (L600).
- "Aside from this free Focus, **a Warrior or Partial Warrior can pick one Focus related to their
  martial background, and an Expert or Partial Expert can pick one Focus related to something other
  than combat.**" (L602).
- The stacking option, from the summary: "Characters with the Expert class or the Partial Expert
  feature of the Adventurer class get one level of a non-combat Focus for free in addition to this.
  **They can spend both levels on the same Focus, starting with level 2 in it if they wish.**
  Characters with the Warrior class or Partial Warrior feature of the Adventurer class can do the
  same in choosing one level of a combat-related Focus." (L45).
- A Mage / Partial Mage adds **no** class focus — neither class line grants a second pick (only the
  "1 Any" appears on the Mage and Partial-Mage tables, L466, L538, L565, L580).

**Resulting focus counts at level 1 (foci = 1 free + class additions):**

| Class / combo | Free | Combat (Warrior) | Non-combat (Expert) | Total foci |
|---|---|---|---|---|
| Warrior | 1 | 1 | — | **2** |
| Expert | 1 | — | 1 | **2** |
| Mage | 1 | — | — | **1** |
| Partial Expert / Partial Warrior | 1 | 1 | 1 | **3** |
| Partial Expert / Partial Mage | 1 | — | 1 | **2** |
| Partial Mage / Partial Warrior | 1 | 1 | — | **2** |
| Partial Mage / Partial Mage | 1 | — | — | **1** |

Note (L596–598): a Focus normally has two levels; the second pick raises it to level 2. Many foci
grant a bonus skill (level-0, or level-1 if already held; pick any other non-Magic skill if already
at level-1).

## Final Touches

(L906–952; numbers cross-checked against the summary L69–101.)

- **Hit points (L910–912):** class hit die + **Con modifier**, minimum **1** HP even with a Con
  penalty. (Warrior 1d6+2, Expert 1d6, Mage 1d6−1; Adventurer per partial tables.)
- **Free skill (L914–916):** pick one skill at level-0 (→ level-1 if already level-0; cannot raise an
  already level-1 skill).
- **Saving throws (L918–920):** roll d20, meet-or-beat the target.
  - **Physical** = 15 − best of Str / Con modifier.
  - **Evasion** = 15 − best of Int / Dex modifier.
  - **Mental** = 15 − best of Wis / Cha modifier.
  - **Luck** = flat **15** (no attribute).
  > Discrepancy: the parent summary's "16 − level − relevant mod" formula is the *advancement* form;
  > at first level the book states flat **15 − relevant modifier** (Luck = 15). With level = 1,
  > "16 − 1 − mod" = "15 − mod", so the two are consistent at level 1.
- **Base attack bonus (L922–924):** from the class table; written down for use in the hit bonus.
- **Hit bonus / damage (L938–942):** total hit = base attack bonus + Stab/Shoot/Punch + weapon's
  attribute mod (−2 if you lack even level-0 in the weapon). Damage = base dice + attribute mod
  (+ Punch skill for Punch/unarmed). Shock also takes the attribute mod.
- **Armor Class (L943–944):** unarmored = **10**; armor sets its own AC value; a shield grants its
  listed AC (e.g. large shield AC 14 when held, or +1 AC when worn over armor); **+ Dex modifier**
  (worsens AC on a penalty).
- **Languages (L930–932):** native language + Trade Cant, plus extras from Connect and Know — level-0
  in either grants +1 language, level-1 grants +2. (E.g. Connect-1 + Know-1 = native + Trade Cant + 4
  more.)
- **Starting spells (L926–928):** full Mage = 4 first-level; Partial Mage = 2; two spellcasting
  partial-Mage classes = 4.
- **Equipment (L934–936):** pick a package or roll 3d6 × 10 silver.
- **Name, goal, ties (L946–952).**

> **Items requested by the parent that are NOT in this chapter:** **Effort** (1 + Magic-skill level +
> better of Int/Cha; partial −1, min 1), **System Strain** (max = Con), and **Initiative** (1d8 + Dex)
> are not defined in 02-Character-Creation.md. They live in the Magic and Combat chapters
> (Effort/Arts → Magic ch. p. 60; Strain & Initiative → Combat ch.). Their values as stated by the
> parent could not be verified against this file.

## Equipment Packages

Packages from p. 29 (L964–991); the tables are mangled in the source markdown, but the recoverable
packages are:

1. **Adventuring Peasant** — War Shirt (AC 11); Large Shield (AC 14 held); Light Spear (1d6, Shock
   2/AC 13); Dagger (1d4, Shock 1/AC 15); Backpack; Rations 1 week; Mule and small cart; Tinder box +
   3 torches.
2. **Ranger or Archer** — Buff Coat (AC 12); Large Bow (1d8, no Shock); 20 arrows & quiver; Dagger
   (1d4, Shock 1/AC 15); Hand Axe (1d6, Shock 1/AC 15); Backpack; cooking utensils + 1 week rations;
   Waterskin; Tinder box + 3 torches; 20 sp cash.
3. **Armored Warrior** — Pieced Armor (AC 14); Large Shield (+1 AC when armored); Short Sword (1d6,
   Shock 2/AC 15); Dagger (1d4, Shock 1/AC 15); Backpack; Tinder box + 3 torches.
4. **Gentry Wayfarer** — Buff Coat (AC 12); Small Shield (AC 13 held); Short Sword (1d6, Shock 2/AC
   15); Backpack; Rations 1 week; Waterskin; fine suit of clothing in pack; writing kit + 20 sheets
   paper; 20 sp cash.
5. **Mage, Healer, or Scholar** — Buff Coat (AC 12); Small Shield (AC 13 held); Short Sword (1d6,
   Shock 2/AC 15); 5 Throwing Blades (1d4, no Shock); Backpack; Rations 1 week; Waterskin; Tinder box
   + 3 torches; Grappling hook + 50' rope.
6. **Roguish Wanderer** — 2 Daggers (1d4, Shock 1/AC 15); Staff (1d6, Shock 1/AC 13); Backpack;
   Lantern, tinder box + 2 pint flasks oil; writing kit + 20 sheets paper; Rations 1 week; Waterskin;
   Healer's pouch; 80 sp cash.

(There are six packages; the source's broken table fuses the "Armored Warrior," "Gentry Wayfarer,"
"Roguish Wanderer," and "Mage/Healer/Scholar" cells into one cluster at L988–991, so the exact split
of the last items between Roguish Wanderer and the others is partially ambiguous in this dump.)


---

# PART 3 — BACKGROUNDS

## Backgrounds

Every hero comes from somewhere. A background is a thumbnail of the kind of life your PC led before
adventuring. Roll on the d20 table or pick from the list. If you want a background not listed, work
with the GM to choose Growth and Learning tables that fit the concept.

### d20 Background Table

| d20 | Background | Examples |
|----|------------|----------|
| 1  | Artisan   | blacksmith, tanner, carpenter |
| 2  | Barbarian | savage hermit, wild man |
| 3  | Carter    | hauling goods or riding post |
| 4  | Courtesan | harlot, artful companion |
| 5  | Criminal  | thief, con man, burglar |
| 6  | Hunter    | trapper, lone hermit, or recluse |
| 7  | Laborer   | skilled or unskilled urban worker |
| 8  | Merchant  | trader, peddler, or shopkeeper |
| 9  | Noble     | spare son, exile, black sheep |
| 10 | Nomad     | raider, tribal wanderer |
| 11 | Peasant   | farmer, rural laborer, serf |
| 12 | Performer | bard, dancer, singer |
| 13 | Physician | village healer, healer-monk |
| 14 | Priest    | monk, nun, holy hermit |
| 15 | Sailor    | bargeman, fisherman, pirate |
| 16 | Scholar   | sage, apprentice mage |
| 17 | Slave     | indentured laborer, runaway prentice |
| 18 | Soldier   | bandit, mercenary, guardsman |
| 19 | Thug      | ruffian, gang member, village bully |
| 20 | Wanderer  | exile, explorer, traveler |

### General Rules (Backgrounds and Skills)

Once you've rolled or chosen your background, you gain its **free skill** at level-0. Then pick **one**
of the following three options before choosing a class:

1. **Take the listed Quick Skills** at level-0. (Choose this for the common skills of the role with no
   further fuss.)
2. **Pick two skills from the background's Learning table** — but *not* the "Any Skill" choice. (Choose
   this if you have specific preferences.)
3. **Roll three times**, splitting the rolls as you wish between the **Growth** (d6) and **Learning**
   (d8) tables for your background. (Choose this to accept the dice in exchange for an extra skill or a
   chance at improved attributes.)

**"Any Combat"** lets you choose Stab, Shoot, or Punch. **"Any Skill"** lets you choose any skill you
wish.

**Skill stacking / level rules:**
- All new skills are gained at **level-0** (a basic, ordinary proficiency — enough to earn a living).
- Roll or pick the **same skill a second time** → it becomes **level-1** (a well-honed veteran).
- You **cannot pick a skill a third time**. If you roll it a third time (or a Focus forces it), instead
  pick **any other skill** you wish — gaining it at level-0, or raising it from level-0 to level-1 if you
  already have it.
- **No novice hero can have a skill above level-1.** Only experienced adventurers develop greater mastery.

**Attribute growths (Growth table):**
- **+1 Any Stat** — raise any one attribute by 1 (potentially improving its modifier).
- **+2 Physical** — a +2 bonus applied to Physical attributes: **Strength, Dexterity, or Constitution**.
- **+2 Mental** — a +2 bonus applied to Mental attributes: **Intelligence, Wisdom, or Charisma**.
- No attribute can be raised above **18**, but a **+2 bonus can be split** between two different
  attributes.

---

### Artisan

A crafter — blacksmith, carpenter, shipwright, weaver, or maker of exotic goods.

- **Free Skill:** Craft
- **Quick Skills:** Trade, Connect
- **Growth (d6):** 1 +1 Any Stat · 2 +2 Physical · 3 +2 Physical · 4 +2 Mental · 5 Exert · 6 Any Skill
- **Learning (d8):** 1 Connect · 2 Convince · 3 Craft · 4 Craft · 5 Exert · 6 Know · 7 Notice · 8 Trade

### Barbarian

A savage frontiersman or hill-tribesman who lives without civilized comforts and accepts violence readily.

- **Free Skill:** Survive
- **Quick Skills:** Any Combat, Notice
- **Growth (d6):** 1 +1 Any Stat · 2 +2 Physical · 3 +2 Physical · 4 +2 Mental · 5 Exert · 6 Any Skill
- **Learning (d8):** 1 Any Combat · 2 Connect · 3 Exert · 4 Lead · 5 Notice · 6 Punch · 7 Sneak · 8 Survive

### Carter

A hauler of overland goods — caravan worker, independent shipper, or messenger rider.

- **Free Skill:** Ride
- **Quick Skills:** Connect, Any Combat
- **Growth (d6):** 1 +1 Any Stat · 2 +2 Physical · 3 +2 Physical · 4 +2 Mental · 5 Connect · 6 Any Skill
- **Learning (d8):** 1 Any Combat · 2 Connect · 3 Craft · 4 Exert · 5 Notice · 6 Ride · 7 Survive · 8 Trade

### Courtesan

A professional companion, from common harlot to polished, cultured artist of song, dance, and company.

- **Free Skill:** Perform
- **Quick Skills:** Notice, Connect
- **Growth (d6):** 1 +1 Any Stat · 2 +2 Mental · 3 +2 Mental · 4 +2 Physical · 5 Connect · 6 Any Skill
- **Learning (d8):** 1 Any Combat · 2 Connect · 3 Convince · 4 Exert · 5 Notice · 6 Perform · 7 Survive · 8 Trade

### Criminal

A professional lawbreaker — con man, pickpocket, footpad, impostor, or sneak thief.

- **Free Skill:** Sneak
- **Quick Skills:** Connect, Convince
- **Growth (d6):** 1 +1 Any Stat · 2 +2 Mental · 3 +2 Physical · 4 +2 Mental · 5 Connect · 6 Any Skill
- **Learning (d8):** 1 Administer · 2 Any Combat · 3 Connect · 4 Convince · 5 Exert · 6 Notice · 7 Sneak · 8 Trade

### Hunter

A professional hunter, trapper, gamekeeper, or wilderness hermit, skilled in marksmanship and stealth.

- **Free Skill:** Shoot
- **Quick Skills:** Survive, Sneak
- **Growth (d6):** 1 +1 Any Stat · 2 +2 Physical · 3 +2 Physical · 4 +2 Mental · 5 Exert · 6 Any Skill
- **Learning (d8):** 1 Any Combat · 2 Exert · 3 Heal · 4 Notice · 5 Ride · 6 Shoot · 7 Sneak · 8 Survive

### Laborer

An urban day-worker — unskilled help employed by a town's artisans and craftsmen.

- **Free Skill:** Work
- **Quick Skills:** Connect, Exert
- **Growth (d6):** 1 +1 Any Stat · 2 +1 Any Stat · 3 +1 Any Stat · 4 +1 Any Stat · 5 Exert · 6 Any Skill
- **Learning (d8):** 1 Administer · 2 Any Skill · 3 Connect · 4 Convince · 5 Craft · 6 Exert · 7 Ride · 8 Work

### Merchant

A trader, from gilded merchant-prince to humble village peddler, brave enough to face this world's perils.

- **Free Skill:** Trade
- **Quick Skills:** Convince, Connect
- **Growth (d6):** 1 +1 Any Stat · 2 +2 Mental · 3 +2 Mental · 4 +2 Mental · 5 Connect · 6 Any Skill
- **Learning (d8):** 1 Administer · 2 Any Combat · 3 Connect · 4 Convince · 5 Craft · 6 Know · 7 Notice · 8 Trade

### Noble

A member of the ruling caste, driven from their former place but retaining the benefit of its education.

- **Free Skill:** Lead
- **Quick Skills:** Connect, Administer
- **Growth (d6):** 1 +1 Any Stat · 2 +2 Mental · 3 +2 Mental · 4 +2 Mental · 5 Connect · 6 Any Skill
- **Learning (d8):** 1 Administer · 2 Any Combat · 3 Connect · 4 Convince · 5 Know · 6 Lead · 7 Notice · 8 Ride

### Nomad

A beast-rider, wagon-driver, or tribal wanderer skilled at riding and surviving harsh environments.

- **Free Skill:** Ride
- **Quick Skills:** Survive, Any Combat
- **Growth (d6):** 1 +1 Any Stat · 2 +2 Physical · 3 +2 Physical · 4 +2 Mental · 5 Exert · 6 Any Skill
- **Learning (d8):** 1 Any Combat · 2 Connect · 3 Exert · 4 Lead · 5 Notice · 6 Ride · 7 Survive · 8 Trade

### Peasant

A rural farmer or serf, marked by ruthless resourcefulness and a hard tolerance of pain and toil.

- **Free Skill:** Exert
- **Quick Skills:** Sneak, Survive
- **Growth (d6):** 1 +1 Any Stat · 2 +2 Physical · 3 +2 Physical · 4 +2 Physical · 5 Exert · 6 Any Skill
- **Learning (d8):** 1 Connect · 2 Exert · 3 Craft · 4 Notice · 5 Sneak · 6 Survive · 7 Trade · 8 Work

### Performer

A singer, dancer, musician, actor, poet, or orator with a practiced way of managing people's affections.

- **Free Skill:** Perform
- **Quick Skills:** Convince, Connect
- **Growth (d6):** 1 +1 Any Stat · 2 +2 Mental · 3 +2 Physical · 4 +2 Physical · 5 Connect · 6 Any Skill
- **Learning (d8):** 1 Any Combat · 2 Connect · 3 Exert · 4 Notice · 5 Perform · 6 Perform · 7 Sneak · 8 Convince

### Physician

A healer — a classically-trained professional or a village herb-and-suture practitioner.

- **Free Skill:** Heal
- **Quick Skills:** Know, Notice
- **Growth (d6):** 1 +1 Any Stat · 2 +2 Physical · 3 +2 Mental · 4 +2 Mental · 5 Connect · 6 Any Skill
- **Learning (d8):** 1 Administer · 2 Connect · 3 Craft · 4 Heal · 5 Know · 6 Notice · 7 Convince · 8 Trade

### Priest

A monk, nun, or holy hermit — moral exemplar or ritual technician, sometimes wielding magical powers.

- **Free Skill:** Pray
- **Quick Skills:** Convince, Know
- **Growth (d6):** 1 +1 Any Stat · 2 +2 Mental · 3 +2 Physical · 4 +2 Mental · 5 Connect · 6 Any Skill
- **Learning (d8):** 1 Administer · 2 Connect · 3 Know · 4 Lead · 5 Heal · 6 Convince · 7 Pray · 8 Pray

### Sailor

A voyager of salt tides or deep rivers — captain, bargeman, or common seaman accustomed to peril and labor.

- **Free Skill:** Sail
- **Quick Skills:** Exert, Notice
- **Growth (d6):** 1 +1 Any Stat · 2 +2 Physical · 3 +2 Physical · 4 +2 Mental · 5 Exert · 6 Any Skill
- **Learning (d8):** 1 Any Combat · 2 Connect · 3 Craft · 4 Exert · 5 Heal · 6 Notice · 7 Perform · 8 Sail

### Scholar

A rare dedicated student, immersed in a life of study and broad learning, fit for perilous field research.

- **Free Skill:** Know
- **Quick Skills:** Heal, Administer
- **Growth (d6):** 1 +1 Any Stat · 2 +2 Physical · 3 +2 Mental · 4 +2 Mental · 5 Connect · 6 Any Skill
- **Learning (d8):** 1 Administer · 2 Connect · 3 Craft · 4 Heal · 5 Know · 6 Notice · 7 Convince · 8 Trade

### Slave

A house slave, mine laborer, runaway, or rebel — well-represented among the desperate adventuring class.

- **Free Skill:** Sneak
- **Quick Skills:** Survive, Exert
- **Growth (d6):** 1 +1 Any Stat · 2 +2 Physical · 3 +2 Physical · 4 +2 Mental · 5 Exert · 6 Any Skill
- **Learning (d8):** 1 Administer · 2 Any Combat · 3 Any Skill · 4 Convince · 5 Exert · 6 Sneak · 7 Survive · 8 Work

### Soldier

A mercenary, regular soldier, temple knight, militiaman, or raider who made their living by war.

- **Free Skill:** Any Combat
- **Quick Skills:** Exert, Survive
- **Growth (d6):** 1 +1 Any Stat · 2 +2 Physical · 3 +2 Physical · 4 +2 Physical · 5 Exert · 6 Any Skill
- **Learning (d8):** 1 Any Combat · 2 Any Combat · 3 Exert · 4 Lead · 5 Notice · 6 Ride · 7 Sneak · 8 Survive

### Thug

A village bully, street ruffian, assassin, bandit, or enforcer who gets what he wants by his right arm.

- **Free Skill:** Any Combat
- **Quick Skills:** Convince, Connect
- **Growth (d6):** 1 +1 Any Stat · 2 +2 Mental · 3 +2 Physical · 4 +2 Physical · 5 Connect · 6 Any Skill
- **Learning (d8):** 1 Any Combat · 2 Any Combat · 3 Connect · 4 Convince · 5 Exert · 6 Notice · 7 Sneak · 8 Survive

### Wanderer

A homeless exile, explorer, or vagabond who journeys for their own reasons, seeking what they hope to find.

- **Free Skill:** Survive
- **Quick Skills:** Sneak, Notice
- **Growth (d6):** 1 +1 Any Stat · 2 +2 Physical · 3 +2 Physical · 4 +2 Mental · 5 Exert · 6 Any Skill
- **Learning (d8):** 1 Any Combat · 2 Connect · 3 Notice · 4 Perform · 5 Ride · 6 Sneak · 7 Survive · 8 Work


---

# PART 4 — MAGE TRADITIONS

> Source: `book/Worlds-Without-Number-Deluxe/05-Magic.md` (pp. 64–97). Gyre traditions: `book/Worlds-Without-Number-Deluxe/11-Arts-of-the-Gyre.md` (pp. covering the Gyre professions).

## Magic System

Mages of Latter Earth draw on the **Legacy**, an ancient accreted mass of arcane laws. Their power comes in two wholly separate resources:

- **Spells** are the ancient invocations, ranked **level 1 (weakest) to level 5 (most potent)**. The common inherited corpus is **High Magic** (scores of surviving incantations). A separate body called **New Magic** is jury-rigged by modern traditions and is **specific to a single tradition** — Elementalist, Necromancer, etc. — and useless to outsiders. Spellcasting is **Vancian**: a mage must first **learn** a spell into their **grimoire/spellbook**, then **prepare** a set after a night's rest, then **cast** from a small **daily pool**. There are *no* petty High Magic spells; even level-1 spells can kill, enslave, or conjure perfect illusions.
- **Arts** are the repeatable tricks and minor magical techniques taught by a particular tradition. They are far weaker than spells but much easier to use, and are fueled by **Effort** rather than spell slots. Each tradition has its own art list; some arts are auto-granted at level 1, others are picked as the mage gains levels. **Once picked, an art is permanent and cannot be exchanged.**

Spells and Arts are **two independent resources**: a mage out of spells for the day may still have a full pool of Effort.

**Targets/visibility:** "creature" = any animate entity (living, undead, or synthetic); plants don't count unless plant-monsters. A "visible" target is one the caster can see or whose exact location is obvious; default max range is a bowshot if none is given.

## Effort

**Effort** represents a mage's available focus and magical energy. It is spent by being **Committed**, and returns on its own after a set duration.

- **General formula:** Effort maximum = **1 + Magic skill level + the better of the Int or Cha modifier** (minimum 1).
- **Partial Mage:** Effort score is **one point lower** than a full Mage, but **never less than 1**. (Healers, Vowed, and other special partials have this reduction already baked into their listed calculation.)
- **Per-tradition pools:** Each tradition has its **own separate Effort pool** (Necromancer Effort, High Mage Effort, Healer Effort, etc.). A PC of two traditions has two pools; neither fuels the other's arts.
- **One point per art:** Committing for an art costs a **single point** unless the art explicitly says otherwise.

**Commit durations** (each art states which it uses):

- **Commit for the day** — point returns next morning after a good night's rest (powerful arts).
- **Commit for the scene** — point returns as soon as the scene ends (modest arts).
- **Commit indefinitely** — keeps a persistent ability active as long as one point stays committed; reclaim it at any time as an Instant action to switch the art off. Survives sleep/unconsciousness if prepared properly beforehand, but ends immediately if you're suddenly knocked unconscious or killed.

## Spell Slots

Vancian spellcasting, in three steps:

- **Learning:** Requires **1 week per spell level, minus 1 week per level of the learner's Magic skill** (minimum 1 day). The mage must be **able to cast the spell** to learn it (a novice casting only 1st-level spells can only learn 1st-level spells). Learning produces/masters a written copy; the mage must **retain the grimoire document** to prepare the spell later. New Magic spells can only be learned by mages of the originating tradition.
- **Preparing:** Takes **one hour, only after a good night's rest.** The number prepared scales by level (from ~2–3 at level 1 up to ~12 at level 10). Any mix of spell levels may be prepared. Once prepared, spells remain prepared indefinitely until swapped.
- **Casting/day:** A mage may cast only a limited number of spells per day before needing a full night's rest (novices ~1, masters up to 6). Each casting may be any prepared spell; the same spell may be cast multiple times if castings remain.
- **Scaling by level:** Both the **max spell level castable** and the **spells cast/prepared per day** rise with level (see each tradition's Full/Partial tables). Full Mages reach 5th-level spells at level 9–10. **Partial Mages** cast fewer spells/day, reach a **lower maximum spell level**, and often prepare fewer — but level-based spell effects still use their **full character level** (a 3rd-level Partial Necromancer's *Coruscating Coffin* does 3d8). **Dual partial spellcasters** (e.g. Partial High Mage/Partial Necromancer) use a special shared table (p. 64): more prepared spells and more arts, but slightly fewer casts/day and never the highest-level spells.

## Casting in Combat

- **Action cost:** Casting a spell usually requires a **Main Action**, **at least one free hand**, and an **audible incantation** (vocalizations at least as loud as normal conversation). The casting is obviously occult to onlookers, but which spell is being cast usually can't be told by looking.
- **Disruption by damage:** Casting requires undisturbed concentration. If the mage has **taken hit point damage or been severely jostled that round, they cannot cast that round.** Acting late in initiative risks being hurt before your turn and losing the cast.
- **Armor restrictions:** High Magic **cannot normally be cast while wearing armor, restrictive clothing, or using a shield** — and this hindrance applies to the tradition's **arts** too, not just spells. This restriction binds **High Mages, Elementalists, and Necromancers** (all spellcasting traditions), as well as the **Vowed** (whose body-arts also can't be used while armored). The **Armored Magic** Focus relaxes this.
  - **Exception — Healers:** Healer arts require only a touch and concentration and **work perfectly well in armor or while carrying a shield**; they're also subtle (no visible/audible tell). (The Vowed are *not* an exception — but they have built-in Unarmored Defense.)

## Traditions

| Tradition | Casts spells? | Effort basis | Partial-only (Adventurer-only)? |
|---|---|---|---|
| High Mage | Yes (High Magic) | Magic | No (full or partial) |
| Elementalist | Yes (High Magic + Elementalist New Magic) | Magic | No (full or partial) |
| Healer | **No** | **Heal** | **Yes — partial only** |
| Necromancer | Yes (High Magic + Necromancer New Magic) | Magic | No (full or partial) |
| Vowed | **No** | order's chosen skill | **Yes — partial only** |

### High Mage

Philosophical tendency rather than a single order; believes true power lies in mastering ancient High Magic and dismisses New Magic.

- **Bonus skill:** Magic (gained at level-0, or level-1 if already at level-0).
- **Spells:** Casts **High Magic only**. Each level-up, picks **two** High Magic spells of a level they can cast (self-sufficient, no tutor needed). Cannot cast in armor/shield without Armored Magic.
- **Effort:** standard (1 + Magic + better of Int/Cha mod; Partial −1, min 1).
- **Level-1 package:** Magic bonus skill; a **full High Mage picks two arts**, a **partial picks one**; prepares up to 3 first-level spells and casts 1/day at level 1.
- **Signature Arts:** spell-manipulation specialists — *Counter Magic* (opposed roll to fizzle an enemy cast), *Empowered Sorcery* (re-roll a spell's variable die), *Hang Sorcery* (hold a cast to trigger later), *Inexorable Effect* (force an enemy to re-roll a successful save), *Iron Resolution* (save vs. disruption), *Restrained Casting* (cast silently/without gestures), *Retain Sorcery* (a free extra cast/day), *Sense Magic*, *Suppress Magic*, *Swift Casting*, *Ward Allies* (omit allies from your area spell), *Arcane Lexicon*, *Wizard's Grandeur*.

### Elementalist

Seeks to master the classical elements (earth, fire, wind, water) to understand and re-stabilize the Legacy.

- **Bonus skill:** Magic (level-0, or level-1 if already level-0).
- **Spells:** Casts **High Magic + Elementalist New Magic** (e.g. *Aqueous Harmony*, *Elemental Vallation*, *Calcifying Scourge*, *Elemental Guardian*, *Fury of the Elements*). Each level-up picks one High Magic *or* Elementalist New Magic spell. No casting in armor/shield.
- **Effort:** standard (1 + Magic + better of Int/Cha; Partial −1, min 1).
- **Level-1 package:** Auto-gains **two arts free — *Elemental Resilience*** (unharmed by mundane cold / non-furnace heat; half damage from magical fire/frost) and ***Elemental Sparks*** (conjure petty flame/water/ice/stone/wind for minor tricks) — **plus one more art of choice** (partial also gets both auto arts + one pick). Prepares 3 spells, casts 1/day at level 1.
- **Other Arts:** *Elemental Blast* (Magic-skill ranged attack, 1d6 + level + attr), *Pavis of Elements* (+4 AC, cap 18), *Petrifying Stare*, *Rune of Destruction*, *Steps of Air* (grant flight), *Stunning Shock*, *Thermal Shield*, *Beckoned Deluge*, *Earthsight*, *Flamesight*.

### Healer

Curative adept; mends wounds, purges disease/poison, preserves life. **Partial Mage class only** — must be taken by an Adventurer alongside another partial class. Does **not** cast spells.

- **Bonus skill:** **Heal** (level-0, or level-1 if already level-0).
- **Effort (exact formula):** Healer Effort = **Heal skill level + the better of the Intelligence or Charisma modifier, to a minimum of 1 point.** (Note: this uses **Heal, not Magic**, and has **no "+1" base** — the partial reduction is already factored in.)
- **Works in armor:** Healer arts need only a touch + concentration and **function even while armored or carrying a shield**; they are subtle (no visible/audible sign).
- **Level-1 package:** Auto-gains **Healing Touch** plus **one more art** of choice.

**Level-1-available Healer Arts** (one-line effects):

- **Healing Touch** — Commit Effort for the scene (Instant); for the scene, heal **2d6 + Heal skill** to a touched ally as a Main Action (+1 System Strain to target each use).
- **Empowered Healer** — your *Healing Touch* adds your **level** to the healing.
- **Facile Healer** — your *Healing Touch* no longer requires Committing Effort to activate.
- **Far Healer** — *Healing Touch* usable at range on a visible target within **10 ft per character level**.
- **Final Repose** — Commit Effort for the day (Instant): a target takes a Physical save penalty = your Heal skill; if dropped to 0 HP this scene they **die with no stabilization/revival**.
- **Healer's Eye** — Commit Effort (On Turn); while committed, Main Action to detect diseases/poisons, diagnose flawlessly, read exact HP totals; also see living creatures regardless of light/mist.
- **Limb Restoration** *(level 8+ only)* — Commit all remaining Effort for the day (min 1) to **regrow a limb/organ** or efface a scar on a touched target; their System Strain is maximized.
- **Purge Ailment** — Commit Effort for the day (Main Action) to cure one poison/disease on a touched ally (can revive poison-killed within 6 min; magical ones may need a Wis/Cha-Heal check vs. 8+). At 7th level, only needs Commit for the scene.
- **Refined Restoration** — you and up to a dozen tended allies lose **2 System Strain** from a night's rest instead of 1.
- **Revive the Fallen** *(level 8+ only)* — Commit Effort for the day (Main Action) to **revive a recently-slain** creature (within 1 min/caster level of death, body intact); Strain maximized, unconscious 24h, then wakes at 1 HP.
- **Swift Healer** — *Healing Touch* usable as an **On Turn action**, once/day per character level (not more than once/round per target).
- **The Healer's Knife** — *Healing Touch* may instead **deal damage** equal to the healing (you take 1 Strain instead of the target); melee use needs a Punch attack (hit bonus = Heal skill).
- **Tireless Vigor** — Commit Effort; while committed, no growing need to eat/drink/breathe/sleep, and **regenerate 1 HP per hour**.
- **Vital Furnace** — Commit Effort for the day (Instant) to **negate the damage** of a non-mortal injury just received; also auto-stabilize at 0 HP and wake at 1 HP after 10 min.

### Necromancer

Seeks to undo death and restore humanity's lost immortality; checkered reputation, often clandestine.

- **Bonus skill:** Magic (level-0, or level-1 if already level-0).
- **Spells:** Casts **High Magic + Necromancer New Magic** (e.g. *Command the Dead*, *Raise Corpse*, *Query the Skull*, *Compel Flesh*, *Raise Grave Knight*, *Call of the Tomb*, *Everlasting*). Each level-up picks one High Magic *or* Necromancer New Magic spell. No casting in armor/shield.
- **Effort:** standard (1 + Magic + better of Int/Cha; Partial −1, min 1).
- **Level-1 package:** Picks **one art** (partial also one); prepares 3 spells, casts 1/day at level 1.
- **Signature Arts:** *Bonetalker* (see/speak with undead), *Cold Flesh* (no sleep, Shock cap 2, natural AC), *Consume Life Energy* (heal from melee damage dealt), *Red Harvest* (gain HP / +4 hit when a nearby creature dies), *Master of Bones* (undead re-roll saves vs. you; negate an undead attack), *Keeper of the Gate*, *Life Bridge*, *Unliving Persistence*, *Unaging*, *False Death*, *Gravesight*, *Uncanny Ichor*.

### Vowed

Bodily/spiritual adepts — monks, brawlers, warrior-ascetics who awaken the Legacy's lingering augmentations within their own bodies. **Partial Mage class only** — taken by an Adventurer alongside another partial class. Does **not** cast spells.

- **Bonus skill:** a **non-combat skill appropriate to the order** (Exert for physical sects, Know for scholarly, Pray for religious, Magic for occult — player's choice with GM approval), gained at level-0 (or level-1 if already level-0).
- **Effort:** based on the **order's chosen focus skill** (Exert / Know / Magic / Pray / etc.): Vowed Effort = **that skill's level + best attribute modifier (any attribute), minimum 1 point.**
- **No casting in armor:** arts can't be used while burdened by heavy clothing/armor/shield (Armored Magic mitigates) — but Vowed train in **Unarmored Defense**.
- **Level-1 package:** Auto-gains **three arts free — *Martial Style*, *Unarmed Might*, and *Unarmored Defense*** — plus **one more art** of choice.
  - **Martial Style:** hit die never worse than 1d6/level; Punch hit bonus never worse than an Expert's; at 3rd level Punch attacks count as a magic weapon.
  - **Unarmed Might:** unarmed damage scales by level (per the Vowed table — 1d6 up to 1d10+3 at level 10).
  - **Unarmored Defense:** unarmored/no-shield base AC = **13 + half character level** (round down).
- **Signature Arts (selection):** *Brutal Counter* (free retaliatory attack after an enemy melee attack), *Hurling Throw* (throw a struck foe), *Leap of the Heavens* (huge leaps; negate falling damage), *Mob Justice* (immune to swarm attacks/Shock when mobbed), *Revivifying Breath* (self-heal 1d6+level, no Strain), *Shattering Strike* (smash through walls / 1d12/level vs. immobilized foe), *Style Weaponry* (use Punch to hit with chosen weapon classes), *The Inward Eye*, *Faultless Awareness*, *Nimble Ascent*, *Purified Body*, *Master's Vigor*, *Unobtrusive Step*.

### Gyre Traditions (pointers)

Six professions unique to the **Gyre** region, detailed in **`book/Worlds-Without-Number-Deluxe/11-Arts-of-the-Gyre.md`**. The **Adunic Invoker** is a spell-point magical tradition takeable as full or partial Mage; the **other five are all non-spellcasting partial Mage classes** mixed into an Adventurer concept:

- **Adunic Invoker** — spell-**point** caster (a non-Vancian alternative); casts High Magic from a daily pool of spell points (= level-based + Int mod) rather than fixed slots, gaining no arts. Cannot mix with another spellcasting partial.
- **Darian Skinshifter** — shapeshifter; masters one alternate animal/hybrid form per level. Effort based on **Survive**. Adds druidic-style shapeshifting to a character.
- **Kistian Duelist** — swashbuckling light-armor combatant; trades durability for mobility and one-on-one duel bonuses, can manifest weapons of will. Effort based on **Stab**.
- **Llaigisan Beastmaster** — relies on a combat-capable **animal companion**; ranger/druid archetype.
- **Sarulite Blood Priest** — traditional cleric type; a modest selection of generally-useful miracles rather than full spellcasting.
- **Vothite Thought Noble** — mind-control / mindbender PC; mental-domination focus (the WWN analogue of a Stars Without Number Telepath).


---

# PART 5 — FOCI (CORE)

## Core Foci (from foci.json — 47 entries)

### Alert
- **L1:** Gain Notice. Can't be surprised or targeted by Execution Attacks; +1 to your side's initiative (or roll individual init twice).
- **L2:** You always act first in a round unless another combatant is equally Alert.
- *src:* `book/Worlds-Without-Number-Deluxe/02-Character-Creation.md#L604`

### Armored Magic
- **Level req:** Mage/Partial Mage only
- **L1:** Cast spells/use arts in armor of Encumbrance 2 or less; may use a shield if your other hand is free to gesture.
- **L2:** Cast in armor of any Encumbrance, and even with both hands full (not bound).
- *src:* `book/Worlds-Without-Number-Deluxe/02-Character-Creation.md#L612`

### Armsmaster
- **L1:** Gain Stab. Ready a stowed melee/thrown weapon as an Instant; add Stab skill to melee/thrown damage or Shock. (Doesn't stack with Deadeye.)
- **L2:** Your melee Shock treats targets as AC 10; +1 to hit with thrown/melee attacks.
- *src:* `book/Worlds-Without-Number-Deluxe/02-Character-Creation.md#L620`

### Artisan
- **L1:** Gain Craft. Craft counts as one level higher (max 5) for mods, which cost one less salvage; Craft works for any crafting profession.
- **L2:** First mod on an item is free of Maintenance and half-cost; auto-succeed at masterwork gear; monthly extra salvage reduction.
- *src:* `book/Worlds-Without-Number-Deluxe/02-Character-Creation.md#L630`

### Assassin
- **L1:** Gain Sneak. Conceal a knife-sized object, draw it On Turn; point-blank surprise-round attacks with it can't miss.
- **L2:** Take a (splittable) Move action on the same round as an Execution Attack, closing without alerting the victim.
- *src:* `book/Worlds-Without-Number-Deluxe/02-Character-Creation.md#L638`

### Authority
- **L1:** Gain Lead. Once/day, a Cha/Lead check vs an NPC's Morale makes them comply with a not-harmful request.
- **L2:** NPCs you directly lead gain +Lead to Morale and hit rolls and +1 to skill checks; followers won't act against you.
- *src:* `book/Worlds-Without-Number-Deluxe/02-Character-Creation.md#L646`

### Close Combatant
- **L1:** Gain any combat skill. Use knife-sized thrown weapons in melee freely; ignore melee Shock (but doing so disrupts your casting that round).
- **L2:** Your melee Shock treats all targets as AC 10; Fighting Withdrawal becomes a free On Turn action for you.
- *src:* `book/Worlds-Without-Number-Deluxe/02-Character-Creation.md#L654`

### Connected
- **L1:** Gain Connect. After a week somewhere not hostile, you have contacts for mildly-illegal favors — one favor/game day.
- **L2:** Once/session, plausibly run into someone you know willing to do a modest favor (GM decides who).
- *src:* `book/Worlds-Without-Number-Deluxe/02-Character-Creation.md#L662`

### Cultured
- **L1:** Gain Connect. Speak all common regional languages; learn a new one in a week; once/day gain a minor no-cost favor from a non-hostile NPC.
- **L2:** Once/session, reroll a failed social skill check using your cultural knowledge.
- *src:* `book/Worlds-Without-Number-Deluxe/02-Character-Creation.md#L670`

### Die Hard
- **L1:** +2 max HP per level (retroactive). Auto-stabilize when Mortally Wounded unless torn apart.
- **L2:** The first time each day an injury would drop you to 0 HP, you survive at 1 HP instead.
- *src:* `book/Worlds-Without-Number-Deluxe/02-Character-Creation.md#L676`

### Deadeye
- **L1:** Gain Shoot. Ready a stowed ranged weapon as an Instant; use a bow in melee at -4; add Shoot skill to ranged damage.
- **L2:** Reload slow weapons On Turn; use any ranged weapon in melee without penalty; once/scene auto-hit an inanimate target.
- *src:* `book/Worlds-Without-Number-Deluxe/02-Character-Creation.md#L684`

### Dealmaker
- **L1:** Gain Trade. In half an hour, find a buyer/seller for any tradeable good or service in the community, legal or not.
- **L2:** Once/session, make a request of a non-hostile sentient; if plausible, they'll deal for a price or favor.
- *src:* `book/Worlds-Without-Number-Deluxe/02-Character-Creation.md#L692`

### Developed Attribute
- **Level req:** Not Mage/Partial Mage
- **L1:** Raise one attribute's modifier by +1 (max +3); the score is unchanged. May be taken multiple times for different attributes.
- **L2:** (No second level — repeatable instead.)
- *src:* `book/Worlds-Without-Number-Deluxe/02-Character-Creation.md#L700`

### Diplomatic Grace
- **L1:** Gain Convince. Speak all common regional languages (learn new in a week, fluent in a month); reroll 1s on negotiation/diplomacy dice.
- **L2:** Once/day, consecrate a bargain; the other party must Mental save to break it (most NPCs won't try). Must be specific and time-limited.
- *src:* `book/Worlds-Without-Number-Deluxe/02-Character-Creation.md#L708`

### Gifted Chirurgeon
- **L1:** Gain Heal. Stabilize one adjacent Mortally Wounded person/round On Turn; roll Heal checks 3d6-drop-lowest; double post-battle first aid healing.
- **L2:** Your healing counts as magical: heal 1d6 + Heal to an adjacent ally as a Main action (+1 Strain), reviving without Frailty.
- *src:* `book/Worlds-Without-Number-Deluxe/02-Character-Creation.md#L714`

### Henchkeeper
- **L1:** Gain Lead. Recruit loyal henchmen (one per 3 levels) within a day of arriving; they escort and risk danger but won't fight except to save themselves.
- **L2:** Henchmen will fight for you (treated as Veteran Soldiers); capable NPCs can become henchmen if you've earned their loyalty.
- *src:* `book/Worlds-Without-Number-Deluxe/02-Character-Creation.md#L722`

### Impervious Defense
- **L1:** Innate Armor Class of 15 + half your level (round up). Doesn't stack with armor, but Dex and shield modifiers apply.
- **L2:** Once/day, as an Instant, shrug off a single weapon attack or physical trauma (not environmental/falling damage).
- *src:* `book/Worlds-Without-Number-Deluxe/02-Character-Creation.md#L732`

### Impostor
- **L1:** Gain Perform or Sneak. Once/scene reroll a failed disguise/imposture check; hold one flawless minor false identity.
- **L2:** Swap between three chosen appearances with a Main action; establish a new false identity in each community you spend a day in.
- *src:* `book/Worlds-Without-Number-Deluxe/02-Character-Creation.md#L740`

### Lucky
- **Level req:** An attribute modifier of -1 or worse
- **L1:** Once/week, a blow or effect that would kill, Mortally Wound, or disable you simply fails. Roll games of chance twice, take the better.
- **L2:** Once/session in peril, roll 1d6: on 2+ something fortunate happens; on a 1 the situation gets much worse.
- *src:* `book/Worlds-Without-Number-Deluxe/02-Character-Creation.md#L750`

### Nullifier
- **Level req:** Not Mage/Partial Mage
- **L1:** You and allies within 20' get +2 saves vs magic; sense magic within 20' On Turn; your first failed save vs magic each day becomes a success.
- **L2:** Once/day, as an Instant, be simply unaffected by an unwanted magical effect or monstrous power, even one with no save.
- *src:* `book/Worlds-Without-Number-Deluxe/02-Character-Creation.md#L758`

### Poisoner
- **L1:** Gain Heal. Reroll failed saves vs poison; brew toxins (one dose/level) dealing 2d6 + level on a hit/Shock, Physical save for half.
- **L2:** Immune to poison; universal antidote; -Heal penalty to detect/save vs your poisons; ingested poisons count as Execution Attacks.
- *src:* `book/Worlds-Without-Number-Deluxe/02-Character-Creation.md#L766`

### Polymath
- **Level req:** Expert/Partial Expert only
- **L1:** Gain any one skill. Treat all non-combat skills as at least level-0 for checks, even ones you lack. (Phantom levels don't stack/discount.)
- **L2:** Treat all non-combat skills as at least level-1 for checks.
- *src:* `book/Worlds-Without-Number-Deluxe/02-Character-Creation.md#L772`

### Rider
- **L1:** Gain Ride. Your steeds count as Morale 12, use your AC if better, and travel 50% further/day; intuitively communicate with riding beasts.
- **L2:** Once/scene negate an attack on your steed (Instant); reroll a failed Ride check; telepathic link with a bonded steed within 200'.
- *src:* `book/Worlds-Without-Number-Deluxe/02-Character-Creation.md#L780`

### Shocking Assault
- **L1:** Gain Punch or Stab. Your weapon's Shock treats all targets as AC 10 (if it can harm them and they aren't Shock-immune).
- **L2:** +2 to the Shock rating of all melee/unarmed attacks that do Shock.
- *src:* `book/Worlds-Without-Number-Deluxe/02-Character-Creation.md#L788`

### Sniper's Eye
- **L1:** Gain Shoot. On a ranged Execution Attack or target-shooting, roll the skill check 3d6-drop-lowest.
- **L2:** Don't miss ranged Execution Attacks; the target takes -4 on the Physical save and double damage even on a success.
- *src:* `book/Worlds-Without-Number-Deluxe/02-Character-Creation.md#L798`

### Special Origin
- **Level req:** GM permission; pick a species origin
- **L1:** Take the origin Focus for a non-human species (from the bestiary) to play that demihuman/alien kind, gaining its listed benefits.
- **L2:** (Varies by chosen origin — see the bestiary entry.)
- *src:* `book/Worlds-Without-Number-Deluxe/02-Character-Creation.md#L806`

### Specialist
- **L1:** Gain any skill (not Magic/Stab/Shoot/Punch). Roll 3d6-drop-lowest for all checks in it. May be taken for different skills.
- **L2:** Roll 4d6-drop-two-lowest for all checks in this skill.
- *src:* `book/Worlds-Without-Number-Deluxe/02-Character-Creation.md#L814`

### Spirit Familiar
- **L1:** Gain a loyal familiar (cat- to human-sized) with Evoked Servitor stats, summon/dismiss as a Main action; once/day it refreshes one Committed Effort.
- **L2:** Pick two upgrades (extra HP, an attack, a skill bonus, a second shape, flight, or speech). Repeatable for two more each time.
- *src:* `book/Worlds-Without-Number-Deluxe/02-Character-Creation.md#L822`

### Trapmaster
- **L1:** Gain Notice. Once/scene reroll a failed trap-related save/check; improvise a trap (non-lethal lose-a-round, or lethal 1d6 + 2x level) in 5 minutes.
- **L2:** Once/scene, your efforts count as Extirpate Arcana (cast as a Mage of twice your level) against a magical trap or hazard.
- *src:* `book/Worlds-Without-Number-Deluxe/02-Character-Creation.md#L842`

### Unarmed Combatant
- **L1:** Gain Punch. Unarmed damage scales with Punch (1d6 at L0 up to 1d12+1 at L4) with Shock = Punch skill vs AC 15; bind ranged-weapon foes.
- **L2:** Even on a missed Punch, deal an unmodified 1d6 plus any Shock the blow would inflict.
- *src:* `book/Worlds-Without-Number-Deluxe/02-Character-Creation.md#L852`

### Unique Gift
- **Level req:** GM agreement
- **L1:** A catch-all special power defined by player and GM together, worth one Focus pick; revisable if it proves too weak or strong.
- **L2:** (As agreed with the GM.)
- *src:* `book/Worlds-Without-Number-Deluxe/02-Character-Creation.md#L860`

### Valiant Defender
- **L1:** Gain Stab or Punch. +2 to Screen Ally checks, screen one more attacker, and once/round screen even spells/area effects (vs the attacker's Magic).
- **L2:** Your first Screen Ally check each round auto-succeeds; +2 AC while screening; screen foes as large as ogres or oxen.
- *src:* `book/Worlds-Without-Number-Deluxe/02-Character-Creation.md#L868`

### Well Met
- **L1:** Reaction rolls get +1 while you're present; even hostile beings usually grant a round of parley first. Works once per target.
- **L2:** Once/session, make a subject as friendly and helpful as plausibly possible when a reaction roll is made.
- *src:* `book/Worlds-Without-Number-Deluxe/02-Character-Creation.md#L876`

### Whirlwind Assault
- **L1:** Gain Stab. Once/scene, as an On Turn action, apply your Shock damage to all foes in melee range susceptible to it.
- **L2:** The first time you kill someone in a round with a normal attack, instantly gain a second attack on any target in range.
- *src:* `book/Worlds-Without-Number-Deluxe/02-Character-Creation.md#L884`

### Xenoblooded
- **Level req:** GM permission
- **L1:** Pick one alien-heritage benefit: heat/smoke immunity; water-adaptation; heavy/light-gravity attribute shift; or need no food/sleep/air + see in the dark.
- **L2:** (No second level — a single heritage benefit.)
- *src:* `book/Worlds-Without-Number-Deluxe/02-Character-Creation.md#L892`

### Mundane Alchemist
- *src:* `book/The-Atlas-of-the-Latter-Earth/04-Optional-Rules-and-Classes.md#L248`

### The Accursed (class)
- *src:* `book/The-Atlas-of-the-Latter-Earth/04-Optional-Rules-and-Classes.md#L411`

### The Bard (class)
- *src:* `book/The-Atlas-of-the-Latter-Earth/04-Optional-Rules-and-Classes.md#L532`

### The Mageslayer (class)
- *src:* `book/The-Atlas-of-the-Latter-Earth/04-Optional-Rules-and-Classes.md#L401`

### The Wise (class)
- *src:* `book/The-Atlas-of-the-Latter-Earth/04-Optional-Rules-and-Classes.md#L405`

### Adunic Invoker (Gyre)
- *src:* `book/Worlds-Without-Number-Deluxe/11-Arts-of-the-Gyre.md#L29`

### Darian Skinshifter (Gyre)
- *src:* `book/Worlds-Without-Number-Deluxe/11-Arts-of-the-Gyre.md#L85`

### Kistian Duelist (Gyre)
- *src:* `book/Worlds-Without-Number-Deluxe/11-Arts-of-the-Gyre.md#L170`

### Llaigisan Beastmaster (Gyre)
- *src:* `book/Worlds-Without-Number-Deluxe/11-Arts-of-the-Gyre.md#L258`

### Sarulite Blood Priest (Gyre)
- *src:* `book/Worlds-Without-Number-Deluxe/11-Arts-of-the-Gyre.md#L340`

### Vothite Thought Noble (Gyre)
- *src:* `book/Worlds-Without-Number-Deluxe/11-Arts-of-the-Gyre.md#L412`

### Legate Writs
- *src:* `book/Worlds-Without-Number-Deluxe/13-Legates.md#L33`



---

# PART 6 — FOCI (ATLAS / OPTIONAL)

## Atlas Foci (Optional)

*Source: `04-Optional-Rules-and-Classes.md`, lines ~838–1210. The source markdown is badly OCR-scrambled: flavor sentences and Level 1 / Level 2 bullets are interleaved and physically displaced between adjacent section headers. Each focus below has been reconstructed by matching theme/keywords. Lines whose attribution is not certain are flagged with ⚠️.*

---

### Maqqatban Knight Styles

**Intro (L840):** Scores of imperial tomb-palaces remain intact amid the ice and snow of far southern Maqqatba, and each such palace has its order of guardian knights. These knight chapters each have their own unique martial styles developed from the ancient military techniques of the First Dynasty, and sometimes the circumstances of exile or foreign curiosity bring these styles north to other lands. (Also L848: similar techniques are practiced by certain esoteric northern swordmasters and martial adepts.)

**Learning Maqqatban Styles (L850–852):** Only Warriors and Partial Warriors can learn these styles, and only one style can be learned by any wielder. A GM may allow a PC to start play with expertise in a style, but later acquisition may require finding a suitable teacher.

**Using These Foci in Your Game (L908, L912, L916):** These Foci have a distinct magical flavor and may not be appropriate for low-magic or grittier campaigns. As with any Focus, it's up to the GM whether to allow them; GMs should not feel obligated to allow them just to optimize a PC's combat skills. A GM can also use these styles as guides to create their own combat-related Foci — but a Focus should change the way the PC fights or give them new combat options, not just improve numbers they're already using.

#### Ghost Archer Style
*Flavor (L844):* You have developed a profound spiritual connection to the concept of the bow. You suffer a -4 penalty to hit with all non-bow or non-crossbow weaponry.

**L1 (L846):** Gain Shoot as a bonus skill. As an On Turn action, generate a spiritual copy of any bow you've ever fired; this copy has no encumbrance and vanishes when it leaves your hands but has all the properties of the original bow. Once a specific bow has been copied by a style practitioner, no one else can manifest that bow until the practitioner is dead. These bows generate their own magical ammunition, though the arrows have no separate hit or damage bonus. You may fire this bow normally even when meleed by a foe.

**L2 (L854):** Once per scene, as an On Turn action, shoot an arrow at any location within its range. You instantly appear where the arrow lands. Gain one System Strain when you use this ability.

#### All Directions Edge Style
*Flavor (L858):* You have exchanged a portion of your life force to master techniques of unbridled violence. Your hit die is penalized by 2 points, so if you would normally roll 1d6+2, you now roll 1d6. If you take this Focus after character creation, decrease your maximum hit points by 2 points per level to reflect this penalty.

**L1 (L866):** ⚠️ attribution uncertain — Candidate: "Gain a combat skill as a bonus skill. As an On Turn action, you may make a normal, non-grappling attack. You may do this only once per round, and after the first time you use it each day each additional use adds a single System Strain point to you." *(This L1 bullet at L866 is an orphan; the only other unclaimed Level-1 in the cluster. Theme of repeated/extra attacks ["unbridled violence"] fits All Directions Edge.)*

**L2 (L868):** ⚠️ attribution uncertain — Candidate: "Once per day, as a Main Action, attack every enemy within range once. For ranged weapons, the maximum is your Shoot skill plus one." *(An "attack every enemy" / whirlwind effect strongly matches "All Directions Edge" — attacks in all directions. This is the best-fit orphan L2.)*

#### One Point Strike Style
*Flavor (L862):* You eschew brute force or crude haste in battle, preferring to rely on clear thought.

**L1 (L864):** Gain a combat skill as a bonus skill. All your attacks use the better of your Intelligence or Wisdom modifiers in place of their usual attributes. As a Main Action, you can make a normal melee attack; it does the minimum possible damage, but your hit roll is treated as an automatic 15 on the d20 rather than rolling it. This attack cannot be used as part of a combat maneuver or grappling attempt.

**L2 (L870):** ⚠️ attribution uncertain — Candidate: "Once per scene, as an Instant action, a melee hit using this style has its weapon damage maximized." *(Maximized-damage precision strike pairs thematically with the "clear thought / auto-15 minimum-damage" L1. Best-fit orphan L2.)*

#### Pyre of Heaven Style
*Flavor (L876):* Your weapons blaze with a celestial fire that burns only your foes. This flame is fueled with your own soul's energies, however, and comes at a cost.

**L1 (L882):** Gain a combat skill as a bonus skill. You ignore the first 5 points of any fire or heat damage you suffer in a round and can glow like a torch at will. As an Instant action you may gain one System Strain to ignite your weapon, fist or ammunition for the rest of the round. While ignited, the weapon gains a damage and Shock bonus equal to your character level+2. A given foe can suffer the bonus damage from this flame only once per scene.

**L2 (L886):** As level 1, but you also become immune to non-magical flame or smoke. When you ignite, your entire body ignites as well, though you do not burn anything you do not intend to harm. You cannot be grappled while ignited. The first time you ignite in a scene, all foes within melee range take 1d6 fire damage per three levels, rounded up.

#### Catalytic Soul Style
*Flavor (L878):* Your ranged attacks catalyze the vital force of your allies, causing spiritual damage to your shared foes. This style functions only with ranged attacks that lack Shock.

**L1 (L880 + L884):** Gain Shoot as a bonus skill. While PC archers normally never accidentally hit allies when shooting into melee, your ranged attacks are actually physically intangible to your allies, and can pass through them as if they weren't there. When you make a ranged attack, nominate an ally who is within melee range of your target as an Instant action. The target suffers Shock as if it had been melee attacked by that ally, assuming it would be susceptible to the ally's Shock damage. *(L1 flavor begins at L880 "While PC archers" and continues at L884 "normally never accidentally hit allies…" — reassembled across the OCR split.)*

**L2 (L888):** If you hit the target with a ranged attack boosted by level 1 of this Focus, either you or your ally may choose to gain one System Strain and heal 2d6 damage plus the target's level or hit dice. A given subject can heal only once per scene this way.

#### Wrathful Mountain Style
*Flavor (L896):* You are a vengeful bulwark against those who would harm your allies, though your extremely defensive style comes with offensive drawbacks. You suffer a -2 penalty to all hit rolls.

**L1 (L898):** Gain Stab or Punch as a bonus skill. You can manifest a zero-encumbrance magical large shield as an Instant action, one that functions even if both your hands are occupied and persists as long as you will it. Once per round, when someone makes a melee attack on an ally you have Screened, get an Instant melee attack on them before their attack completes.

**L2 (L902):** Your melee retaliation can now be applied as a magical attack on those who make ranged attacks on your Screened ally, regardless of their distance. If you accept a point of System Strain as an Instant action, for the rest of the round you can retaliate against all enemies who attack your ward, though only once per round for any given foe.

#### Righteous Iron Style
*Flavor (L894):* You have learned to make a second skin of your armor, moving effortlessly in it despite its weight. The benefits of this style apply only when you wear heavy armor, and its level 1 benefits do not extend to shields you may carry. If taken at first level, you may begin play with a free suit of heavy armor that costs no more than 750 silver pieces.

**L1 (L900):** Gain Exert as a bonus skill. Armor you wear has a +1 bonus to its Armor Class and has no encumbrance value, though it retains it for *Armored Magic* Focus purposes. Armor does not penalize your Sneak or Exert skill checks, and you can sleep comfortably in it. You and your armor remain clean and well-maintained short of magical befouling.

**L2 (L904):** You partake of the obduracy of the steel you wear. While armored, you need not eat, drink, sleep, or breathe, and you are immune to normal climatic ranges of heat or cold. The style's armor AC bonus becomes +2 instead of +1.

#### World Tree Lance Style
*Flavor (L910):* Your spear is a pillar of heaven, and no foe is beyond its reach. This style functions only with spears, pikes, and similar polearms.

**L1 (L914):** Gain Stab as a bonus skill. The spear you wield has no encumbrance and always returns to your hand if thrown. If a spear is normally throwable, its ranges are doubled. If it isn't, it still has a thrown range of 30/60 feet. Your spear gains a +1 bonus to hit and damage and is treated as a magic weapon.

**L2 (L918):** While wielding a spear, your effective melee range is 10 feet plus your character level. Allies between you and your target do not hinder your melee attacks in any way, but a wall of enemy bodies might be sufficient to interpose. This ability does not stack with the *Long* magic weapon property.

---

### Amundi Godblood Foci

**Intro (L922, L926):** The myriad gods of Old Amund are all long-dead or vanished, but now and then some hint of their old gifts is revived in some unsuspecting man or woman. The ancient forces that once gave birth to so many divinities still bestow small but potent blessings on the occasional fortunate newborn. Some travel in recognized family lineages; many appear as unexpected outcrops in otherwise-unremarkable families. Similar gifts are found throughout the western hemisphere, suggesting the Amundi gods were not the only ones to leave fragments of their power behind.

**Learning Godblood Foci (L934–942):** Most manifest shortly after birth (often subtly), though some manifest only later in life, so a PC might pick one as a later advancement. Only one Godblood Focus can be taken by any single PC. Only full or partial Experts can take these Foci, as they all require an affinity for the subtler laws of reality. Godblood Foci may have semi-magical effects but do not count as magic for dispelling/detecting magic. Foci that grant ability-modifier increases cannot raise the modifier above +2.

**Using These Foci in Your Game (L994, L998, L1006):** These Expert-exclusive Foci are cinematic but not so impossible they couldn't be added to a relatively low-magic campaign; they help close the gap for Experts in magic-heavy parties. Additional Foci in this vein should open up play options otherwise impractical or impossible for the PC. The given Foci all have a +1 attribute modifier at second level as a sweetener, which you may omit if your own second-level power is strong enough.

#### Master Tracker
*Flavor (L930):* You have an instinctive sense for the trails of those whom you would pursue.

**L1 (L932):** Gain Survive as a bonus skill. You can follow any trail created within the past day in a city or past week in the wilderness, detecting even the minutest traces of passage and ignoring the obfuscations of weather or water. You can identify numbers of creatures from trail sign and their general physical shape and condition.

**L2 (L938):** Your senses are razor-sharp; gain a +1 bonus to your Wisdom modifier. You can identify specific people by their tracks if you've met them before. Once per day, by examining the mostly-undisturbed scene of a particular event that happened within the past week, you can reconstruct the general physical actions that happened there.

#### Night Walker
*Flavor (L948):* You have a deep affinity for evening hours and dark places, and can function well in the deepest gloom.

**L1 (L952 + L956):** Gain Sneak as a bonus skill. You can see normally in all but pitch blackness, and even when blinded your senses allow you to function as if you could see out to 30 feet around you. Your sleep is so light it is effectively wakefulness; you are fully aware of your surroundings while asleep and can wake at will. *(Reassembled across OCR split: L952 "You can see normal-" → L956 "ly in all but pitch blackness…")*

**L2 (L960):** Your adroit stealthiness is superb. Gain a +1 bonus to your Dexterity modifier. Unless an area is lit by torchlight or brighter radiance, you are effectively invisible in it until you do something to draw attention.

#### Danger Sense
*Flavor (L950):* You have a near-supernatural sense of when you are about to face an unexpected peril.

**L1 (L954 + L958):** Gain Notice as a bonus skill. You become aware of Execution Attacks on yourself or those in your presence just in time to spoil the attack. Once per day, just before you trigger a trap, walk into an ambush, or otherwise do something that would likely get you wounded or killed, you sense your danger in time to stop the action. *(Reassembled across OCR split: L954 "You become aware" → L958 "of Execution Attacks…")*

**L2 (L962):** Your awareness sharpens. Gain a +1 bonus to your Wisdom modifier. Once per day as an Instant action when in danger, you get an intuitive sense of the best course of action to get you and your allies out of the peril with minimum losses, as the GM thinks most likely.

#### Pack Beast
*Flavor (L966):* You have an ox-like capacity for carrying heavy loads over long distances.

**L1 (L970):** Gain Exert as a bonus skill. Your Strength is treated as 18 for encumbrance purposes, or 22 if it's already 18.

**L2 (L974):** Gain a +1 bonus to your Strength modifier. Once per scene, as an On Turn action, you can pick up and move an object that weighs no more than 1,000 pounds so long as you drop it or set it down by the end of your turn.

#### Folie a Deux
*Flavor (L972):* Your deceptions have such conviction that even you are temporarily convinced of them.

**L1 (L976):** Gain Convince as a bonus skill. Your lies or deceptions never register as such; spells and abilities simply read you as sincerely believing what you say. Once per day, make a listener believe that you are absolutely sincere in whatever claim or statement you are making. This belief lasts until the situation or new evidence would justify disbelief. A target becomes immune to this after the first lie is disproven.

**L2 (L924):** Your sincerity shines forth in everything you do. Gain a +1 Charisma modifier bonus. Once per day, utter a bald-faced lie to someone; unless it is physically impossible or emotionally intolerable, they must make a Mental save at a penalty equal to your Convince skill or believe it for 1d4 rounds. After that, their normal reason reasserts itself. *(Note: this L2 is displaced far upward to L924, immediately under the Godblood section intro; matched to Folie a Deux by the lie/Convince theme.)*

#### Provident Crafter
*Flavor (L984):* You always seem to have just what you need close to hand, or can fabricate it out of available materials.

**L1 (L986 + L988):** Gain Craft as a bonus skill. Your Strength is treated as 4 higher for encumbrance purposes. When making a skill check or using an item such as an elixir or calyx, any equipment or items you need to do so are treated as Readied even if you have them Stowed. *(Reassembled across OCR split: L986 "Your Strength is" → L988 "treated as 4 higher…")*

**L2 (L990):** Your hands are swift and nimble; gain +1 to your Dexterity modifier. Once per day, as an Instant action, you happen to have Stowed a particular normal item of 2 encumbrance or less if you could have reasonably bought or made it within the past week. Pay its purchase or crafting price and add it to your inventory afterwards. Provisions cannot be added this way, nor can the same item be produced more than once per week.

#### Wildtongue
*Flavor (L982):* You have a profound link with the natural world around you, and possess an instinctive sense of what its feral denizens desire. For the purposes of this Focus, "animals" are natural or magical living creatures of bestial intellect.

**L1 (L982):** Gain Survive as a bonus skill. You can communicate with animals, conveying such simple ideas as they are capable of comprehending. If appeased, these animals may be willing to do very basic favors that require no more than immediate attention.

**L2 (L992):** The primal force of your presence is considerable. Gain a +1 to your Charisma modifier. Once per day you can command a visible animal for one scene, causing it to obey even complex orders normally impossible for it to comprehend so long as they don't seem suicidal or extremely hazardous to it. Magical beasts get a Mental saving throw to resist.

#### Walk Like Wind
*Flavor (L1000):* Your astonishing acrobatic abilities give you mobility options that others lack.

**L1 (L1002):** Gain Exert as a bonus skill. Your base ground movement rate increases by +10'. You can move normally up or down vertical surfaces so long as you end your turn standing on a flat surface or clinging to a usable handhold.

**L2 (L1004):** Gain a +1 to your Dexterity modifier. You can leap up to 20 feet horizontally or 10 feet vertically as a Move action. Once per scene, as an On Turn action, gain a bonus Move action.

---

### Arcane Secret Foci

**Intro & rule (L1010–1012):** A multitude of occult traditions have risen and decayed across the ages of the Latter Earth; a few resilient techniques survive into the present. Arcane Secret Foci can be taken only by Mages and Partial Mages, and some are of no use to non-spellcasters. Only one Arcane Secret Focus can be mastered by any given sorcerer, as they usually require mutually-contradictory pacts and ritual practices.

**Using these Foci in your Game (L1044–1050):** These Foci often boost spellcasting (an extra spell/day via Hemomancy, greater subtlety via Mind-Sorcery, an easily-cast spell via Sigilism); some GMs may find them too much. Others grant a stand-alone magical power — these should be largely non-combat, to avoid stepping on Warriors, and avoid directly replicating an existing tradition's arts. **These Foci all have only one level**, as mages tend to have too few Focus picks to use two levels.

#### Atlantean Divination
*Flavor (L1016):* The House of Days in Atlantis is a school of several dozen different occult divinatory methods, all highly complex. While some techniques are strictly-held secrets, others have become known in the outside world.

**L1 (L1018):** Gain Know as a bonus skill. You may spend an hour in a complex divinatory ritual. At the end of it, ask a one-sentence question about some future event or plan. The GM secretly rolls an Int/Know skill check against difficulty 9; on a success, gain an answer of a few words reflecting the GM's best judgment of the future. On a failure, get a plausible but false oracle. This art cannot plumb the future beyond a week, cannot ask the same essential question twice, and cannot answer questions about current or past events. Each use after the first within seven days adds +1 to the difficulty. You gain one System Strain each time you use this ability.

*(No Level 2 — Arcane Secret Foci are single-level by rule.)*

#### Iteral Pacting
*Flavor (L1022):* Numerous traditions of occult pacting and bargains with extra-Iteral beings persist, despite the obvious dangers. This method is relatively safe, albeit its rewards are more limited than wholehearted soul-slavery would grant.

**L1 (L1024):** Gain Pray as a bonus skill. Roll or pick a patron portfolio from the divine portfolios on page 142 of the core rulebook. Once per day, gain 1 System Strain and gain one of the following benefits as an Instant action: +4 on a hit roll, +1 on a skill check, or the ability to use a Main Action to cast a first-level spell that has some relation to the patron's portfolio. This spellcasting does not require a prepared spell or spell slot, and can be used even by non-spellcasters, though it follows all the usual rules for casting a spell. Your alien alliances have left some eldritch mark on you and others instinctively find you disturbing; suffer a -1 penalty on all social skill checks not related to intimidation.

*(No Level 2.)*

#### Nagadi Hemomancy
*Flavor (L1028):* The vanished demihumans known as the Nagadi practiced bloody rituals of self-sacrifice for the protection of their people and the forestalling of violence. Modern mages rarely share their devotion to peace.

**L1 (L1030):** Gain Heal as a bonus skill. Once per day, as an Instant action after casting a spell, accept 1d4 damage per level of the spell; the casting does not count against your usable spells per day. Gain one System Strain each time this ability is used. This Focus cannot assist spells that harm others or affect unwilling targets.

*(No Level 2.)*

#### Old Empire Sigilism
*Flavor (L1034):* The vanished Marchen empire of northeastern Agathon is almost wholly lost to history, but this art of imbuing small tokens with magical power has yet survived.

**L1 (L1036):** You can embed spells in small tokens that function as calyxes only usable by yourself. Creating such a token takes ten minutes per level of the spell and the expenditure of a normal daily spell use. This expended slot may be recovered normally. Using them takes a Main Action, but the sigil need only be presented firmly; no vocalization or gestures are required, and it cannot be interrupted by damage. Only one token can be empowered at any one time.

*(No Level 2.)*

#### Vothite Mind-Sorcery
*Flavor (L1040):* The Thought Noble tradition of mental arts is not the only technique to have survived from the Vothite Empire. The principles of purely cerebral sorcery are also practiced by some mages, though it comes at a cost to their ability to inflict direct harm on other creatures.

**L1 (L1042):** Your spellcasting does not require vocalizations or gestures, though it still takes a Main Action, it still can be disrupted by damage, and it still disallows casting in armor for most spellcasters. Your spells manifest without any obvious connection to you unless your actions make it clear that you are the source of the magic, though those with magic-detecting powers such as *Apprehend the Arcane Form* can discern the connection. Once this Focus is taken, however, you cannot cast any spell that inflicts hit point damage on a target unless the damage is purely mental in nature. Spells that inflict non-mental damage as a secondary spell effect simply do not inflict it when cast.

*(No Level 2.)*

---

### Non-Human Origin Foci

**Intro (L1054):** There are numerous demihumans and even some Blighted who might fit as player characters in a given campaign. While adventurers wander far from home, it's up to the GM to decide whether any particular origin Focus is appropriate for their campaign setting.

**Origin Foci and Modifiers (L1062–1070):** Many origin Foci grant a bonus or penalty to one of the PC's attribute modifiers. Some let the PC choose which attribute to modify, but in no case can the Focus increase an attribute bonus above +2 or a penalty below -2. Some origin Foci mention special abilities; these are described more thoroughly in the Bestiary section under their creature headings.

**Creating New Origin Foci (L1198–1210):** The Latter Earth is wide; GMs may want to make origin Foci for unlisted demihumans. Guidelines: (1) Don't do it unless you need to. (2) Start with a bonus skill characteristic of their physiology/upbringing (or two to choose between). (3) Set their attribute modifiers (+1 / -1 each, never above +2 or below -2, preferably offering a choice of two). (4) Add a unique ability a human can't do (special senses, movement, immunity, innate power); strong/general ones should have per-scene or per-day limits or add System Strain. (5) Add a weakness if necessary, kept generally relevant rather than concept-specific.

*Note: The original task focused on Choeru Beastfolk + the "Origin Foci and Modifiers" rule, but the section actually contains a long roster of origin Foci (each single-level). All are listed below for completeness.*

#### Choeru Beastfolk
*Flavor (L1058):* Short, stout, and mild-tempered, the capybara-folk have a natural disposition towards peacemaking and diplomacy.

**L1 (L1060):** Gain Convince or Connect as a bonus skill. Gain a +1 to your Cha modifier. When rolling Reaction Rolls with you present, add +1 to the dice. You can obtain serviceable fluency in a language with no more than a week of exposure to it.

#### Ghoul
*Flavor (L1068):* You have been infected with ghoulishness by long contact with ghouls or sheer bad luck on briefer exposures. While your new dietary demands are harsh, you have enough self-possession to decide how they should be satisfied.

**L1 (L1074):** You must eat a pound of fresh human flesh a month, but gain Sneak as a bonus skill, the benefits of *Ghoulish Vigor*, and may add a +1 bonus to either your Strength or Dexterity modifier. After 21 days without cannibalism, make a Mental save daily or attack the nearest human with the intent to devour them. This condition is automatic after 30 days.

#### !Man
*Flavor (L1076):* You are an organic simulacrum of humanity that operates purely by algorithmic principles and the translated mimicry of future or past human actions. You have no personal awareness or consciousness, but you act exactly like a normal human being, with normal human motivations.

**L1 (L1076 + L1078):** Pick any skill but Magic as a bonus skill. Once per day, your algorithm picks a particularly successful action to mimic and you gain a +1 bonus on a skill check or a +2 bonus to hit as an Instant action. You are impervious to mind-affecting magical effects. You otherwise function as a perfectly normal human being, and do not have the usual qualities of an automaton.

#### Guer Beastfolk
*Flavor (L1082):* Cunning humanoid swamp foxes, the Guer were made to be spies and observers for their Nakadi creators. It leaves many of them with insatiable curiosity and a tendency towards manipulativeness.

**L1 (L1084):** Gain Notice or Sneak as a bonus skill. Gain +1 to your Wis or Cha modifiers. You can see clearly in low-light conditions and are unusually quick on your feet, adding 10' to your ground movement rate.

#### Accipiter Anak
*Flavor (L1088):* You are a winged Anak, usually hideous in appearance, though some of your kind are quite handsome. By some quirk of nature or the circumstances of your tribe, you are capable of functioning rationally around humans. This origin assumes the GM has produced some justification for your PC avoiding immediate mob violence at the hands of panicked locals.

**L1 (L1094 + L1100):** Gain Exert as a bonus skill. You are an accipiter, with the *Accipiter Flight* special ability, a -1 Con modifier penalty, and a +1 Dex modifier bonus. *(Reassembled across OCR split: L1094 "Gain Exert as a bonus skill. You are an accipiter," → L1100 "with the Accipiter Flight special ability…")*

#### Harbinger Anak
*Flavor (L1092):* You are a Harbinger, a face-shifting Anak capable of infiltrating human society. Whether by some chance of fate or your own indomitable will, you can contain the Hate and function normally in human society.

**L1 (L1096 + L1098):** Gain Sneak or Convince as a bonus skill and the *Harbinger's Face* ability. Gain a +1 bonus to your Charisma modifier and a -1 penalty to your Constitution modifier. *(Reassembled across OCR split: L1096 → L1098.)*

#### Aristoi Anak
*Flavor (L1106):* You are a natural-born ruler of men, the product of an extensive magical eugenic breeding program. While not so physically powerful as other breeds of Anak, you have an uncannily acute sense of judgment and superb self-discipline.

**L1 (L1110):** Gain Lead and any one other skill except Magic as bonus skills. Gain +1 to your Wis modifier. Your keen foresight allows you to use Wis as an applicable attribute for any weapon, in place of Strength or Dexterity.

#### Hua Beastfolk
*Flavor (L1108):* A mighty bullfolk created for agricultural labor and meat for the temple tables, Hua are a foot taller than baselines and much broader in build. Most have horns, but they are largely impractical for combat use.

**L1 (L1112):** Gain Exert as a bonus skill. Gain a +1 to your Str modifier and -1 to your Dex modifier. You treat your Strength as 4 higher than normal for Encumbrance purposes and your System Strain maximum is 2 points higher than normal.

#### Kitsune Beastfolk
*Flavor (L1116):* You are of the magically-gifted Xindai kin to the Guer fox-folk of Runom. Your pelt is usually brighter and ruddier than that of your swamp-dwelling cousins, and you are often more human in appearance, but almost all your kind retain the tail and ears of a fox.

**L1 (L1118 + L1120):** Gain Notice or Convince as a bonus skill. Gain a +1 bonus to your Charisma modifier. Gain the *Elemental Sparks* Elementalist art; if you already have it, pick a bonus Elementalist art instead. *(Reassembled across OCR split: L1118 → L1120.)*

#### Deepfolk
*Flavor (L1124):* A human native of the Far Deeps that lie among the roots of the world, you have ascended into the lethal sunlit regions for reasons of your own. So long as you remain fully covered and have your tinted goggles in place you can tolerate the sun, but extended exposure can cause incapacitating spiritual damage to you.

**L1 (L1126 + L1128):** You can see clearly with any degree of light. You require only half the food, water, and air of a baseline human. You may raise one physical attribute to 14 if it is lower than that. Exposure of your eyes or more than a handsbreadth of skin to direct sunlight forces a Physical save each round or you will gain one System Strain; if this would put you over your maximum, you will collapse, dying in 1d6 minutes if not covered. *(Reassembled across OCR split: L1126 → L1128.)*

#### Manu Beastfolk
*Flavor (L1132):* The Manu are scaled lizardfolk of the Zapalla swamps in Runom, not entirely cold-blooded but much favoring warmth.

**L1 (L1134):** Gain Exert or Survive as a bonus skill. Gain a +1 to your Con or Str modifier and a -1 to your Dex or Cha modifier. You swim at your normal movement speed, can hold your breath for fifteen minutes, and your tough hide reduces all Shock damage by 1 point, to a minimum of 1.

#### Nahu Beastfolk
*Flavor (L1138):* Slim, deft, and sometimes given to a cold-blooded pleasure in cruelty, the Nahu are catfolk who were designed to hunt fleeing slaves or troublesome escaped beasts by their Nakadi masters.

**L1 (L1140):** Gain Sneak or Notice as a bonus skill. Gain +1 to your Dex or Cha modifiers. Your claws count as daggers for melee purposes and you can see clearly in low-light conditions. During real combat, you must make a Mental save to inflict non-lethal damage; on a failure, your attack is lethal instead.

#### Oni
*Flavor (L1144):* You are an oni, most likely from one of the isolated communities in Xindai. You likely stand about seven feet tall, horned and powerfully muscled, with a fierce appetite for indulgences of all kinds. Many of your sort are bright red or blue, though more human-like shades are known, as are other small novelties of form.

**L1 (L1146):** Gain Stab or Punch as a bonus skill. Gain a +1 to your Strength modifier and count your Strength as 4 points higher for Encumbrance purposes. Suffer a -1 penalty to your Wisdom modifier and a -2 penalty on all Mental saving throws.

#### Pichi Beastfolk
*Flavor (L1150):* Little ratfolk, usually a head shorter than baselines, with a more slender build. Their keen senses were given them to hunt rare materials and ingredients from the jungle.

**L1 (L1150 + L1152):** Gain Notice as a bonus skill. Gain +1 to your Wis or Dex modifiers and -1 to your Str or Con modifier. You can see normally in low-light conditions. Your senses are sharp enough that you can interact with objects within ten feet as if sighted, even in pitch blackness or while blinded. *(Reassembled across OCR split: L1150 → L1152.)*

#### Piren Beastfolk
*Flavor (L1156):* Fierce wolfmen, created as warriors and enforcers for their masters against unruly slaves. Even so, they have an instinct towards cooperation within their own social circles.

**L1 (L1158):** Gain Exert as a bonus skill. Once per scene as a Move action, give an ally within melee distance a bonus Main Action as you coordinate with them. This Main Action can only be used for a physical act, not spellcasting or magic item activation. A given ally can receive this benefit only once per scene.

#### Still Cities Undead
*Flavor (L1162):* You are one of the more intelligent undead from the Still Cities, either a recent conversion from the living or having died only a few times since you were created. You appear human at first glance but close inspection makes plain your cold flesh, though you can mimic most human needs and activities.

**L1 (L1164):** You are undead, and do not need to eat, sleep, drink, or breathe, though you still require eight hours of comfortable quiet to regain HP, spells, or Effort. You can be healed by conventional methods, and are immune to poisons and diseases. You automatically stabilize at zero hit points unless decapitated or otherwise mangled. If you do die, it will be decades until you revive, if intact, or centuries if you are burnt and scattered. Due to your link with the Pale Emperor's power, you do not count as undead for conventional Necromancer spells. Special incantations may exist that affect you, however.

#### Sui Beastfolk
*Flavor (L1168):* These robust pigfolk were created by the Nakadi priests to be good spiritual and anatomical matches for their experiments. Some suffer from great rages when wounded or infuriated, during which they attack without care for friend or foe.

**L1 (L1170):** Gain Survive as a bonus skill. Gain +1 to your Constitution modifier. You are immune to mundane poisons, and once per day you can continue acting for 1 full round after falling to zero hit points, provided you are not hopelessly mangled. This time counts against your stabilization timer.

#### Tanuki Beastfolk
*Flavor (L1174):* A beastfolk unique to Xindai, these raccoon-dog humanoids were the product of an inquisitive Nakadi exile who hoped to create a shapeshifting species for multiple purposes. While an unsuccessful experiment, their heirs can still be found in Xindai's mountain forests.

**L1 (L1174 + L1176):** Gain Sneak as a bonus skill. You can climb scalable surfaces at your full movement rate, and once per day as a Main Action you can transform as if with the *Adopt the Simulacular Visage* spell, albeit without its language-granting powers. This transformation lasts up to two hours per level. *(Reassembled across OCR split: L1174 → L1176.)*

#### Tengu Beastfolk
*Flavor (L1180):* A winged crow-folk once the pet project of their exiled Nakadi creator, found chiefly in a few remaining martial monastery-communities in Xindai. Like other beastfolk, their appearance ranges from humanoid avians to almost completely human forms, save for their black-feathered wings.

**L1 (L1182):** Gain Stab as a bonus skill. You can fly at a movement rate of 30' outdoors while carrying your normal encumbrance, but interiors are too cramped for it, and you cannot fight or perform other complex actions while flying. Flight is too exhausting to manage long-distance overland travel.

#### Usagi Beastfolk
*Flavor (L1186):* Largely extinct in Runom, several colonies of these rabbit-folk can still be found in the Xindai lands. Their creators devised them as livestock that could better survive jungle dangers, imbuing them with both speed and a strange propensity towards good fortune.

**L1 (L1188 + L1190):** Gain Exert or Sneak as a bonus skill and a +1 bonus to all saving throws. Gain +1 Dex modifier and either a -1 Str or -1 Con modifier. Once per scene, as an On Turn action, double your ground movement rate for the round. Once per week, as an Instant action, automatically make a Luck save. *(Reassembled across OCR split: L1188 → L1190.)*

#### Zakathi
*Flavor (L1194):* As much as a foot taller than baselines and well-toned from their constant exertions, the Zakathi need for constant labor tends to wear them down. Most are crippled beyond conventional healing aid before sixty, whereupon they wither away or accept euthanasia.

**L1 (L1196):** Gain Exert as a bonus skill. If your Constitution is lower than 14, raise it to 14; if equal or higher, raise it to 18. Your maximum System Strain increases by 2. You must exhaust yourself with labor or other exertions by the end of a day to regain System Strain, Effort, HP, or spells with sleep; lacking this, you gain 1 System Strain overnight instead, dying if it exceeds your maximum. While exhausted, roll all hit and skill rolls twice and take the worst.

---

### OCR-reconstruction notes / open questions

- **All Directions Edge Style** has NO clearly-labeled flavor-adjacent bullets in the source; its L1 (L866) and L2 (L868) are orphan bullets matched by theme. The "attack every enemy within range" L2 (L868) is a strong thematic fit ("all directions"), but both bullets are flagged ⚠️.
- **One Point Strike Style L2 (L870)** "maximized weapon damage" is an orphan matched by elimination/theme; flagged ⚠️. (The L1 at L864 is explicit and certain.)
- Within the One Point Strike / All Directions cluster (L864–L870) there are exactly two L1 and two L2 orphans serving two styles. L864 is unambiguously One Point Strike (auto-15, Int/Wis attacks). The remaining three (L866 L1, L868 L2, L870 L2) were assigned: L866→All Directions L1, L868→All Directions L2, L870→One Point Strike L2. This is the most coherent reading but the L2 assignments are the uncertain ones.
- Pyre of Heaven (L876 flavor "fire that burns only your foes") and Catalytic Soul (L878 flavor "ranged attacks catalyze allies' vital force") had their flavor lines swapped relative to header order; reassigned by keyword. Their L1/L2 bullets (L880/882/884/886/888) likewise interleave and were matched by keyword (fire/ignite → Pyre; ranged/ally/heal → Catalytic).
