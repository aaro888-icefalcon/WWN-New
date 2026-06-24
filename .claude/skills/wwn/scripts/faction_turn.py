#!/usr/bin/env python3
"""
faction_turn.py — resolve ONE Worlds Without Number faction turn from a
faction-sheet markdown file, with HONEST, SHOWN dice.

Implements the WWN faction turn (Worlds Without Number Deluxe, ch.10):
  1. Initiative — every faction rolls 1d8, highest first (GM breaks ties).
  2. Earn Treasure — half Wealth + a quarter of (Force + Cunning), rounded up.
  3. Pay upkeep — flagged Asset upkeep + 1 Treasure per Asset over an attribute's
     rating (unpaid excess Assets are dropped, lowest-cost first).
  4. Trigger free Asset abilities (reported for the GM to apply).
  5. Take ONE Faction Action; every valid Asset performs it. Attacks resolve as
     opposed attribute checks: attacker 1d10+ATT vs defender 1d10+ATT, attacker
     wins only on a strictly higher total. On success the defender takes the
     attacker's attack-damage; on failure the attacker takes the defender's
     counterattack. Damage to a Base of Influence is also dealt to faction HP.
  6. Advance each faction's Major-Project clock (+1, or +2 if it acted on it).
  7. Roll ONE Background Actor event (general d20 or a typed d12 sub-table).

Prints a clear per-faction turn log and an end-of-turn DELTA summary. With
--out, also rewrites the sheet's live numbers (Treasure / project clock / Asset
& faction HP) in place.

The attribute checks are the genuine WWN dice (1d10 + attribute, opposed; ties
to the defender) and are printed every time.  Reproduce a run with --seed N.
If MYTHIC_GM_DICE is set, a one-line note is printed; the honest roll itself is
still produced and shown here so behaviour and reproducibility are unchanged.

USAGE
  python3 scripts/faction_turn.py <faction-sheet.md> [--seed N] [--out <path>]
  python3 scripts/faction_turn.py <faction-sheet.md> --seed 2          # dry run, log only
  python3 scripts/faction_turn.py <faction-sheet.md> --seed 2 --out same  # rewrite the sheet

FACTION-SHEET FORMAT (see assets/templates/faction-sheet.md)
  ## Faction: <Name>
  - Tags: Martial, Rooted          (optional)
  - Force: 5    Cunning: 2   Wealth: 3
  - HP: 15 / 15
  - Treasure: 4
  - Goal: Blood the Enemy (Difficulty 2)
  - Project: Fortify the Pass — clock 2/6        (optional Major Project clock)
  - Stance: aggressive | defensive | builder | schemer   (optional AI hint)
  - Actor: Warlords and Warband Chiefs            (optional background-actor type)
  ### Assets
  - <Location> | <AssetName> | HP a/b | [stealth] [base]
  - Skarn's Hold | Infantry | HP 6/6
  - Skarn's Hold | Base of Influence | HP 15/15 | base

Std-lib only; Python 3.6+.  Reads bridge/generators/faction.json for asset stats.
"""
import json
import math
import os
import random
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(HERE)
FACTION_JSON = os.path.join(SKILL_ROOT, "bridge", "generators", "faction.json")

ATTRS = ("Force", "Cunning", "Wealth")
ATTR_LETTER = {"F": "Force", "C": "Cunning", "W": "Wealth"}

ACTOR_TABLE = {
    "adventuring parties": "Background Actor — Adventuring Parties (d12)",
    "demagogues": "Background Actor — Demagogues and Religious Zealots (d12)",
    "demagogues and religious zealots": "Background Actor — Demagogues and Religious Zealots (d12)",
    "nobles": "Background Actor — Nobles and Gentry (d12)",
    "nobles and gentry": "Background Actor — Nobles and Gentry (d12)",
    "merchants": "Background Actor — Merchants and Oligarchs (d12)",
    "merchants and oligarchs": "Background Actor — Merchants and Oligarchs (d12)",
    "warlords": "Background Actor — Warlords and Warband Chiefs (d12)",
    "warlords and warband chiefs": "Background Actor — Warlords and Warband Chiefs (d12)",
    "sorcerers": "Background Actor — Sorcerers and Magic-Users (d12)",
    "sorcerers and magic-users": "Background Actor — Sorcerers and Magic-Users (d12)",
}


