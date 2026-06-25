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
import json
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
# TRADITIONS (WWN Magic ch., pp.64-97; Gyre pp.348-359; Atlas pp.385-838).
# A "tradition" is the arcane / arts profession that fills a caster slot, OR
# (for the Atlas/Gyre partial-class chassis) a non-spellcasting Arts profession
# layered onto a partial slot.  Each entry:
#   slot            : which partial slot it occupies — "mage" | "expert" | "warrior".
#   availability    : "full" | "partial" | "both".
#   casts           : "none" | "highmagic" | "highmagic+newmagic" | "spellpoints".
#   effort          : None (no Effort pool — Spell-Point or no-resource traditions),
#                     or {"skill":.., "attrs":[..], "base":0|1, "partial_penalty":bool}.
#                     If "best" is in attrs, the BEST modifier of all six is used.
#   bonus_skill     : skill granted at level-0 (stacks to level-1), or None.
#   auto_arts       : arts auto-granted at L1.
#   arts_pick       : # of arts the player additionally chooses at L1.
#   armor_ok        : arts usable in armor?
#   hd_min_d6       : Flaw of Fragility — when paired with Warrior, floor HD at 1d6.
#   focus_grant     : a focus name granted free (Mageslayer -> Nullifier), or None.
#   note            : a one-line summary.
# ---------------------------------------------------------------------------
TRADITIONS = {
    "high-mage": {
        "display": "High Mage", "slot": "mage", "availability": "both",
        "casts": "highmagic",
        "effort": {"skill": "Magic", "attrs": ["Int", "Cha"], "base": 1, "partial_penalty": True},
        "bonus_skill": "Magic", "auto_arts": [], "arts_pick": 0,
        "armor_ok": False, "hd_min_d6": False, "focus_grant": None,
        "note": "Masters ancient High Magic; spell-manipulation arts. Cannot cast in armor."},
    "elementalist": {
        "display": "Elementalist", "slot": "mage", "availability": "both",
        "casts": "highmagic+newmagic",
        "effort": {"skill": "Magic", "attrs": ["Int", "Cha"], "base": 1, "partial_penalty": True},
        "bonus_skill": "Magic",
        "auto_arts": ["Elemental Resilience", "Elemental Sparks"], "arts_pick": 0,
        "armor_ok": False, "hd_min_d6": False, "focus_grant": None,
        "note": "High Magic + Elementalist New Magic; element-mastery arts. No casting in armor."},
    "healer": {
        "display": "Healer", "slot": "mage", "availability": "partial",
        "casts": "none",
        "effort": {"skill": "Heal", "attrs": ["Int", "Cha"], "base": 0, "partial_penalty": False},
        "bonus_skill": "Heal", "auto_arts": ["Healing Touch"], "arts_pick": 1,
        "armor_ok": True, "hd_min_d6": False, "focus_grant": None,
        "note": "Curative adept; arts only, no spells. Heal arts work even in armor."},
    "necromancer": {
        "display": "Necromancer", "slot": "mage", "availability": "both",
        "casts": "highmagic+newmagic",
        "effort": {"skill": "Magic", "attrs": ["Int", "Cha"], "base": 1, "partial_penalty": True},
        "bonus_skill": "Magic", "auto_arts": [], "arts_pick": 0,
        "armor_ok": False, "hd_min_d6": False, "focus_grant": None,
        "note": "High Magic + Necromancer New Magic; death/undeath arts. No casting in armor."},
    "vowed": {
        "display": "Vowed", "slot": "mage", "availability": "partial",
        "casts": "none",
        "effort": {"skill": "Exert", "attrs": ["best"], "base": 0, "partial_penalty": False},
        "bonus_skill": "Exert",  # order's chosen skill; defaults to Exert
        "auto_arts": ["Martial Style", "Unarmed Might", "Unarmored Defense"], "arts_pick": 1,
        "armor_ok": False, "hd_min_d6": False, "focus_grant": None,
        "note": "Warrior-ascetic; body arts only, no spells. Built-in Unarmored Defense."},
    "adunic-invoker": {
        "display": "Adunic Invoker", "slot": "mage", "availability": "both",
        "casts": "spellpoints",
        "effort": None,  # uses Spell Points = level-based value + Int mod, not Effort
        "bonus_skill": "Magic", "auto_arts": [], "arts_pick": 0,
        "armor_ok": False, "hd_min_d6": False, "focus_grant": None,
        "note": "Spell-point caster of High Magic; no arts by default. Same armor limits as High Magic."},
    "darian-skinshifter": {
        "display": "Darian Skinshifter", "slot": "mage", "availability": "partial",
        "casts": "none",
        "effort": {"skill": "Survive", "attrs": ["Con", "Cha"], "base": 0, "partial_penalty": False},
        "bonus_skill": "Survive", "auto_arts": ["Change Form"], "arts_pick": 1,
        "armor_ok": False, "hd_min_d6": False, "focus_grant": None,
        "note": "Shapeshifter; arts only, no spells. One alternate form per level."},
    "kistian-duelist": {
        "display": "Kistian Duelist", "slot": "mage", "availability": "partial",
        "casts": "none",
        "effort": {"skill": "Stab", "attrs": ["Dex", "Int"], "base": 0, "partial_penalty": False},
        "bonus_skill": "Stab", "auto_arts": ["Favored Weapon"], "arts_pick": 1,
        "armor_ok": False, "hd_min_d6": True, "focus_grant": None,
        "note": "Light-armor duelist; arts only. Flaw of Fragility -> 1d6 HD with a Warrior."},
    "llaigisan-beastmaster": {
        "display": "Llaigisan Beastmaster", "slot": "mage", "availability": "partial",
        "casts": "none",
        "effort": {"skill": "Survive", "attrs": ["Wis", "Cha"], "base": 0, "partial_penalty": False},
        "bonus_skill": "Survive", "auto_arts": ["Bind Companion"], "arts_pick": 1,
        "armor_ok": True, "hd_min_d6": False, "focus_grant": None,
        "note": "Animal-companion master; arts only, no spells. Arts usable while armored."},
    "sarulite-blood-priest": {
        "display": "Sarulite Blood Priest", "slot": "mage", "availability": "partial",
        "casts": "none",
        "effort": {"skill": "Pray", "attrs": ["Wis", "Cha"], "base": 0, "partial_penalty": False},
        "bonus_skill": "Pray", "auto_arts": [], "arts_pick": 2,
        "armor_ok": True, "hd_min_d6": False, "focus_grant": None,
        "note": "Fighting-priest; chooses two miracles (arts) at L1. Miracles unhindered by armor."},
    "vothite-thought-noble": {
        "display": "Vothite Thought Noble", "slot": "mage", "availability": "partial",
        "casts": "none",
        "effort": {"skill": "Notice", "attrs": ["Int", "Wis"], "base": 0, "partial_penalty": False},
        "bonus_skill": "Notice", "auto_arts": ["Open Mind"], "arts_pick": 1,
        "armor_ok": False, "hd_min_d6": False, "focus_grant": None,
        "note": "Mind-control psychic; arts only, no spells. Effort from Notice."},
    "accursed": {
        "display": "The Accursed", "slot": "mage", "availability": "partial",
        "casts": "none",
        "effort": {"skill": "Magic", "attrs": ["Int", "Cha"], "base": 0, "partial_penalty": False},
        "bonus_skill": "Magic", "auto_arts": ["Accursed Blade or Accursed Bolt"], "arts_pick": 1,
        "armor_ok": True, "hd_min_d6": False, "focus_grant": None,
        "note": "Outsider-pacted Mage; arts only, no spells. Accursed arts usable in or out of armor."},
    "bard": {
        "display": "The Bard", "slot": "expert", "availability": "partial",
        "casts": "none",
        "effort": {"skill": "Perform", "attrs": ["Cha"], "base": 0, "partial_penalty": False},
        "bonus_skill": "Perform", "auto_arts": ["A Thousand Tongues"], "arts_pick": 1,
        "armor_ok": True, "hd_min_d6": False, "focus_grant": None,
        "note": "Performer; non-magical Legacy arts hearten allies. No bonus Expert focus/skill."},
    "mageslayer": {
        "display": "The Mageslayer", "slot": "warrior", "availability": "partial",
        "casts": "none",
        "effort": {"skill": "Magic", "attrs": ["Int", "Con"], "base": 0, "partial_penalty": False},
        "bonus_skill": "Magic", "auto_arts": ["Antimage", "Magebane"], "arts_pick": 0,
        "armor_ok": True, "hd_min_d6": False, "focus_grant": "Nullifier",
        "note": "Wizard-killer; fixed arts (Antimage grants a free Nullifier focus). No Mage pairing."},
    "wise": {
        "display": "The Wise", "slot": "expert", "availability": "partial",
        "casts": "none",
        "effort": None,  # The Wise do NOT use Effort; arts are constant or X/day
        "bonus_skill": "Know",  # concept skill (Pray/Know/Magic/Survive); defaults to Know
        "auto_arts": [], "arts_pick": 1,  # one concept art, e.g. Holy Sanctity / Dread Awe
        "armor_ok": True, "hd_min_d6": False, "focus_grant": None,
        "note": "Low/no-magic scholar-priest-witch; arts only, no Effort, no spells."},
}
# canonical aliases / fuzzy keys for traditions
TRADITION_ALIASES = {
    "highmage": "high-mage", "high mage": "high-mage",
    "the accursed": "accursed", "the bard": "bard",
    "the mageslayer": "mageslayer", "the wise": "wise",
    "adunic": "adunic-invoker", "invoker": "adunic-invoker",
    "skinshifter": "darian-skinshifter", "darian": "darian-skinshifter",
    "duelist": "kistian-duelist", "kistian": "kistian-duelist",
    "beastmaster": "llaigisan-beastmaster", "llaigisan": "llaigisan-beastmaster",
    "blood priest": "sarulite-blood-priest", "sarulite": "sarulite-blood-priest",
    "thought noble": "vothite-thought-noble", "vothite": "vothite-thought-noble",
}


