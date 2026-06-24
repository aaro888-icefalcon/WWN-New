#!/usr/bin/env python3
"""
build_magic.py — Magic-layer lookup builder for the Worlds Without Number
companion that rides on the mythic-gm engine.

Emits two machine-readable lookup files into ../bridge/generators/ that a
central lookup.py consumes (`python3 scripts/lookup.py spell|focus <name>`):

  spells.json  — the full High Magic spell list (52 spells, circles 1-5) PLUS
                 one entry per *named Art* of the four book traditions that have
                 them (Elementalist, Healer, Necromancer, Vowed) and their
                 tradition-specific New Magic spells.  Arts are tagged
                 type:"<Tradition> Art"; New Magic spells type:"<Tradition>".
  foci.json    — all 35 core character Foci (level-1 / level-2 effects, concise)
                 PLUS name+page pointers to the special Foci/classes of the
                 Atlas, the Arts of the Gyre, and the Legate Writs (not fully
                 encoded — use the book chapter via the cited page).

Schema (both files), exactly as the lookup.py consumer expects:

  { "id":"wwn.spells", "kind":"lookup", "category":"spell", "key":"name",
    "records": { "<Name>": { ...fields... }, ... } }

Spell record fields: circle (int), type, effect, dice, duration, page.
Focus  record fields: level_req, level_1, level_2, page  (pointer foci carry
                      a "pointer": true flag and just name+effect+page).

Effects are deliberately concise (1-2 sentences) GM-table paraphrases, NOT the
full book text — the page pointer is the source of record.

Re-runnable / idempotent: rewrites both target files from the data below on
every run, and prints a count summary.

Std-lib only; Python 3.6+.

USAGE
  python3 scripts/build_magic.py            # build both files, print summary
  python3 scripts/build_magic.py --quiet    # build, print only the OK line
"""
import json
import os
import sys

# ---------------------------------------------------------------------------
# Paths.  Resolve relative to this file so the script runs from anywhere.
# ---------------------------------------------------------------------------
HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(HERE)
OUT_DIR = os.path.join(SKILL_ROOT, "bridge", "generators")

# Book chapter the page pointers reference.
MAGIC = "book/Worlds Without Number Deluxe/05 - Magic.md"
CHARGEN = "book/Worlds Without Number Deluxe/02 - Character Creation.md"
GYRE = "book/Worlds Without Number Deluxe/11 - Arts of the Gyre.md"
LEGATES = "book/Worlds Without Number Deluxe/13 - Legates.md"
ATLAS04 = "book/The Atlas of the Latter Earth/04 - Optional Rules and Classes.md"


def _pg(chapter, line):
    return f"{chapter}#L{line}"