# ---------------------------------------------------------------------------
# Honest dice.  Format mirrors gen.py: "1dN -> [r] = r".
# ---------------------------------------------------------------------------
class Roller:
    def __init__(self, seed=None):
        self.rng = random.Random(seed)
        self.engine = os.environ.get("MYTHIC_GM_DICE")

    def banner(self):
        if self.engine:
            print(f"[dice] engine roller available at MYTHIC_GM_DICE={self.engine}; "
                  f"rolls shown below are honest and reproducible.")

    def roll(self, sides, label=None, n=1, keep_high=False):
        rolls = [self.rng.randint(1, sides) for _ in range(n)]
        kept = max(rolls) if keep_high else rolls[0]
        shown = f"{n}d{sides} -> {rolls}" if n > 1 else f"1d{sides} -> [{rolls[0]}] = {rolls[0]}"
        if n > 1:
            shown += f"  keep-high = {kept}"
        if label:
            shown = f"{label}: {shown}"
        print("     " + shown)
        return kept

    def roll_expr(self, expr, label=None):
        """Roll NdM(+/-K); print honestly; return the total."""
        m = re.match(r"(\d*)d(\d+)([+-]\d+)?$", expr.replace(" ", ""))
        if not m:
            # a flat number ("5") or a non-dice token
            try:
                return int(expr)
            except ValueError:
                return 0
        n = int(m.group(1) or 1)
        sides = int(m.group(2))
        k = int(m.group(3) or 0)
        rolls = [self.rng.randint(1, sides) for _ in range(n)]
        total = sum(rolls) + k
        shown = f"{expr} -> {rolls}{('%+d' % k) if k else ''} = {total}"
        if label:
            shown = f"{label}: {shown}"
        print("       " + shown)
        return total


# ---------------------------------------------------------------------------
# Data + sheet parsing.
# ---------------------------------------------------------------------------
def load_faction_data():
    if not os.path.exists(FACTION_JSON):
        sys.exit("bridge/generators/faction.json missing — run: python3 scripts/build_faction.py")
    return json.load(open(FACTION_JSON, encoding="utf-8"))


def _asset_index(data):
    idx = {}
    for key in ("Cunning_assets", "Force_assets", "Wealth_assets"):
        attr = key.split("_")[0]
        for a in data[key]:
            rec = dict(a)
            rec["attr"] = attr
            idx[a["name"].lower()] = rec
    return idx


def parse_sheet(path):
    """Parse the faction-sheet markdown into a list of faction dicts."""
    text = open(path, encoding="utf-8").read()
    factions = []
    cur = None
    in_assets = False
    for raw in text.splitlines():
        line = raw.rstrip()
        m = re.match(r"##\s+Faction:\s+(.*)", line)
        if m:
            cur = {"name": m.group(1).strip(), "tags": [], "attrs": {}, "hp": None,
                   "hp_max": None, "treasure": 0, "goal": "", "project": None,
                   "stance": "", "actor": "", "assets": [], "_log": []}
            factions.append(cur)
            in_assets = False
            continue
        if cur is None:
            continue
        if re.match(r"###\s+Assets", line, re.I):
            in_assets = True
            continue
        if in_assets and line.strip().startswith("-"):
            body = line.strip()[1:].strip()
            parts = [p.strip() for p in body.split("|")]
            if len(parts) < 2:
                continue
            loc, name = parts[0], parts[1]
            hp = hp_max = None
            flags = []
            for p in parts[2:]:
                hm = re.search(r"HP\s+(\d+)\s*/\s*(\d+)", p, re.I)
                if hm:
                    hp, hp_max = int(hm.group(1)), int(hm.group(2))
                else:
                    flags.append(p.lower())
            cur["assets"].append({"loc": loc, "name": name, "hp": hp, "hp_max": hp_max,
                                  "stealth": "stealth" in " ".join(flags),
                                  "base": "base" in " ".join(flags)
                                          or "base of influence" in name.lower()})
            continue
        # attribute / scalar lines
        for a in ATTRS:
            am = re.search(rf"{a}\s*:\s*(\d+)", line)
            if am:
                cur["attrs"][a] = int(am.group(1))
        tm = re.search(r"Tags?\s*:\s*(.*)", line)
        if tm and not in_assets:
            cur["tags"] = [t.strip() for t in re.split(r"[,;]", tm.group(1)) if t.strip()]
        hm = re.search(r"\bHP\s*:\s*(\d+)\s*/\s*(\d+)", line)
        if hm and not in_assets:
            cur["hp"], cur["hp_max"] = int(hm.group(1)), int(hm.group(2))
        trm = re.search(r"Treasure\s*:\s*(\d+)", line)
        if trm:
            cur["treasure"] = int(trm.group(1))
        gm = re.search(r"Goal\s*:\s*(.*)", line)
        if gm:
            cur["goal"] = gm.group(1).strip()
        pm = re.search(r"Project\s*:\s*(.*?)(?:clock\s*(\d+)\s*/\s*(\d+))?\s*$", line, re.I)
        if pm and pm.group(2):
            cur["project"] = {"name": pm.group(1).strip().rstrip("—- "),
                              "n": int(pm.group(2)), "N": int(pm.group(3))}
        sm = re.search(r"Stance\s*:\s*(\w+)", line, re.I)
        if sm:
            cur["stance"] = sm.group(1).lower()
        acm = re.search(r"Actor\s*:\s*(.*)", line, re.I)
        if acm:
            cur["actor"] = acm.group(1).strip()
    return factions, text


