#!/usr/bin/env python3
"""
chargen.py — Worlds Without Number character creation with honest, shown dice.

Builds a WWN PC step by step, printing every die it rolls, exactly per the
book's procedure (Character Creation, pp. 8-35; Equipment, pp. 36-41).

Dice are reproducible with --seed. Every die is printed like:
    3d6 -> [4,2,5] = 11
By default the internal roller is used so the script always runs standalone.
If the env var MYTHIC_GM_DICE points at the engine's dice.py the rolls are
still produced here and printed in the same honest way (the engine roller is
only consulted to confirm availability; see roll()).

USAGE
  python3 chargen.py [--name NAME] [--background BG] [--class CLASS]
                     [--level N] [--random] [--package PKG | --roll-wealth]
                     [--seed S] [--out PATH]

  --class : warrior | expert | mage | adventurer | <partial combos>, e.g.
            "partial-warrior/partial-expert", "partial-mage/partial-warrior",
            "partial-expert/partial-mage", or "partial-mage/partial-mage".
  --random: make every unspecified choice by an honest roll.
  With no flags at all, a sensible random level-1 build is produced.

Std-lib only; Python 3.6+.
"""
import argparse
import os
import random
import re
import sys

# ---------------------------------------------------------------------------
# DICE — honest and shown.  Format: "3d6 -> [4,2,5] = 11"
# ---------------------------------------------------------------------------
LOG = []  # captured dice lines, also echoed to stderr-free stdout via roll()


def roll(expr, label=None, silent=False):
    """Parse NdM[+/-K], return the integer total, and PRINT the roll.

    The internal roller is always used to produce the result (so the script is
    standalone and seed-reproducible).  If MYTHIC_GM_DICE is set we note that
    the engine roller is available, but we still roll here so every die is
    shown in one consistent transparent format.
    """
    m = re.match(r"\s*(\d*)d(\d+)\s*([+-]\s*\d+)?\s*$", str(expr))
    if not m:
        # allow a bare integer "constant" so callers can log fixed values
        if re.match(r"^\s*[+-]?\d+\s*$", str(expr)):
            return int(str(expr))
        sys.exit("roll() expects NdM[+/-K], got %r" % expr)
    n = int(m.group(1) or 1)
    sides = int(m.group(2))
    k = int((m.group(3) or "0").replace(" ", ""))
    rolls = [random.randint(1, sides) for _ in range(n)]
    total = sum(rolls) + k
    ktxt = (" %+d" % k) if k else ""
    line = "  %s -> %s%s = %d" % (str(expr).replace(" ", ""), rolls, ktxt, total)
    if label:
        line += "   (%s)" % label
    LOG.append(line)
    if not silent:
        print(line)
    return total


def _engine_dice_available():
    p = os.environ.get("MYTHIC_GM_DICE")
    return bool(p) and os.path.exists(p)


# ---------------------------------------------------------------------------
# ATTRIBUTE MODIFIERS — p.9:  3 = -2 | 4-7 = -1 | 8-13 = 0 | 14-17 = +1 | 18 = +2
# ---------------------------------------------------------------------------
def attr_mod(score):
    if score <= 3:
        return -2
    if score <= 7:
        return -1
    if score <= 13:
        return 0
    if score <= 17:
        return 1
    return 2


ATTRS = ["Str", "Dex", "Con", "Int", "Wis", "Cha"]

# ---------------------------------------------------------------------------
# SKILLS (p.10)
# ---------------------------------------------------------------------------
SKILLS = ["Administer", "Connect", "Convince", "Craft", "Exert", "Heal", "Know",
          "Lead", "Magic", "Notice", "Perform", "Pray", "Punch", "Ride", "Sail",
          "Shoot", "Sneak", "Stab", "Survive", "Trade", "Work"]
COMBAT_SKILLS = ["Stab", "Shoot", "Punch"]
NONCOMBAT_SKILLS = [s for s in SKILLS if s not in COMBAT_SKILLS]

# ---------------------------------------------------------------------------
# BACKGROUNDS (pp.11-17).  Each: free skill, quick skills, d6 Growth, d8 Learning.
# Growth entries that begin "+" are attribute growths; "skill" entries are skill
# gains.  "Any Stat" = +1 to any one attribute; "+2 Physical/Mental" per p.11.
# ---------------------------------------------------------------------------
BACKGROUNDS = {
    "Artisan": {
        "free": "Craft", "quick": ["Trade", "Connect"],
        "growth": ["+1 Any", "+2 Physical", "+2 Physical", "+2 Mental", "Exert", "Any Skill"],
        "learning": ["Connect", "Convince", "Craft", "Craft", "Exert", "Know", "Notice", "Trade"]},
    "Barbarian": {
        "free": "Survive", "quick": ["Any Combat", "Notice"],
        "growth": ["+1 Any", "+2 Physical", "+2 Physical", "+2 Mental", "Exert", "Any Skill"],
        "learning": ["Any Combat", "Connect", "Exert", "Lead", "Notice", "Punch", "Sneak", "Survive"]},
    "Carter": {
        "free": "Ride", "quick": ["Connect", "Any Combat"],
        "growth": ["+1 Any", "+2 Physical", "+2 Physical", "+2 Mental", "Connect", "Any Skill"],
        "learning": ["Any Combat", "Connect", "Craft", "Exert", "Notice", "Ride", "Survive", "Trade"]},
    "Courtesan": {
        "free": "Perform", "quick": ["Notice", "Connect"],
        "growth": ["+1 Any", "+2 Mental", "+2 Mental", "+2 Physical", "Connect", "Any Skill"],
        "learning": ["Any Combat", "Connect", "Convince", "Exert", "Notice", "Perform", "Survive", "Trade"]},
    "Criminal": {
        "free": "Sneak", "quick": ["Connect", "Convince"],
        "growth": ["+1 Any", "+2 Mental", "+2 Physical", "+2 Mental", "Connect", "Any Skill"],
        "learning": ["Administer", "Any Combat", "Connect", "Convince", "Exert", "Notice", "Sneak", "Trade"]},
    "Hunter": {
        "free": "Shoot", "quick": ["Survive", "Sneak"],
        "growth": ["+1 Any", "+2 Physical", "+2 Physical", "+2 Mental", "Exert", "Any Skill"],
        "learning": ["Any Combat", "Exert", "Heal", "Notice", "Ride", "Shoot", "Sneak", "Survive"]},
    "Laborer": {
        "free": "Work", "quick": ["Connect", "Exert"],
        "growth": ["+1 Any", "+1 Any", "+1 Any", "+1 Any", "Exert", "Any Skill"],
        "learning": ["Administer", "Any Skill", "Connect", "Convince", "Craft", "Exert", "Ride", "Work"]},
    "Merchant": {
        "free": "Trade", "quick": ["Convince", "Connect"],
        "growth": ["+1 Any", "+2 Mental", "+2 Mental", "+2 Mental", "Connect", "Any Skill"],
        "learning": ["Administer", "Any Combat", "Connect", "Convince", "Craft", "Know", "Notice", "Trade"]},
    "Noble": {
        "free": "Lead", "quick": ["Connect", "Administer"],
        "growth": ["+1 Any", "+2 Mental", "+2 Mental", "+2 Mental", "Connect", "Any Skill"],
        "learning": ["Administer", "Any Combat", "Connect", "Convince", "Know", "Lead", "Notice", "Ride"]},
    "Nomad": {
        "free": "Ride", "quick": ["Survive", "Any Combat"],
        "growth": ["+1 Any", "+2 Physical", "+2 Physical", "+2 Mental", "Exert", "Any Skill"],
        "learning": ["Any Combat", "Connect", "Exert", "Lead", "Notice", "Ride", "Survive", "Trade"]},
    "Peasant": {
        "free": "Exert", "quick": ["Sneak", "Survive"],
        "growth": ["+1 Any", "+2 Physical", "+2 Physical", "+2 Physical", "Exert", "Any Skill"],
        "learning": ["Connect", "Exert", "Craft", "Notice", "Sneak", "Survive", "Trade", "Work"]},
    "Performer": {
        "free": "Perform", "quick": ["Convince", "Connect"],
        "growth": ["+1 Any", "+2 Mental", "+2 Physical", "+2 Physical", "Connect", "Any Skill"],
        "learning": ["Any Combat", "Connect", "Exert", "Notice", "Perform", "Perform", "Sneak", "Convince"]},
    "Physician": {
        "free": "Heal", "quick": ["Know", "Notice"],
        "growth": ["+1 Any", "+2 Physical", "+2 Mental", "+2 Mental", "Connect", "Any Skill"],
        "learning": ["Administer", "Connect", "Craft", "Heal", "Know", "Notice", "Convince", "Trade"]},
    "Priest": {
        "free": "Pray", "quick": ["Convince", "Know"],
        "growth": ["+1 Any", "+2 Mental", "+2 Physical", "+2 Mental", "Connect", "Any Skill"],
        "learning": ["Administer", "Connect", "Know", "Lead", "Heal", "Convince", "Pray", "Pray"]},
    "Sailor": {
        "free": "Sail", "quick": ["Exert", "Notice"],
        "growth": ["+1 Any", "+2 Physical", "+2 Physical", "+2 Mental", "Exert", "Any Skill"],
        "learning": ["Any Combat", "Connect", "Craft", "Exert", "Heal", "Notice", "Perform", "Sail"]},
    "Scholar": {
        "free": "Know", "quick": ["Heal", "Administer"],
        "growth": ["+1 Any", "+2 Mental", "+2 Mental", "+2 Mental", "Connect", "Any Skill"],
        "learning": ["Administer", "Heal", "Craft", "Know", "Notice", "Perform", "Pray", "Convince"]},
    "Slave": {
        "free": "Sneak", "quick": ["Survive", "Exert"],
        "growth": ["+1 Any", "+2 Physical", "+2 Physical", "+2 Mental", "Exert", "Any Skill"],
        "learning": ["Administer", "Any Combat", "Any Skill", "Convince", "Exert", "Sneak", "Survive", "Work"]},
    "Soldier": {
        "free": "Any Combat", "quick": ["Exert", "Survive"],
        "growth": ["+1 Any", "+2 Physical", "+2 Physical", "+2 Physical", "Exert", "Any Skill"],
        "learning": ["Any Combat", "Any Combat", "Exert", "Lead", "Notice", "Ride", "Sneak", "Survive"]},
    "Thug": {
        "free": "Any Combat", "quick": ["Convince", "Connect"],
        "growth": ["+1 Any", "+2 Mental", "+2 Physical", "+2 Physical", "Connect", "Any Skill"],
        "learning": ["Any Combat", "Any Combat", "Connect", "Convince", "Exert", "Notice", "Sneak", "Survive"]},
    "Wanderer": {
        "free": "Survive", "quick": ["Sneak", "Notice"],
        "growth": ["+1 Any", "+2 Physical", "+2 Physical", "+2 Mental", "Exert", "Any Skill"],
        "learning": ["Any Combat", "Connect", "Notice", "Perform", "Ride", "Sneak", "Survive", "Work"]},
}
# d20 background table (p.11). Entries 4-5, 15-16 etc map 1:1 to the 20-row list.
BACKGROUND_D20 = ["Artisan", "Barbarian", "Carter", "Courtesan", "Criminal", "Hunter",
                  "Laborer", "Merchant", "Noble", "Nomad", "Peasant", "Performer",
                  "Physician", "Priest", "Sailor", "Scholar", "Slave", "Soldier",
                  "Thug", "Wanderer"]