# ===========================================================================
# HIGH MAGIC SPELLS — 52, circles 1-5.  effect = concise paraphrase.
# dice = damage/scaling die or "—".  Page lines point into 05 - Magic.md.
# ===========================================================================
HIGH_MAGIC = {
    # ---- First Level (13) ----
    "Apprehending the Arcane Form": dict(
        circle=1, effect="See active magic, curses, and enchanted items as auras (1-sentence read); also see in total darkness.",
        dice="—", duration="15 min/level", line=277),
    "Cognitive Supersession of the Inferior Orders": dict(
        circle=1, effect="Telepathically bond with and command one visible normal animal, sharing its senses. It obeys non-suicidal orders but won't fight.",
        dice="—", duration="Until released/dispelled", line=307),
    "The Coruscating Coffin": dict(
        circle=1, effect="One visible creature within 100'/level takes 1d8/level, Physical save for half. 1-HD NPC foes die outright. Ignores non-magical cover.",
        dice="1d8/level", duration="Instant", line=333),
    "Damnation of the Sense": dict(
        circle=1, effect="Seize control of one sense of a visible creature (blind, deafen, feed false impressions). Mental save; failure = whole scene, success = 1 round.",
        dice="—", duration="Scene (save: 1 round)", line=339),
    "Decree of Ligneous Dissolution": dict(
        circle=1, effect="Annihilate all non-magical plant/fungus matter (wood, rope, cloth) in up to 1 cube/level. Plant-monsters take 1d10/level, Physical save for half.",
        dice="1d10/level vs plants", duration="Instant", line=351),
    "The Excellent Transpicuous Transformation": dict(
        circle=1, effect="Turn up to one willing target/level invisible. Breaks for all if any subject runs, attacks, or casts.",
        dice="—", duration="1 hour/level", line=387),
    "Imperceptible Cerebral Divulgence": dict(
        circle=1, effect="Read a visible creature's surface thoughts and query its memories (1 question/level; each risks ending it on a Mental save). Cast subtly, no gestures.",
        dice="—", duration="Scene", line=433),
    "Ineluctable Shackles of Volition": dict(
        circle=1, effect="Enthrall a visible creature's will (Mental save at -Magic). It obeys non-suicidal physical commands but appears dazed; recasting frees prior thralls.",
        dice="—", duration="Until released/dispelled", line=439),
    "The Long Amber Moment": dict(
        circle=1, effect="On Turn: put a touched willing/helpless creature into invulnerable temporal stasis, immune to non-magical harm.",
        dice="—", duration="Up to 1 day/level", line=467),
    "Phantasmal Mimesis": dict(
        circle=1, effect="Create a self-acting multi-sensory illusion in up to 1 cube/level. Illusory attackers hit with caster's bonus for 1d8, vanish if struck; disbelief allows a Mental save.",
        dice="1d8 illusory", duration="Until dropped/dispelled", line=497),
    "Velocitous Imbuement": dict(
        circle=1, effect="On Turn: up to one willing target/level doubles ground move, can run on walls/ceilings and leave melee freely. +1 System Strain to users.",
        dice="—", duration="Scene", line=557),
    "Wardpact Invocation": dict(
        circle=1, effect="Either make a creature partly weapon-immune (hits need a Physical save to land, 1 round/2 levels) OR render one visible weapon harmless for the scene.",
        dice="—", duration="1 round/2 levels or scene", line=565),
    "The Wind of the Final Repose": dict(
        circle=1, effect="Living creatures of 4 HD or fewer in a 20' radius fall asleep; roused by damage or a Main Action, else wake at scene's end.",
        dice="—", duration="Scene", line=575),

    # ---- Second Level (12) ----
    "Calculation of the Evoked Servitor": dict(
        circle=2, effect="Summon an intelligent familiar (1 HP/level, AC 14, no attack) that obeys any order, even suicidal, and shares a telepathic bond. Can be re-summoned if slain.",
        dice="—", duration="Until dawn/dismissed", line=265),
    "Casting Forth the Inner Eye": dict(
        circle=2, effect="Scry a distant location through a reflective/luminous surface (within 100'/level or a place you've been). Warded sites are immune; can't repeat a site within a week.",
        dice="—", duration="While concentrating", line=299),
    "Conjunction of the Inexorable Step": dict(
        circle=2, effect="Teleport a visible creature or loose object (<= horse) within 100' to a visible safe spot within a half-mile. Unwilling targets get a Mental save (success swaps the caster instead).",
        dice="—", duration="Instant", line=319),
    "Decree of Lithic Dissolution": dict(
        circle=2, effect="Reduce all non-magical stone/earth/mineral in up to 1 cube/level to dust (metal unaffected); may collapse structures. Rock-monsters take 1d10/level, save for half.",
        dice="1d10/level vs rock", duration="Instant", line=357),
    "Extirpate Arcana": dict(
        circle=2, effect="Dispel unwanted magic in a 20' radius. Auto-negates effects from equal/lower-HD casters; else a contested Magic check (higher level +2). Standing magics only suppressed 1d6 rounds.",
        dice="—", duration="Instant (suppress 1d6 rds)", line=401),
    "The Inexorable Imputation": dict(
        circle=2, effect="Make a one-sentence statement; all who hear within 40' must Mental save or believe it (unless impossible or abhorrent). Exempt 2 allies/level.",
        dice="—", duration="1 hour/level belief", line=447),
    "Jade Palanquin of the Faceless God": dict(
        circle=2, effect="Conjure a floating 12'x8' stone palanquin that bears up to 2,000 lb at shoulder height; pulled by one bearer.",
        dice="—", duration="Until dusk/dawn or struck", line=457),
    "Mantle of Disjecting Dissection": dict(
        circle=2, effect="A willing creature is wreathed in blade-shards; anyone touching/meleeing them makes an Evasion save or takes 1d6+level first. Indiscriminate (hits allies too).",
        dice="1d6+level", duration="Scene (give up Move/rd)", line=473),
    "Prudentially Transient Abnegation of Life": dict(
        circle=2, effect="Instant: a target dropped to 0 HP appears gorily dead to all examination, then revives within 2 hours at 2 HP/level (+2 Strain). Destroyed remains can't revive.",
        dice="—", duration="Up to 2 hours", line=503),
    "Resounding Temporal Echo": dict(
        circle=2, effect="Up to one ally/level gains an extra Main Action (not for casting) for 1d4+1 rounds; +1 System Strain per round the bonus is used.",
        dice="—", duration="1d4+1 rounds", line=521),
    "The Verdant Vallation": dict(
        circle=2, effect="Grow a 20'-high, 3'-thick wall of vines up to 20'/level wide; 5 HP/level to cut through, optional thorns deal 2d6 to climbers. Persists if rooted in good earth.",
        dice="2d6 thorns", duration="Scene or permanent if planted", line=563),
    "Visitation of the Clement Clime": dict(
        circle=2, effect="Caster and up to 3 allies/level become immune to mundane heat/cold/acid/electricity; half (or no) damage from magical versions.",
        dice="—", duration="1 hour/level", line=581),

    # ---- Third Level (11) ----
    "Adopt the Simulacular Visage": dict(
        circle=3, effect="Transform up to one willing target/level into a perfect simulacrum of any humanoid seen (voice, scent, clothing, language). No special abilities granted.",
        dice="—", duration="Until next dawn", line=271),
    "Conjunct the Vital Viscera": dict(
        circle=3, effect="Render up to one subject/level plastic: transfer HP, poisons, diseases, or body parts between willing/bound creatures; a willing target can be absorbed into another.",
        dice="—", duration="1 hour/level", line=313),
    "Exhalation of Congelating Cold": dict(
        circle=3, effect="Freeze a radius of 10'/level; living creatures take 1d6/2 levels (Physical save half), liquids freeze 2' deep. Failed save = lose Move action 1d4 rounds.",
        dice="1d6/2 levels", duration="Instant (thaws naturally)", line=395),
    "Foresightful Apprehension": dict(
        circle=3, effect="Describe an intended action; the GM tells you the most likely outcome within the next 5 minutes. Once/week per general topic.",
        dice="—", duration="Instant", line=407),
    "The Glass Chimes of the Bamboo Terrace": dict(
        circle=3, effect="Summon floating chimes for subtle long-distance messaging (10 miles/level), audible only to chosen targets; shatter them as a Main Action to deal 3d6 in 40'.",
        dice="3d6 if shattered", duration="Until shattered/scene ends", line=413),
    "The Howl of Light": dict(
        circle=3, effect="Detonate a 20' radius blast at a point within 50'/level for 1d8/level (Evasion save half); channels down narrow passages for extra 1d6x10'.",
        dice="1d8/level", duration="Instant", line=427),
    "Phobic Storm": dict(
        circle=3, effect="Enemies within 40' make a Morale check at -1 or flee; those who hold take 1 damage/level. No effect on the fearless or Morale-12 foes.",
        dice="1 dmg/level", duration="Instant", line=509),
    "Scorn the Fetters of Earth": dict(
        circle=3, effect="Caster and up to one ally/level can walk/run through the air in three dimensions; or force one flyer/level to land (Physical save at -Magic).",
        dice="—", duration="Scene", line=527),
    "The Torment of Tumefaction": dict(
        circle=3, effect="Curse a visible creature with boils and tumors; vigorous action (not moving) costs 2 dmg/level/round. Main-action Physical save to end; weaker foes are cursed indefinitely.",
        dice="2 dmg/level", duration="Scene (indefinite vs weaker)", line=539),
    "Touch of Elucidating Intangibility": dict(
        circle=3, effect="Touch a non-magical barrier: see/hear through a 10' cube of it, or make it intangible 1 round/level. Anyone caught when it re-solidifies takes 2d10 and is ejected.",
        dice="2d10 if caught", duration="While touching / 1 rd/level", line=545),
    "Vallation of Specified Exclusion": dict(
        circle=3, effect="Draw a line (<=20'/level) that bars a describable kind of target (e.g. 'humans') and their powers, as a wall 100' up. Shatters if the warded are attacked across it.",
        dice="—", duration="1 hour/level", line=551),

    # ---- Fourth Level (9) ----
    "Calculation of the Phantasmal Eidolon": dict(
        circle=4, effect="Summon an ox-sized obedient combatant (4 HD, 20 HP, AC 15, +6/1d8 Shock 2/AC15) that fights to the death. Its damage only knocks out (1 HP after an hour). Pick one quality (fly/mimic/telepathy/use gear).",
        dice="1d8 (non-lethal)", duration="Until destroyed/dawn", line=281),
    "Contingent Excision of Arcana": dict(
        circle=4, effect="Set a trigger to later dispel magic (as Extirpate Arcana) as an Instant action once. Ends when used.",
        dice="—", duration="Until next dawn / one use", line=327),
    "Disjunctive Temporal Reversion": dict(
        circle=4, effect="Instant: one creature within 100' replays its current round's actions as if they never happened. Unwilling targets get a Mental save.",
        dice="—", duration="Instant", line=369),
    "Evert the Inwardness": dict(
        circle=4, effect="Extract a container's contents into your hands; OR tear out a creature's innards — equal/lower-HD targets save or die, all take 1d10/level (Physical save half).",
        dice="1d10/level", duration="Instant", line=381),
    "The Grinding Geas": dict(
        circle=4, effect="Bind a visible creature to a one-sentence command (not suicidal/impossible). Defiance brings a wasting disease that kills in 1d6 weeks; complying reverses it. Mental save if able to resist.",
        dice="—", duration="Until lifted/dispelled", line=421),
    "Obnubilation of the Will": dict(
        circle=4, effect="A helpless/restrained creature makes a Mental save or becomes an intelligent, initiative-using slave (suicidal acts need another save). Cap = 2x level thralls; obvious tics give it away.",
        dice="—", duration="Until released/dispelled", line=479),
    "Ochre Sigil of Juxtaposition": dict(
        circle=4, effect="Cast in two parts within a mile (one slot): inscribe a sigil, then swap everything within 10' of you with everything within 10' of the sigil. Weak unwilling targets get no save.",
        dice="—", duration="Sigil lasts 1 day", line=485),
    "Pierce the Pallid Gate": dict(
        circle=4, effect="Open a cart-sized rift between two known points within 100'/level (>=20' apart) to see and pass through. Closable as an Instant action.",
        dice="—", duration="1 round/level", line=515),
    "Sigil of Aeolian Auctoritas": dict(
        circle=4, effect="Conjure a 100'x30' gust (Physical save or bowled back 30' for 1d6 and lose next Main); or outdoors, control local weather for 1 hour/level.",
        dice="1d6", duration="Instant gust / 1 hr-level weather", line=533),

    # ---- Fifth Level (7) ----
    "Abdication of Temporal Presence": dict(
        circle=5, effect="Caster and up to one ally/level step outside time for 1d4+1 free rounds while the world freezes; they can't affect outside objects or those still in time.",
        dice="—", duration="1d4+1 rounds", line=261),
    "Banishment to the Black Glass Labyrinth": dict(
        circle=5, effect="Exile all but the caster in a 10' radius (within 300') into an infinite obsidian maze. Mental save to return next round; <=5-HD victims get no save and are trapped until the caster dies.",
        dice="—", duration="Until saved/caster dies", line=291),
    "The Dazzling Prismatic Hemicycle": dict(
        circle=5, effect="A 100' cone forces a Physical save; failures roll 1d6 for a random gruesome fate (dust, sleep, insanity, petrification, or enthrallment).",
        dice="1d6 effect table", duration="Varies (up to 1 hour)", line=345),
    "Deluge of Hell": dict(
        circle=5, effect="Rain ruin on a 200'/level radius (within 3,000') for 1d8/level (Physical save half); 4-HD-or-less targets die. Outdoors only; caster saves or takes a quarter of the damage.",
        dice="1d8/level", duration="Instant", line=363),
    "The Earth as Clay": dict(
        circle=5, effect="Over an hour, mold natural stone/earth within 300'/level — raise hills, dig tunnels, form simple buildings. Can't work earth shaped by intelligent hands within 1,000'.",
        dice="—", duration="Permanent (shaped over 1 hr)", line=375),
    "Invocation of the Invincible Citadel": dict(
        circle=5, effect="Instant: raise a 20'-radius force bubble around the caster, impervious to attacks, magic, and matter from either side. Those inside may leave but not return.",
        dice="—", duration="Until caster leaves bubble", line=453),
    "Open the High Road": dict(
        circle=5, effect="Open a one-way gate from the caster to a prepared point within 100 miles/level (1-hour attunement). Cart-sized, 1 minute/level. 1-in-10 chance to misfire 1d100 miles off.",
        dice="—", duration="1 minute/level", line=491),
}

