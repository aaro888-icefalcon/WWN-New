#!/usr/bin/env python3
"""
build_faction.py — (re)build bridge/generators/faction.json from the WWN faction
rules (Worlds Without Number Deluxe, ch.10 "Factions and Major Projects", pp.326-347).

This is a SEPARATE builder from scripts/build_data.py (which is left untouched).
It emits ONE kind:"bundle" file holding the WWN faction reference data the
Faction Turn needs:

  * faction_tags            — name + effect (the special qualities a faction may have)
  * Cunning_assets          — full asset catalog (rating req, cost, HP, attack, counter, ability)
  * Force_assets            — "
  * Wealth_assets           — "
  * background_actor_events — rollable: a generic d20 table + six d12 actor sub-tables
  * example_goals           — rollable: faction goals with their difficulty (XP value)
  * tables (meta)           — the HP-by-rating / XP-cost table and the faction-turn earn formula

faction_turn.py reads this file. lookup.py / gen.py can also surface single
records. The validator (mythic-gm/scripts/bridge.py) only roll-tests files whose
TOP-LEVEL "type" starts with "list_"; a bundle (no top-level list_ type) is safe
even though its inner rollable tables declare list_dN types.

Std-lib only; Python 3.6+.  Run:  python3 scripts/build_faction.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(HERE)
OUT = os.path.join(SKILL_ROOT, "bridge", "generators", "faction.json")

SRC = "Worlds Without Number Deluxe, Factions and Major Projects (pp.326-347)"

# ---------------------------------------------------------------------------
# Faction Tags  (book 10, "Faction Tags")
# ---------------------------------------------------------------------------
FACTION_TAGS = [
    {"name": "Antimagical",
     "effect": "Dwarven or other skilled counter-sorcerers. Assets that require Medium or "
               "higher Magic to purchase roll all attribute checks twice against this faction "
               "during an Attack and take the worst roll."},
    {"name": "Concealed",
     "effect": "All Assets the faction purchases enter play with the Stealth quality."},
    {"name": "Imperialist",
     "effect": "Once per turn it can use the Expand Influence action as a free special ability "
               "instead of it taking a full action."},
    {"name": "Innovative",
     "effect": "Can purchase Assets as if their attribute ratings were two points higher than "
               "they are. Only two such over-complex Assets may be owned at any one time."},
    {"name": "Machiavellian",
     "effect": "Diabolically cunning. Rolls an extra die for all Cunning attribute checks. "
               "Its Cunning must always be its highest attribute."},
    {"name": "Martial",
     "effect": "Devoted to war. Rolls an extra die for all Force attribute checks. Force must "
               "always be its highest attribute."},
    {"name": "Massive",
     "effect": "An empire or huge edifice. Automatically wins attribute checks if its attribute "
               "is more than twice the opposing side's, unless the other side is also Massive."},
    {"name": "Mobile",
     "effect": "Exceptionally fast. Its faction-turn movement range is twice what another "
               "faction would have in the same situation."},
    {"name": "Populist",
     "effect": "Widespread popular support. Assets costing 5 Treasure or less to buy cost one "
               "point less, to a minimum of 1."},
    {"name": "Rich",
     "effect": "Rich or mercantile. Rolls an extra die for all Wealth attribute checks. Wealth "
               "must always be its highest attribute."},
    {"name": "Rooted",
     "effect": "Deep roots in its area. Rolls an extra die for checks in its headquarters; all "
               "rivals roll their checks there twice and take the worst die."},
    {"name": "Scavenger",
     "effect": "When it destroys an enemy Asset it gains a quarter of that Asset's purchase "
               "value in Treasure, rounded up."},
    {"name": "Supported",
     "effect": "Excellent logistics. All damaged Assets except Bases of Influence regain one "
               "lost hit point per faction turn automatically."},
    {"name": "Tenacious",
     "effect": "Hard to dislodge. When one of its Bases of Influence is reduced to zero HP it "
               "instead survives with 1 HP. Not usable again on that base until fully fixed."},
    {"name": "Zealot",
     "effect": "Once per turn, when an Asset fails an Attack action check, it can reroll the "
               "check. It automatically takes the target's counterattack damage, or 1d6 if the "
               "target has less or none."},
]

# ---------------------------------------------------------------------------
# Asset catalogs.  Stats transcribed from the book's Cunning / Force / Wealth
# asset tables; the "ability" line is the asset's special-ability text (trimmed).
# Fields: name · rating (attribute req) · cost · hp · magic · attack · counter ·
#         qualities · ability
# attack/counter "-" means none.
# ---------------------------------------------------------------------------

CUNNING_ASSETS = [
    # Cunning 1
    {"name": "Informers", "rating": 1, "cost": 2, "hp": 3, "magic": "None",
     "attack": "C v. C / Special", "counter": "-", "qualities": ["Subtle", "Special"],
     "ability": "Free action, once/turn, spend 1 Treasure: make a Cunning vs. Cunning Attack on "
                "a chosen faction; on success, all that faction's Stealthed Assets within one "
                "move are revealed. No counterattack on failure."},
    {"name": "Petty Seers", "rating": 1, "cost": 2, "hp": 2, "magic": "Medium",
     "attack": "-", "counter": "1d6 damage", "qualities": ["Subtle"],
     "ability": "Fortune-tellers who foresee perils and allow swift counterattacks."},
    {"name": "Smugglers", "rating": 1, "cost": 2, "hp": 4, "magic": "None",
     "attack": "C v. W / 1d4 damage", "counter": "-", "qualities": ["Subtle", "Action"],
     "ability": "Free action, once/turn: move any allied Wealth or Cunning Asset in their "
                "location to a destination in range, even where an un-Subtle Asset is forbidden."},
    {"name": "Useful Idiots", "rating": 1, "cost": 1, "hp": 2, "magic": "None",
     "attack": "-", "counter": "-", "qualities": ["Subtle", "Special"],
     "ability": "Disposable minions. If another Asset within one move is struck by an Attack, "
                "the faction can sacrifice the Useful Idiots to negate it. Only one band per turn."},
    # Cunning 2
    {"name": "Blackmail", "rating": 2, "cost": 4, "hp": 4, "magic": "None",
     "attack": "C v. C / 1d4 damage", "counter": "-", "qualities": ["Subtle", "Special"],
     "ability": "While in a location, hostile factions can't roll more than one die for Attacks "
                "by or against them there, even with tags/Assets that grant bonus dice."},
    {"name": "Dancing Girls", "rating": 2, "cost": 4, "hp": 3, "magic": "None",
     "attack": "C v. W / 2d4 damage", "counter": "-", "qualities": ["Subtle", "Special"],
     "ability": "Immune to Attack/Counterattack damage from Force Assets, but cannot defend "
                "against Attacks from Force Assets."},
    {"name": "Hired Friends", "rating": 2, "cost": 4, "hp": 4, "magic": "None",
     "attack": "C v. C / 1d6 damage", "counter": "-", "qualities": ["Subtle", "Special"],
     "ability": "Free action, once/turn, spend 1 Treasure: grant a Wealth Asset within one move "
                "the Subtle quality until the Hired Friends are destroyed or reuse this."},
    {"name": "Saboteurs", "rating": 2, "cost": 5, "hp": 6, "magic": "None",
     "attack": "C v. W / 2d4 damage", "counter": "-", "qualities": ["Subtle", "Special"],
     "ability": "An Asset Attacked by the Saboteurs can't use any free-action abilities next "
                "turn, whether or not the Attack succeeded."},
    # Cunning 3
    {"name": "Bewitching Charmer", "rating": 3, "cost": 6, "hp": 4, "magic": "Low",
     "attack": "C v. C / Special", "counter": "-", "qualities": ["Subtle", "Special"],
     "ability": "On a successful Attack, the target can't leave the Charmer's location until the "
                "Charmer moves or is destroyed. Immune to Counterattack."},
    {"name": "Covert Transport", "rating": 3, "cost": 8, "hp": 4, "magic": "None",
     "attack": "-", "counter": "-", "qualities": ["Subtle", "Special"],
     "ability": "Free action, once/turn, pay 1 Treasure: move any Cunning or Wealth Asset in its "
                "location; the moved Asset gains Stealth until it acts or is used."},
    {"name": "Occult Infiltrators", "rating": 3, "cost": 6, "hp": 4, "magic": "Medium",
     "attack": "C v. C / 2d6 damage", "counter": "-", "qualities": ["Subtle", "Special"],
     "ability": "Magically-gifted spies/assassins; always begin play with the Stealth quality."},
    {"name": "Spymaster", "rating": 3, "cost": 8, "hp": 4, "magic": "None",
     "attack": "C v. C / 1d6 damage", "counter": "2d6 damage", "qualities": ["Subtle"],
     "ability": "A veteran operative running a counterintelligence bureau and offensive schemes."},
    # Cunning 4
    {"name": "Court Patronage", "rating": 4, "cost": 8, "hp": 8, "magic": "None",
     "attack": "C v. C / 1d6 damage", "counter": "1d6 damage", "qualities": ["Subtle", "Special"],
     "ability": "Automatically grants 1 Treasure to its owning faction each turn."},
    {"name": "Idealistic Thugs", "rating": 4, "cost": 8, "hp": 12, "magic": "None",
     "attack": "C v. F / 1d6 damage", "counter": "1d6 damage", "qualities": ["Subtle"],
     "ability": "Easily-manipulated hotheads enlisted under whatever ideology enthuses them for "
                "violence."},
    {"name": "Seditionists", "rating": 4, "cost": 12, "hp": 8, "magic": "None",
     "attack": "Special", "counter": "-", "qualities": ["Subtle"],
     "ability": "In place of an Attack, spend 1d4 Treasure to attach to a hostile Asset in the "
                "same location; until destroyed, moved, or relocated, that Asset can't be used "
                "and grants no benefits."},
    {"name": "Vigilant Agents", "rating": 4, "cost": 12, "hp": 8, "magic": "None",
     "attack": "-", "counter": "1d4 damage", "qualities": ["Subtle", "Special"],
     "ability": "When another faction moves a Stealthed Asset within one move, make a Cunning "
                "vs. Cunning Attack; on success the intruder loses Stealth after the move."},
    # Cunning 5
    {"name": "Cryptomancers", "rating": 5, "cost": 14, "hp": 6, "magic": "Low",
     "attack": "C v. C / Special", "counter": "-", "qualities": ["Subtle"],
     "ability": "In place of an Attack, make a Cunning vs. Cunning attack on a hostile Asset "
                "within one move; on success it can't act or be used on its owner's next turn. "
                "No counterattack on failure."},
    {"name": "Organization Moles", "rating": 5, "cost": 8, "hp": 10, "magic": "None",
     "attack": "C v. C / 2d6 damage", "counter": "-", "qualities": ["Subtle"],
     "ability": "Sleeper agents burrowed into hostile organizations to disrupt them on command."},
    {"name": "Shapeshifters", "rating": 5, "cost": 14, "hp": 8, "magic": "Medium",
     "attack": "C v. C / 2d6 damage", "counter": "-", "qualities": ["Subtle", "Special"],
     "ability": "Free action, once/turn, spend 1 Treasure: grant the Shapeshifters the Stealth "
                "quality."},
    # Cunning 6
    {"name": "Interrupted Logistics", "rating": 6, "cost": 20, "hp": 10, "magic": "None",
     "attack": "-", "counter": "-", "qualities": ["Subtle", "Special"],
     "ability": "Non-Stealthed hostile units can't enter its location without paying 1d4 "
                "Treasure and waiting one turn to arrive."},
    {"name": "Prophet", "rating": 6, "cost": 20, "hp": 10, "magic": "None",
     "attack": "C v. C / 2d8 damage", "counter": "1d8 damage", "qualities": ["Subtle"],
     "ability": "A prophet, philosopher, or rebel leader of popular appeal, firmly controlled."},
    {"name": "Underground Roads", "rating": 6, "cost": 18, "hp": 15, "magic": "None",
     "attack": "-", "counter": "-", "qualities": ["Subtle", "Special"],
     "ability": "Free action, pay 1 Treasure: move any friendly Asset from within one move of "
                "the Roads to a destination also within one move of the Roads."},
    # Cunning 7
    {"name": "Expert Treachery", "rating": 7, "cost": 10, "hp": 5, "magic": "None",
     "attack": "C v. C / Special", "counter": "-", "qualities": ["Subtle"],
     "ability": "On a successful Attack this Asset is lost, 5 Treasure is gained, and the "
                "targeted Asset switches to the attacker's side (even if they lack the attributes "
                "to maintain it)."},
    {"name": "Mindbenders", "rating": 7, "cost": 20, "hp": 10, "magic": "Medium",
     "attack": "-", "counter": "2d8 damage", "qualities": ["Subtle"],
     "ability": "Once/turn, free action: force a rival faction to reroll a check/Attack/roll and "
                "take whichever result the Mindbenders prefer. A faction is affected only once "
                "per Mindbender turn."},
    {"name": "Popular Movement", "rating": 7, "cost": 25, "hp": 16, "magic": "None",
     "attack": "C v. C / 2d6 damage", "counter": "1d6 damage", "qualities": ["Subtle", "Special"],
     "ability": "Any friendly Asset may move into its location even if normally forbidden and "
                "un-Subtle; if the Movement moves or dies, those Assets must also leave."},
    # Cunning 8
    {"name": "Just As Planned", "rating": 8, "cost": 40, "hp": 15, "magic": "None",
     "attack": "-", "counter": "1d10 damage", "qualities": ["Subtle", "Special"],
     "ability": "Whenever any of the faction's Assets makes a Cunning roll, it may reroll a "
                "failed check at the cost of 1d6 damage to Just As Planned. Repeatable; no range "
                "limit; may destroy the Asset."},
    {"name": "Omniscient Seers", "rating": 8, "cost": 30, "hp": 10, "magic": "High",
     "attack": "-", "counter": "1d8 damage", "qualities": ["Subtle", "Special"],
     "ability": "Each hostile Stealthed Asset within one move must pass a Cunning vs. Cunning "
                "check at turn start or lose Stealth; all Cunning rolls within one move gain an "
                "extra die."},
]

FORCE_ASSETS = [
    # Force 1
    {"name": "Fearful Intimidation", "rating": 1, "cost": 2, "hp": 4, "magic": "None",
     "attack": "-", "counter": "1d4 damage", "qualities": [],
     "ability": "Intimidated locals are reluctant to cooperate with anyone opposing the faction."},
    {"name": "Local Guard", "rating": 1, "cost": 3, "hp": 4, "magic": "None",
     "attack": "F v. F / 1d3+1 damage", "counter": "1d4+1 damage", "qualities": [],
     "ability": "Night-watch and guard units; most effective defending from a fortified position."},
    {"name": "Summoned Hunter", "rating": 1, "cost": 4, "hp": 4, "magic": "Medium",
     "attack": "C v. F / 1d6 damage", "counter": "-", "qualities": ["Subtle"],
     "ability": "A summoned magical beast or bound disposable assassin."},
    {"name": "Thugs", "rating": 1, "cost": 2, "hp": 1, "magic": "None",
     "attack": "F v. C / 1d6 damage", "counter": "-", "qualities": ["Subtle"],
     "ability": "Gutter ruffians and common kneebreakers organized for the faction's causes."},
    # Force 2
    {"name": "Guerrilla Populace", "rating": 2, "cost": 6, "hp": 4, "magic": "None",
     "attack": "F v. F / 1d4+1 damage", "counter": "-", "qualities": [],
     "ability": "Locals aided by trained guerrilla leaders in sabotage and ambush."},
    {"name": "Military Transport", "rating": 2, "cost": 4, "hp": 6, "magic": "None",
     "attack": "-", "counter": "-", "qualities": ["Action"],
     "ability": "Free action, once/turn: bring an allied Asset within one move to its location, "
                "or move one from its location to a target in range. Multiple can chain movement."},
    {"name": "Reserve Corps", "rating": 2, "cost": 4, "hp": 4, "magic": "None",
     "attack": "F v. F / 1d6 damage", "counter": "1d6 damage", "qualities": [],
     "ability": "Retired/rear-line troops spread as workers, available to resist hostilities."},
    {"name": "Scouts", "rating": 2, "cost": 5, "hp": 5, "magic": "None",
     "attack": "F v. F / 2d4 damage", "counter": "1d4+1 damage", "qualities": ["Subtle"],
     "ability": "Long-range reconnaissance experts who can venture deep into hostile territory."},
    # Force 3
    {"name": "Enchanted Elites", "rating": 3, "cost": 8, "hp": 6, "magic": "Medium",
     "attack": "F v. F / 1d10 damage", "counter": "1d6 damage", "qualities": ["Subtle"],
     "ability": "Skilled warriors given magical armaments and arcane blessings."},
    {"name": "Infantry", "rating": 3, "cost": 6, "hp": 6, "magic": "None",
     "attack": "F v. F / 1d8 damage", "counter": "1d6 damage", "qualities": [],
     "ability": "Common foot soldiers; rarely heroic, but they have the advantage of numbers."},
    {"name": "Temple Fanatics", "rating": 3, "cost": 4, "hp": 6, "magic": "None",
     "attack": "F v. F / 2d6 damage", "counter": "2d6 damage", "qualities": ["Special"],
     "ability": "After every time they defend or successfully attack, they take 1d4 damage."},
    {"name": "Witch Hunters", "rating": 3, "cost": 6, "hp": 4, "magic": "Low",
     "attack": "C v. C / 1d4+1 damage", "counter": "1d6 damage", "qualities": [],
     "ability": "Trained to sniff out traitors, spies, and hostile or hidden spellcraft."},
    # Force 4
    {"name": "Cavalry", "rating": 4, "cost": 8, "hp": 12, "magic": "None",
     "attack": "F v. F / 2d6 damage", "counter": "1d4 damage", "qualities": [],
     "ability": "Mounted troops; weak on defense, but can harry logistics and mount charges."},
    {"name": "Military Roads", "rating": 4, "cost": 10, "hp": 10, "magic": "None",
     "attack": "-", "counter": "-", "qualities": ["Action"],
     "ability": "Once/turn, pay 1 Treasure: move any one Asset from any location in reach to any "
                "other location in reach."},
    {"name": "Vanguard Unit", "rating": 4, "cost": 10, "hp": 10, "magic": "None",
     "attack": "-", "counter": "1d6 damage", "qualities": ["Action"],
     "ability": "On a Relocate action, move the Vanguard and allied units in its location to any "
                "location in range, even where a force is normally barred; they may remain after."},
    {"name": "War Fleet", "rating": 4, "cost": 12, "hp": 8, "magic": "None",
     "attack": "F v. F / 2d6 damage", "counter": "1d8 damage", "qualities": ["Action"],
     "ability": "Attacks only along waterways; once/turn may freely relocate to any coastal area "
                "in range. Must be based out of a landward supply location."},
    # Force 5
    {"name": "Demonic Slayer", "rating": 5, "cost": 12, "hp": 4, "magic": "High",
     "attack": "C v. C / 2d6+2 damage", "counter": "-", "qualities": ["Subtle", "Special"],
     "ability": "An inhuman assassin-beast that enters play Stealthed."},
    {"name": "Magical Logistics", "rating": 5, "cost": 14, "hp": 6, "magic": "Medium",
     "attack": "-", "counter": "-", "qualities": ["Special"],
     "ability": "Once/turn, free action: repair 2 HP of damage to an allied Force Asset."},
    {"name": "Siege Experts", "rating": 5, "cost": 10, "hp": 8, "magic": "None",
     "attack": "F v. W / 1d6 damage", "counter": "1d6 damage", "qualities": [],
     "ability": "On a successful Attack, the target's owner loses 1d4 Treasure and this faction "
                "gains it."},
    # Force 6
    {"name": "Fortification Program", "rating": 6, "cost": 20, "hp": 18, "magic": "None",
     "attack": "-", "counter": "2d6 damage", "qualities": ["Action"],
     "ability": "Once/turn, when an enemy Attack targets the faction's Force, it may defend with "
                "this Asset if within one move of the attack."},
    {"name": "Knights", "rating": 6, "cost": 18, "hp": 16, "magic": "None",
     "attack": "F v. F / 2d8 damage", "counter": "2d6 damage", "qualities": [],
     "ability": "Elite warriors of considerable personal prowess."},
    {"name": "War Machines", "rating": 6, "cost": 25, "hp": 14, "magic": "Medium",
     "attack": "F v. F / 2d10+4 damage", "counter": "1d10 damage", "qualities": [],
     "ability": "Mobile war machines driven by trained beasts or magical motive power."},
    # Force 7
    {"name": "Brilliant General", "rating": 7, "cost": 25, "hp": 8, "magic": "None",
     "attack": "C v. F / 1d8 damage", "counter": "-", "qualities": ["Subtle", "Special"],
     "ability": "Whenever the General or any allied Force Asset in its location Attacks or "
                "defends, it rolls an extra die."},
    {"name": "Purity Rites", "rating": 7, "cost": 20, "hp": 10, "magic": "Low",
     "attack": "-", "counter": "2d8+2 damage", "qualities": ["Special"],
     "ability": "Can only defend against Attacks that target the faction's Cunning, but allows "
                "an extra die to defend."},
    {"name": "Warshaped", "rating": 7, "cost": 30, "hp": 16, "magic": "High",
     "attack": "F v. F / 2d8+2 damage", "counter": "2d8 damage", "qualities": ["Subtle"],
     "ability": "Magical war-creatures or greatly altered humans, few and elusive enough to "
                "evade easy detection."},
    # Force 8
    {"name": "Apocalypse Engine", "rating": 8, "cost": 35, "hp": 20, "magic": "Medium",
     "attack": "F v. F / 3d10+4 damage", "counter": "-", "qualities": [],
     "ability": "An unearthed ancient super-weapon that rains eldritch horror on a target."},
    {"name": "Invincible Legion", "rating": 8, "cost": 40, "hp": 30, "magic": "None",
     "attack": "F v. F / 2d10+4 damage", "counter": "2d10+4 damage", "qualities": ["Special"],
     "ability": "On a Relocate action, can relocate where a formal army is normally barred, as "
                "if Subtle (though it is not subtle). Needs no support units to smash opposition."},
]

WEALTH_ASSETS = [
    # Wealth 1
    {"name": "Armed Guards", "rating": 1, "cost": 1, "hp": 3, "magic": "None",
     "attack": "W v. F / 1d3 damage", "counter": "1d4 damage", "qualities": [],
     "ability": "Hired caravan guards, bodyguards, or other armed minions."},
    {"name": "Cooperative Businesses", "rating": 1, "cost": 1, "hp": 2, "magic": "None",
     "attack": "W v. W / 1d4-1 damage", "counter": "-", "qualities": ["Subtle", "Special"],
     "ability": "Any other faction creating an Asset in this location pays +1 Treasure; stacks."},
    {"name": "Farmers", "rating": 1, "cost": 2, "hp": 4, "magic": "None",
     "attack": "-", "counter": "1d4 damage", "qualities": ["Action"],
     "ability": "Once/turn, free action: roll 1d6; on 5+ gain 1 Treasure from the Farmers."},
    {"name": "Front Merchant", "rating": 1, "cost": 2, "hp": 3, "magic": "None",
     "attack": "W v. W / 1d4 damage", "counter": "1d4-1 damage", "qualities": ["Subtle"],
     "ability": "On a successful Attack, the target faction loses 1 Treasure (if any) and the "
                "Front Merchant's owner gains it. Once/turn."},
    # Wealth 2
    {"name": "Caravan", "rating": 2, "cost": 5, "hp": 4, "magic": "None",
     "attack": "W v. W / 1d4 damage", "counter": "-", "qualities": ["Action"],
     "ability": "Free action, once/turn, spend 1 Treasure: move itself and one other Asset in "
                "its location to a new location within one move."},
    {"name": "Dragomans", "rating": 2, "cost": 4, "hp": 4, "magic": "None",
     "attack": "-", "counter": "1d4 damage", "qualities": ["Subtle", "Special"],
     "ability": "A faction taking Expand Influence in its location rolls an extra die on all "
                "checks there that turn. Free action, once/turn, it can move."},
    {"name": "Pleaders", "rating": 2, "cost": 6, "hp": 4, "magic": "None",
     "attack": "C v. W / 2d4 damage", "counter": "1d6 damage", "qualities": ["Special"],
     "ability": "Legal specialists who turn local law against enemies; can neither Attack nor "
                "inflict Counterattack damage on Force Assets."},
    {"name": "Worker Mob", "rating": 2, "cost": 4, "hp": 6, "magic": "None",
     "attack": "W v. F / 1d4+1 damage", "counter": "1d4 damage", "qualities": [],
     "ability": "The roughest laborers, quietly organized to discipline the faction's enemies."},
    # Wealth 3
    {"name": "Ancient Mechanisms", "rating": 3, "cost": 8, "hp": 4, "magic": "Medium",
     "attack": "-", "counter": "-", "qualities": ["Special"],
     "ability": "When an Asset in its location rolls to make a profit (e.g. Farmers, "
                "Manufactory), it may roll twice and take the better result."},
    {"name": "Arcane Laboratory", "rating": 3, "cost": 6, "hp": 4, "magic": "None",
     "attack": "-", "counter": "-", "qualities": ["Special"],
     "ability": "The faction's Magic counts as one step higher for creating Assets in its "
                "location. Multiple labs stack the boost."},
    {"name": "Free Company", "rating": 3, "cost": 8, "hp": 6, "magic": "None",
     "attack": "W v. F / 2d4+2 damage", "counter": "1d6 damage", "qualities": ["Action", "Special"],
     "ability": "Free action, once/turn: move itself. Costs 1 Treasure upkeep each turn; if "
                "unpaid, roll 1d6 — 1-3 lost, 4-6 goes rogue and attacks the richest target. "
                "Repeats until back pay is paid or it is lost."},
    {"name": "Manufactory", "rating": 3, "cost": 8, "hp": 4, "magic": "None",
     "attack": "-", "counter": "1d4 damage", "qualities": ["Action"],
     "ability": "Once/turn, free action: roll 1d6 — 1 lose 1 Treasure, 2-5 gain 1, 6 gain 2. If "
                "owed Treasure can't be paid by turn's end, the Manufactory is lost."},
    # Wealth 4
    {"name": "Healers", "rating": 4, "cost": 12, "hp": 8, "magic": "None",
     "attack": "-", "counter": "-", "qualities": ["Action"],
     "ability": "When an Asset within one move is destroyed by an Attack that used Force against "
                "it, the owner may pay half its purchase price (round up) to restore it with 1 "
                "HP. Not usable on Bases of Influence."},
    {"name": "Monopoly", "rating": 4, "cost": 8, "hp": 12, "magic": "None",
     "attack": "W v. W / 1d6 damage", "counter": "1d6 damage", "qualities": ["Action"],
     "ability": "Once/turn, free action: target an Asset in its location; that owner must pay 1 "
                "Treasure or lose the targeted Asset."},
    {"name": "Occult Countermeasures", "rating": 4, "cost": 10, "hp": 8, "magic": "Low",
     "attack": "W v. C / 2d10 damage", "counter": "1d10 damage", "qualities": ["Special"],
     "ability": "Can only Attack or inflict Counterattack damage on Assets that require at least "
                "Low Magic to purchase."},
    {"name": "Usurers", "rating": 4, "cost": 12, "hp": 8, "magic": "None",
     "attack": "W v. W / 1d10 damage", "counter": "-", "qualities": ["Action"],
     "ability": "Each unit owned lowers the Treasure cost of buying Assets by 2 (min half cost); "
                "each use deals 1d4 damage to the Usurers from popular displeasure."},
    # Wealth 5
    {"name": "Mad Genius", "rating": 5, "cost": 6, "hp": 2, "magic": "None",
     "attack": "W v. C / 1d6 damage", "counter": "-", "qualities": ["Action"],
     "ability": "Free action, once/turn: move. Free action, once/turn: be sacrificed to treat "
                "its location's Magic as High for buying the next Asset there."},
    {"name": "Smuggling Fleet", "rating": 5, "cost": 12, "hp": 6, "magic": "None",
     "attack": "W v. F / 2d6 damage", "counter": "-", "qualities": ["Subtle", "Action"],
     "ability": "Once/turn, free action: move itself and one Asset in its location to any "
                "water-accessible location in one move; the moved Asset gains Subtle until it "
                "acts at the destination."},
    {"name": "Supply Interruption", "rating": 5, "cost": 10, "hp": 8, "magic": "None",
     "attack": "C v. W / 1d6 damage", "counter": "-", "qualities": ["Subtle", "Action"],
     "ability": "Free action, once/turn: make a Cunning vs. Wealth check against an Asset in its "
                "location; on success that owner must pay half the target's purchase cost or the "
                "Asset is disabled until paid."},
    # Wealth 6
    {"name": "Economic Disruption", "rating": 6, "cost": 25, "hp": 10, "magic": "None",
     "attack": "W v. W / 2d6 damage", "counter": "-", "qualities": ["Subtle", "Action"],
     "ability": "Free action, once/turn: move itself without cost."},
    {"name": "Merchant Prince", "rating": 6, "cost": 20, "hp": 10, "magic": "None",
     "attack": "W v. W / 2d8 damage", "counter": "1d8 damage", "qualities": ["Action"],
     "ability": "Free action, once/turn before buying an Asset in its location: the Merchant "
                "Prince takes 1d4 damage and that Asset costs 1d8 Treasure less (min half price)."},
    {"name": "Trade Company", "rating": 6, "cost": 15, "hp": 10, "magic": "None",
     "attack": "W v. W / 2d6 damage", "counter": "1d6 damage", "qualities": ["Action"],
     "ability": "Free action, once/turn: accept 1d4 damage to the Asset in exchange for 1d6-1 "
                "Treasure."},
    # Wealth 7
    {"name": "Ancient Workshop", "rating": 7, "cost": 25, "hp": 16, "magic": "Medium",
     "attack": "-", "counter": "-", "qualities": [],
     "ability": "Free action, once/turn: the Workshop takes 1d6 damage and the owner gains 1d6 "
                "Treasure."},
    {"name": "Lead or Silver", "rating": 7, "cost": 20, "hp": 10, "magic": "None",
     "attack": "W v. W / 2d10 damage", "counter": "2d8 damage", "qualities": [],
     "ability": "If its Attack reduces an enemy Asset to 0 HP, the owner may pay half the "
                "target's purchase cost to claim it, reviving it with 1 HP."},
    {"name": "Transport Network", "rating": 7, "cost": 15, "hp": 5, "magic": "None",
     "attack": "W v. W / 1d12 damage", "counter": "-", "qualities": ["Action"],
     "ability": "Free action, spend 1 Treasure: move any friendly Asset within two moves to any "
                "location within one move of either the target or the Network."},
    # Wealth 8
    {"name": "Golden Prosperity", "rating": 8, "cost": 40, "hp": 30, "magic": "Medium",
     "attack": "-", "counter": "2d10 damage", "qualities": [],
     "ability": "Each turn, free action: gain 1d6 Treasure usable to fix damaged Assets as the "
                "Repair Assets action. Any unspent on repairs is lost."},
    {"name": "Hired Legion", "rating": 8, "cost": 30, "hp": 20, "magic": "None",
     "attack": "W v. F / 2d10+4 damage", "counter": "2d10 damage", "qualities": ["Action"],
     "ability": "Free action, once/turn: move. Costs 2 Treasure upkeep each turn or it goes "
                "rogue as a Free Company. Cannot be voluntarily sold or disbanded."},
]

# ---------------------------------------------------------------------------
# Background Actor events  (book 10, "Background Actors")
# A generic d20 table plus six d12 actor-specific sub-tables.
# ---------------------------------------------------------------------------
GENERAL_ACTOR = [
    "They came into a large amount of money",
    "They became sick or diseased somehow",
    "A friend betrayed their trust",
    "A stroke of luck aided their pursuit of their goal",
    "They defeated a rival or significant enemy",
    "They made a grave social mistake",
    "A friend or ally was slain or lost to them",
    "They overcame an obstacle to their goal",
    "A source of power they have was threatened",
    "They were defeated by a rival in their ambition",
    "They were accused of a serious crime",
    "They obtained a useful item of magic",
    "They vanished mysteriously for a time",
    "They were attacked by monsters",
    "They made some unsavory associates",
    "They stole something or were robbed in turn",
    "They ventured into dangerous terrain",
    "They offended a powerful entity",
    "A plan of theirs came to its fruition",
    "They gained a powerful new ally",
]

ADVENTURING_PARTIES = [
    "They're delving into a perilous Deep",
    "They've been savaged by monsters",
    "They slew a powerful foe",
    "They're quarreling over some treasure",
    "They committed an outrageous social crime",
    "They're spending huge amounts of money",
    "A member has betrayed the others",
    "They murdered someone important",
    "A promising new member joined them",
    "They've gotten or lost a noble patron",
    "They've been cursed or blighted by magic",
    "They're heading into dangerous territory",
]

DEMAGOGUES = [
    "A noble patron is finding them useful",
    "Their followers are getting out of hand",
    "They're picking a fight with existing authority",
    "They've made ties with local crime figures",
    "They've struck against a hated local figure",
    "They're spreading an appealing new idea",
    "An important local has joined their cause",
    "They've gotten a major donation from believers",
    "They're being suppressed by local authorities",
    "Followers are arguing over ideological points",
    "They're trying to create a new power base",
    "They've gotten a stroke of divine good fortune",
]

NOBLES = [
    "A rival has encroached on their lands or rights",
    "They're making a familial tie by marriage",
    "A trusted lieutenant has died or betrayed them",
    "They've ruthlessly quashed a non-noble rival",
    "A family scion has gotten in big trouble",
    "Their superior has repaid a favor owed them",
    "They're fighting with a rival local power base",
    "They've formed an alliance with a neighbor",
    "An old enemy of their line has struck them",
    "They're fighting over rights to a particular title",
    "They've committed some grave social faux pas",
    "They've infuriated their superior somehow",
]

MERCHANTS = [
    "A local industry fell under their control",
    "They made a deal with a local crime boss",
    "They bought or built something fabulous",
    "Criminals are assaulting their wealth sources",
    "They cut a very profitable new deal",
    "Their employees or minions are getting restive",
    "They opened a new branch of operations",
    "They made an alliance with a local noble",
    "They've enlisted adventurers for dire work",
    "A noble has marked them as a dangerous foe",
    "They drove a rival out of business",
    "Some enterprise of theirs has collapsed",
]

WARLORDS = [
    "They've attacked a poorly-defended place",
    "They've got a promising new lieutenant",
    "One of their underlings betrayed them",
    "Their men went on an undisciplined rampage",
    "They've moved their base of operations",
    "They've gotten backing from an outside power",
    "They're trying to become legitimate rulers",
    "They're infighting over loot, women, or rank",
    "They were badly wounded in a fight",
    "They pulled off a remarkable victory",
    "Their band split due to a quarrel",
    "They absorbed a weaker group",
]

SORCERERS = [
    "They've acquired \"subjects\" for their work",
    "They suffered a magical mishap of some kind",
    "They've acquired an esoteric magic item",
    "A rival sorcerer has struck at them",
    "They've hired adventurers to acquire something",
    "A noble has enlisted their aid in a cause",
    "They've been venturing into ancient ruins",
    "They've created a Working to pursue an end",
    "They're accused of a heinous crime",
    "The locals begged their aid in a time of need",
    "They've acquired a promising apprentice",
    "They've devised a new and potent magic",
]

# ---------------------------------------------------------------------------
# Example faction goals (book 10).  difficulty = XP awarded on success.
# A small rollable d10 of the fixed-difficulty goals; the variable-difficulty
# goals are carried in `notes` for the GM.
# ---------------------------------------------------------------------------
EXAMPLE_GOALS = [
    {"name": "Blood the Enemy", "difficulty": "2",
     "text": "Inflict HP of damage on enemy faction assets/bases equal to your faction's total "
             "Force + Cunning + Wealth ratings."},
    {"name": "Destroy the Foe", "difficulty": "2 + avg(F,C,W)",
     "text": "Destroy a rival faction. Difficulty equals 2 plus the average of the faction's "
             "Force, Cunning, and Wealth ratings."},
    {"name": "Eliminate Target", "difficulty": "1",
     "text": "Choose an undamaged rival Asset; destroy it within three turns. On failure, pick a "
             "new goal without the usual turn of paralysis."},
    {"name": "Expand Influence", "difficulty": "1 (+1 if contested)",
     "text": "Plant a Base of Influence at a new location."},
    {"name": "Inside Enemy Territory", "difficulty": "2",
     "text": "Have a number of Stealthed assets in locations with a rival Base of Influence equal "
             "to your Cunning. Already-Stealthed units when the goal is adopted don't count."},
    {"name": "Invincible Valor", "difficulty": "2",
     "text": "Destroy a Force asset whose minimum purchase rating is higher than your faction's "
             "Force rating."},
    {"name": "Peaceable Kingdom", "difficulty": "1",
     "text": "Don't take an Attack action for four turns."},
    {"name": "Root Out the Enemy", "difficulty": "half avg(ruler F,C,W), round up",
     "text": "Destroy a Base of Influence of a rival faction in a specific location."},
    {"name": "Sphere Dominance", "difficulty": "1 per 2 destroyed, round up",
     "text": "Choose Wealth, Force, or Cunning; destroy a number of rival assets of that kind "
             "equal to your score in it."},
    {"name": "Wealth of Kingdoms", "difficulty": "2",
     "text": "Spend Treasure equal to four times your Wealth on bribes and influence (lost). "
             "Wealth must rise before this goal can be picked again."},
]

# ---------------------------------------------------------------------------
# Assemble bundle tables.
# ---------------------------------------------------------------------------

def _asset_lines(assets):
    """Render an asset catalog as one human/agent-readable string per asset, and
    keep the structured record alongside so faction_turn.py can read stats."""
    out = []
    for a in assets:
        q = ", ".join(a["qualities"]) if a["qualities"] else "-"
        line = (f"{a['name']} (req {a['rating']}; cost {a['cost']}; HP {a['hp']}; "
                f"Magic {a['magic']}; atk {a['attack']}; counter {a['counter']}; "
                f"qualities {q}) — {a['ability']}")
        out.append({"name": a["name"], "rating": a["rating"], "cost": a["cost"],
                    "hp": a["hp"], "magic": a["magic"], "attack": a["attack"],
                    "counter": a["counter"], "qualities": a["qualities"],
                    "ability": a["ability"], "line": line})
    return out


def _list_table(dice, entries):
    """Build a rollable list_dN table (each entry one slot) for the bundle."""
    n = len(entries)
    return {
        "type": f"list_d{n}",
        "dice": f"1d{n}",
        "entries": [{"min": i + 1, "max": i + 1, "value": v} for i, v in enumerate(entries)],
    }


def _goal_table(goals):
    n = len(goals)
    return {
        "type": f"list_d{n}",
        "dice": f"1d{n}",
        "entries": [{"min": i + 1, "max": i + 1,
                     "value": f"{g['name']} (Difficulty {g['difficulty']}): {g['text']}"}
                    for i, g in enumerate(goals)],
    }


def build():
    doc = {
        "id": "wwn.faction",
        "title": "Factions and Major Projects",
        "source": SRC,
        "kind": "bundle",
        # --- the faction-turn machinery the script & cards reference -------
        "rules": {
            "attribute_check": "Attacker and defender each roll 1d10 + relevant attribute. "
                               "The attacker wins only if their total is higher; the defender "
                               "wins on a tie or a higher roll. Extra-die abilities roll more "
                               "dice and keep the highest.",
            "initiative": "At the start of every faction turn each faction rolls 1d8; highest "
                          "goes first, GM breaks ties.",
            "treasure_income": "Each turn a faction earns Treasure equal to half its Wealth plus "
                               "a quarter of its combined Force and Cunning, rounded up.",
            "turn_sequence": [
                "Earn Treasure (half Wealth + quarter of (Force+Cunning), round up).",
                "Pay upkeep for Asset costs and for excess Assets (1 Treasure per Asset over an "
                "attribute's rating); unpaid excess Assets are lost.",
                "Trigger any special Asset abilities (movement, profit, etc.).",
                "Take ONE Faction Action; every valid owned Asset performs it.",
                "Check the current goal: if met, collect its XP and pick a new goal; if not, may "
                "abandon it for a new one at the cost of next turn's action + abilities.",
            ],
            "hp_by_rating": {"1": 1, "2": 2, "3": 4, "4": 6, "5": 9, "6": 12, "7": 16, "8": 20},
            "xp_cost_by_rating": {"2": 2, "3": 4, "4": 6, "5": 9, "6": 12, "7": 16, "8": 20},
            "hp_formula": "Max HP = sum of the HP values for the faction's Force, Cunning, and "
                          "Wealth ratings (rating 1=1, 2=2, 3=4, 4=6, 5=9, 6=12, 7=16, 8=20). "
                          "The HQ Base of Influence always has HP equal to the faction maximum.",
            "actions": {
                "Attack": "Nominate Assets to attack enemy Assets in their location; the defender "
                          "picks which Asset meets each attack. Roll the acting Asset's attribute "
                          "check; on success deal its attack score, on failure take the "
                          "defender's counterattack. Damage to a Base of Influence is also dealt "
                          "to faction HP (no overflow).",
                "Move Asset": "Move one or more Assets up to one turn's movement (~100 mi/month). "
                              "The destination must not forbid the Asset; Subtle/Stealthed ignore "
                              "this. An Asset that loses Subtle/Stealth in a hostile location must "
                              "retreat within one turn or take half its max HP in damage.",
                "Repair Asset": "Spend 1 Treasure per Asset to heal half its relevant attribute "
                                "(round up); further fixes that turn cost +1 each. Once/turn may "
                                "also heal faction HP for 1 Treasure equal to (highest + lowest of "
                                "F/W/C) / 2, round up.",
                "Expand Influence": "Plant a new Base of Influence where you already have an "
                                    "Asset; pay 1 Treasure per HP it will have. Then make a "
                                    "Cunning vs. Cunning check against each rival with an Asset "
                                    "present; a winner may immediately Attack the new base.",
                "Create Asset": "Buy one Asset at a Base of Influence you own; you must meet its "
                                "attribute + Magic requirements and pay its cost. One Asset per "
                                "turn. No more Assets of an attribute than its rating, or pay 1 "
                                "Treasure/excess per turn.",
                "Hide Asset": "Cunning 3+ only. Give an owned Asset the Stealth quality for every "
                              "2 Treasure spent. Assets in a location with a rival Base can't be "
                              "hidden; no refund if Stealth is later lost.",
                "Sell Asset": "Decommission an Asset for half its purchase cost (round down). A "
                              "damaged Asset yields no Treasure.",
                "Use Asset Ability": "In place of another action, use an Asset ability that "
                                     "replaces the Attack action (e.g. Cryptomancers, "
                                     "Seditionists). Free-action abilities fire in the trigger "
                                     "step regardless of the chosen action.",
            },
            "major_projects": {
                "currency": "Renown — earned ~1 per adventure (plus bonus Renown for relevant "
                            "work), spent to buy down a project's difficulty.",
                "difficulty": "Difficulty = base (Plausible 1 / Improbable 2 / Impossible 4) x "
                              "scope multiplier (Village x2 / City x4 / Region x8 / Kingdom x16 / "
                              "Known World x32) x opposition multiplier (Minor figures x2 / Local "
                              "leaders x4 / Major noble or beast x8 / King or famed monster x16). "
                              "x2 again if the local population is emotionally against it.",
                "reduce": "Lower difficulty by spending money (Renown bought at rising silver "
                          "cost: first 1-4 pts 500/pt, next 4 at 2000, next 8 at 4000, next 16 at "
                          "8000, next 32 at 16000, next 64 at 32000), building institutions, "
                          "nullifying opposition (only the greatest opponent counts), or "
                          "adventuring toward the goal (the most efficient route).",
                "faction_help": "A faction may aid a project once per faction turn as its action: "
                                "spend 1 Treasure and lower the difficulty by its total Force + "
                                "Cunning + Wealth (doubled if ideally suited), to a minimum of 1. "
                                "It may also burn Asset/Base HP 1-for-1 to lower difficulty, then "
                                "each contributing Asset/Base takes +1d4 damage.",
            },
            "domains": {
                "property_tax": "Owners of property on land controlled by another power pay ~5% "
                                "of its total worth per year to the local ruler (titled nobles "
                                "are often exempt).",
                "construction": "A skilled artisan-mason builds 25 sp of structure per labor-day "
                                "(unskilled 5 sp/day). Sample costs: keep on the borderlands "
                                "50,000 sp; military watchtower 5,000 sp; minor lord's "
                                "landholdings 25,000 sp; major noble's 200,000 sp.",
                "upkeep": "Garrisons and households cost monthly wages (e.g. light infantry 40 "
                          "sp, heavy infantry 60 sp, archer 75 sp, light cavalry 100 sp, heavy "
                          "cavalry 200 sp; reeve/spymaster/majordomo 200-500 sp). Long-term "
                          "housing halves a hireling's or soldier's monthly price.",
            },
        },
        "tables": {
            # Faction tags as a flat reference list (name + effect) AND rollable.
            "Faction Tags": {
                "type": f"list_d{len(FACTION_TAGS)}",
                "dice": f"1d{len(FACTION_TAGS)}",
                "entries": [{"min": i + 1, "max": i + 1,
                             "value": f"{t['name']}: {t['effect']}"}
                            for i, t in enumerate(FACTION_TAGS)],
            },
            "Background Actor — General (d20)": _list_table("1d20", GENERAL_ACTOR),
            "Background Actor — Adventuring Parties (d12)": _list_table("1d12", ADVENTURING_PARTIES),
            "Background Actor — Demagogues and Religious Zealots (d12)": _list_table("1d12", DEMAGOGUES),
            "Background Actor — Nobles and Gentry (d12)": _list_table("1d12", NOBLES),
            "Background Actor — Merchants and Oligarchs (d12)": _list_table("1d12", MERCHANTS),
            "Background Actor — Warlords and Warband Chiefs (d12)": _list_table("1d12", WARLORDS),
            "Background Actor — Sorcerers and Magic-Users (d12)": _list_table("1d12", SORCERERS),
            "Example Faction Goals": _goal_table(EXAMPLE_GOALS),
        },
        # Structured catalogs (not flat-rolled; read by faction_turn.py / lookup).
        "faction_tags": FACTION_TAGS,
        "Cunning_assets": _asset_lines(CUNNING_ASSETS),
        "Force_assets": _asset_lines(FORCE_ASSETS),
        "Wealth_assets": _asset_lines(WEALTH_ASSETS),
        "example_goals": EXAMPLE_GOALS,
    }
    return doc


def main():
    doc = build()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=2, ensure_ascii=False)
        f.write("\n")
    n_assets = len(CUNNING_ASSETS) + len(FORCE_ASSETS) + len(WEALTH_ASSETS)
    print(f"wrote {os.path.relpath(OUT, SKILL_ROOT)}")
    print(f"  faction_tags        : {len(FACTION_TAGS)}")
    print(f"  Cunning_assets      : {len(CUNNING_ASSETS)}")
    print(f"  Force_assets        : {len(FORCE_ASSETS)}")
    print(f"  Wealth_assets       : {len(WEALTH_ASSETS)}  (total assets {n_assets})")
    print(f"  background tables   : 1 general d20 + 6 actor d12")
    print(f"  example_goals       : {len(EXAMPLE_GOALS)}")
    # quick self-check: validator coverage rule for any inner list_ table
    for tname, t in doc["tables"].items():
        typ = t.get("type", "")
        if typ.startswith("list_d"):
            need = int(typ.split("list_d")[1])
            cov = sum(e["max"] - e["min"] + 1 for e in t["entries"])
            assert cov == need, f"{tname}: coverage {cov} != {need}"
    print("  inner table coverage: OK")


if __name__ == "__main__":
    main()