def tradition_effort(trad, ch):
    """Compute the tradition's starting Effort per the registry rule, or None
    for Spell-Point / no-resource traditions.  Returns (effort_int_or_None, basis_str)."""
    spec = trad.get("effort")
    if spec is None:
        return None, None
    if "best" in spec["attrs"]:
        amod = max(attr_mod(ch.scores[a]) for a in ATTRS)
    else:
        amod = max(attr_mod(ch.scores[a]) for a in spec["attrs"])
    skill_lvl = ch.skills.get(spec["skill"], -1)
    if skill_lvl < 0:
        skill_lvl = 0  # treat an untrained bonus-skill as level-0 baseline
    eff = spec["base"] + skill_lvl + amod
    if spec["partial_penalty"] and ch.cls.get("caster") in ("partial", "dual-partial"):
        eff -= 1
    if eff < 1:
        eff = 1
    return eff, "%s-based" % spec["skill"]


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

    # --- Atlas optional Foci (The Atlas of the Latter Earth, ch.4) ---------
    # Maqqatban Knight Styles: Warriors / Partial Warriors only; only ONE style.
    "Ghost Archer Style": {"page": 844, "skill": "Shoot", "combat": True,
                           "classes": ["warrior", "partial-warrior"], "one_style": True,
                           "note": "Manifest a spirit copy of any bow you've fired (own ammo); fire it while meleed. -4 to hit with non-bow weapons. L2: 1/scene shoot+teleport to where the arrow lands (+1 Strain)."},
    "All Directions Edge Style": {"page": 858, "skill": "Any Combat", "combat": True,
                                  "classes": ["warrior", "partial-warrior"], "one_style": True,
                                  "hd_penalty2": True,
                                  "note": "Hit die penalized 2 (1d6+2 -> 1d6). 1/round bonus On-Turn attack (extra uses cost Strain). L2: 1/day attack every enemy in range."},
    "One Point Strike Style": {"page": 862, "skill": "Any Combat", "combat": True,
                               "classes": ["warrior", "partial-warrior"], "one_style": True,
                               "note": "Attacks use better of Int/Wis. Main Action: a melee hit auto-rolls as a 15 but deals minimum damage. L2: 1/scene maximize a melee hit's weapon damage."},
    "Pyre of Heaven Style": {"page": 876, "skill": "Any Combat", "combat": True,
                             "classes": ["warrior", "partial-warrior"], "one_style": True,
                             "note": "Ignore first 5 fire/heat dmg/round. Instant (+1 Strain): ignite weapon for +level+2 dmg/Shock (once/foe/scene). L2: immune to mundane flame; ignite whole body, AoE 1d6/3 levels."},
    "Catalytic Soul Style": {"page": 878, "skill": "Shoot", "combat": True,
                             "classes": ["warrior", "partial-warrior"], "one_style": True,
                             "note": "Ranged-only. Shots pass through allies; Instant: nominate an ally adjacent to your target to apply that ally's Shock. L2: on a boosted hit, you or the ally gain 1 Strain to heal 2d6 + target level (1/foe/scene)."},
    "Wrathful Mountain Style": {"page": 896, "skill": "Stab/Punch", "combat": True,
                                "classes": ["warrior", "partial-warrior"], "one_style": True,
                                "note": "-2 to all hit rolls. Manifest a 0-enc magic large shield (works hands-full); 1/round Instant melee riposte when a Screened ally is meleed. L2: riposte vs ranged too; +1 Strain to riposte all attackers that round."},
    "Righteous Iron Style": {"page": 894, "skill": "Exert", "combat": True,
                             "classes": ["warrior", "partial-warrior"], "one_style": True,
                             "note": "Heavy-armor only. Worn armor +1 AC and 0 encumbrance (keeps it for Armored Magic); no Sneak/Exert penalty; sleep in it. L1: free 750sp heavy armor. L2: need not eat/drink/sleep/breathe while armored; AC bonus becomes +2."},
    "World Tree Lance Style": {"page": 910, "skill": "Stab", "combat": True,
                               "classes": ["warrior", "partial-warrior"], "one_style": True,
                               "note": "Spears only. Spear is 0-enc, returns when thrown, +1 hit/dmg, treated as magic. L2: melee reach 10' + level; allies between you and the target don't hinder."},

    # Amundi Godblood Foci: full or partial Experts only; only ONE Godblood.
    "Master Tracker": {"page": 930, "skill": "Survive", "combat": False,
                       "classes": ["expert", "partial-expert"],
                       "note": "Follow any trail (1 day in city / 1 week wild), ignoring weather/water; read numbers, shape, condition. L2: +1 Wis mod; ID known people by tracks; 1/day reconstruct a recent scene's events."},
    "Night Walker": {"page": 948, "skill": "Sneak", "combat": False,
                     "classes": ["expert", "partial-expert"],
                     "note": "See in all but pitch black; 'see' 30' even when blinded; sleep as wakefulness. L2: +1 Dex mod; effectively invisible in any sub-torchlight gloom until you act."},
    "Danger Sense": {"page": 950, "skill": "Notice", "combat": False,
                     "classes": ["expert", "partial-expert"],
                     "note": "Spoil Execution Attacks on you/nearby; 1/day sense a trap/ambush in time to stop. L2: +1 Wis mod; 1/day Instant intuition of the best escape from peril."},
    "Pack Beast": {"page": 966, "skill": "Exert", "combat": False,
                   "classes": ["expert", "partial-expert"],
                   "note": "Treat Str as 18 (or 22 if already 18) for encumbrance. L2: +1 Str mod; 1/scene On-Turn lift/move up to 1000 lb until end of turn."},
    "Folie a Deux": {"page": 972, "skill": "Convince", "combat": False,
                     "classes": ["expert", "partial-expert"],
                     "note": "Lies never read as false; 1/day make a listener believe you absolutely sincere. L2: +1 Cha mod; 1/day a bald lie forces a Mental save (penalty = Convince) or believed 1d4 rounds."},
    "Provident Crafter": {"page": 984, "skill": "Craft", "combat": False,
                          "classes": ["expert", "partial-expert"],
                          "note": "Treat Str +4 for encumbrance; needed gear counts as Readied even if Stowed. L2: +1 Dex mod; 1/day Instant 'happen to have' a <=2-enc item (pay its price; not provisions)."},
    "Wildtongue": {"page": 982, "skill": "Survive", "combat": False,
                   "classes": ["expert", "partial-expert"],
                   "note": "Communicate simple ideas with animals; appease them for basic favors. L2: +1 Cha mod; 1/day command a visible animal for a scene (magical beasts get a Mental save)."},
    "Walk Like Wind": {"page": 1000, "skill": "Exert", "combat": False,
                       "classes": ["expert", "partial-expert"],
                       "note": "+10' move; walk up/down vertical surfaces (end on a foothold). L2: +1 Dex mod; leap 20' across/10' up as a Move; 1/scene On-Turn bonus Move action."},

    # Arcane Secret Foci: Mages / Partial Mages only; only ONE; single-level.
    "Atlantean Divination": {"page": 1016, "skill": "Know", "combat": False,
                             "classes": ["mage", "partial-mage"], "one_level": True,
                             "note": "Hour-long ritual to ask one future question (Int/Know vs 9; fail = false oracle). Max a week out; no repeats; +1 Strain/use, +1 diff per use in 7 days. (Single level.)"},
    "Iteral Pacting": {"page": 1022, "skill": "Pray", "combat": False,
                       "classes": ["mage", "partial-mage"], "one_level": True,
                       "note": "Pick a patron portfolio. 1/day +1 Strain for +4 hit, +1 skill, or cast a related 1st-level spell (no slot, even by non-casters). -1 to non-intimidation social checks. (Single level.)"},
    "Nagadi Hemomancy": {"page": 1028, "skill": "Heal", "combat": False,
                         "classes": ["mage", "partial-mage"], "one_level": True,
                         "note": "1/day after a (non-harmful) cast, take 1d4/spell-level damage to not spend the daily slot; +1 Strain/use. (Single level.)"},
    "Old Empire Sigilism": {"page": 1034, "skill": None, "combat": False,
                            "classes": ["mage", "partial-mage"], "one_level": True,
                            "note": "Embed one spell in a personal token-calyx (10 min/level + a daily slot, recoverable); cast it as a Main Action with no voice/gesture, undisruptable. (Single level.)"},
    "Vothite Mind-Sorcery": {"page": 1040, "skill": None, "combat": False,
                             "classes": ["mage", "partial-mage"], "one_level": True,
                             "note": "Cast with no voice/gesture (still Main Action, still disruptable, still no-armor); spells hide their source. Can't deal non-mental HP damage thereafter. (Single level.)"},

    # Non-Human Origin Foci: any class (no gating); single-level; choose one.
    "Choeru Beastfolk": {"page": 1058, "skill": "Convince/Connect", "combat": None,
                         "origin": True,
                         "note": "Capybara-folk. +1 Cha mod; +1 to reaction rolls in your presence; gain serviceable fluency in a language in a week."},
    "Ghoul": {"page": 1068, "skill": "Sneak", "combat": None, "origin": True,
              "note": "Must eat human flesh monthly; gain Ghoulish Vigor and +1 Str or Dex mod. Mental save daily after 21 days without, automatic frenzy at 30."},
    "!Man": {"page": 1076, "skill": "Any Non-Magic", "combat": None, "origin": True,
             "note": "Algorithmic simulacrum. 1/day Instant +1 skill or +2 hit; immune to mind-affecting magic; otherwise a normal human."},
    "Guer Beastfolk": {"page": 1082, "skill": "Notice/Sneak", "combat": None, "origin": True,
                       "note": "Swamp fox-folk. +1 Wis or Cha mod; low-light vision; +10' ground move."},
    "Accipiter Anak": {"page": 1088, "skill": "Exert", "combat": None, "origin": True,
                       "note": "Winged Anak with Accipiter Flight; -1 Con mod, +1 Dex mod."},
    "Harbinger Anak": {"page": 1092, "skill": "Sneak/Convince", "combat": None, "origin": True,
                       "note": "Face-shifting Anak with Harbinger's Face; +1 Cha mod, -1 Con mod."},
    "Aristoi Anak": {"page": 1106, "skill": "Lead", "combat": None, "origin": True,
                     "note": "Born ruler. Gain Lead + any one non-Magic skill; +1 Wis mod; use Wis for any weapon attribute."},
    "Hua Beastfolk": {"page": 1108, "skill": "Exert", "combat": None, "origin": True,
                      "note": "Bullfolk. +1 Str mod, -1 Dex mod; treat Str +4 for encumbrance; +2 max System Strain."},
    "Kitsune Beastfolk": {"page": 1116, "skill": "Notice/Convince", "combat": None, "origin": True,
                          "note": "Magical fox-folk. +1 Cha mod; gain the Elemental Sparks art (or a bonus Elementalist art if you have it)."},
    "Deepfolk": {"page": 1124, "skill": None, "combat": None, "origin": True,
                 "note": "Far-Deeps native. See in any light; half food/water/air; raise one physical attribute to 14. Sun exposure forces a Physical save/round vs Strain."},
    "Manu Beastfolk": {"page": 1132, "skill": "Exert/Survive", "combat": None, "origin": True,
                       "note": "Lizardfolk. +1 Con or Str mod, -1 Dex or Cha mod; swim at full speed; 15-min breath-hold; -1 Shock taken (min 1)."},
    "Nahu Beastfolk": {"page": 1138, "skill": "Sneak/Notice", "combat": None, "origin": True,
                       "note": "Catfolk. +1 Dex or Cha mod; claws count as daggers; low-light vision; Mental save to deal non-lethal damage."},
    "Oni": {"page": 1144, "skill": "Stab/Punch", "combat": None, "origin": True,
            "note": "Horned oni. +1 Str mod, count Str +4 for encumbrance; -1 Wis mod, -2 on Mental saves."},
    "Pichi Beastfolk": {"page": 1150, "skill": "Notice", "combat": None, "origin": True,
                        "note": "Ratfolk. +1 Wis or Dex mod, -1 Str or Con mod; low-light vision; sense objects within 10' even when blinded."},
    "Piren Beastfolk": {"page": 1156, "skill": "Exert", "combat": None, "origin": True,
                        "note": "Wolfmen. 1/scene Move action grants an adjacent ally a bonus physical Main Action (1/ally/scene)."},
    "Still Cities Undead": {"page": 1162, "skill": None, "combat": None, "origin": True,
                            "note": "Intelligent undead. No food/sleep/drink/breath (but 8h rest to recover); immune to poison/disease; auto-stabilize at 0 HP unless mangled."},
    "Sui Beastfolk": {"page": 1168, "skill": "Survive", "combat": None, "origin": True,
                      "note": "Pigfolk. +1 Con mod; immune to mundane poison; 1/day act 1 round after dropping to 0 HP (counts vs stabilization)."},
    "Tanuki Beastfolk": {"page": 1174, "skill": "Sneak", "combat": None, "origin": True,
                         "note": "Raccoon-dog folk. Climb at full move; 1/day Main Action transform as Adopt the Simulacular Visage (no languages) for 2h/level."},
    "Tengu Beastfolk": {"page": 1180, "skill": "Stab", "combat": None, "origin": True,
                        "note": "Crow-folk. Fly 30' outdoors at normal encumbrance, but cannot fight/act complexly while flying or use it for long travel."},
    "Usagi Beastfolk": {"page": 1186, "skill": "Exert/Sneak", "combat": None, "origin": True,
                        "note": "Rabbit-folk. +1 to all saves; +1 Dex mod, -1 Str or Con mod; 1/scene double ground move; 1/week auto-make a Luck save."},
    "Zakathi": {"page": 1194, "skill": "Exert", "combat": None, "origin": True,
                "note": "Laborer-folk. Raise Con to 14 (or 18 if already 14+); +2 max System Strain; must exert daily to recover with rest or gain 1 Strain overnight."},
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
        self.effort = None         # int if caster, else None
        self.effort_basis = None   # e.g. "Heal-based"; "Spell Points" handled separately
        self.spell_points = None   # int if Spell-Point caster (Adunic Invoker)
        self.tradition = None      # tradition registry dict, or None
        self.tradition2 = None     # second tradition for dual-partial casters
        self.arts = []             # list of known Art names (auto + picked)
        self.spells = []           # prepared spell names if a spell-caster
        self.notes = []

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