# ===========================================================================
# TRADITION ARTS — named Arts treated as "spells" for the lookup.
# Each tradition: list of (name, effort, action, effect, line).
# effort durations: "Day" / "Scene" / "Indefinite" / "—" (passive/always-on).
# These become spell records with type "<Tradition> Art", circle 0, dice from
# the effect where one applies.
# ===========================================================================
ELEMENTALIST_ARTS = {
    "Elemental Resilience": dict(effort="—", action="Passive",
        effect="Unharmed by mundane cold or sub-furnace heat; half damage from magical/intense flame or frost. (Granted at 1st level.)",
        dice="—", line=635),
    "Elemental Sparks": dict(effort="—", action="On Turn",
        effect="Conjure petty flame, water, ice, stone, or wind for minor tricks. Can't meaningfully solve a problem more than once/session. (Granted at 1st level.)",
        dice="—", line=637),
    "Beckoned Deluge": dict(effort="Scene", action="Main",
        effect="Conjure water drenching 1 cube/level within 50'/level — ruins bowstrings, douses fire, deals 1d6/level to fiery supernatural creatures. Persists; hydrates ten/level.",
        dice="1d6/level vs fire-creatures", line=641),
    "Earthsight": dict(effort="Scene", action="On Turn",
        effect="See solid object outlines in total darkness and peer through earth/stone up to your level in feet.",
        dice="—", line=643),
    "Elemental Blast": dict(effort="Scene", action="Main",
        effect="Hurl an elemental bolt at a target within 50'/level (Magic + Int/Cha/Dex + level to hit, no melee penalty) for 1d6 + level + attribute.",
        dice="1d6+level+mod", line=645),
    "Flamesight": dict(effort="Indefinite", action="On Turn",
        effect="See thermal gradients (and living creatures) in total darkness; optionally make your eyes shed 30' of light.",
        dice="—", line=647),
    "Pavis of Elements": dict(effort="Indefinite", action="On Turn",
        effect="Conjure an elemental barrier granting +4 AC (stacking, but never above AC 18) while Committed.",
        dice="—", line=649),
    "Petrifying Stare": dict(effort="Day", action="Main",
        effect="A visible creature makes a Physical save or is partly petrified, losing its Move action for half your level (round up). Flyers land, swimmers sink.",
        dice="—", line=651),
    "Rune of Destruction": dict(effort="Day", action="Main",
        effect="Lay a trap-rune on an adjacent surface (1 hour/level); anyone coming within 2' triggers a 5' elemental blast for 2d6 + level.",
        dice="2d6+level", line=653),
    "Steps of Air": dict(effort="Scene", action="On Turn",
        effect="A visible ally flies at normal Move for 1 round/level; or use Instantly to negate one target's falling damage.",
        dice="—", line=655),
    "Stunning Shock": dict(effort="Day", action="Main",
        effect="A metal-wearing or wet creature within 50'/level loses its next Main action (Physical save downgrades to losing its Move). Once/scene per target.",
        dice="—", line=657),
    "Thermal Shield": dict(effort="Scene", action="Instant",
        effect="Negate one instance of fire or frost damage to a visible ally or object.",
        dice="—", line=659),
}