# ---------------------------------------------------------------------------
# CLASSES (pp.18-21).  Level-1 line only matters for novice creation, but the
# attack-bonus / hit-die progressions are stored so --level works.
# hit_die_expr(level) -> the dice string to roll for max HP at that level.
# attack_bonus(level) -> base attack bonus.
# foci: list of (kind, count) granted at level 1, kind in {expert, warrior, any}.
# ---------------------------------------------------------------------------
def _hd(per_die_mod):
    """Return a function giving 'Ld6[+/-K]' for a given total HD-die modifier.
    Warriors +2/die, Mages -1/die, Experts +0.  K scales with level."""
    def f(level):
        bonus = per_die_mod * level
        if bonus > 0:
            return "%dd6+%d" % (level, bonus)
        if bonus < 0:
            return "%dd6%d" % (level, bonus)
        return "%dd6" % level
    return f


# Attack-bonus tables, indexed by level (1-10), from the book's class tables.
AB_WARRIOR = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
AB_EXPERT = [0, 1, 1, 2, 2, 3, 3, 4, 4, 5]
AB_MAGE = [0, 0, 0, 0, 1, 1, 1, 1, 1, 2]
AB_PARTIAL_WAR = [1, 2, 2, 3, 4, 5, 5, 6, 6, 7]      # Pe/Pw & Pm/Pw share this
AB_PARTIAL_EXPMAGE = [0, 1, 1, 2, 2, 3, 3, 4, 4, 5]  # Pe/Pm

CLASSES = {
    "warrior": {
        "name": "Warrior", "hd": _hd(2), "ab": AB_WARRIOR,
        "foci": [("warrior", 1), ("any", 1)], "caster": False,
        "ability": "Veteran's Luck; Killing Blow (+half level, round up, to damage & Shock)."},
    "expert": {
        "name": "Expert", "hd": _hd(0), "ab": AB_EXPERT,
        "foci": [("expert", 1), ("any", 1)], "caster": False,
        "ability": "Masterful Expertise (1/scene reroll a non-combat check); Quick Learner."},
    "mage": {
        "name": "Mage", "hd": _hd(-1), "ab": AB_MAGE,
        "foci": [("any", 1)], "caster": "full",
        "ability": "Arcane Tradition (pick a tradition; full caster)."},
    # Adventurer partial combos (pp.21). Hit die: any Partial Warrior uses +2/die;
    # otherwise +0/die.  Foci per the combo's level-1 line.
    "partial-expert/partial-warrior": {
        "name": "Adventurer (Partial Expert/Partial Warrior)", "hd": _hd(2), "ab": AB_PARTIAL_WAR,
        "foci": [("expert", 1), ("warrior", 1), ("any", 1)], "caster": False,
        "ability": "Quick Learner (no Masterful Expertise / Veteran's Luck / Killing Blow)."},
    "partial-expert/partial-mage": {
        "name": "Adventurer (Partial Expert/Partial Mage)", "hd": _hd(0), "ab": AB_PARTIAL_EXPMAGE,
        "foci": [("expert", 1), ("any", 1)], "caster": "partial",
        "ability": "Quick Learner; Arcane Tradition (partial caster)."},
    "partial-mage/partial-warrior": {
        "name": "Adventurer (Partial Mage/Partial Warrior)", "hd": _hd(2), "ab": AB_PARTIAL_WAR,
        "foci": [("warrior", 1), ("any", 1)], "caster": "partial",
        "ability": "Arcane Tradition (partial caster); improved HD & attack (no Veteran's Luck/Killing Blow)."},
    "partial-mage/partial-mage": {
        "name": "Adventurer (Partial Mage/Partial Mage)", "hd": _hd(-1), "ab": AB_MAGE,
        "foci": [("any", 1)], "caster": "dual-partial",
        "ability": "Two Arcane Traditions (each a partial pool of Effort/spells)."},
}
# canonical aliases for convenience
CLASS_ALIASES = {
    "adventurer": "partial-expert/partial-warrior",
    "pe/pw": "partial-expert/partial-warrior",
    "pe/pm": "partial-expert/partial-mage",
    "pm/pw": "partial-mage/partial-warrior",
    "pm/pm": "partial-mage/partial-mage",
    "partial-warrior/partial-expert": "partial-expert/partial-warrior",
    "partial-mage/partial-expert": "partial-expert/partial-mage",
    "partial-warrior/partial-mage": "partial-mage/partial-warrior",
}

# ---------------------------------------------------------------------------
# MAGE TRADITIONS (Magic ch., pp.64-97).  Each: caster?, the bonus skill it
# grants, the Effort formula ('magic' | 'heal' | 'order'), the arts auto-granted
# at L1, how many arts it picks at L1 (full vs partial), the full art list, and
# the tradition's own 1st-circle New-Magic spells (High Magic is shared).
# ---------------------------------------------------------------------------
HIGH_MAGIC_1ST = [
    "Apprehending the Arcane Form", "Cognitive Supersession of the Inferior Orders",
    "The Coruscating Coffin", "Damnation of the Sense", "Decree of Ligneous Dissolution",
    "The Excellent Transpicuous Transformation", "Imperceptible Cerebral Divulgence",
    "Ineluctable Shackles of Volition", "The Long Amber Moment", "Phantasmal Mimesis",
    "Velocitous Imbuement", "Wardpact Invocation", "The Wind of the Final Repose",
]
TRADITIONS = {
    "High Mage": {
        "caster": True, "bonus_skill": "Magic", "effort": "magic",
        "auto_arts": [], "l1_arts_full": 2, "l1_arts_partial": 1,
        "spells_1st": [],  # High Magic only
        "arts": ["Arcane Lexicon", "Counter Magic", "Empowered Sorcery", "Hang Sorcery",
                 "Inexorable Effect", "Iron Resolution", "Preparatory Countermagic",
                 "Psychic Conversion", "Restrained Casting", "Retain Sorcery", "Sense Magic",
                 "Suppress Magic", "Swift Casting", "Ward Allies", "Wizard's Grandeur"]},
    "Elementalist": {
        "caster": True, "bonus_skill": "Magic", "effort": "magic",
        "auto_arts": ["Elemental Resilience", "Elemental Sparks"],
        "l1_arts_full": 1, "l1_arts_partial": 1,
        "spells_1st": ["Aqueous Harmony", "Flame Scrying", "Elemental Favor", "Elemental Spy"],
        "arts": ["Beckoned Deluge", "Earthsight", "Elemental Blast", "Flamesight",
                 "Pavis of Elements", "Petrifying Stare", "Rune of Destruction", "Steps of Air",
                 "Stunning Shock", "Thermal Shield"]},
    "Necromancer": {
        "caster": True, "bonus_skill": "Magic", "effort": "magic",
        "auto_arts": [], "l1_arts_full": 1, "l1_arts_partial": 1,
        "spells_1st": ["Command the Dead", "Query the Skull", "Smite the Dead", "Terrible Liveliness"],
        "arts": ["Bonetalker", "Cold Flesh", "Consume Life Energy", "False Death", "Gravesight",
                 "Keeper of the Gate", "Life Bridge", "Master of Bones", "Red Harvest",
                 "Unaging", "Uncanny Ichor", "Unliving Persistence"]},
    "Healer": {
        "caster": False, "bonus_skill": "Heal", "effort": "heal", "partial_only": True,
        "auto_arts": ["Healing Touch"], "l1_arts_full": 1, "l1_arts_partial": 1,
        "spells_1st": [],
        "arts": ["Empowered Healer", "Facile Healer", "Far Healer", "Final Repose",
                 "Healer's Eye", "Limb Restoration (L8+)", "Purge Ailment", "Refined Restoration",
                 "Revive the Fallen (L8+)", "Swift Healer", "The Healer's Knife", "Tireless Vigor",
                 "Vital Furnace"]},
    "Vowed": {
        "caster": False, "bonus_skill": None, "effort": "order", "partial_only": True,
        "auto_arts": ["Martial Style", "Unarmed Might", "Unarmored Defense"],
        "l1_arts_full": 1, "l1_arts_partial": 1, "spells_1st": [],
        "arts": ["Brutal Counter", "Faultless Awareness", "Hurling Throw", "The Inward Eye",
                 "Leap of the Heavens", "Master's Vigor", "Mob Justice", "Nimble Ascent",
                 "Purified Body", "Revivifying Breath", "Shattering Strike", "Style Weaponry",
                 "Unobtrusive Step"]},
}
CASTING_TRADITIONS = [n for n, t in TRADITIONS.items() if t["caster"]]
# tokens accepted in --class for each partial type / tradition
_CLASS_TOKENS = {
    "warrior": ("warrior", None), "pw": ("warrior", None), "partial-warrior": ("warrior", None),
    "expert": ("expert", None), "pe": ("expert", None), "partial-expert": ("expert", None),
    "mage": ("mage", None), "pm": ("mage", None), "partial-mage": ("mage", None),
    "high-mage": ("mage", "High Mage"), "highmage": ("mage", "High Mage"), "hm": ("mage", "High Mage"),
    "elementalist": ("mage", "Elementalist"), "elem": ("mage", "Elementalist"),
    "necromancer": ("mage", "Necromancer"), "necro": ("mage", "Necromancer"),
    "healer": ("mage", "Healer"), "vowed": ("mage", "Vowed"),
}