# ---------------------------------------------------------------------------
# CLASS-KEY -> component tokens (for focus gating + tradition compatibility).
# ---------------------------------------------------------------------------
def class_tokens(key):
    """Return the set of class component tokens for a (normalized) class key.
    e.g. 'partial-mage/partial-warrior' -> {'partial-mage','partial-warrior'};
    'mage' -> {'mage'}; 'warrior' -> {'warrior'}."""
    if not key:
        return set()
    if "/" in key:
        return set(p.strip() for p in key.split("/") if p.strip())
    return {key}


def _trad_compatible(trad, key):
    """Is tradition `trad` legal on class `key`?  Returns (ok, reason)."""
    toks = class_tokens(key)
    slot = trad["slot"]
    avail = trad["availability"]
    full_tok = slot  # "mage" / "expert" / "warrior"
    partial_tok = "partial-" + slot
    has_full = full_tok in toks
    has_partial = partial_tok in toks
    # Mageslayer additionally forbids any Mage pairing.
    if trad["display"] == "The Mageslayer":
        if any(t in toks for t in ("mage", "partial-mage")):
            return False, "The Mageslayer cannot be paired with any Mage class (only Partial Expert/Partial Warrior)."
    if has_partial:
        return True, ""
    if has_full and avail in ("full", "both"):
        return True, ""
    if has_full and avail == "partial":
        return False, "%s is a partial-only tradition; it cannot be taken by a full %s." % (trad["display"], slot.capitalize())
    return False, ("%s occupies the %s slot; your class %r has no %s component."
                   % (trad["display"], slot, key, partial_tok))