ELEMENTALIST_SPELLS = {
    "Aqueous Harmony": dict(circle=1,
        effect="Caster and up to a dozen allies gain water-breathing, pressure/cold tolerance, clear underwater sight, and unhindered movement and attacks underwater.",
        dice="—", duration="1 hour/level (while submerged)", line=673),
    "Flame Scrying": dict(circle=1,
        effect="Sense all open flames within 30'/level and scry through one chosen flame, seeing and hearing around it while you stay focused.",
        dice="—", duration="While focused", line=683),
    "Elemental Favor": dict(circle=1,
        effect="Appeal to a <=10' cube of earth, stone, water, flame, or air; it reshapes/moves as asked, holding the new form until scene's end (or permanently if stable).",
        dice="—", duration="Scene (or permanent if stable)", line=695),
    "Elemental Spy": dict(circle=1,
        effect="Enchant a stone, bit of liquid, flame, or smoke; for 1 day/level, see and hear around the object as a Main action while it survives.",
        dice="—", duration="1 day/level", line=707),
    "Boreal Wings": dict(circle=2,
        effect="A visible ally within 100' flies at twice their Move; descends gently if it ends aloft. Lasts a scene (longer at higher levels).",
        dice="—", duration="Scene (longer 5th/8th level)", line=719),
    "The Burrower Below": dict(circle=2,
        effect="Carve a stabilizable tunnel through natural stone/earth up to 20'/level long, 10' across (only 2'/level through worked stone).",
        dice="—", duration="Permanent", line=675),
    "Flame Without End": dict(circle=2,
        effect="Make a flame (<= caster's size) eternal and non-consuming; resists all but burial/immersion. As a weapon it adds +2 damage. One free per level.",
        dice="+2 dmg as weapon", duration="Until dispelled/released", line=689),
    "Pact of Stone and Sea": dict(circle=2,
        effect="Pick earth/water/fire/wind; a visible target is immune to that element's mundane harm and secondary effects (e.g. fire-pacted can't be boiled) for the scene.",
        dice="—", duration="Scene", line=701),
    "Elemental Vallation": dict(circle=3,
        effect="Raise a 10'/level wall of earth (20 HP), fire (3d6+level passing through), water (2d6 + ejection), or air (1d6+level electric, invisible).",
        dice="3d6+level (fire)", duration="Scene", line=713),
    "Like the Stones": dict(circle=3,
        effect="Take on an element's qualities for the scene: stone (stabilize, ignore 3 dmg), water (squeeze through gaps), air (fly, +4 AC vs ranged), or fire (1d6 to melee foes, heat-immune).",
        dice="1d6 (fire)", duration="Scene", line=727),
    "Wind Walking": dict(circle=3,
        effect="A target and their gear become an insubstantial mist, harmable only by cloud-disrupting forces; they move freely in 3D but can't manipulate objects.",
        dice="—", duration="Scene", line=733),
    "Calcifying Scourge": dict(circle=4,
        effect="A visible target within 100' makes a Physical save or is turned to stone until the caster undoes it (success = lose Move action 1d6 rounds). Damage while petrified carries over.",
        dice="—", duration="Until undone/dispelled", line=739),
    "Elemental Guardian": dict(circle=4,
        effect="Animate a human-sized mass of an element as a loyal 4-HD guardian (AC 15, +6/1d10) with element-based perks (earth = 6 HD, fire = Shock, water = AC 18, air = flight). One at a time.",
        dice="1d10", duration="Until destroyed/dawn", line=745),
    "Fury of the Elements": dict(circle=5,
        effect="Erupt molten rock and steam on a point within 200'/level for 10d6 in 30', then the zone wanders 1d6x10' randomly each round for 1d6 rounds. Molten remnants linger all day.",
        dice="10d6", duration="1d6 rounds (remnants all day)", line=751),
    "Tremors of the Depths": dict(circle=5,
        effect="Call up an earthquake over a 500' radius that topples unreinforced structures, tunnels, and caves. Builds over 5 minutes; negated only if dispelled within a minute.",
        dice="—", duration="Builds over 5 min", line=757),
}

HEALER_ARTS = {
    "Healing Touch": dict(effort="Scene", action="Instant",
        effect="For the scene, heal a touched ally 2d6 + Heal skill as a Main action (+1 System Strain to the target each time). (Granted at 1st level.)",
        dice="2d6+Heal", line=799),
    "Empowered Healer": dict(effort="—", action="Passive",
        effect="Your Healing Touch also adds your level to the healing done.",
        dice="+level", line=803),
    "Facile Healer": dict(effort="—", action="Passive",
        effect="Your Healing Touch no longer requires you to Commit Effort to activate it.",
        dice="—", line=805),
    "Far Healer": dict(effort="—", action="Passive",
        effect="Your Healing Touch can reach a visible target within 10'/level.",
        dice="—", line=807),
    "Final Repose": dict(effort="Day", action="Instant",
        effect="A visible creature takes a Physical-save penalty equal to your Heal skill for the scene; if dropped to 0 HP they die outright with no stabilization or revival.",
        dice="—", line=809),
    "Healer's Eye": dict(effort="Indefinite", action="On Turn",
        effect="While Committed, use a Main action to diagnose diseases/poisons, read physiology and current HP; also see living creatures regardless of light.",
        dice="—", line=811),
    "Limb Restoration": dict(effort="Day (all)", action="Main",
        effect="(8th level+) Commit all remaining Effort to regrow a touched target's missing limb/organ or efface a debility; their System Strain is maxed.",
        dice="—", line=813),
    "Purge Ailment": dict(effort="Day", action="Main",
        effect="Cure one poison or disease in a touched ally (revives poison-deaths within 6 minutes). Magical ailments may need a Heal check vs 8+. 7th level: only Scene effort.",
        dice="—", line=815),
    "Refined Restoration": dict(effort="—", action="Passive",
        effect="You and up to a dozen allies you tend before sleep lose 2 System Strain from a night's rest instead of 1.",
        dice="—", line=817),
    "Revive the Fallen": dict(effort="Day", action="Main",
        effect="(8th level+) Revive a touched creature dead within 1 minute/level (not dismembered/incinerated). Strain is maxed; they wake after 24 hours at 1 HP.",
        dice="—", line=819),
    "Swift Healer": dict(effort="—", action="On Turn",
        effect="Your Healing Touch can be used as an On Turn action once/day per level (not twice/round on one target).",
        dice="—", line=823),
    "The Healer's Knife": dict(effort="—", action="Main",
        effect="Your Healing Touch can instead deal its healing amount as damage to a living target (you take 1 System Strain). Melee use needs a Punch attack (hit bonus = Heal).",
        dice="2d6+Heal as damage", line=825),
    "Tireless Vigor": dict(effort="Indefinite", action="On Turn",
        effect="While Committed, your need to eat/drink/breathe/sleep does not worsen and you regenerate 1 lost HP per hour.",
        dice="—", line=827),
    "Vital Furnace": dict(effort="Day", action="Instant",
        effect="Negate the damage from a non-mortal injury you just took. Also: you auto-stabilize at 0 HP and wake in 10 minutes at 1 HP.",
        dice="—", line=829),
}