def parse_class(spec):
    """Parse a --class spec into (base_key, [traditions]).

    Accepts plain tokens (warrior/expert/mage), partial combos joined by '/', and
    tradition names in the mage slot (e.g. 'partial-warrior/partial-healer',
    'necromancer/healer', 'vowed', 'high-mage').  Returns the canonical CLASSES
    base key plus any traditions explicitly named (others are filled in later)."""
    k = spec.strip().lower()
    k = re.sub(r"\s*/\s*", "/", k)   # tidy spaces around slashes
    k = re.sub(r"\s+", "-", k)        # spaces within a token -> hyphen (e.g. "high mage")
    if k in CLASS_ALIASES:
        k = CLASS_ALIASES[k]
    if k in CLASSES and "/" not in k:
        # plain full class
        base = k
        trads = []
        if base == "mage":
            trads = [None]  # one tradition, chosen later
        return base, trads
    if k in CLASSES:  # already a canonical partial combo, no tradition named
        n_mage = k.count("partial-mage")
        return k, [None] * n_mage
    # compositional parse: split on '/'
    parts = [p for p in k.split("/") if p]
    types, trads = [], []
    for p in parts:
        tok = p if p in _CLASS_TOKENS else p.replace("partial-", "", 1)
        if tok not in _CLASS_TOKENS:
            sys.exit("Unknown class token '%s' in '%s'. Tokens: %s"
                     % (p, spec, ", ".join(sorted(_CLASS_TOKENS))))
        typ, trad = _CLASS_TOKENS[tok]
        types.append(typ)
        if typ == "mage":
            trads.append(trad)
    if len(types) == 1:
        base = types[0]
        if base == "mage" and not trads:
            trads = [None]
        return base, trads
    if len(types) != 2:
        sys.exit("A class is one full class or two partials; got %d in '%s'." % (len(types), spec))
    s = set(types)
    if s == {"warrior", "expert"}:
        base = "partial-expert/partial-warrior"
    elif s == {"warrior", "mage"}:
        base = "partial-mage/partial-warrior"
    elif s == {"expert", "mage"}:
        base = "partial-expert/partial-mage"
    elif s == {"mage"}:
        base = "partial-mage/partial-mage"
    else:
        sys.exit("Unsupported partial pairing in '%s'." % spec)
    return base, trads


# ---------------------------------------------------------------------------
# FOCI (pp.22-28).  bonus_skill: a skill, "Any Combat", "Punch/Stab", "Perform/Sneak",
#   "Any", "Any Non-Magic", or None.  hp_per_level / ac / attr_mod where mechanical.
#   page = book page for record-keeping.  combat: True/False/None (None = either).
# Effects that aren't a simple number are recorded as text in `note`.
# ---------------------------------------------------------------------------
FOCI = {
    "Alert": {"page": 22, "skill": "Notice", "combat": True,
              "note": "Cannot be surprised; +1 side initiative or roll init twice."},
    "Armored Magic": {"page": 22, "skill": None, "combat": False,
                      "note": "Mage may cast in armor (Enc <=2 at L1, any at L2)."},
    "Armsmaster": {"page": 23, "skill": "Stab", "combat": True,
                   "note": "Add Stab level to melee/thrown damage & Shock."},
    "Artisan": {"page": 23, "skill": "Craft", "combat": False,
                "note": "Craft counts +1 for mods; craft any profession's wares."},
    "Assassin": {"page": 23, "skill": "Sneak", "combat": True,
                 "note": "Surprise point-blank attacks can't miss; conceal a knife."},
    "Authority": {"page": 23, "skill": "Lead", "combat": False,
                  "note": "1/day Cha/Lead vs Morale to compel a non-hostile NPC."},
    "Close Combatant": {"page": 24, "skill": "Any Combat", "combat": True,
                        "note": "Ignore melee Shock; use knife-thrown in melee."},
    "Connected": {"page": 24, "skill": "Connect", "combat": False,
                  "note": "A web of contacts; 1 favor/day after a week somewhere."},
    "Cultured": {"page": 24, "skill": "Connect", "combat": False,
                 "note": "Speak regional languages; 1 minor favor/day."},
    "Deadeye": {"page": 24, "skill": "Shoot", "combat": True,
                "note": "Add Shoot level to ranged damage; Ready ranged as Instant."},
    "Dealmaker": {"page": 25, "skill": "Trade", "combat": False,
                  "note": "Find any buyer/seller in a community in a half hour."},
    "Developed Attribute": {"page": 25, "skill": None, "combat": None,
                            "note": "Choose an attribute; its MODIFIER +1 (max +3). Not for Mages.",
                            "needs_attr": True},
    "Diplomatic Grace": {"page": 25, "skill": "Convince", "combat": False,
                         "note": "Reroll 1s on negotiation/diplomacy checks."},
    "Die Hard": {"page": 25, "skill": None, "combat": None,
                 "hp_per_level": 2,
                 "note": "+2 max HP/level; auto-stabilize when Mortally Wounded."},
    "Gifted Chirurgeon": {"page": 26, "skill": "Heal", "combat": False,
                          "note": "Heal checks roll 3d6 drop lowest; double first-aid HP."},
    "Henchkeeper": {"page": 26, "skill": "Lead", "combat": False,
                    "note": "Recruit loyal henchmen (1 per 3 levels, round up)."},
    "Impervious Defense": {"page": 26, "skill": None, "combat": True,
                           "innate_ac": True,
                           "note": "Innate AC = 15 + half level (round up); no stack w/ armor."},
    "Impostor": {"page": 27, "skill": "Perform/Sneak", "combat": False,
                 "note": "1/scene reroll a disguise check; one flawless false identity."},
    "Lucky": {"page": 27, "skill": None, "combat": None,
              "needs_neg_attr": True,
              "note": "1/week a lethal blow fails to connect. Needs an attr mod <= -1."},
    "Nullifier": {"page": 27, "skill": None, "combat": None,
                  "note": "+2 saves vs magic (allies w/in 20'); sense magic. Not for Mages."},
    "Poisoner": {"page": 27, "skill": "Heal", "combat": False,
                 "note": "Brew toxins (2d6+level, Phys save half); reroll saves vs poison."},
    "Polymath": {"page": 28, "skill": "Any", "combat": False, "expert_only": True,
                 "note": "Treat all non-combat skills as >= level-0 (L1) / level-1 (L2)."},
    "Rider": {"page": 28, "skill": "Ride", "combat": None,
              "note": "Steeds Morale 12, use your AC, travel +50%; bond with a mount."},
    "Shocking Assault": {"page": 28, "skill": "Punch/Stab", "combat": True,
                         "note": "Melee Shock treats all targets as AC 10."},
    "Sniper's Eye": {"page": 28, "skill": "Shoot", "combat": True,
                     "note": "Ranged Execution/target checks roll 3d6 drop lowest."},
    "Special Origin": {"page": 28, "skill": None, "combat": None,
                       "note": "Non-human origin Focus (bestiary). GM permission. # TODO verify p.280"},
    "Specialist": {"page": 28, "skill": "Any Non-Magic", "combat": False,
                   "note": "Chosen skill rolls 3d6 drop lowest (L1) / 4d6 drop two (L2)."},
    "Spirit Familiar": {"page": 28, "skill": None, "combat": None,
                        "note": "A loyal minor spirit companion; refreshes 1 Effort/day."},
    "Trapmaster": {"page": 28, "skill": "Notice", "combat": None,
                   "note": "1/scene reroll a trap check; improvise traps."},
    "Unarmed Combatant": {"page": 28, "skill": "Punch", "combat": True,
                          "note": "Unarmed scales: Punch-0 1d6, -1 1d8, -2 1d10, -3 1d12, -4 1d12+1."},
    "Unique Gift": {"page": 28, "skill": None, "combat": None,
                    "note": "GM-defined special power. # TODO verify p.28 (define with GM)."},
    "Valiant Defender": {"page": 28, "skill": "Stab/Punch", "combat": True,
                         "note": "+2 Screen Ally checks; screen one extra attacker."},
    "Well Met": {"page": 28, "skill": None, "combat": False,
                 "note": "+1 to reaction rolls while present."},
    "Whirlwind Assault": {"page": 28, "skill": "Stab", "combat": True,
                          "note": "1/scene apply Shock to all foes in melee range."},
    "Xenoblooded": {"page": 28, "skill": None, "combat": None,
                    "note": "Alien adaptation (choose a benefit). # TODO verify p.28."},
}

# ---------------------------------------------------------------------------
# WEAPONS & ARMOR (pp.35-37) — only what packages need plus a small lookup.
# weapon: (damage, shock_str, attrs[list], note)
# ---------------------------------------------------------------------------
WEAPONS = {
    "Dagger": ("1d4", "1/AC15", ["Str", "Dex"], "S,T,PM"),
    "Light Spear": ("1d6", "2/AC13", ["Str", "Dex"], "T"),
    "Short Sword": ("1d6", "2/AC15", ["Str", "Dex"], ""),
    "Long Sword": ("1d8", "2/AC13", ["Str", "Dex"], ""),
    "Hand Axe": ("1d6", "1/AC15", ["Str", "Dex"], "T"),
    "Staff": ("1d6", "1/AC13", ["Str", "Dex"], "2H,LL"),
    "Bow, Large": ("1d8", "None", ["Dex"], "2H,R"),
    "Throwing Blade": ("1d4", "None", ["Dex"], "S,T,N"),
}
ARMOR = {  # name: (ac, enc)
    "No Armor": (10, 0), "War Shirt": (11, 0), "Buff Coat": (12, 0),
    "Linothorax": (13, 1), "War Robe": (14, 3), "Pieced Armor": (14, 2),
    "Mail Shirt": (14, 1), "Cuirass and Greaves": (15, 2), "Scaled Armor": (16, 3),
    "Mail Hauberk": (16, 2), "Plate Armor": (17, 2), "Great Armor": (19, 3),
}
SHIELDS = {"Small Shield": 13, "Large Shield": 14}  # base AC when held; +1 if armored