def _minimal_combo_for(trad):
    """When --tradition is given without a compatible --class, pick the simplest
    legal class key and note it."""
    slot = trad["slot"]
    avail = trad["availability"]
    if slot == "mage":
        if avail in ("full", "both"):
            return "mage"            # a full Mage can take a full/both mage tradition
        return "partial-mage/partial-warrior"   # partial-only mage tradition
    if slot == "expert":
        return "partial-expert/partial-warrior"
    if slot == "warrior":
        # warrior-slot traditions are partial-only (Mageslayer forbids mage pairing)
        return "partial-expert/partial-warrior"
    return "partial-expert/partial-warrior"


def resolve_tradition(name, random_choice=False, slot_hint=None):
    """Fuzzy-match a --tradition name to a registry entry, or pick a random one
    appropriate to slot_hint when --random.  Returns the tradition key."""
    if name:
        q = name.strip().lower()
        if q in TRADITIONS:
            return q
        if q in TRADITION_ALIASES:
            return TRADITION_ALIASES[q]
        # match against display names / keys (substring)
        cands = []
        for k, t in TRADITIONS.items():
            if q == t["display"].lower() or q == k:
                return k
            if q in t["display"].lower() or q in k:
                cands.append(k)
        if len(cands) == 1:
            return cands[0]
        if cands:
            return sorted(cands, key=lambda k: len(TRADITIONS[k]["display"]))[0]
        sys.exit("Unknown tradition '%s'. Options: %s"
                 % (name, ", ".join(sorted(t["display"] for t in TRADITIONS.values()))))
    # random pick (optionally restricted to a slot)
    pool = [k for k, t in TRADITIONS.items() if slot_hint is None or t["slot"] == slot_hint]
    return random.choice(pool)