NECROMANCER_ARTS = {
    "Bonetalker": dict(effort="Scene", action="Passive/On Turn",
        effect="See and speak with any undead; Commit Effort to read a visible undead's surface thoughts and orders. Mindless undead won't attack you unless commanded.",
        dice="—", line=886),
    "Cold Flesh": dict(effort="—", action="Passive",
        effect="No sleep needed, abstract pain only, take at most 2 damage from any Shock, and gain natural AC 12 + half level (round down).",
        dice="—", line=888),
    "Consume Life Energy": dict(effort="—", action="Passive",
        effect="With a Punch or a consecrated melee weapon, heal 1d6 per hit (up to the damage dealt, never above the target's remaining HP).",
        dice="1d6/hit", line=890),
    "False Death": dict(effort="Indefinite", action="Instant",
        effect="While Committed you appear dead to mundane examination (lose Main actions but move and perceive; no bodily needs; poisons/diseases pause). Up to 1 day/level.",
        dice="—", line=892),
    "Gravesight": dict(effort="Indefinite", action="On Turn",
        effect="While Committed, see living creatures' life energies (and their sicknesses/poisons) as glowing patterns, and see normally in total darkness.",
        dice="—", line=894),
    "Keeper of the Gate": dict(effort="Day", action="Passive/On Turn",
        effect="At will, Mortally Wounded creatures within 20'/level die unrevivably; or Commit Effort to auto-stabilize any/all within range (+1 Strain each).",
        dice="—", line=896),
    "Life Bridge": dict(effort="Day", action="Main",
        effect="For the scene, shift HP between two willing/helpless creatures (>= dog-sized) you touch — even enough to Mortally Wound the donor, but not past the recipient's max.",
        dice="—", line=898),
    "Master of Bones": dict(effort="Scene", action="Passive/Instant",
        effect="Undead roll saves vs your powers twice, worse result; Commit Effort to negate one attack/power/spell from an undead (unless it has 2x your levels in HD).",
        dice="—", line=900),
    "Red Harvest": dict(effort="Day", action="Instant",
        effect="When an intelligent 1+ HD creature dies within 50', heal 1d6 + level OR gain +4 on your next hit roll this scene. Once/round, no stacking.",
        dice="1d6+level", line=902),
    "Unaging": dict(effort="—", action="Passive",
        effect="You no longer naturally age (hale to species max +20%/level) and become immune to poisons and diseases.",
        dice="—", line=904),
    "Uncanny Ichor": dict(effort="—", action="Passive",
        effect="Predators won't bite you. Puncture/stab wounds can Mortally Wound but not kill you unless you're utterly pincushioned or catastrophically maimed.",
        dice="—", line=906),
    "Unliving Persistence": dict(effort="Day", action="On Turn",
        effect="Auto-stabilize when Mortally Wounded; can be used on a touched ally instead. Won't save the dismembered or finally-slain.",
        dice="—", line=908),
}

NECROMANCER_SPELLS = {
    "Command the Dead": dict(circle=1,
        effect="Bind up to 2x level HD of visible undead within 100' (Mental save at -Magic); the fully-bound become suicidally loyal. Cap of 2x level HD held at once.",
        dice="—", duration="Until released", line=920),
    "Query the Skull": dict(circle=1,
        effect="A corpse dead no more than 1 day/level answers 1 truthful question/level, tersely and literally. Once per corpse.",
        dice="—", duration="Instant", line=938),
    "Smite the Dead": dict(circle=1,
        effect="Blast a 20' radius within 100'/level; hostile undead take 1d10/level and those of <= your level in HD save or are destroyed. May Commit Effort to make it free of a slot.",
        dice="1d10/level", duration="Instant", line=950),
    "Terrible Liveliness": dict(circle=1,
        effect="Give an undead the tangible semblance of a healthy living being at any age, able to do all activities its cognition allows. One disguise/level; not on unwilling sentients.",
        dice="—", duration="Until dropped/dispelled", line=962),
    "Augment Mortal Vitality": dict(circle=2,
        effect="A willing target gains a Physical-save bonus equal to your Magic skill and auto-stabilizes when Mortally Wounded; once/scene heal a non-mortal injury. +1 Strain.",
        dice="—", duration="Scene", line=922),
    "Enfeebling Wave": dict(circle=2,
        effect="Living creatures in a 20' radius (within 100') save or, for the scene, halve their Move and roll attacks/damage twice taking the worse (success = next turn only).",
        dice="—", duration="Scene", line=932),
    "Final Death": dict(circle=2,
        effect="Curse one target/level: for the scene they can't regain HP and die instantly if Mortally Wounded. A Physical save after each failed healing ends it.",
        dice="—", duration="Scene", line=944),
    "Raise Corpse": dict(circle=2,
        effect="Animate a skeleton/corpse as a loyal 1-HD servant (AC 13, +1/1d6) with a human degree of intelligence but only vague memories. Active count <= caster level.",
        dice="1d6", duration="Until destroyed/released", line=954),
    "Compel Flesh": dict(circle=3,
        effect="A living creature or bodied undead within 100' is paralyzed unless you command it each turn (On Turn). Physical save each turn to break free, taking 1 dmg/level per attempt.",
        dice="1 dmg/level", duration="Scene", line=968),
    "Festering Curse": dict(circle=3,
        effect="Force a corpse's qualities on a living target: food tastes of ash, no physical pleasure, -2 social checks. No injury, just misery, until lifted. Stronger foes save.",
        dice="—", duration="Until lifted/dispelled", line=974),
    "Forgetting the Grave": dict(circle=3,
        effect="A willing target cannot die for 1 round/level; at 0 HP they lose their Move but act on (further damage forces Physical saves). At the end, 0-HP targets are Mortally Wounded.",
        dice="—", duration="1 round/level", line=980),
    "Merge Souls": dict(circle=3,
        effect="Bond two touched willing/helpless creatures to pool HP and communicate telepathically; neither dies until the pool hits 0 (then both Mortally Wounded). Ends at daybreak.",
        dice="—", duration="Until daybreak", line=986),
    "Boneshaper": dict(circle=4,
        effect="Reshape a willing/helpless living or undead body over an hour — add/remove limbs, recolor, retexture. Can shift a Cha/physical modifier +1/-1 (max +2/-2). Imitation: Dex/Magic vs 10.",
        dice="—", duration="Until lifted/dispelled", line=992),
    "Raise Grave Knight": dict(circle=4,
        effect="Raise a 4+ HD corpse as a strong, fully intelligent, loyal undead knight (4 HD, AC 15, +6/1d10) that recalls its life and regains all HP at dusk. One at a time.",
        dice="1d10", duration="Until destroyed", line=998),
    "Call of the Tomb": dict(circle=5,
        effect="Enemies within 40' save or, for 1 round/level (success = 1 round), are auto-hit by all attacks with maximized damage dice and lose all special damage defenses.",
        dice="maximized", duration="1 round/level", line=1004),
    "Everlasting": dict(circle=5,
        effect="Instant: for 5 rounds no allied creature within 50' can drop below 1 HP. At the end, the caster is left at 1 HP. Once/day per creature.",
        dice="—", duration="5 rounds", line=1010),
}