# ---------------------------------------------------------------------------
# EQUIPMENT PACKAGES (p.29).  Each: armor (name), shield (name|None), weapons,
# gear list, cash (sp).  Stored verbatim from the book.
# ---------------------------------------------------------------------------
PACKAGES = {
    "adventuring-peasant": {
        "armor": "War Shirt", "shield": "Large Shield",
        "weapons": ["Light Spear", "Dagger"],
        "gear": ["Backpack", "Rations, 1 week", "Mule and small cart", "Tinder box and 3 torches"],
        "cash": 0},
    "ranger-or-archer": {
        "armor": "Buff Coat", "shield": None,
        "weapons": ["Bow, Large", "20 arrows & quiver", "Dagger", "Hand Axe"],
        "gear": ["Backpack", "Cooking utensils and 1 week of rations", "Waterskin",
                 "Tinder box and 3 torches"],
        "cash": 20},
    "armored-warrior": {
        "armor": "Pieced Armor", "shield": "Large Shield",
        "weapons": ["Short Sword", "Dagger"],
        "gear": ["Backpack", "Tinder box and 3 torches"],
        "cash": 0},
    "gentry-wayfarer": {
        "armor": "Buff Coat", "shield": "Small Shield",
        "weapons": ["Short Sword"],
        "gear": ["Backpack", "Rations, 1 week", "Waterskin",
                 "Fine suit of clothing carried in the pack", "Writing kit & 20 sheets of paper"],
        "cash": 20},
    "mage-healer-or-scholar": {
        "armor": "Buff Coat", "shield": "Small Shield",
        "weapons": ["Short Sword", "Throwing Blades, 5"],
        "gear": ["Backpack", "Rations, 1 week", "Waterskin", "Tinder box and 3 torches",
                 "Grappling hook and 50' of rope"],
        "cash": 0},
    "roguish-wanderer": {
        "armor": "No Armor", "shield": None,
        "weapons": ["Daggers, 2", "Staff"],
        "gear": ["Backpack", "Lantern, tinder box, and 2 pint flasks of oil",
                 "Writing kit & 20 sheets of paper", "Rations, 1 week", "Waterskin",
                 "Healer's pouch"],
        "cash": 80},
}
# which package suits which class, for sensible random/auto selection
PACKAGE_FOR_CLASS = {
    "warrior": "armored-warrior", "expert": "roguish-wanderer", "mage": "mage-healer-or-scholar",
    "partial-expert/partial-warrior": "gentry-wayfarer",
    "partial-expert/partial-mage": "mage-healer-or-scholar",
    "partial-mage/partial-warrior": "gentry-wayfarer",
    "partial-mage/partial-mage": "mage-healer-or-scholar",
}


# ===========================================================================
# CHARACTER MODEL
# ===========================================================================
class Character(object):
    def __init__(self):
        self.name = None
        self.level = 1
        self.cls_key = None
        self.cls = None
        self.background = None
        self.scores = {a: 10 for a in ATTRS}
        self.skills = {}            # name -> level (0..1 at creation)
        self.foci = []             # list of dicts: {name, level, page, note}
        self.hp_max = 1
        self.armor = "No Armor"
        self.shield = None
        self.weapons = []          # list of weapon names (from package)
        self.gear = []
        self.cash = 0
        self.mod_bonus = {a: 0 for a in ATTRS}  # Developed Attribute etc. (modifier-only bumps)
        self.is_caster = False     # any spell-casting tradition present
        self.traditions = []       # list of {name, effort, arts:[...], spells:[...]}
        self.vowed_skill = None    # the order-skill a Vowed picked (drives Effort)
        self.effort = None         # legacy single value (kept for old callers/tests)
        self.tradition = None      # legacy single label (kept for old callers/tests)
        self.spells = []           # legacy flat spell list (mirrors traditions' spells)
        self.notes = []

    def amod(self, attr):
        """Effective attribute modifier including Developed-Attribute bonuses."""
        return min(3, attr_mod(self.scores[attr]) + self.mod_bonus.get(attr, 0))

    # --- skill helpers (the level-0/1/swap rule, p.11) -------------------
    def gain_skill(self, name, prefer_combat=None):
        """Apply one skill gain following: 1st = lvl0, 2nd = lvl1, 3rd+ = swap.
        Resolves 'Any Combat' / 'Any Skill' / 'Any' / combo tokens to a concrete
        skill, choosing one not yet at the cap so the pick is never wasted."""
        name = self._resolve_skill_token(name, prefer_combat)
        cur = self.skills.get(name)
        if cur is None:
            self.skills[name] = 0
            return name, 0
        if cur == 0:
            self.skills[name] = 1
            return name, 1
        # already level-1: must pick any other skill below level-1 (p.11)
        alt = self._pick_skill_below_cap(exclude=name)
        if alt is None:
            return name, cur  # nothing left to improve; no-op
        if self.skills.get(alt) is None:
            self.skills[alt] = 0
            return alt, 0
        self.skills[alt] = 1
        return alt, 1

    def _resolve_skill_token(self, token, prefer_combat):
        if token == "Any Combat":
            pool = COMBAT_SKILLS
        elif token in ("Any Skill", "Any"):
            pool = SKILLS
        elif token == "Any Non-Magic":
            pool = [s for s in SKILLS if s != "Magic"]
        elif "/" in token:
            pool = token.split("/")
        else:
            return token
        # prefer a skill not yet maxed; honour combat preference if given
        candidates = [s for s in pool if self.skills.get(s, -1) < 1]
        if prefer_combat is True:
            cc = [s for s in candidates if s in COMBAT_SKILLS]
            candidates = cc or candidates
        if not candidates:
            candidates = pool
        return random.choice(candidates)

    def _pick_skill_below_cap(self, exclude=None):
        cands = [s for s in SKILLS if s != exclude and self.skills.get(s, -1) < 1]
        return random.choice(cands) if cands else None


# ===========================================================================
# CREATION STEPS
# ===========================================================================
def section(title):
    print("\n" + "=" * 64)
    print(title)
    print("=" * 64)


def step_attributes(ch, set14=None, random_choice=False):
    section("STEP 1 - ATTRIBUTES  (3d6 in order, p.9)")
    for a in ATTRS:
        ch.scores[a] = roll("3d6", label=a)
    # WWN rule (p.9): after rolling, you MAY change one attribute to 14.
    pick = set14
    if pick is None and (random_choice or True):
        # auto: raise the most useful low score for the chosen class to 14,
        # but only if it actually improves the modifier.
        pick = _choose_14_attr(ch)
    if pick:
        if ch.scores[pick] < 14:
            print("  Rule (p.9): set one attribute to 14 -> %s (%d -> 14)" % (pick, ch.scores[pick]))
            ch.scores[pick] = 14
        else:
            print("  (Chosen 14-attribute %s already >= 14; left as rolled.)" % pick)
    print("  Final attributes:")
    for a in ATTRS:
        print("    %-3s %2d  (mod %+d)" % (a, ch.scores[a], attr_mod(ch.scores[a])))


def _choose_14_attr(ch):
    """Pick which attribute to set to 14, biased by class need."""
    key = ch.cls_key or "expert"
    if "warrior" in key:
        order = ["Str", "Dex", "Con"]
    elif key == "expert" or key.startswith("partial-expert"):
        order = ["Dex", "Int", "Wis", "Con"]
    elif "mage" in key:
        order = ["Int", "Cha", "Con", "Dex"]
    else:
        order = ["Con", "Dex", "Str"]
    # choose the first in priority order whose modifier would actually improve
    for a in order:
        if attr_mod(ch.scores[a]) < attr_mod(14):
            return a
    # otherwise any score under 14
    under = [a for a in ATTRS if ch.scores[a] < 14]
    return random.choice(under) if under else order[0]


def _choose_developed_attr(ch):
    """Developed Attribute: pick a class-relevant attribute whose modifier can
    still rise (< +3), favouring the highest current modifier so it's never wasted."""
    key = ch.cls_key or "expert"
    if "warrior" in key:
        order = ["Str", "Dex", "Con"]
    elif key == "expert" or key.startswith("partial-expert"):
        order = ["Dex", "Int", "Wis", "Con"]
    else:
        order = ["Con", "Dex", "Str", "Wis", "Int", "Cha"]
    cand = [a for a in order if ch.amod(a) < 3] or [a for a in ATTRS if ch.amod(a) < 3]
    if not cand:
        return order[0]
    return max(cand, key=lambda a: ch.amod(a))


def step_background(ch, name=None, mode="quick", random_choice=False):
    section("STEP 2 - BACKGROUND  (p.11)")
    if name is None:
        if random_choice:
            r = roll("1d20", label="background")
            name = BACKGROUND_D20[r - 1]
            print("  Rolled background: %s" % name)
        else:
            name = random.choice(BACKGROUND_D20)
            print("  Picked background: %s" % name)
    name = _match_background(name)
    ch.background = name
    bg = BACKGROUNDS[name]
    # free skill at level-0
    gained, lvl = ch.gain_skill(bg["free"])
    print("  Free skill: %s-%d" % (gained, lvl))

    # Then ONE of: quick skills | pick two Learning | roll three (Growth/Learning).
    if random_choice and mode == "quick":
        mode = "roll"  # honest rolls -> use the rolled table for randoms
    print("  Skill acquisition mode: %s" % mode)
    if mode == "quick":
        for s in bg["quick"]:
            g, l = ch.gain_skill(s)
            print("    Quick skill: %s-%d" % (g, l))
    elif mode == "pick":
        # pick two distinct Learning entries (not 'Any Skill')
        choices = [s for s in bg["learning"] if s != "Any Skill"]
        random.shuffle(choices)
        taken = 0
        for s in choices:
            if taken >= 2:
                break
            g, l = ch.gain_skill(s)
            print("    Learning pick: %s-%d" % (g, l))
            taken += 1
    else:  # roll: three rolls split across Growth/Learning (here: dice decide split)
        for i in range(3):
            tbl = roll("1d2", label="table: 1=Growth 2=Learning")
            if tbl == 1:
                r = roll("1d6", label="%s Growth" % name)
                entry = bg["growth"][r - 1]
                _apply_growth(ch, entry)
            else:
                r = roll("1d8", label="%s Learning" % name)
                entry = bg["learning"][r - 1]
                g, l = ch.gain_skill(entry)
                print("    Learning: %s -> %s-%d" % (entry, g, l))