def resolve_class_key(key=None, random_choice=False, tradition=None):
    """Resolve the final (normalized) class key WITHOUT printing or applying
    anything — so the attribute-14 auto-pick can be class-aware before the CLASS
    section is printed.  Also returns the resolved tradition key (or None) so the
    caller need not re-fuzzy-match it."""
    trad_key = None
    if tradition:
        trad_key = resolve_tradition(tradition, random_choice)
    if key is None and trad_key is not None:
        key = _minimal_combo_for(TRADITIONS[trad_key])
    if key is None:
        if random_choice:
            pool = ["warrior", "expert", "mage", "partial-expert/partial-warrior",
                    "partial-mage/partial-warrior", "partial-expert/partial-mage"]
            r = roll("1d6", label="class")
            key = pool[r - 1]
        else:
            key = random.choice(list(CLASSES.keys()))
    return _normalize_class(key), trad_key


def step_class(ch, key=None, random_choice=False, tradition=None, arts=None,
               trad_key=None, class_was_explicit=True):
    section("STEP 3 - CLASS + TRADITION  (pp.18-21; Magic ch.)")
    # If the caller pre-resolved the key/tradition (so attribute-14 could be
    # class-aware), trust them; otherwise resolve now.
    if key is None:
        key, trad_key = resolve_class_key(None, random_choice, tradition)
    if trad_key is None and tradition:
        trad_key = resolve_tradition(tradition, random_choice)
    key = _normalize_class(key)
    ch.cls_key = key
    ch.cls = CLASSES[key]
    if tradition and not class_was_explicit and trad_key is not None:
        print("  (No --class given for tradition %r; auto-picked compatible class %r.)"
              % (TRADITIONS[trad_key]["display"], key))
    print("  Class: %s" % ch.cls["name"])
    print("  Attack bonus (L%d): +%d" % (ch.level, ch.cls["ab"][ch.level - 1]))
    print("  Class ability: %s" % ch.cls["ability"])
    # Determine the tradition(s).
    if trad_key is None and (ch.cls["caster"] or tradition):
        # caster slot but no explicit tradition: pick a slot-appropriate one
        if ch.cls["caster"] == "dual-partial":
            k1 = resolve_tradition(None, True, slot_hint="mage")
            # ensure a second, distinct, partial-compatible mage tradition
            others = [k for k, t in TRADITIONS.items()
                      if t["slot"] == "mage" and k != k1]
            k2 = random.choice(others) if others else k1
            ch.tradition = TRADITIONS[k1]
            ch.tradition2 = TRADITIONS[k2]
            trad_key = k1
        else:
            trad_key = resolve_tradition(None, True, slot_hint="mage")
    if trad_key is not None:
        ok, why = _trad_compatible(TRADITIONS[trad_key], key)
        if not ok:
            sys.exit("Incompatible class/tradition: %s" % why)
        ch.tradition = TRADITIONS[trad_key]
        # The primary tradition consumes the --art picks; the secondary
        # (dual-partial) tradition auto-fills placeholders.
        _apply_tradition(ch, ch.tradition, picked_arts=arts)
        if ch.tradition2 is not None and ch.tradition2 is not ch.tradition:
            _apply_tradition(ch, ch.tradition2)