VOWED_ARTS = {
    "Martial Style": dict(effort="—", action="Passive",
        effect="Your hit die is at least 1d6/level and your Punch hit bonus is at least an Expert's. At 3rd level, Punch attacks count as magic weapons. (Granted at 1st level.)",
        dice="—", line=1067),
    "Unarmed Might": dict(effort="—", action="Passive",
        effect="Your unarmed damage rises by level (per the Vowed table), and you add Punch skill to it. (Granted at 1st level.)",
        dice="1d6 -> 1d10+3", line=1069),
    "Unarmored Defense": dict(effort="—", action="Passive",
        effect="Unarmored and shieldless, your base Armor Class is 13 + half your level (round down). (Granted at 1st level.)",
        dice="—", line=1071),
    "Brutal Counter": dict(effort="Scene", action="Instant",
        effect="After an enemy's melee attack on you (hit or miss), make a free physical attack or one-Main-action offensive ability against them. Usable during Total Defense.",
        dice="—", line=1075),
    "Faultless Awareness": dict(effort="—", action="Passive",
        effect="You cannot be surprised and wake from deep sleep in time to respond to imminent peril.",
        dice="—", line=1077),
    "Hurling Throw": dict(effort="Scene", action="Instant",
        effect="After a successful attack, the target (<= ox-sized) saves or is thrown up to 10', falls prone, and takes your attack's damage. Once/round per target.",
        dice="attack damage", line=1079),
    "The Inward Eye": dict(effort="Indefinite", action="On Turn",
        effect="While Committed, you sense your surroundings like normal sight regardless of darkness, mist, or blindness.",
        dice="—", line=1081),
    "Leap of the Heavens": dict(effort="Scene", action="Move",
        effect="Leap up to your full Move horizontally (half vertically); or use Instantly to negate falling damage from any height.",
        dice="—", line=1083),
    "Master's Vigor": dict(effort="—", action="Passive",
        effect="You keep youthful vigor for your full lifespan and regain 2 lost HP per hour naturally.",
        dice="—", line=1087),
    "Mob Justice": dict(effort="Day", action="Instant",
        effect="For the scene, foes can't Swarm-attack you, and you're immune to Shock while meleeing 2+ foes. Using it disrupts your spellcasting that round.",
        dice="—", line=1089),
    "Nimble Ascent": dict(effort="Scene", action="On Turn",
        effect="For the scene, move up vertical/overhanging surfaces and difficult terrain at full Move with no slipping (needs one free hand, not on glass/enchanted surfaces).",
        dice="—", line=1091),
    "Purified Body": dict(effort="Day", action="Instant",
        effect="Cure any disease or poison on you, or negate your need for sleep/food/water/air for 24 hours.",
        dice="—", line=1093),
    "Revivifying Breath": dict(effort="Day", action="On Turn",
        effect="Heal yourself 1d6 + level with no Strain (usable even at 0 HP, but then Commits all remaining Effort). Once/scene.",
        dice="1d6+level", line=1095),
    "Shattering Strike": dict(effort="Day", action="Main",
        effect="After a round of stillness, shatter a wooden barrier (1'/level deep; stone at 4th, metal at 7th). Against an immobilized creature, the blow does 1d12/level.",
        dice="1d12/level", line=1097),
    "Style Weaponry": dict(effort="—", action="Passive",
        effect="Pick three weapon classes; use Punch for their hit rolls (no Punch damage bonus, but Martial Style applies).",
        dice="—", line=1099),
    "Unobtrusive Step": dict(effort="Day", action="Instant",
        effect="Once/scene, reroll a failed Sneak check or an impersonation check.",
        dice="—", line=1101),
}

# Map tradition -> (arts dict, new-magic spells dict-or-None)
TRADITIONS = [
    ("Elementalist", ELEMENTALIST_ARTS, ELEMENTALIST_SPELLS),
    ("Healer", HEALER_ARTS, None),
    ("Necromancer", NECROMANCER_ARTS, NECROMANCER_SPELLS),
    ("Vowed", VOWED_ARTS, None),
]