def _apply_growth(ch, entry):
    if entry.startswith("+1 Any"):
        a = _best_attr_to_raise(ch, ATTRS)
        ch.scores[a] = min(18, ch.scores[a] + 1)
        print("    Growth: +1 Any Stat -> %s now %d (mod %+d)" % (a, ch.scores[a], attr_mod(ch.scores[a])))
    elif entry.startswith("+2 Physical"):
        _apply_two(ch, ["Str", "Dex", "Con"], "Physical")
    elif entry.startswith("+2 Mental"):
        _apply_two(ch, ["Int", "Wis", "Cha"], "Mental")
    elif entry == "Exert":
        g, l = ch.gain_skill("Exert")
        print("    Growth: Exert -> %s-%d" % (g, l))
    elif entry == "Connect":
        g, l = ch.gain_skill("Connect")
        print("    Growth: Connect -> %s-%d" % (g, l))
    elif entry == "Any Skill":
        g, l = ch.gain_skill("Any Skill")
        print("    Growth: Any Skill -> %s-%d" % (g, l))
    else:
        g, l = ch.gain_skill(entry)
        print("    Growth: %s -> %s-%d" % (entry, g, l))


def _apply_two(ch, pool, label):
    """+2 to one attribute or +1/+1 to two (p.11). Auto: put both where useful."""
    a = _best_attr_to_raise(ch, pool)
    if ch.scores[a] <= 16:
        ch.scores[a] = min(18, ch.scores[a] + 2)
        print("    Growth: +2 %s -> %s now %d (mod %+d)" % (label, a, ch.scores[a], attr_mod(ch.scores[a])))
    else:
        # split to avoid wasting against the 18 cap
        a2 = _best_attr_to_raise(ch, [x for x in pool if x != a]) or a
        ch.scores[a] = min(18, ch.scores[a] + 1)
        ch.scores[a2] = min(18, ch.scores[a2] + 1)
        print("    Growth: +2 %s split -> %s %d, %s %d" % (label, a, ch.scores[a], a2, ch.scores[a2]))


def _best_attr_to_raise(ch, pool):
    """Raise the score that is closest to crossing a modifier breakpoint (13->14)."""
    pool = [a for a in pool if ch.scores[a] < 18]
    if not pool:
        return None
    # prefer a 13 (one point from +1) or a 17 (one from +2); else the lowest
    for target in (13, 17, 12, 16):
        for a in pool:
            if ch.scores[a] == target:
                return a
    return min(pool, key=lambda a: ch.scores[a])


def step_class(ch, key=None, random_choice=False, traditions=None):
    section("STEP 3 - CLASS  (pp.18-21)")
    if key is None:
        if random_choice:
            # weight toward the three core classes; Adventurer combos less often
            pool = ["warrior", "expert", "mage", "partial-expert/partial-warrior",
                    "partial-mage/partial-warrior", "partial-expert/partial-mage"]
            r = roll("1d6", label="class")
            base, named = pool[r - 1], []
        else:
            base, named = random.choice(list(CLASSES.keys())), []
        if base == "mage":
            named = [None]
        elif "partial-mage" in base:
            named = [None] * base.count("partial-mage")
    else:
        base, named = parse_class(key)
    ch.cls_key = base
    ch.cls = CLASSES[base]
    print("  Base class: %s" % ch.cls["name"])
    # resolve traditions for every mage-partial slot
    requested = list(traditions) if traditions else list(named)
    _setup_traditions(ch, base, requested, random_choice)
    # Vowed floors the hit die at 1d6/level (Martial Style)
    if any(t["name"] == "Vowed" for t in ch.traditions) and ch.cls["hd"](ch.level) != _hd(0)(ch.level):
        if "-" in ch.cls["hd"](ch.level):  # negative per-die (Mage table) -> floor to plain d6
            ch.cls = dict(ch.cls)
            ch.cls["hd"] = _hd(0)
            ch.notes.append("Vowed Martial Style floors the hit die at 1d6/level.")
    print("  Attack bonus (L%d): +%d" % (ch.level, ch.cls["ab"][ch.level - 1]))
    print("  Class ability: %s" % ch.cls["ability"])
    if ch.traditions:
        print("  Tradition(s): %s" % ", ".join(t["name"] for t in ch.traditions))


def _is_partial(base):
    return base != "mage"  # only the full Mage gets the no-penalty Effort form


def _setup_traditions(ch, base, requested, random_choice):
    """Resolve one tradition per mage-partial slot (or one for full Mage).
    Grants each tradition's bonus skill and records its Effort/arts/spell plan."""
    n_slots = 1 if base == "mage" else base.count("partial-mage")
    if n_slots == 0:
        return
    chosen = []
    used = set()
    for i in range(n_slots):
        want = requested[i] if i < len(requested) else None
        want = _match_tradition(want) if want else None
        if want is None:
            # full Mage and spellcasting partials must be casters; dual picks distinct
            pool = CASTING_TRADITIONS if base == "mage" else list(TRADITIONS.keys())
            pool = [t for t in pool if t not in used] or pool
            if base == "mage":
                pool = [t for t in pool if not TRADITIONS[t].get("partial_only")]
            want = random.choice(pool)
        if base == "mage" and TRADITIONS[want].get("partial_only"):
            sys.exit("%s exists only as a partial Mage class; pick it on an Adventurer." % want)
        used.add(want)
        chosen.append(want)
    ch.is_caster = any(TRADITIONS[t]["caster"] for t in chosen)
    for name in chosen:
        T = TRADITIONS[name]
        rec = {"name": name, "caster": T["caster"], "arts": list(T["auto_arts"]),
               "spells": [], "effort": 0}
        # bonus skill (Magic / Heal / order-skill)
        bs = T["bonus_skill"]
        if name == "Vowed":
            bs = ch.vowed_skill or _pick_vowed_skill(ch)
            ch.vowed_skill = bs
        if bs:
            g, l = ch.gain_skill(bs)
            rec["bonus_skill"] = "%s-%d" % (g, l)
            print("  %s bonus skill: %s-%d" % (name, g, l))
        ch.traditions.append(rec)
    # legacy mirror
    ch.tradition = " + ".join(t["name"] for t in ch.traditions) or None


def _pick_vowed_skill(ch):
    """Vowed Effort/bonus is a non-combat order-skill (Exert/Know/Pray/Magic...)."""
    order = ["Exert", "Know", "Pray", "Magic"]
    have = [s for s in order if s in ch.skills]
    return have[0] if have else "Exert"


def step_foci(ch, requested=None, random_choice=False):
    section("STEP 4 - FOCI  (pp.22-28)")
    grants = list(ch.cls["foci"])  # e.g. [("warrior",1),("any",1)]
    # describe what the class grants
    desc = ", ".join("%dx %s" % (cnt, kind) for kind, cnt in grants)
    print("  Class grants: %s focus pick(s)." % desc)
    chosen_names = list(requested or [])
    # Determine an ordered list of (kind) slots to fill
    slots = []
    for kind, cnt in grants:
        slots += [kind] * cnt
    # extra "Any" Focus picks gained at levels 2, 5, 7, 10 (class tables, pp.18-21)
    extra = sum(1 for lv in (2, 5, 7, 10) if lv <= ch.level)
    if extra:
        slots += ["any"] * extra
        print("  +%d extra Focus pick(s) for reaching level %d." % (extra, ch.level))
    for i, kind in enumerate(slots):
        nm = chosen_names[i] if i < len(chosen_names) else None
        if nm is None:
            nm = _auto_focus(ch, kind)
        else:
            nm = _match_focus(nm)
        _apply_focus(ch, nm, kind)


def _focus_is_combat(f):
    return FOCI[f].get("combat") is True


def _focus_ok_for(ch, name, kind):
    f = FOCI[name]
    if f.get("expert_only") and "expert" not in (ch.cls_key or ""):
        return False
    if f.get("needs_neg_attr") and not any(attr_mod(ch.scores[a]) <= -1 for a in ATTRS):
        return False
    if name in ("Developed Attribute", "Nullifier") and "mage" in (ch.cls_key or ""):
        return False  # both forbidden to Mages/Partial Mages
    if name == "Armored Magic":
        # only Mages/Partial Mages whose arts/casting are hindered by armor (not Healers)
        if not any(t["name"] != "Healer" for t in ch.traditions):
            return False
    if kind == "warrior" and f.get("combat") is False:
        return False
    if kind == "expert" and f.get("combat") is True:
        return False
    return True


def _auto_focus(ch, kind):
    pool = [n for n in FOCI if _focus_ok_for(ch, n, kind)]
    # avoid duplicating an already-taken focus name at creation
    taken = {x["name"] for x in ch.foci}
    pool = [n for n in pool if n not in taken] or pool
    # bias: warriors -> a combat focus that grants a useful skill; experts -> skill foci
    if kind == "warrior":
        prefer = [n for n in pool if FOCI[n].get("combat") is True]
    elif kind == "expert":
        prefer = [n for n in pool if FOCI[n].get("combat") is False and FOCI[n].get("skill")]
    else:
        prefer = [n for n in pool if FOCI[n].get("skill")]
    pool = prefer or pool
    return random.choice(pool)


def _apply_focus(ch, name, kind):
    f = FOCI[name]
    rec = {"name": name, "level": 1, "page": f["page"], "note": f["note"]}
    # bonus skill
    skl = f.get("skill")
    if skl:
        g, l = ch.gain_skill(skl, prefer_combat=(f.get("combat") is True))
        rec["bonus_skill"] = "%s-%d" % (g, l)
    # mechanical numbers
    if f.get("hp_per_level"):
        bonus = f["hp_per_level"] * ch.level
        ch.hp_max += bonus
        rec["hp_bonus"] = bonus
    if f.get("needs_attr"):
        # Developed Attribute: raise one modifier by +1 (max +3). Apply it for real
        # so every derived number (hit, damage, saves, Effort) reflects it.
        a = _choose_developed_attr(ch)
        ch.mod_bonus[a] = ch.mod_bonus.get(a, 0) + 1
        ch.notes.append("Developed Attribute: %s modifier +1 (now %+d, applied to all rolls)."
                        % (a, ch.amod(a)))
        rec["attr_mod_bonus"] = a
    if f.get("innate_ac"):
        innate = 15 + (ch.level + 1) // 2
        rec["innate_ac"] = innate
        ch.notes.append("Impervious Defense: innate AC %d (used if > worn armor)." % innate)
    ch.foci.append(rec)
    line = "  Focus [%s]: %s (p.%d)" % (kind, name, f["page"])
    if rec.get("bonus_skill"):
        line += "  -> bonus skill %s" % rec["bonus_skill"]
    if rec.get("hp_bonus"):
        line += "  -> +%d HP" % rec["hp_bonus"]
    print(line)
    print("      %s" % f["note"])