# ---------------------------------------------------------------------------
# Turn helpers.
# ---------------------------------------------------------------------------
def treasure_income(f):
    w = f["attrs"].get("Wealth", 0)
    fo = f["attrs"].get("Force", 0)
    c = f["attrs"].get("Cunning", 0)
    return math.ceil(w / 2 + (fo + c) / 4)


def excess_upkeep(f, aidx):
    """1 Treasure per Asset over its attribute's rating (Bases don't count)."""
    counts = {a: 0 for a in ATTRS}
    for a in f["assets"]:
        if a["base"]:
            continue
        rec = aidx.get(a["name"].lower())
        if rec:
            counts[rec["attr"]] += 1
    excess = 0
    detail = []
    for attr in ATTRS:
        over = counts[attr] - f["attrs"].get(attr, 0)
        if over > 0:
            excess += over
            detail.append(f"{over} excess {attr} asset(s)")
    return excess, detail


def attack_assets(f, aidx):
    """Owned non-base Assets with a real attack string (not '-')."""
    out = []
    for a in f["assets"]:
        if a["base"]:
            continue
        rec = aidx.get(a["name"].lower())
        if rec and rec["attack"] and rec["attack"] != "-":
            out.append((a, rec))
    return out


def parse_attack(attack_str):
    """'F v. F / 1d8 damage' -> ('Force','Force','1d8'); 'C v. C / Special' -> dmg None."""
    m = re.match(r"\s*([FCW])\s*v\.?\s*([FCW])\s*/\s*(.*)", attack_str)
    if not m:
        return None, None, None
    atk_attr = ATTR_LETTER[m.group(1)]
    def_attr = ATTR_LETTER[m.group(2)]
    dmg = m.group(3).replace("damage", "").strip()
    if "special" in dmg.lower() or not re.search(r"\d*d\d", dmg) and not dmg.strip().isdigit():
        dmg = None
    return atk_attr, def_attr, dmg


def counter_expr(rec):
    c = rec.get("counter", "-")
    if not c or c == "-":
        return None
    cc = c.replace("damage", "").strip()
    return cc if re.search(r"\d*d\d", cc) or cc.isdigit() else None


def extra_dice_for(f, attr):
    """Tag-granted extra die on an attribute check (Machiavellian/Martial/Rich)."""
    tags = [t.lower() for t in f["tags"]]
    if attr == "Cunning" and "machiavellian" in tags:
        return 2
    if attr == "Force" and "martial" in tags:
        return 2
    if attr == "Wealth" and "rich" in tags:
        return 2
    return 1