# ===========================================================================
# FOCI — 35 core foci.  level_1 / level_2 are concise paraphrases.
# Page lines point into 02 - Character Creation.md (foci span L604-905).
# ===========================================================================
FOCI = {
    "Alert": dict(level_req="None", line=604,
        level_1="Gain Notice. Can't be surprised or targeted by Execution Attacks; +1 to your side's initiative (or roll individual init twice).",
        level_2="You always act first in a round unless another combatant is equally Alert."),
    "Armored Magic": dict(level_req="Mage/Partial Mage only", line=612,
        level_1="Cast spells/use arts in armor of Encumbrance 2 or less; may use a shield if your other hand is free to gesture.",
        level_2="Cast in armor of any Encumbrance, and even with both hands full (not bound)."),
    "Armsmaster": dict(level_req="None", line=620,
        level_1="Gain Stab. Ready a stowed melee/thrown weapon as an Instant; add Stab skill to melee/thrown damage or Shock. (Doesn't stack with Deadeye.)",
        level_2="Your melee Shock treats targets as AC 10; +1 to hit with thrown/melee attacks."),
    "Artisan": dict(level_req="None", line=630,
        level_1="Gain Craft. Craft counts as one level higher (max 5) for mods, which cost one less salvage; Craft works for any crafting profession.",
        level_2="First mod on an item is free of Maintenance and half-cost; auto-succeed at masterwork gear; monthly extra salvage reduction."),
    "Assassin": dict(level_req="None", line=638,
        level_1="Gain Sneak. Conceal a knife-sized object, draw it On Turn; point-blank surprise-round attacks with it can't miss.",
        level_2="Take a (splittable) Move action on the same round as an Execution Attack, closing without alerting the victim."),
    "Authority": dict(level_req="None", line=646,
        level_1="Gain Lead. Once/day, a Cha/Lead check vs an NPC's Morale makes them comply with a not-harmful request.",
        level_2="NPCs you directly lead gain +Lead to Morale and hit rolls and +1 to skill checks; followers won't act against you."),
    "Close Combatant": dict(level_req="None", line=654,
        level_1="Gain any combat skill. Use knife-sized thrown weapons in melee freely; ignore melee Shock (but doing so disrupts your casting that round).",
        level_2="Your melee Shock treats all targets as AC 10; Fighting Withdrawal becomes a free On Turn action for you."),
    "Connected": dict(level_req="None", line=662,
        level_1="Gain Connect. After a week somewhere not hostile, you have contacts for mildly-illegal favors — one favor/game day.",
        level_2="Once/session, plausibly run into someone you know willing to do a modest favor (GM decides who)."),
    "Cultured": dict(level_req="None", line=670,
        level_1="Gain Connect. Speak all common regional languages; learn a new one in a week; once/day gain a minor no-cost favor from a non-hostile NPC.",
        level_2="Once/session, reroll a failed social skill check using your cultural knowledge."),
    "Die Hard": dict(level_req="None", line=676,
        level_1="+2 max HP per level (retroactive). Auto-stabilize when Mortally Wounded unless torn apart.",
        level_2="The first time each day an injury would drop you to 0 HP, you survive at 1 HP instead."),
    "Deadeye": dict(level_req="None", line=684,
        level_1="Gain Shoot. Ready a stowed ranged weapon as an Instant; use a bow in melee at -4; add Shoot skill to ranged damage.",
        level_2="Reload slow weapons On Turn; use any ranged weapon in melee without penalty; once/scene auto-hit an inanimate target."),
    "Dealmaker": dict(level_req="None", line=692,
        level_1="Gain Trade. In half an hour, find a buyer/seller for any tradeable good or service in the community, legal or not.",
        level_2="Once/session, make a request of a non-hostile sentient; if plausible, they'll deal for a price or favor."),
    "Developed Attribute": dict(level_req="Not Mage/Partial Mage", line=700,
        level_1="Raise one attribute's modifier by +1 (max +3); the score is unchanged. May be taken multiple times for different attributes.",
        level_2="(No second level — repeatable instead.)"),
    "Diplomatic Grace": dict(level_req="None", line=708,
        level_1="Gain Convince. Speak all common regional languages (learn new in a week, fluent in a month); reroll 1s on negotiation/diplomacy dice.",
        level_2="Once/day, consecrate a bargain; the other party must Mental save to break it (most NPCs won't try). Must be specific and time-limited."),
    "Gifted Chirurgeon": dict(level_req="None", line=714,
        level_1="Gain Heal. Stabilize one adjacent Mortally Wounded person/round On Turn; roll Heal checks 3d6-drop-lowest; double post-battle first aid healing.",
        level_2="Your healing counts as magical: heal 1d6 + Heal to an adjacent ally as a Main action (+1 Strain), reviving without Frailty."),
    "Henchkeeper": dict(level_req="None", line=722,
        level_1="Gain Lead. Recruit loyal henchmen (one per 3 levels) within a day of arriving; they escort and risk danger but won't fight except to save themselves.",
        level_2="Henchmen will fight for you (treated as Veteran Soldiers); capable NPCs can become henchmen if you've earned their loyalty."),
    "Impervious Defense": dict(level_req="None", line=732,
        level_1="Innate Armor Class of 15 + half your level (round up). Doesn't stack with armor, but Dex and shield modifiers apply.",
        level_2="Once/day, as an Instant, shrug off a single weapon attack or physical trauma (not environmental/falling damage)."),
    "Impostor": dict(level_req="None", line=740,
        level_1="Gain Perform or Sneak. Once/scene reroll a failed disguise/imposture check; hold one flawless minor false identity.",
        level_2="Swap between three chosen appearances with a Main action; establish a new false identity in each community you spend a day in."),
    "Lucky": dict(level_req="An attribute modifier of -1 or worse", line=750,
        level_1="Once/week, a blow or effect that would kill, Mortally Wound, or disable you simply fails. Roll games of chance twice, take the better.",
        level_2="Once/session in peril, roll 1d6: on 2+ something fortunate happens; on a 1 the situation gets much worse."),
    "Nullifier": dict(level_req="Not Mage/Partial Mage", line=758,
        level_1="You and allies within 20' get +2 saves vs magic; sense magic within 20' On Turn; your first failed save vs magic each day becomes a success.",
        level_2="Once/day, as an Instant, be simply unaffected by an unwanted magical effect or monstrous power, even one with no save."),
    "Poisoner": dict(level_req="None", line=766,
        level_1="Gain Heal. Reroll failed saves vs poison; brew toxins (one dose/level) dealing 2d6 + level on a hit/Shock, Physical save for half.",
        level_2="Immune to poison; universal antidote; -Heal penalty to detect/save vs your poisons; ingested poisons count as Execution Attacks."),
    "Polymath": dict(level_req="Expert/Partial Expert only", line=772,
        level_1="Gain any one skill. Treat all non-combat skills as at least level-0 for checks, even ones you lack. (Phantom levels don't stack/discount.)",
        level_2="Treat all non-combat skills as at least level-1 for checks."),
    "Rider": dict(level_req="None", line=780,
        level_1="Gain Ride. Your steeds count as Morale 12, use your AC if better, and travel 50% further/day; intuitively communicate with riding beasts.",
        level_2="Once/scene negate an attack on your steed (Instant); reroll a failed Ride check; telepathic link with a bonded steed within 200'."),
    "Shocking Assault": dict(level_req="None", line=788,
        level_1="Gain Punch or Stab. Your weapon's Shock treats all targets as AC 10 (if it can harm them and they aren't Shock-immune).",
        level_2="+2 to the Shock rating of all melee/unarmed attacks that do Shock."),
    "Sniper's Eye": dict(level_req="None", line=798,
        level_1="Gain Shoot. On a ranged Execution Attack or target-shooting, roll the skill check 3d6-drop-lowest.",
        level_2="Don't miss ranged Execution Attacks; the target takes -4 on the Physical save and double damage even on a success."),
    "Special Origin": dict(level_req="GM permission; pick a species origin", line=806,
        level_1="Take the origin Focus for a non-human species (from the bestiary) to play that demihuman/alien kind, gaining its listed benefits.",
        level_2="(Varies by chosen origin — see the bestiary entry.)"),
    "Specialist": dict(level_req="None", line=814,
        level_1="Gain any skill (not Magic/Stab/Shoot/Punch). Roll 3d6-drop-lowest for all checks in it. May be taken for different skills.",
        level_2="Roll 4d6-drop-two-lowest for all checks in this skill."),
    "Spirit Familiar": dict(level_req="None", line=822,
        level_1="Gain a loyal familiar (cat- to human-sized) with Evoked Servitor stats, summon/dismiss as a Main action; once/day it refreshes one Committed Effort.",
        level_2="Pick two upgrades (extra HP, an attack, a skill bonus, a second shape, flight, or speech). Repeatable for two more each time."),
    "Trapmaster": dict(level_req="None", line=842,
        level_1="Gain Notice. Once/scene reroll a failed trap-related save/check; improvise a trap (non-lethal lose-a-round, or lethal 1d6 + 2x level) in 5 minutes.",
        level_2="Once/scene, your efforts count as Extirpate Arcana (cast as a Mage of twice your level) against a magical trap or hazard."),
    "Unarmed Combatant": dict(level_req="None", line=852,
        level_1="Gain Punch. Unarmed damage scales with Punch (1d6 at L0 up to 1d12+1 at L4) with Shock = Punch skill vs AC 15; bind ranged-weapon foes.",
        level_2="Even on a missed Punch, deal an unmodified 1d6 plus any Shock the blow would inflict."),
    "Unique Gift": dict(level_req="GM agreement", line=860,
        level_1="A catch-all special power defined by player and GM together, worth one Focus pick; revisable if it proves too weak or strong.",
        level_2="(As agreed with the GM.)"),
    "Valiant Defender": dict(level_req="None", line=868,
        level_1="Gain Stab or Punch. +2 to Screen Ally checks, screen one more attacker, and once/round screen even spells/area effects (vs the attacker's Magic).",
        level_2="Your first Screen Ally check each round auto-succeeds; +2 AC while screening; screen foes as large as ogres or oxen."),
    "Well Met": dict(level_req="None", line=876,
        level_1="Reaction rolls get +1 while you're present; even hostile beings usually grant a round of parley first. Works once per target.",
        level_2="Once/session, make a subject as friendly and helpful as plausibly possible when a reaction roll is made."),
    "Whirlwind Assault": dict(level_req="None", line=884,
        level_1="Gain Stab. Once/scene, as an On Turn action, apply your Shock damage to all foes in melee range susceptible to it.",
        level_2="The first time you kill someone in a round with a normal attack, instantly gain a second attack on any target in range."),
    "Xenoblooded": dict(level_req="GM permission", line=892,
        level_1="Pick one alien-heritage benefit: heat/smoke immunity; water-adaptation; heavy/light-gravity attribute shift; or need no food/sleep/air + see in the dark.",
        level_2="(No second level — a single heritage benefit.)"),
}