def step_final(ch, package=None, roll_wealth=False, random_choice=False):
    section("STEP 5 - FINAL TOUCHES  (pp.28-29)")

    # --- Free skill pick (p.28) -----------------------------------------
    g, l = ch.gain_skill("Any Skill")
    print("  Free skill pick: %s-%d" % (g, l))

    # --- Hit points (p.28): class hit die + Con mod, min 1 --------------
    hd = ch.cls["hd"](ch.level)
    base = roll(hd, label="hit points (%s)" % ch.cls["name"])
    con = ch.amod("Con")
    hp = base + con
    if hp < 1:
        hp = 1
    # Die Hard etc. already added a flat bonus to ch.hp_max during foci.
    ch.hp_max = ch.hp_max - 1 + hp if ch.hp_max != 1 else hp
    # (ch.hp_max started at 1; fold the rolled HP in, keep any focus HP bonus)
    print("  HP = %s + Con(%+d) = %d  (min 1)%s"
          % (hd, con, hp, "  +focus HP already added" if any('hp_bonus' in f for f in ch.foci) else ""))
    if ch.hp_max != hp:
        print("  HP (incl. Die Hard / focus): %d" % ch.hp_max)

    # --- Equipment (p.29): package OR 3d6 x10 sp ------------------------
    if roll_wealth:
        sp = roll("3d6", label="starting wealth x10") * 10
        ch.cash = sp
        print("  Starting wealth: %d sp (rolled; buy gear individually).")
        ch.notes.append("No package chosen; spend %d sp on gear from pp.33-37." % sp)
    else:
        pkg = package or PACKAGE_FOR_CLASS.get(ch.cls_key, "gentry-wayfarer")
        pkg = _match_package(pkg)
        P = PACKAGES[pkg]
        ch.armor = P["armor"]
        ch.shield = P["shield"]
        ch.weapons = list(P["weapons"])
        ch.gear = list(P["gear"])
        ch.cash = P["cash"]
        print("  Equipment package: %s" % pkg)
        print("    Armor: %s   Shield: %s" % (P["armor"], P["shield"] or "none"))
        print("    Weapons: %s" % ", ".join(P["weapons"]))
        print("    Gear: %s" % "; ".join(P["gear"]))
        print("    Cash: %d sp" % P["cash"])

    # --- Traditions: Effort pools, Arts, and starting spells (Magic ch.) -----
    if ch.traditions:
        _finalize_traditions(ch, random_choice)


def _finalize_traditions(ch, random_choice, chooser=None):
    """Compute each tradition's Effort pool, pick/list its Arts, and assign
    starting spells.  Effort: High Mage/Elementalist/Necromancer = 1 + Magic +
    better Int/Cha (partial -1); Healer = Heal + better Int/Cha; Vowed =
    order-skill + best attribute mod.  All to a minimum of 1.
    `chooser(label, options, n) -> [picks]` lets the interactive mode pick arts
    and spells; otherwise --random picks honestly and the default lists options."""
    partial = _is_partial(ch.cls_key)
    better_ic = max(ch.amod("Int"), ch.amod("Cha"))
    best_any = max(ch.amod(a) for a in ATTRS)
    casting = [t for t in ch.traditions if t["caster"]]

    for t in ch.traditions:
        T = TRADITIONS[t["name"]]
        if T["effort"] == "magic":
            lvl = ch.skills.get("Magic", 0)
            eff = 1 + lvl + better_ic - (1 if partial else 0)
            formula = "1 + Magic(%d) + better Int/Cha(%+d)%s" % (lvl, better_ic, " -1 partial" if partial else "")
        elif T["effort"] == "heal":
            lvl = ch.skills.get("Heal", 0)
            eff = lvl + better_ic
            formula = "Heal(%d) + better Int/Cha(%+d)" % (lvl, better_ic)
        else:  # order (Vowed)
            sk = ch.vowed_skill or "Exert"
            lvl = ch.skills.get(sk, 0)
            eff = lvl + best_any
            formula = "%s(%d) + best attr mod(%+d)" % (sk, lvl, best_any)
        t["effort"] = max(1, eff)
        # Arts: auto-granted + the L1 picks for this tradition
        n_pick = T["l1_arts_full"] if not partial else T["l1_arts_partial"]
        options = [a for a in T["arts"] if a not in t["arts"]]
        if chooser and n_pick and options:
            picks = chooser("%s — pick %d art(s)" % (t["name"], n_pick), options, n_pick)
            t["arts"] += picks
            t["art_pick_note"] = "+%d chosen" % len(picks)
        elif random_choice and n_pick and options:
            picks = random.sample(options, min(n_pick, len(options)))
            t["arts"] += picks
            t["art_pick_note"] = "+%d chosen" % len(picks)
        else:
            t["art_pick_note"] = "choose %d more from: %s" % (n_pick, ", ".join(options)) if n_pick else ""
        print("  %s Effort = %s = %d" % (t["name"], formula, t["effort"]))
        if t["arts"]:
            print("    Arts: %s" % ", ".join(t["arts"]))
        if t.get("art_pick_note") and not random_choice:
            print("    (%s)" % t["art_pick_note"])

    # legacy mirror of the first pool
    ch.effort = ch.traditions[0]["effort"] if ch.traditions else None

    # starting spells (a per-character total assigned to the casting traditions)
    if not casting:
        return
    if ch.cls_key == "mage":
        total = 4
    elif ch.cls_key == "partial-mage/partial-mage" and len(casting) == 2:
        total = 4
    else:
        total = 2 * len(casting)
    pool = list(HIGH_MAGIC_1ST)
    for t in casting:
        pool += TRADITIONS[t["name"]]["spells_1st"]
    if chooser:
        ch.spells = chooser("pick %d starting 1st-circle spell(s)" % total, pool, total)
    elif random_choice:
        ch.spells = random.sample(pool, min(total, len(pool)))
    else:
        ch.spells = ["<1st-circle spell %d>" % (i + 1) for i in range(total)]
    casting[0]["spells"] = list(ch.spells)
    print("  Starting spells: %d 1st-circle (full=4 / partial=2 / dual=4)." % total)
    if not random_choice:
        print("    Choose from: %s" % ", ".join(pool))


# ---------------------------------------------------------------------------
# DERIVED NUMBERS
# ---------------------------------------------------------------------------
def compute_ac(ch):
    base = ARMOR[ch.armor][0]
    dex = ch.amod("Dex")
    # Impervious Defense innate AC overrides armor if higher
    innate = None
    for f in ch.foci:
        if f.get("innate_ac"):
            innate = f["innate_ac"]
    if innate is not None and innate > base:
        base = innate
        worn = "Impervious Defense"
    else:
        worn = ch.armor
    ac = base + dex
    shield_txt = ""
    if ch.shield:
        sh_base = SHIELDS[ch.shield]
        if base >= sh_base:                   # already equal/better armor -> +1
            ac += 1
            shield_txt = " +1 %s" % ch.shield
        else:                                 # shield sets the base instead (held)
            ac = sh_base + dex
            worn = "%s held (AC %d base)" % (ch.shield, sh_base)
            shield_txt = ""
    return ac, worn, shield_txt, dex


def compute_saves(ch):
    L = ch.level
    s = lambda best: max(2, 16 - L - best)  # noqa: E731  (target can't go below 2 sanely)
    phys = s(max(ch.amod("Str"), ch.amod("Con")))
    evas = s(max(ch.amod("Int"), ch.amod("Dex")))
    ment = s(max(ch.amod("Wis"), ch.amod("Cha")))
    luck = max(2, 16 - L)
    return {"Physical": phys, "Evasion": evas, "Mental": ment, "Luck": luck}


def compute_weapon_lines(ch):
    """For each carried weapon, total hit bonus and damage (p.28)."""
    ab = ch.cls["ab"][ch.level - 1]
    # NOTE: the class attack bonus already encodes martial aptitude (a Warrior's
    # +1..+10 equals their level). Hit = attack bonus + combat-skill + attr mod;
    # do NOT add level again. (Killing Blow adds to DAMAGE only.)
    lines = []
    for wname in ch.weapons:
        # normalize package strings like "Daggers, 2" / "Bow, Large"
        key = _weapon_key(wname)
        if key not in WEAPONS:
            lines.append((wname, None, None, None, "non-weapon / see book"))
            continue
        dmg, shock, attrs, traits = WEAPONS[key]
        best_attr = max(attrs, key=lambda a: ch.amod(a))
        amod = ch.amod(best_attr)
        # combat skill: Shoot for ranged/thrown-by-shoot, else Stab (Punch for unarmed)
        cs = "Shoot" if "Bow" in key or key == "Throwing Blade" else "Stab"
        skill_lvl = ch.skills.get(cs, None)
        if skill_lvl is None:
            hit = ab + amod - 2  # untrained -2
            skill_txt = "%s untrained(-2)" % cs
            sl = -2
        else:
            hit = ab + skill_lvl + amod
            skill_txt = "%s-%d" % (cs, skill_lvl)
            sl = skill_lvl
        dmg_txt = "%s%+d" % (dmg, amod) if amod else dmg
        lines.append((wname, hit, dmg_txt, shock, "%s, %s(%+d)" % (skill_txt, best_attr, amod)))
    return lines, ab


def _weapon_key(s):
    s2 = s.lower()
    if s2.startswith("bow"):
        return "Bow, Large"
    if s2.startswith("dagger"):
        return "Dagger"
    if s2.startswith("throwing blade"):
        return "Throwing Blade"
    if s2.startswith("short sword"):
        return "Short Sword"
    if s2.startswith("long sword"):
        return "Long Sword"
    if s2.startswith("light spear"):
        return "Light Spear"
    if s2.startswith("hand axe"):
        return "Hand Axe"
    if s2.startswith("staff"):
        return "Staff"
    return s