def choose_action(f, aidx, enemies):
    """Lightweight, readable faction AI. Returns (action, note)."""
    stance = f["stance"]
    has_targets = any(e["assets"] for e in enemies if e is not f)
    can_attack = bool(attack_assets(f, aidx)) and has_targets
    damaged = (f["hp"] is not None and f["hp_max"] and f["hp"] < f["hp_max"]) or \
              any(a["hp"] is not None and a["hp_max"] and a["hp"] < a["hp_max"]
                  for a in f["assets"])
    # explicit stance wins
    if stance == "aggressive" and can_attack:
        return "Attack", "stance: aggressive"
    if stance == "defensive" and damaged and f["treasure"] >= 1:
        return "Repair Asset", "stance: defensive, licking wounds"
    if stance == "builder" and f["treasure"] >= 4:
        return "Create Asset", "stance: builder, investing Treasure"
    if stance == "schemer" and can_attack:
        return "Attack", "stance: schemer, applying pressure"
    # default heuristic: hurt and able to pay → repair; rich → build; else attack/move
    if damaged and f["treasure"] >= 2:
        return "Repair Asset", "wounded and can afford repairs"
    if can_attack:
        return "Attack", "enemy assets in reach"
    if f["treasure"] >= 4:
        return "Create Asset", "no targets; banking growth"
    return "Move Asset", "consolidating / repositioning"


def find_targets(attacker, enemies):
    """Return list of (enemy, asset) the attacker's assets share a location with."""
    my_locs = {a["loc"] for a in attacker["assets"]}
    targets = []
    for e in enemies:
        if e is attacker:
            continue
        for a in e["assets"]:
            if a["loc"] in my_locs and (a["hp"] is None or a["hp"] > 0) and not a["stealth"]:
                targets.append((e, a))
    return targets


def hp_repair_amount(f):
    vals = [f["attrs"].get(a, 0) for a in ATTRS]
    return math.ceil((max(vals) + min(vals)) / 2)