# ---------------------------------------------------------------------------
# POINTER FOCI — special Foci / class-arts encoded by NAME + PAGE only.
# (Atlas optional classes & their Arcane Secret/specialist foci, the six Gyre
# traditions and their arts, and the Legate Writs.)  These are not fully
# encoded — pull the detail from the cited chapter.
# ---------------------------------------------------------------------------
POINTER_FOCI = {
    # --- Atlas: Optional Rules & Classes (Atlas/04) ---
    "Mundane Alchemist": dict(source="Atlas", line=248,
        note="Atlas optional Focus (Experts only): grants the Alchemy skill and basic formulae to brew lesser/greater alchemical works."),
    "The Accursed (class)": dict(source="Atlas", line=411,
        note="Atlas partial-Mage class pacted with an Outsider; wields Accursed Blade/Bolt arts (use Magic to attack) plus dark Effort-fueled arts."),
    "The Bard (class)": dict(source="Atlas", line=532,
        note="Atlas class whose non-magical performance arts hearten allies and dismay foes by tapping the Legacy's archetypes."),
    "The Mageslayer (class)": dict(source="Atlas", line=401,
        note="Atlas combatant class specialized in resisting hostile magic and swiftly butchering enemy spellcasters."),
    "The Wise (class)": dict(source="Atlas", line=405,
        note="Atlas low/no-magic scholar-priest-witch class with limited tricks for settings where full magic is absent."),

    # --- Arts of the Gyre (ch. 11): six traditions ---
    "Adunic Invoker (Gyre)": dict(source="Gyre", line=29,
        note="Gyre tradition: invokes the names and authority of the Adunic powers. Has its own arts list and the Traditional Education focus."),
    "Darian Skinshifter (Gyre)": dict(source="Gyre", line=85,
        note="Gyre tradition: shapeshifts into beast forms via Effort-fueled Skinshifter arts."),
    "Kistian Duelist (Gyre)": dict(source="Gyre", line=170,
        note="Gyre tradition: magical warrior-duelist (with the Flaw of Fragility); arts sharpen martial prowess."),
    "Llaigisan Beastmaster (Gyre)": dict(source="Gyre", line=258,
        note="Gyre tradition: bonds and commands animal companions (the Chosen Friend) through Beastmaster arts."),
    "Sarulite Blood Priest (Gyre)": dict(source="Gyre", line=340,
        note="Gyre tradition: blood-sacrifice priest whose arts trade vitality for power."),
    "Vothite Thought Noble (Gyre)": dict(source="Gyre", line=412,
        note="Gyre tradition: psychic noble whose arts dominate and read minds."),

    # --- Legate Writs (ch. 13) ---
    "Legate Writs": dict(source="Legates", line=33,
        note="Legate-tier powers (Writs of Might/Skill/Sorcery/Mastery), fueled by Legate Effort, undispellable and undetectable. Begin with Legate's Impunity + Legate's Wrath. See ch. 13 for the full Writ list."),
}


# ===========================================================================
# Build the two lookup documents.
# ===========================================================================
def build_spells():
    records = {}
    # High Magic
    for name, d in HIGH_MAGIC.items():
        records[name] = {
            "circle": d["circle"],
            "type": "High Magic",
            "effect": d["effect"],
            "dice": d["dice"],
            "duration": d["duration"],
            "page": _pg(MAGIC, d["line"]),
        }
    # Tradition arts + New Magic spells
    for trad, arts, spells in TRADITIONS:
        for name, d in arts.items():
            records[name] = {
                "circle": 0,
                "type": f"{trad} Art",
                "effort": d["effort"],
                "action": d["action"],
                "effect": d["effect"],
                "dice": d["dice"],
                "duration": "—",
                "page": _pg(MAGIC, d["line"]),
            }
        if spells:
            for name, d in spells.items():
                records[name] = {
                    "circle": d["circle"],
                    "type": trad,
                    "effect": d["effect"],
                    "dice": d["dice"],
                    "duration": d["duration"],
                    "page": _pg(MAGIC, d["line"]),
                }
    return {
        "id": "wwn.spells",
        "kind": "lookup",
        "category": "spell",
        "key": "name",
        "records": records,
    }


def build_foci():
    records = {}
    for name, d in FOCI.items():
        records[name] = {
            "level_req": d["level_req"],
            "level_1": d["level_1"],
            "level_2": d["level_2"],
            "page": _pg(CHARGEN, d["line"]),
        }
    src_map = {"Atlas": ATLAS04, "Gyre": GYRE, "Legates": LEGATES}
    for name, d in POINTER_FOCI.items():
        records[name] = {
            "pointer": True,
            "effect": d["note"],
            "page": _pg(src_map[d["source"]], d["line"]),
        }
    return {
        "id": "wwn.foci",
        "kind": "lookup",
        "category": "focus",
        "key": "name",
        "records": records,
    }


def write_json(name, obj):
    path = os.path.join(OUT_DIR, name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return path


def main():
    quiet = "--quiet" in sys.argv[1:]
    os.makedirs(OUT_DIR, exist_ok=True)

    spells = build_spells()
    foci = build_foci()
    write_json("spells.json", spells)
    write_json("foci.json", foci)

    # Counts.
    high = sum(1 for r in spells["records"].values() if r["type"] == "High Magic")
    arts = sum(1 for r in spells["records"].values() if r["type"].endswith(" Art"))
    new_magic = len(spells["records"]) - high - arts
    core_foci = sum(1 for r in foci["records"].values() if not r.get("pointer"))
    ptr_foci = len(foci["records"]) - core_foci

    if quiet:
        print(f"OK  spells={len(spells['records'])}  foci={len(foci['records'])}")
        return

    print("build_magic.py — wrote bridge/generators/spells.json + foci.json")
    print()
    print("spells.json")
    print(f"  High Magic spells : {high}")
    print(f"  Tradition Arts    : {arts}")
    print(f"  Tradition spells  : {new_magic}  (Elementalist + Necromancer New Magic)")
    print(f"  TOTAL records     : {len(spells['records'])}")
    # Per-circle High Magic breakdown.
    by_circle = {}
    for r in spells["records"].values():
        if r["type"] == "High Magic":
            by_circle[r["circle"]] = by_circle.get(r["circle"], 0) + 1
    circ = "  ".join(f"C{c}={by_circle[c]}" for c in sorted(by_circle))
    print(f"  High Magic by circle: {circ}")
    print()
    print("foci.json")
    print(f"  Core foci (full)  : {core_foci}")
    print(f"  Pointer foci      : {ptr_foci}  (Atlas / Gyre / Legate, name+page only)")
    print(f"  TOTAL records     : {len(foci['records'])}")


if __name__ == "__main__":
    main()