# ---------------------------------------------------------------------------
# OUTPUT
# ---------------------------------------------------------------------------
def render_summary(ch):
    ac, worn, shtxt, dex = compute_ac(ch)
    saves = compute_saves(ch)
    wlines, ab = compute_weapon_lines(ch)
    con_score = ch.scores["Con"]

    out = []
    out.append("\n" + "#" * 64)
    out.append("# CHARACTER SUMMARY")
    out.append("#" * 64)
    out.append("Name:        %s" % (ch.name or "(unnamed)"))
    out.append("Level/Class: %d  %s" % (ch.level, ch.cls["name"]))
    out.append("Background:  %s" % ch.background)
    out.append("")
    out.append("ATTRIBUTES")
    out.append("  " + "  ".join("%s %d(%+d)" % (a, ch.scores[a], ch.amod(a)) for a in ATTRS))
    out.append("")
    out.append("DEFENSES")
    out.append("  AC %d  (%s%s, Dex %+d)" % (ac, worn, shtxt, dex))
    out.append("  HP %d / %d      System Strain 0 / %d (=Con)" % (ch.hp_max, ch.hp_max, con_score))
    out.append("  Attack bonus +%d    Initiative 1d8%+d (Dex)" % (ab, dex))
    out.append("  Saves:  Physical %d  Evasion %d  Mental %d  Luck %d"
               % (saves["Physical"], saves["Evasion"], saves["Mental"], saves["Luck"]))
    out.append("")
    out.append("SKILLS")
    if ch.skills:
        out.append("  " + ", ".join("%s-%d" % (k, v) for k, v in sorted(ch.skills.items())))
    else:
        out.append("  (none)")
    out.append("  Total skills: %d" % len(ch.skills))
    out.append("")
    out.append("FOCI")
    for f in ch.foci:
        extra = []
        if f.get("bonus_skill"):
            extra.append("skill %s" % f["bonus_skill"])
        if f.get("hp_bonus"):
            extra.append("+%d HP" % f["hp_bonus"])
        if f.get("innate_ac"):
            extra.append("innate AC %d" % f["innate_ac"])
        tail = ("  [%s]" % ", ".join(extra)) if extra else ""
        out.append("  - %s (L%d, p.%d)%s" % (f["name"], f["level"], f["page"], tail))
        out.append("      %s" % f["note"])
    if ch.traditions:
        out.append("")
        out.append("MAGIC")
        for t in ch.traditions:
            kind = "caster" if t["caster"] else "art-user"
            out.append("  %s (%s) — Effort %d" % (t["name"], kind, t["effort"]))
            if t["arts"]:
                out.append("    Arts: %s" % ", ".join(t["arts"]))
            if t.get("art_pick_note") and "choose" in t["art_pick_note"]:
                out.append("    (%s)" % t["art_pick_note"])
        if ch.spells:
            out.append("  Spells (1st circle): %s" % ", ".join(ch.spells))
    out.append("")
    out.append("WEAPONS")
    for (nm, hit, dmg, shock, note) in wlines:
        if hit is None:
            out.append("  - %s  (%s)" % (nm, note))
        else:
            out.append("  - %-18s hit %+d, dmg %s, Shock %s   [%s]" % (nm, hit, dmg, shock, note))
    out.append("")
    out.append("ARMOR & GEAR")
    out.append("  Armor: %s   Shield: %s" % (ch.armor, ch.shield or "none"))
    out.append("  Gear: %s" % ("; ".join(ch.gear) if ch.gear else "(buy with cash)"))
    out.append("  Cash: %d sp" % ch.cash)
    if ch.notes:
        out.append("")
        out.append("NOTES")
        for n in ch.notes:
            out.append("  - %s" % n)
    out.append("")
    out.append("GOAL / TIES: <fill in: every PC needs an active goal and a reason to")
    out.append("             trust the party> (p.29)")
    return "\n".join(out)


def render_sheet(ch):
    """Fill the assets/templates/character-sheet.md template for --out."""
    ac, worn, shtxt, dex = compute_ac(ch)
    saves = compute_saves(ch)
    wlines, ab = compute_weapon_lines(ch)
    con = ch.scores["Con"]

    def mods():
        return " · ".join("%s %d (%+d)" % (a, ch.scores[a], attr_mod(ch.scores[a])) for a in ATTRS)

    L = []
    L.append("# %s" % (ch.name or "Unnamed Hero"))
    L.append("")
    L.append("> Use this when: this is a player character's record. Extends the engine's")
    L.append("> campaign character record (`assets/templates/_engine-character-sheet.reference.md`).")
    L.append("")
    L.append("- **Level / Class:** %d  %s" % (ch.level, ch.cls["name"]))
    L.append("- **Background:** %s" % ch.background)
    L.append("- **Goal:** <active goal — required>")
    L.append("- **Ties:** <why this PC trusts the party>")
    L.append("")
    L.append("## Attributes")
    L.append("| Str | Dex | Con | Int | Wis | Cha |")
    L.append("|-----|-----|-----|-----|-----|-----|")
    L.append("| %s |" % " | ".join("%d (%+d)" % (ch.scores[a], ch.amod(a)) for a in ATTRS))
    L.append("")
    L.append("## Defenses & Health")
    L.append("- **AC:** %d  (%s%s, Dex %+d)" % (ac, worn, shtxt, dex))
    L.append("- **HP:** %d / %d   ·   **System Strain:** 0 / %d (max = Con)" % (ch.hp_max, ch.hp_max, con))
    L.append("- **Attack bonus:** +%d   ·   **Initiative:** 1d8 %+d" % (ab, dex))
    L.append("- **Saves:** Physical %d · Evasion %d · Mental %d · Luck %d"
             % (saves["Physical"], saves["Evasion"], saves["Mental"], saves["Luck"]))
    L.append("")
    L.append("## Skills")
    L.append("`2d6 + level + attribute mod`")
    L.append("")
    if ch.skills:
        for k, v in sorted(ch.skills.items()):
            L.append("- %s-%d" % (k, v))
    else:
        L.append("- (none)")
    L.append("")
    L.append("## Foci")
    for f in ch.foci:
        bits = []
        if f.get("bonus_skill"):
            bits.append("skill %s" % f["bonus_skill"])
        if f.get("hp_bonus"):
            bits.append("+%d HP" % f["hp_bonus"])
        if f.get("innate_ac"):
            bits.append("innate AC %d" % f["innate_ac"])
        tail = ("  — %s" % ", ".join(bits)) if bits else ""
        L.append("- **%s** (L%d, p.%d)%s — %s" % (f["name"], f["level"], f["page"], tail, f["note"]))
    L.append("")
    if ch.traditions:
        L.append("## Magic")
        for t in ch.traditions:
            kind = "caster" if t["caster"] else "art-user"
            L.append("- **%s** (%s) — **Effort %d**" % (t["name"], kind, t["effort"]))
            if t["arts"]:
                L.append("  - Arts: %s" % ", ".join(t["arts"]))
            if t.get("art_pick_note") and "choose" in t["art_pick_note"]:
                L.append("  - _%s_" % t["art_pick_note"])
        if ch.spells:
            L.append("- **Spells (1st circle):** %s" % ", ".join(ch.spells))
        L.append("")
    L.append("## Weapons")
    L.append("| Weapon | Hit | Damage | Shock | Notes |")
    L.append("|--------|-----|--------|-------|-------|")
    for (nm, hit, dmg, shock, note) in wlines:
        if hit is None:
            L.append("| %s | — | — | — | %s |" % (nm, note))
        else:
            L.append("| %s | %+d | %s | %s | %s |" % (nm, hit, dmg, shock, note))
    L.append("")
    L.append("## Armor & Gear")
    L.append("- **Armor:** %s   ·   **Shield:** %s" % (ch.armor, ch.shield or "none"))
    L.append("- **Gear:** %s" % ("; ".join(ch.gear) if ch.gear else "(buy with cash)"))
    L.append("- **Cash / wealth:** %d sp" % ch.cash)
    L.append("")
    L.append("## Record-keeping")
    L.append("- **XP:** 0")
    L.append("- **Conditions / injuries:** none")
    L.append("- **Languages:** native + Trade Cant + (1 per Connect/Know level-0, 2 per level-1)")
    if ch.notes:
        L.append("")
        L.append("## Notes")
        for n in ch.notes:
            L.append("- %s" % n)
    L.append("")
    L.append("_Generated by `scripts/chargen.py`. Rules: Character Creation (book pp.8-35),"
             " Equipment (pp.36-41)._")
    return "\n".join(L)


# ---------------------------------------------------------------------------
# FUZZY MATCHERS
# ---------------------------------------------------------------------------
def _match_one(query, options, kind):
    q = query.strip().lower()
    for o in options:
        if o.lower() == q:
            return o
    cands = [o for o in options if q in o.lower()]
    if len(cands) == 1:
        return cands[0]
    sys.exit("Unknown %s '%s'. Options: %s" % (kind, query, ", ".join(sorted(options))))


def _match_background(q):
    return _match_one(q, list(BACKGROUNDS.keys()), "background")


def _match_focus(q):
    return _match_one(q, list(FOCI.keys()), "focus")


def _match_tradition(q):
    return _match_one(q, list(TRADITIONS.keys()), "tradition")


def _match_package(q):
    return _match_one(q.replace(" ", "-"), list(PACKAGES.keys()), "package")


def _normalize_class(q):
    k = q.strip().lower().replace(" ", "")
    k = k.replace("/", "/")  # keep slashes
    if k in CLASSES:
        return k
    if k in CLASS_ALIASES:
        return CLASS_ALIASES[k]
    # try partial spelled out
    for full, canon in CLASS_ALIASES.items():
        if k == full.replace(" ", ""):
            return canon
    sys.exit("Unknown class '%s'. Options: warrior, expert, mage, adventurer, "
             "partial-expert/partial-warrior, partial-expert/partial-mage, "
             "partial-mage/partial-warrior, partial-mage/partial-mage." % q)


# ---------------------------------------------------------------------------
# INTERACTIVE (step-by-step, player-in-the-loop; honest dice shown)
# ---------------------------------------------------------------------------
def _in(prompt, default=""):
    try:
        s = input(prompt).strip()
    except EOFError:
        s = ""
    return s or default


def _choose(label, options, allow_blank_random=True, n=1):
    """Prompt for one or n options from a numbered list; blank = random pick(s)."""
    print("  %s:" % label)
    for i, o in enumerate(options, 1):
        print("    %2d) %s" % (i, o))
    picks = []
    while len(picks) < n:
        hint = " (blank = random)" if allow_blank_random else ""
        s = _in("  choose %s%s: " % ("#%d" % (len(picks) + 1) if n > 1 else "one", hint))
        if not s and allow_blank_random:
            rest = [o for o in options if o not in picks] or options
            picks.append(random.choice(rest))
            print("    -> %s (random)" % picks[-1])
            continue
        if s.isdigit() and 1 <= int(s) <= len(options):
            cand = options[int(s) - 1]
        else:
            try:
                cand = _match_one(s, options, label)
            except SystemExit:
                print("    ? not recognized")
                continue
        if cand in picks:
            print("    already picked")
            continue
        picks.append(cand)
    return picks if n > 1 else picks[0]