def _apply_tradition(ch, trad, picked_arts=None):
    """Grant a tradition's bonus skill, auto arts, picked arts, armor note,
    Flaw of Fragility, and any granted focus.  Records arts on the character."""
    print("  Tradition: %s" % trad["display"])
    print("      %s" % trad["note"])
    # bonus skill (stacks level-0 -> level-1)
    if trad.get("bonus_skill"):
        g, l = ch.gain_skill(trad["bonus_skill"])
        print("      Bonus skill: %s-%d" % (g, l))
    # arts: auto-granted, then player-picked (filled from --art, else placeholder)
    arts = list(trad.get("auto_arts", []))
    for a in arts:
        if a not in ch.arts:
            ch.arts.append(a)
        print("      Art (auto): %s" % a)
    n_pick = trad.get("arts_pick", 0)
    picks = list(picked_arts or [])
    for i in range(n_pick):
        if i < len(picks):
            chosen = picks[i]
        else:
            chosen = "<choose a %s art>" % trad["display"]
        ch.arts.append(chosen)
        print("      Art (pick %d/%d): %s" % (i + 1, n_pick, chosen))
    # armor note
    if not trad.get("armor_ok", False):
        ch.notes.append("%s arts/spells cannot be used in armor or with a shield (Armored Magic relaxes this)." % trad["display"])
    else:
        ch.notes.append("%s arts function normally even while armored." % trad["display"])
    # Flaw of Fragility: with a Warrior, floor the hit die at 1d6.
    if trad.get("hd_min_d6") and "partial-warrior" in class_tokens(ch.cls_key):
        if ch.cls.get("hd_floor_d6"):
            pass  # already floored
        ch.cls = dict(ch.cls)  # shallow copy so we don't mutate the shared registry
        ch.cls["hd"] = _hd(0)   # cancel the +2/die -> plain 1d6/level
        ch.cls["hd_floor_d6"] = True
        ch.notes.append("Flaw of Fragility: hit die floored at 1d6/level (no Partial Warrior +2/die).")
        print("      Flaw of Fragility: hit die floored to 1d6/level.")
    # granted focus (Mageslayer's Antimage -> free Nullifier focus level)
    if trad.get("focus_grant"):
        fname = trad["focus_grant"]
        # apply it as a granted focus (bypass class-slot gating; it is free)
        _apply_focus(ch, fname, "granted", forced=True)
        print("      Granted focus: %s (free, from %s)." % (fname, trad["display"]))


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
    # Atlas class gating: focus `classes` list vs the PC's class component tokens.
    allowed = f.get("classes")
    if allowed:
        if not (class_tokens(ch.cls_key) & set(allowed)):
            return False
    # Maqqatban one-style rule: only one style may be taken.
    if f.get("one_style") and any(FOCI[x["name"]].get("one_style") for x in ch.foci):
        return False
    if kind == "warrior" and f.get("combat") is False:
        return False
    if kind == "expert" and f.get("combat") is True:
        return False
    return True


