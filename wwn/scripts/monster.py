#!/usr/bin/env python3
"""
monster.py — WWN monster helper with HONEST, SHOWN dice.

  python3 scripts/monster.py --context [--seed N]   # roll a One-Roll Monstrous Context concept
  python3 scripts/monster.py --hd 4   [--seed N]    # stat a generic foe of N HD
  python3 scripts/monster.py --lookup "ghoul"       # print a bestiary statblock (fuzzy)

Every die is printed (e.g. `1d12 -> [7] = 7`).  Reproducible with --seed.
If env MYTHIC_GM_DICE is set it is noted, but rolls are produced internally so
the script always runs standalone.  Std-lib only; Python 3.6+.
"""
import argparse
import json
import os
import random
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GEN = os.path.join(os.path.dirname(HERE), "bridge", "generators")


def load(name):
    p = os.path.join(GEN, name)
    if not os.path.exists(p):
        sys.exit(f"Missing {name} — run the build scripts first.")
    return json.load(open(p, encoding="utf-8"))


class Roller:
    def __init__(self, seed=None):
        self.r = random.Random(seed)

    def roll(self, n, d, label=""):
        vals = [self.r.randint(1, d) for _ in range(n)]
        tot = sum(vals)
        print(f"  {n}d{d} -> {vals} = {tot}" + (f"   ({label})" if label else ""))
        return tot


def pick(roller, bundle, table_name):
    t = bundle["tables"][table_name]
    m = re.match(r"(\d+)d(\d+)", t.get("dice", ""))
    n, d = (int(m.group(1)), int(m.group(2))) if m else (1, t["entries"][-1]["max"])
    roll = roller.roll(n, d, table_name)
    for e in t["entries"]:
        if e["min"] <= roll <= e["max"]:
            return e["value"]
    return t["entries"][-1]["value"]


CONTEXT = ["Basic Body Plan", "Animal Resemblance", "How It Hunts",
           "Why Isn't It Dead Yet", "Monstrous Drive"]


def cmd_context(roller):
    mg = load("monster_gen.json")
    print("== One-Roll Monstrous Context ==")
    out = []
    for name in CONTEXT:
        if name in mg["tables"]:
            out.append((name, pick(roller, mg, name)))
    print("\nConcept:")
    for k, v in out:
        print(f"  {k}: {v}")
    print("\n  → Stat it with --hd N, then add an Uncanny Power for a signature threat"
          " (see monster_gen.json / references/gm/monsters.md).")


def cmd_hd(roller, hd):
    print(f"== Generic foe — {hd} HD ==")
    hp = roller.roll(hd, 8, "HP (d8 per HD)")
    atk = min(hd, 10)
    save = 15 - hd // 2
    ac = 12 if hd < 3 else (13 if hd < 6 else 15)
    dmg = "1d6" if hd < 3 else ("1d8" if hd < 6 else "1d10")
    skill = max(1, hd // 2)
    print(f"\n  HD {hd} | HP {hp} | AC {ac} | Atk +{atk} | Dmg {dmg} (Shock 1/{ac})"
          f" | Move 30' | ML 8 | Instinct (pick) | Skill +{skill} | Save {save}+")
    print("  (Baseline — tune AC/damage and add abilities to fit the concept.)")


def cmd_lookup(name):
    best = load("bestiary.json")["records"]
    nl = name.strip().lower()
    hits = ([k for k in best if k.lower() == nl]
            or [k for k in best if k.lower().startswith(nl)]
            or [k for k in best if nl in k.lower()])
    if not hits:
        sample = ", ".join(list(best)[:10])
        sys.exit(f"No bestiary match for '{name}'. e.g. {sample} …")
    for k in hits[:3]:
        r = best[k]
        print(f"== {k} ==")
        print(f"  HD {r['hd']} | AC {r['ac']} | Atk {r['atk']} | Dmg {r['damage']}"
              f" | Shock {r['shock']} | Move {r['move']} | ML {r['morale']}"
              f" | Instinct {r['instinct']} | Skill {r['skill']} | Save {r['save']}")
        if r.get("notes"):
            print(f"  {r['notes']}")
        if r.get("source"):
            print(f"  Source: {r['source']}")
        print()


def main():
    if os.environ.get("MYTHIC_GM_DICE"):
        print("[MYTHIC_GM_DICE set — rolls shown below are honest and reproducible]\n")
    ap = argparse.ArgumentParser(description="WWN monster helper (honest dice).")
    ap.add_argument("--context", action="store_true",
                    help="roll a One-Roll Monstrous Context concept")
    ap.add_argument("--hd", type=int, help="stat a generic foe of N HD")
    ap.add_argument("--lookup", metavar="NAME", help="print a bestiary statblock")
    ap.add_argument("--seed", type=int)
    a = ap.parse_args()
    roller = Roller(a.seed)
    if a.context:
        cmd_context(roller)
    elif a.hd is not None:
        cmd_hd(roller, a.hd)
    elif a.lookup:
        cmd_lookup(a.lookup)
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