# ---------------------------------------------------------------------------
# The turn.
# ---------------------------------------------------------------------------
def run_turn(factions, data, roller):
    aidx = _asset_index(data)
    deltas = []  # (faction, text)

    print("=" * 64)
    print("WWN FACTION TURN")
    print("=" * 64)

    # snapshot for deltas
    snap = {f["name"]: {"treasure": f["treasure"], "hp": f["hp"],
                        "project": (f["project"]["n"] if f["project"] else None),
                        "assets": {(a["loc"], a["name"]): a["hp"] for a in f["assets"]}}
            for f in factions}

    # 1) Initiative — 1d8 each, highest first.
    print("\n-- Initiative (1d8, highest first) --")
    inits = []
    for f in factions:
        r = roller.roll(8, f"{f['name']}")
        inits.append((r, f))
    order = [f for _, f in sorted(inits, key=lambda x: -x[0])]
    print("   order: " + " > ".join(f["name"] for f in order))

    for f in order:
        print("\n" + "-" * 64)
        tagstr = (" [" + ", ".join(f["tags"]) + "]") if f["tags"] else ""
        print(f"### {f['name']}{tagstr}")
        print(f"   F{f['attrs'].get('Force',0)} "
              f"C{f['attrs'].get('Cunning',0)} "
              f"W{f['attrs'].get('Wealth',0)} | "
              f"HP {f['hp']}/{f['hp_max']} | Treasure {f['treasure']}")

        # 2) Earn Treasure.
        inc = treasure_income(f)
        f["treasure"] += inc
        print(f"   [income] +{inc} Treasure (½·W {f['attrs'].get('Wealth',0)} + "
              f"¼·(F+C {f['attrs'].get('Force',0)}+{f['attrs'].get('Cunning',0)}), "
              f"round up) → {f['treasure']}")

        # 3) Upkeep (excess assets).
        exc, detail = excess_upkeep(f, aidx)
        if exc:
            pay = min(exc, f["treasure"])
            f["treasure"] -= pay
            print(f"   [upkeep] {', '.join(detail)} → owe {exc}; pay {pay} → {f['treasure']}")
            if pay < exc:
                # drop cheapest excess assets
                drop = exc - pay
                non_base = [a for a in f["assets"] if not a["base"]]
                non_base.sort(key=lambda a: aidx.get(a["name"].lower(), {}).get("cost", 99))
                for a in non_base[:drop]:
                    f["assets"].remove(a)
                    print(f"           ! can't pay — lose Asset: {a['name']} @ {a['loc']}")
                    deltas.append((f["name"], f"lost {a['name']} (unpaid upkeep)"))
        else:
            print("   [upkeep] none owed")

        # 4) Trigger free abilities (report).
        free = [a for a in f["assets"]
                if aidx.get(a["name"].lower(), {}).get("qualities") and
                "Action" in aidx[a["name"].lower()]["qualities"]]
        if free:
            print("   [abilities] free-action assets to resolve: "
                  + ", ".join(a["name"] for a in free))

        # 5) Faction Action.
        enemies = [g for g in factions if g is not f]
        action, why = choose_action(f, aidx, factions)
        print(f"   [action] {action}  ({why})")

        acted_on_project = False

        if action == "Attack":
            targets = find_targets(f, factions)
            attackers = attack_assets(f, aidx)
            if not targets or not attackers:
                print("           no valid attackers/targets in shared locations — holds position")
            else:
                # each attacker hits the first available target in its own location
                for a, rec in attackers:
                    local = [(e, t) for (e, t) in targets if t["loc"] == a["loc"]
                             and (t["hp"] is None or t["hp"] > 0)]
                    if not local:
                        continue
                    enemy, tgt = local[0]
                    trec = aidx.get(tgt["name"].lower(), {})
                    atk_attr, def_attr, dmg = parse_attack(rec["attack"])
                    if not atk_attr:
                        continue
                    print(f"           {a['name']} ({a['loc']}) attacks "
                          f"{enemy['name']}'s {tgt['name']}  [{rec['attack']}]")
                    an = extra_dice_for(f, atk_attr)
                    dn = extra_dice_for(enemy, def_attr)
                    atk_roll = roller.roll(10, f"           atk {atk_attr}", n=an,
                                           keep_high=an > 1) + f["attrs"].get(atk_attr, 0)
                    def_roll = roller.roll(10, f"           def {def_attr}", n=dn,
                                           keep_high=dn > 1) + enemy["attrs"].get(def_attr, 0)
                    print(f"           → {atk_attr} {atk_roll} vs {def_attr} {def_roll} "
                          f"(attacker needs strictly higher)")
                    if atk_roll > def_roll:
                        dealt = roller.roll_expr(dmg, "           damage") if dmg else None
                        if dealt is None:
                            print("           HIT — special effect (apply per asset ability)")
                            deltas.append((f["name"],
                                           f"{a['name']} landed a special effect on "
                                           f"{enemy['name']}'s {tgt['name']}"))
                        else:
                            if tgt["hp"] is not None:
                                tgt["hp"] = max(0, tgt["hp"] - dealt)
                            print(f"           HIT — {dealt} damage → {tgt['name']} "
                                  f"HP {tgt['hp']}/{tgt['hp_max']}")
                            # base damage carries to faction HP (no overflow)
                            if tgt["base"] and enemy["hp"] is not None:
                                carry = min(dealt, snap_base_overflow(tgt, dealt))
                                enemy["hp"] = max(0, enemy["hp"] - carry)
                                print(f"           (Base of Influence — {carry} also to "
                                      f"{enemy['name']} faction HP → {enemy['hp']}/{enemy['hp_max']})")
                            if tgt["hp"] == 0:
                                print(f"           {tgt['name']} DESTROYED")
                                if tgt in enemy["assets"]:
                                    enemy["assets"].remove(tgt)
                                deltas.append((enemy["name"], f"lost {tgt['name']} @ {tgt['loc']}"))
                            deltas.append((f["name"],
                                           f"{a['name']} dealt {dealt} to "
                                           f"{enemy['name']}'s {tgt['name']}"))
                    else:
                        cexpr = counter_expr(trec)
                        if cexpr:
                            taken = roller.roll_expr(cexpr, "           counter")
                            if a["hp"] is not None:
                                a["hp"] = max(0, a["hp"] - taken)
                            print(f"           MISS — counterattack {taken} → {a['name']} "
                                  f"HP {a['hp']}/{a['hp_max']}")
                            if a["hp"] == 0:
                                print(f"           {a['name']} DESTROYED by counterattack")
                                if a in f["assets"]:
                                    f["assets"].remove(a)
                                deltas.append((f["name"], f"lost {a['name']} (counterattack)"))
                        else:
                            print("           MISS — no counterattack from target")
                # attacking the enemy advances a Project only if the sheet frames it so
        elif action == "Repair Asset":
            # heal one wounded asset (half its attribute, round up) + optionally faction HP
            wounded = [a for a in f["assets"]
                       if a["hp"] is not None and a["hp_max"] and a["hp"] < a["hp_max"]
                       and not a["base"]]
            if wounded and f["treasure"] >= 1:
                a = wounded[0]
                rec = aidx.get(a["name"].lower(), {})
                attr = rec.get("attr", "Force")
                heal = math.ceil(f["attrs"].get(attr, 0) / 2)
                f["treasure"] -= 1
                a["hp"] = min(a["hp_max"], a["hp"] + heal)
                print(f"           repair {a['name']}: +{heal} HP (½ {attr}) for 1 Treasure "
                      f"→ {a['hp']}/{a['hp_max']}; Treasure {f['treasure']}")
                deltas.append((f["name"], f"repaired {a['name']} (+{heal} HP)"))
            if f["hp"] is not None and f["hp_max"] and f["hp"] < f["hp_max"] and f["treasure"] >= 1:
                heal = hp_repair_amount(f)
                f["treasure"] -= 1
                f["hp"] = min(f["hp_max"], f["hp"] + heal)
                print(f"           repair faction HP: +{heal} for 1 Treasure "
                      f"→ {f['hp']}/{f['hp_max']}; Treasure {f['treasure']}")
                deltas.append((f["name"], f"healed faction HP (+{heal})"))
            if not wounded and (f["hp"] is None or f["hp"] >= (f["hp_max"] or 0)):
                print("           nothing to repair")
        elif action == "Create Asset":
            print("           buys an Asset at a Base of Influence (GM picks from the catalog; "
                  "must meet attribute + Magic req and pay cost). One per turn.")
            deltas.append((f["name"], "intends to Create an Asset (GM to resolve purchase)"))
        elif action == "Move Asset":
            print("           repositions Assets up to one turn's move (~100 mi); "
                  "Subtle/Stealth ignore restrictions.")
            deltas.append((f["name"], "moved/repositioned Assets"))

        # 6) Advance Major-Project clock.
        if f["project"]:
            adv = 2 if (action == "Create Asset" or acted_on_project) else 1
            before = f["project"]["n"]
            f["project"]["n"] = min(f["project"]["N"], f["project"]["n"] + adv)
            filled = f["project"]["n"] >= f["project"]["N"]
            print(f"   [project] {f['project']['name']}: {before} → "
                  f"{f['project']['n']}/{f['project']['N']} (+{adv})"
                  + ("  ★ FILLED — fire it next beat (Turning Point / Random Event)" if filled else ""))
            deltas.append((f["name"],
                           f"project {f['project']['name']} {f['project']['n']}/{f['project']['N']}"
                           + (" FILLED" if filled else "")))

        # goal reminder
        if f["goal"]:
            print(f"   [goal] check vs: {f['goal']}")

    # 7) ONE Background Actor event for the turn.
    print("\n" + "-" * 64)
    print("Background Actor event (one per turn)")
    actor_type = next((f["actor"] for f in factions if f.get("actor")), "")
    tbl_name = ACTOR_TABLE.get(actor_type.lower().strip(), "Background Actor — General (d20)")
    tbl = data["tables"][tbl_name]
    sides = int(tbl["type"].split("list_d")[1])
    r = roller.roll(sides, f"   {tbl_name}")
    val = next(e["value"] for e in tbl["entries"] if e["min"] <= r <= e["max"])
    who = actor_type if actor_type else "the background actor"
    print(f"   → {who}: {val}")
    deltas.append(("(actor)", f"{who}: {val}"))

    # DELTA SUMMARY
    print("\n" + "=" * 64)
    print("END-OF-TURN DELTAS")
    print("=" * 64)
    for f in factions:
        s = snap[f["name"]]
        bits = []
        if f["treasure"] != s["treasure"]:
            bits.append(f"Treasure {s['treasure']}→{f['treasure']}")
        if f["hp"] != s["hp"]:
            bits.append(f"HP {s['hp']}→{f['hp']}")
        if f["project"] and s["project"] is not None and f["project"]["n"] != s["project"]:
            bits.append(f"project {s['project']}→{f['project']['n']}/{f['project']['N']}")
        # asset hp/loss
        now = {(a["loc"], a["name"]): a["hp"] for a in f["assets"]}
        for k, v in s["assets"].items():
            if k not in now:
                bits.append(f"lost {k[1]}@{k[0]}")
            elif now[k] != v:
                bits.append(f"{k[1]} HP {v}→{now[k]}")
        print(f"  {f['name']}: " + ("; ".join(bits) if bits else "no change"))
    for who, txt in deltas:
        if who == "(actor)":
            print(f"  actor: {txt}")
    print("\nRecord the deltas to campaign-state.md (faction board + project clocks); "
          "surface any FILLED clock next beat per bridge/world-model.md.")
    return factions, deltas