def _origin_attr_note(ch, name):
    """Atlas Non-Human Origin / Godblood foci often shift an attribute modifier.
    We record the text rather than mutating scores (modifier caps at +2 per the
    Atlas rule; the player applies the concrete attribute their build chose)."""
    ch.notes.append("%s: apply its origin attribute modifier shift(s) by hand "
                    "(cap +2 / floor -2 per the Atlas rule)." % name)


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


def _apply_focus(ch, name, kind, forced=False):
    """Apply a focus.  forced=True skips slot/class gating (used for free
    granted foci such as the Mageslayer's Nullifier)."""
    f = FOCI[name]
    if not forced and not _focus_ok_for(ch, name, kind):
        sys.exit("Focus %r is not legal for class %r in a %r slot "
                 "(class gating / one-of rule)." % (name, ch.cls_key, kind))
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
        # Developed Attribute: +1 to a modifier. Apply to best class attribute.
        a = _choose_14_attr(ch)
        ch.notes.append("Developed Attribute: %s modifier +1 (now treated as %+d)."
                        % (a, attr_mod(ch.scores[a]) + 1))
        rec["attr_mod_bonus"] = a
    if f.get("innate_ac"):
        innate = 15 + (ch.level + 1) // 2
        rec["innate_ac"] = innate
        ch.notes.append("Impervious Defense: innate AC %d (used if > worn armor)." % innate)
    if f.get("hd_penalty2"):
        # All Directions Edge Style: hit die penalized by 2 (cancel a +2/die).
        ch.cls = dict(ch.cls)
        ch.cls["hd"] = _hd(0)
        ch.cls["hd_floor_d6"] = True
        ch.notes.append("%s: hit die penalized 2 (e.g. 1d6+2 -> 1d6)." % name)
    if f.get("origin"):
        _origin_attr_note(ch, name)
    ch.foci.append(rec)
    line = "  Focus [%s]: %s (p.%s)" % (kind, name, f["page"])
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
    con = attr_mod(ch.scores["Con"])
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

    # --- Magic: Effort / Spell Points / Arts / starting spells -----------
    if ch.tradition is not None:
        _finalize_magic(ch)


def _finalize_magic(ch):
    """Compute the tradition's Effort (or Spell Points), and assign starting
    High Magic spells for spell-casting traditions.  Arts were already recorded
    in step_class via _apply_tradition."""
    trad = ch.tradition
    casts = trad["casts"]
    print("  Magic — tradition: %s (%s)" % (trad["display"], casts))

    # Resource: Effort, Spell Points, or none.
    if casts == "spellpoints":
        # Adunic Invoker: Spell Points = level-based value + Int mod. At L1 the
        # level-based value is 1 (full or partial), so SP = 1 + Int mod (min 1).
        sp = max(1, 1 + attr_mod(ch.scores["Int"]))
        ch.spell_points = sp
        ch.effort = None
        ch.effort_basis = "Spell Points"
        print("  Spell Points = 1 (level value) + Int(%+d) = %d  (refresh each morning)"
              % (attr_mod(ch.scores["Int"]), sp))
    else:
        eff, basis = tradition_effort(trad, ch)
        if eff is None:
            ch.effort = None
            ch.effort_basis = "this tradition uses no Effort (arts are constant or X/day)"
            print("  Effort: none — %s arts are constant or used X/day, no pool." % trad["display"])
        else:
            ch.effort = eff
            ch.effort_basis = basis
            spec = trad["effort"]
            penalty = (spec["partial_penalty"] and ch.cls.get("caster") in ("partial", "dual-partial"))
            print("  Effort = base %d + %s skill(%d) + best %s mod = %d%s  (%s)"
                  % (spec["base"], spec["skill"], max(0, ch.skills.get(spec["skill"], 0)),
                     "/".join(spec["attrs"]), eff, "  (-1 partial applied)" if penalty else "", basis))

    # Starting spells (only spell-casting traditions get them).
    if casts in ("highmagic", "highmagic+newmagic", "spellpoints"):
        partial = ch.cls.get("caster") in ("partial", "dual-partial")
        n_spells = 2 if partial else 4
        ch.spells = _pick_starting_spells(n_spells)
        print("  Starting High Magic spells (%s, %d): %s"
              % ("partial" if partial else "full", n_spells, ", ".join(ch.spells)))
        if casts == "highmagic+newmagic":
            print("      (May also learn this tradition's New Magic at level-up.)")
    else:
        ch.spells = []
        print("  No spells — %s is an arts-only tradition." % trad["display"])

    if ch.arts:
        print("  Known Arts: %s" % ", ".join(ch.arts))


def _pick_starting_spells(n):
    """Choose n distinct 1st-circle High Magic spells from spells.json by honest
    roll.  Falls back to placeholders if the data file is unavailable."""
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(os.path.dirname(here), "bridge", "generators", "spells.json")
    try:
        with open(path, encoding="utf-8") as fh:
            recs = json.load(fh)["records"]
    except Exception:
        return ["<1st-level spell %d>" % (i + 1) for i in range(n)]
    pool = [name for name, r in recs.items()
            if str(r.get("circle")) == "1" and "High Magic" in str(r.get("type", "High Magic"))]
    if not pool:
        pool = [name for name, r in recs.items() if str(r.get("circle")) == "1"]
    pool = sorted(pool)
    chosen = []
    while pool and len(chosen) < n:
        idx = roll("1d%d" % len(pool), label="starting spell %d" % (len(chosen) + 1)) - 1
        chosen.append(pool.pop(idx))
    return chosen


