# Magic and Effort — caster card

> Use this when: a PC casts a spell or uses an Art, you need to adjudicate Effort, spell slots, or casting in combat, or you're statting a caster NPC. WWN magic is artillery, not snipers — powerful, loud, and limited. Run it straight.

**Spells and Arts are pulled verbatim from data, not memory:** `python3 scripts/lookup.py spell <name>` (all 52 High Magic spells + every named tradition Art + the Elementalist/Necromancer New Magic spells) and `python3 scripts/lookup.py focus <name>`.

## Spells vs Arts — two separate resources
- **Spells** are the mighty inherited **High Magic** (circles 1–5, ~52 of them) plus a tradition's **New Magic** spells. Vancian: learned into a grimoire, prepared, then cast from a daily pool. Always big — even a 1st-circle spell can kill.
- **Arts** are a tradition's lesser, repeatable tricks, fueled by **Effort** (a wholly separate pool from spell slots). A mage out of spells for the day may still have Effort. Once an Art is picked at level-up it's permanent.

## Effort
- **Score = 1 + Magic-skill level + better of Int or Cha modifier.** (Partial Mage −1, min 1. Healers use **Heal** not Magic; Vowed use their order's chosen skill — Exert/Know/Pray/Magic.)
- Using an Art **Commits** one point of Effort, returned after a set duration:
  - **Commit for the day** — returns after a night's rest (powerful Arts).
  - **Commit for the scene** — returns when the scene ends (modest Arts).
  - **Commit indefinitely** — stays Committed to keep a persistent Art on; reclaim it as an Instant action to switch the Art off. Ends instantly if you're knocked out or killed.
- Only **one point** per Art unless it says otherwise. **Each tradition has its own Effort pool** — a dual-tradition Adventurer can't spend one tradition's Effort on the other's Arts.

## Vancian spell slots
- **Learn** a spell (into the grimoire): one week per spell level, −1 week per Magic level, min 1 day; you must be able to cast that circle to learn it. Keep the written copy or you can't prepare it.
- **Prepare** a set after a night's rest (1 hour); they stay prepared until you swap them. Slots scale with level — roughly **2–3 prepared at level 1 up to ~12 at level 10**; you may fill them with any mix of circles you can cast.
- **Cast** from a separate daily limit (≈ **1/day novice → ~6/day master**); pick any prepared spell, repeatable while castings remain.

## Casting in combat
- A spell is a **Main Action** + at least one free hand + audible incantation (onlookers can tell it's magic, not which spell).
- **Disrupted by damage:** if the caster took HP damage (or was badly jostled) that round, they **cannot cast** that round — acting late is risky. (The High Mage's *Iron Resolution* and *Restrained Casting* Arts mitigate this.)
- **No armor:** High Mages, Elementalists, Necromancers, and Vowed **can't cast or use Arts in armor or with a shield** (the *Armored Magic* focus lifts this). **Healers are the exception** — their Arts work freely in armor.

## Tradition roster (one line each)
- **High Mage** — the orthodox wizard; casts High Magic and has Arts that bend, shield, and counter spellcasting itself. Magic-based Effort. (L172)
- **Elementalist** — masters earth/fire/wind/water; casts High Magic + Elementalist New Magic; auto-gains *Elemental Resilience* + *Elemental Sparks*. Magic-based Effort. (L587)
- **Healer** — partial-class mender; **no spells**, only healing Arts (auto *Healing Touch*); works in armor. **Heal**-based Effort. (L763)
- **Necromancer** — broker of life and death; casts High Magic + Necromancer New Magic, raises and commands the dead. Magic-based Effort. (L839)
- **Vowed** — partial-class body-adept/monk; **no spells**, only inner-power Arts (auto *Martial Style*, *Unarmed Might*, *Unarmored Defense*). Effort from the order's skill. (L1016)

**Pointers (not encoded here — go to the chapter):** the six **Gyre traditions** (Adunic Invoker, Darian Skinshifter, Kistian Duelist, Llaigisan Beastmaster, Sarulite Blood Priest, Vothite Thought Noble) in `book/Worlds-Without-Number-Deluxe/11-Arts-of-the-Gyre.md`; **Legate Writs** (Might/Skill/Sorcery/Mastery, on Legate Effort) in `book/Worlds-Without-Number-Deluxe/13-Legates.md`; the **Atlas casters** (Accursed, Bard, Mageslayer, Wise + the Arcane Secret / specialist foci) in `book/The-Atlas-of-the-Latter-Earth/04-Optional-Rules-and-Classes.md`. The lookup `foci.json` carries name+page stubs for all of these.

**Spell research / item creation (costs only):** new spell — lab + materials + time scaling 50k sp / 1 month (L1) up to 1M sp / 2 years (L5), then an Int/Magic check vs 10+circle. Workings — caster L6+, 1,000 sp/difficulty point. Magic items — 250 sp single-use up to 250k sp for a powerful item, always +1 component-fetching adventure. Full tables in `05 - Magic.md` L1107–1321.

Source: `book/Worlds-Without-Number-Deluxe/05-Magic.md` (Spells vs Arts L33–46; prepare/cast L47–71; targets/visibility L73–79; Arts & Effort L81–103; High Magic spell list L148–170; High Mage L172–256; Elementalist L587–760; Healer L763–837; Necromancer L839–1014; Vowed L1016–1101; research/Workings/items L1107–1321).