def snap_base_overflow(tgt, dealt):
    """Damage to a base carries to faction HP but does not overflow beyond the
    base's remaining HP at the moment of the hit."""
    # tgt["hp"] has already been reduced; the carried amount is min(dealt, pre-hit HP)
    pre = (tgt["hp"] if tgt["hp"] is not None else 0) + dealt
    return min(dealt, pre)


# ---------------------------------------------------------------------------
# Rewrite the sheet (optional).
# ---------------------------------------------------------------------------
def rewrite_sheet(path, factions, text):
    out_lines = []
    cur = None
    fmap = {f["name"]: f for f in factions}
    in_assets = False
    asset_pos = {}  # name -> iterator index per faction
    for raw in text.splitlines():
        line = raw
        m = re.match(r"##\s+Faction:\s+(.*)", line)
        if m:
            cur = fmap.get(m.group(1).strip())
            in_assets = False
            asset_pos = {}
            out_lines.append(line)
            continue
        if cur is None:
            out_lines.append(line)
            continue
        if re.match(r"###\s+Assets", line, re.I):
            in_assets = True
            out_lines.append(line)
            continue
        if not in_assets:
            if re.search(r"\bHP\s*:\s*\d+\s*/\s*\d+", line) and cur["hp"] is not None:
                line = re.sub(r"(\bHP\s*:\s*)\d+(\s*/\s*)\d+",
                              rf"\g<1>{cur['hp']}\g<2>{cur['hp_max']}", line)
            if re.search(r"Treasure\s*:\s*\d+", line):
                line = re.sub(r"(Treasure\s*:\s*)\d+", rf"\g<1>{cur['treasure']}", line)
            if cur["project"] and re.search(r"clock\s*\d+\s*/\s*\d+", line, re.I):
                line = re.sub(r"(clock\s*)\d+(\s*/\s*)\d+",
                              rf"\g<1>{cur['project']['n']}\g<2>{cur['project']['N']}", line, flags=re.I)
            out_lines.append(line)
            continue
        # asset line: match by name+loc, update HP, drop if destroyed/removed
        if line.strip().startswith("-"):
            body = line.strip()[1:].strip()
            parts = [p.strip() for p in body.split("|")]
            if len(parts) >= 2:
                loc, name = parts[0], parts[1]
                live = next((a for a in cur["assets"]
                             if a["loc"] == loc and a["name"] == name
                             and (loc, name) not in asset_pos), None)
                if live is None:
                    # asset was destroyed/lost this turn — drop the line
                    continue
                asset_pos[(loc, name)] = True
                if live["hp"] is not None and re.search(r"HP\s+\d+\s*/\s*\d+", line, re.I):
                    line = re.sub(r"(HP\s+)\d+(\s*/\s*)\d+",
                                  rf"\g<1>{live['hp']}\g<2>{live['hp_max']}", line, flags=re.I)
                out_lines.append(line)
                continue
        out_lines.append(line)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out_lines) + ("\n" if not text.endswith("\n") else ""))
    print(f"\n[--out] rewrote {path}")


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return
    sheet = args[0]
    seed = None
    if "--seed" in args:
        seed = int(args[args.index("--seed") + 1])
    out = None
    if "--out" in args:
        out = args[args.index("--out") + 1]
        if out == "same":
            out = sheet
    if not os.path.exists(sheet):
        sys.exit(f"No faction-sheet at '{sheet}'.")

    data = load_faction_data()
    factions, text = parse_sheet(sheet)
    if not factions:
        sys.exit("No '## Faction: <name>' blocks found in the sheet.")

    roller = Roller(seed)
    roller.banner()
    factions, _ = run_turn(factions, data, roller)

    if out:
        rewrite_sheet(out, factions, text)


if __name__ == "__main__":
    main()