def run_interactive(args):
    print("\n=== Interactive WWN character creation — book order, honest dice shown ===")
    print("(Press Enter at most prompts to let the dice/the script decide.)")
    ch = Character()
    ch.level = max(1, args.level)
    ch.name = args.name or _in("Name (optional): ")

    # --- STEP 1: ATTRIBUTES -------------------------------------------------
    section("STEP 1 - ATTRIBUTES  (p.9)")
    if _in("Roll 3d6 in order (r) or take the array 14/12/11/10/9/7 (a)? [r]: ", "r").lower().startswith("a"):
        vals = [14, 12, 11, 10, 9, 7]
        print("  Assign the array %s." % vals)
        remaining = list(vals)
        for a in ATTRS:
            v = _choose("%s — assign a value" % a, [str(x) for x in remaining], allow_blank_random=True)
            ch.scores[a] = int(v)
            remaining.remove(int(v))
        print("  (Array taken: no free 14.)")
    else:
        for a in ATTRS:
            ch.scores[a] = roll("3d6", label=a)
        p = _in("Set ONE attribute to 14 (you rolled)? name or blank to skip: ")
        if p:
            pa = _match_one(p, ATTRS, "attribute")
            if ch.scores[pa] < 14:
                ch.scores[pa] = 14
                print("  %s -> 14" % pa)
    for a in ATTRS:
        print("    %-3s %2d  (mod %+d)" % (a, ch.scores[a], ch.amod(a)))

    # --- STEP 2: BACKGROUND -------------------------------------------------
    section("STEP 2 - BACKGROUND  (p.11)")
    if _in("Roll for background (r) or pick (p)? [p]: ", "p").lower().startswith("r"):
        r = roll("1d20", label="background")
        bg_name = BACKGROUND_D20[r - 1]
        print("  Rolled: %s" % bg_name)
    else:
        bg_name = _choose("Background", BACKGROUND_D20, allow_blank_random=True)
    ch.background = bg_name
    bg = BACKGROUNDS[bg_name]
    g, l = ch.gain_skill(bg["free"])
    print("  Free skill: %s-%d" % (g, l))
    m = _in("Skills: quick (q) / pick two Learning (p) / roll three (r)? [q]: ", "q").lower()
    if m.startswith("p"):
        opts = [s for s in bg["learning"] if s != "Any Skill"]
        for s in _choose("Pick TWO Learning skills", opts, allow_blank_random=True, n=2):
            gg, ll = ch.gain_skill(s)
            print("    %s-%d" % (gg, ll))
    elif m.startswith("r"):
        for i in range(3):
            t = _in("  roll #%d on Growth (g) or Learning (l)? [l]: " % (i + 1), "l").lower()
            if t.startswith("g"):
                rr = roll("1d6", label="%s Growth" % bg_name)
                _apply_growth(ch, bg["growth"][rr - 1])
            else:
                rr = roll("1d8", label="%s Learning" % bg_name)
                gg, ll = ch.gain_skill(bg["learning"][rr - 1])
                print("    Learning: %s -> %s-%d" % (bg["learning"][rr - 1], gg, ll))
    else:
        for s in bg["quick"]:
            gg, ll = ch.gain_skill(s)
            print("    Quick: %s-%d" % (gg, ll))

    # --- STEP 3: CLASS ------------------------------------------------------
    section("STEP 3 - CLASS  (pp.18-21)")
    print("  Core: warrior · expert · mage")
    print("  Adventurer combos: partial-expert/partial-warrior · partial-expert/partial-mage ·")
    print("                     partial-mage/partial-warrior · partial-mage/partial-mage")
    print("  Name a tradition directly in the mage slot, e.g. partial-warrior/partial-healer,")
    print("  partial-expert/vowed, necromancer/healer, or just: high-mage / necromancer / elementalist.")
    spec = _in("Class: ", "expert")
    base, named = parse_class(spec)
    if "vowed" in spec.lower() or any(t == "Vowed" for t in named):
        vs = _in("Vowed order-skill (Exert/Know/Pray/Magic...) [Exert]: ", "Exert")
        ch.vowed_skill = _match_one(vs, NONCOMBAT_SKILLS, "skill")
    # let the player name any unfilled traditions
    n_slots = 1 if base == "mage" else base.count("partial-mage")
    trads = list(named)
    for i in range(len(trads), n_slots):
        pool = CASTING_TRADITIONS if base == "mage" else list(TRADITIONS.keys())
        trads.append(_choose("Tradition for mage slot %d" % (i + 1), pool, allow_blank_random=True))
    # build class state directly (mirror of step_class, without re-prompting)
    ch.cls_key = base
    ch.cls = CLASSES[base]
    _setup_traditions(ch, base, trads, random_choice=False)
    if any(t["name"] == "Vowed" for t in ch.traditions) and "-" in ch.cls["hd"](ch.level):
        ch.cls = dict(ch.cls); ch.cls["hd"] = _hd(0)
        ch.notes.append("Vowed Martial Style floors the hit die at 1d6/level.")
    print("  %s | attack +%d (L%d) | %s"
          % (ch.cls["name"], ch.cls["ab"][ch.level - 1], ch.level, ch.cls["ability"]))

    # --- STEP 4: FOCI -------------------------------------------------------
    section("STEP 4 - FOCI  (pp.22-28)")
    slots = []
    for kind, cnt in ch.cls["foci"]:
        slots += [kind] * cnt
    slots += ["any"] * sum(1 for lv in (2, 5, 7, 10) if lv <= ch.level)
    for kind in slots:
        pool = sorted(n for n in FOCI if _focus_ok_for(ch, n, kind)
                      and n not in {x["name"] for x in ch.foci})
        nm = _choose("Focus [%s slot]" % kind, pool, allow_blank_random=True)
        _apply_focus(ch, nm, kind)

    # --- STEP 5: FINAL ------------------------------------------------------
    section("STEP 5 - FINAL TOUCHES  (pp.28-29)")
    fs = _in("Free skill pick (name) [random]: ")
    if fs:
        g, l = ch.gain_skill(_match_one(fs, SKILLS, "skill"))
    else:
        g, l = ch.gain_skill("Any Skill")
    print("  Free skill: %s-%d" % (g, l))
    hd = ch.cls["hd"](ch.level)
    base_hp = roll(hd, label="hit points (%s)" % ch.cls["name"])
    hp = max(1, base_hp + ch.amod("Con"))
    ch.hp_max = ch.hp_max - 1 + hp if ch.hp_max != 1 else hp
    print("  HP = %s + Con(%+d) = %d (min 1)" % (hd, ch.amod("Con"), hp))
    if _in("Equipment: package (k) or roll 3d6x10 silver (r)? [k]: ", "k").lower().startswith("r"):
        ch.cash = roll("3d6", label="wealth x10") * 10
        ch.notes.append("Spend %d sp on gear (pp.33-37)." % ch.cash)
    else:
        pk = _choose("Equipment package", list(PACKAGES.keys()),
                     allow_blank_random=True)
        P = PACKAGES[pk]
        ch.armor, ch.shield = P["armor"], P["shield"]
        ch.weapons, ch.gear, ch.cash = list(P["weapons"]), list(P["gear"]), P["cash"]
    if ch.traditions:
        chooser = lambda label, options, n: _choose(label, options, allow_blank_random=True, n=n)
        _finalize_traditions(ch, random_choice=False, chooser=chooser)
    print("\n  Goal & ties — every PC needs an active goal worth dying for, and a reason to trust the party.")
    ch.notes.append("Goal: %s" % _in("  Goal: ", "<fill in>"))
    ch.notes.append("Ties: %s" % _in("  Ties: ", "<fill in>"))
    return ch


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description="Create a Worlds Without Number character (honest dice).")
    ap.add_argument("--name")
    ap.add_argument("--background")
    ap.add_argument("--class", dest="cls")
    ap.add_argument("--level", type=int, default=1)
    ap.add_argument("--random", action="store_true",
                    help="make every unspecified choice by an honest roll")
    ap.add_argument("--package", help="equipment package id (see --help-packages)")
    ap.add_argument("--roll-wealth", action="store_true", help="roll 3d6x10 sp instead of a package")
    ap.add_argument("--focus", action="append", help="name a focus (repeatable, in slot order)")
    ap.add_argument("--seed", type=int, help="seed the dice for reproducibility")
    ap.add_argument("--out", help="write the filled character sheet to this path")
    ap.add_argument("--set14", help="attribute (Str..Cha) to set to 14 after rolling")
    ap.add_argument("--skill-mode", choices=["quick", "pick", "roll"], default="quick",
                    help="background skill acquisition (default quick; --random forces roll)")
    ap.add_argument("--tradition", action="append",
                    help="name a mage tradition (repeatable, per mage slot): "
                         "High Mage|Elementalist|Necromancer|Healer|Vowed")
    ap.add_argument("--vowed-skill", help="the Vowed order-skill (drives Effort), e.g. Exert/Know/Pray")
    ap.add_argument("--interactive", "--step", action="store_true", dest="interactive",
                    help="walk through creation step by step, player-in-the-loop")
    args = ap.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    print("Worlds Without Number — Character Creation (honest dice shown)")
    if _engine_dice_available():
        print("(engine dice.py detected at MYTHIC_GM_DICE; rolls shown here in matching format)")
    if args.seed is not None:
        print("Seed: %d" % args.seed)

    if args.interactive:
        ch = run_interactive(args)
        summary = render_summary(ch)
        print(summary)
        if args.out:
            with open(args.out, "w", encoding="utf-8") as fh:
                fh.write(render_sheet(ch) + "\n")
            print("\nCharacter sheet written to %s" % args.out)
        return

    ch = Character()
    ch.name = args.name
    ch.level = max(1, args.level)
    if args.vowed_skill:
        ch.vowed_skill = _match_one(args.vowed_skill, NONCOMBAT_SKILLS, "skill")

    # class first so attribute-14 and foci choices can be class-aware
    step_class(ch, key=args.cls, random_choice=args.random, traditions=args.tradition)
    step_attributes(ch, set14=args.set14, random_choice=args.random)
    step_background(ch, name=args.background, mode=args.skill_mode, random_choice=args.random)
    step_foci(ch, requested=args.focus, random_choice=args.random)
    step_final(ch, package=args.package, roll_wealth=args.roll_wealth, random_choice=args.random)

    summary = render_summary(ch)
    print(summary)

    if args.out:
        sheet = render_sheet(ch)
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(sheet + "\n")
        print("\nCharacter sheet written to %s" % args.out)


if __name__ == "__main__":
    main()