# ---------------------------------------------------------------------------
# DERIVED NUMBERS
# ---------------------------------------------------------------------------
def compute_ac(ch):
    base = ARMOR[ch.armor][0]
    dex = attr_mod(ch.scores["Dex"])
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
    phys = s(max(attr_mod(ch.scores["Str"]), attr_mod(ch.scores["Con"])))
    evas = s(max(attr_mod(ch.scores["Int"]), attr_mod(ch.scores["Dex"])))
    ment = s(max(attr_mod(ch.scores["Wis"]), attr_mod(ch.scores["Cha"])))
    luck = max(2, 16 - L)
    return {"Physical": phys, "Evasion": evas, "Mental": ment, "Luck": luck}


def compute_weapon_lines(ch):
    """For each carried weapon, total hit bonus and damage (p.28)."""
    ab = ch.cls["ab"][ch.level - 1]
    is_warrior_attack = "warrior" in ch.cls_key  # Warriors/partials add level? No:
    # NOTE: base attack bonus already encodes class martial aptitude. The hit
    # bonus = AB + combat-skill + attr mod. (Killing Blow adds to DAMAGE only.)
    lines = []
    for wname in ch.weapons:
        # normalize package strings like "Daggers, 2" / "Bow, Large"
        key = _weapon_key(wname)
        if key not in WEAPONS:
            lines.append((wname, None, None, None, "non-weapon / see book"))
            continue
        dmg, shock, attrs, traits = WEAPONS[key]
        best_attr = max(attrs, key=lambda a: attr_mod(ch.scores[a]))
        amod = attr_mod(ch.scores[best_attr])
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
    out.append("  " + "  ".join("%s %d(%+d)" % (a, ch.scores[a], attr_mod(ch.scores[a])) for a in ATTRS))
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
    if ch.tradition is not None:
        out.append("")
        out.append("MAGIC")
        td = ch.tradition["display"]
        if ch.tradition2 is not None:
            td += " + " + ch.tradition2["display"]
        out.append("  Tradition: %s" % td)
        if ch.spell_points is not None:
            out.append("  Spell Points: %d  (basis: level value + Int mod)" % ch.spell_points)
        elif ch.effort is not None:
            out.append("  Effort: %d  (%s)" % (ch.effort, ch.effort_basis or ""))
        else:
            out.append("  Effort: none — %s" % (ch.effort_basis or "no Effort pool"))
        out.append("  Known Arts: %s" % (", ".join(ch.arts) if ch.arts else "(none)"))
        if ch.spells:
            out.append("  Prepared spells: %s" % ", ".join(ch.spells))
        else:
            out.append("  Prepared spells: (none — arts-only tradition)")
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
    L.append("| %s |" % " | ".join("%d (%+d)" % (ch.scores[a], attr_mod(ch.scores[a])) for a in ATTRS))
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
    if ch.tradition is not None:
        L.append("## Magic")
        td = ch.tradition["display"]
        if ch.tradition2 is not None:
            td += " + " + ch.tradition2["display"]
        L.append("- **Tradition:** %s" % td)
        if ch.spell_points is not None:
            L.append("- **Spell Points:** %d  (level value + Int modifier; refresh each morning)"
                     % ch.spell_points)
        elif ch.effort is not None:
            L.append("- **Effort:** %d  (%s)" % (ch.effort, ch.effort_basis or ""))
        else:
            L.append("- **Effort:** none — %s" % (ch.effort_basis or "this tradition uses no Effort"))
        L.append("- **Known Arts:** %s" % (", ".join(ch.arts) if ch.arts else "(none)"))
        L.append("- **Prepared spells:** %s"
                 % (", ".join(ch.spells) if ch.spells else "(none — arts-only tradition)"))
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
    ap.add_argument("--tradition", help="arcane/arts tradition (e.g. healer, 'high mage', "
                                        "necromancer, bard, mageslayer, accursed, wise, "
                                        "'adunic invoker', 'kistian duelist', ...)")
    ap.add_argument("--art", action="append",
                    help="name an Art the tradition lets you pick (repeatable)")
    ap.add_argument("--seed", type=int, help="seed the dice for reproducibility")
    ap.add_argument("--out", help="write the filled character sheet to this path")
    ap.add_argument("--set14", help="attribute (Str..Cha) to set to 14 after rolling")
    ap.add_argument("--skill-mode", choices=["quick", "pick", "roll"], default="quick",
                    help="background skill acquisition (default quick; --random forces roll)")
    args = ap.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    print("Worlds Without Number — Character Creation (honest dice shown)")
    if _engine_dice_available():
        print("(engine dice.py detected at MYTHIC_GM_DICE; rolls shown here in matching format)")
    if args.seed is not None:
        print("Seed: %d" % args.seed)

    ch = Character()
    ch.name = args.name
    ch.level = max(1, args.level)

    # Resolve the class key (and any named tradition) SILENTLY first, so the
    # attribute-14 auto-pick is class-aware — but PRINT the steps in the player's
    # reading order: Attributes -> Background -> Class(+Tradition) -> Foci -> Final.
    cls_key, trad_key = resolve_class_key(args.cls, args.random, args.tradition)
    ch.cls_key = cls_key
    ch.cls = CLASSES[cls_key]

    step_attributes(ch, set14=args.set14, random_choice=args.random)
    step_background(ch, name=args.background, mode=args.skill_mode, random_choice=args.random)
    step_class(ch, key=cls_key, random_choice=args.random, tradition=args.tradition,
               arts=args.art, trad_key=trad_key, class_was_explicit=(args.cls is not None))
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
