#!/usr/bin/env python3
"""
check.py — the WWN RESOLVE front-door (rung 1 of the oracle ladder).

Use this for anything a PC *attempts to do*, instead of a Fate Question.
Honest dice, shown. Std-lib only; reproducible with --seed.

  check.py skill   <skill+attr> --vs <6|8|10|12|14>     # 2d6 skill check
  check.py attack  <hitBonus>   --ac <AC>               # 1d20 attack (reminds Shock on a miss)
  check.py save    <target>                             # 1d20 >= target (16-level-attr; Luck 16-level)
  check.py opposed <pcMod> <foeMod>                     # 2d6 vs 2d6, ties to the PC

Fate Questions (mythic-gm dice.py fate) are ONLY for world facts the rules don't
cover — never for a PC task/attack/save/contest. If you're here, you're doing it right.
"""
import argparse
import random
import sys


class Roller:
    def __init__(self, seed=None):
        self.r = random.Random(seed)

    def roll(self, n, d, label=""):
        vals = [self.r.randint(1, d) for _ in range(n)]
        tot = sum(vals)
        print(f"  {n}d{d} -> {vals} = {tot}" + (f"   ({label})" if label else ""))
        return tot


def cmd_skill(a, R):
    raw = R.roll(2, 6, "skill check")
    tot = raw + a.mod
    ok = tot >= a.vs
    print(f"\n  2d6 + {a.mod:+d} = {tot}  vs difficulty {a.vs}  ->  {'SUCCESS' if ok else 'FAILURE'}")
    if not ok:
        print("  (failure = no progress OR success at a cost/complication — GM decides)")


def cmd_attack(a, R):
    raw = R.roll(1, 20, "attack")
    tot = raw + a.bonus
    hit = tot >= a.ac
    print(f"\n  1d20 + {a.bonus:+d} = {tot}  vs AC {a.ac}  ->  {'HIT' if hit else 'MISS'}")
    if hit:
        print("  Roll damage: weapon die + attribute mod (+ magic/Focus). A hit never deals less than its Shock.")
    else:
        print("  MISS — if the weapon has Shock N/AC and the target's AC <= that value, it still deals N (+attr).")


def cmd_save(a, R):
    raw = R.roll(1, 20, "save")
    ok = raw >= a.target
    print(f"\n  1d20 = {raw}  vs save target {a.target}  ->  {'SAVE' if ok else 'FAIL'}")


def cmd_opposed(a, R):
    pc = R.roll(2, 6, "PC") + a.pcmod
    foe = R.roll(2, 6, "foe") + a.foemod
    pc_wins = pc >= foe  # ties to the PC
    print(f"\n  PC 2d6{a.pcmod:+d} = {pc}   vs   foe 2d6{a.foemod:+d} = {foe}   ->  {'PC WINS' if pc_wins else 'FOE WINS'}  (ties to PC)")


def main():
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--seed", type=int)
    ap = argparse.ArgumentParser(description="WWN resolve front-door (honest dice).")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("skill", parents=[common]); s.add_argument("mod", type=int); s.add_argument("--vs", type=int, required=True); s.set_defaults(fn=cmd_skill)
    s = sub.add_parser("attack", parents=[common]); s.add_argument("bonus", type=int); s.add_argument("--ac", type=int, required=True); s.set_defaults(fn=cmd_attack)
    s = sub.add_parser("save", parents=[common]); s.add_argument("target", type=int); s.set_defaults(fn=cmd_save)
    s = sub.add_parser("opposed", parents=[common]); s.add_argument("pcmod", type=int); s.add_argument("foemod", type=int); s.set_defaults(fn=cmd_opposed)
    a = ap.parse_args()
    a.fn(a, Roller(a.seed))


if __name__ == "__main__":
    main()
