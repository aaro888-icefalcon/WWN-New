#!/usr/bin/env python3
"""
bookkeep.py — the MANDATORY end-of-scene bookkeeping step for a WWN campaign.

Run this at every scene end. It prints the ordered checklist (with the exact
commands) so nothing silently stalls — the world-tick, Effort, Strain, the Lists,
Chaos, and the self-audit. The forcing function: if you didn't run this, the
scene isn't finished.

  python3 scripts/bookkeep.py <campaign_dir> <scene#> [--control pc|chaotic] [--at-sea] [--exploring]

Std-lib only. It does no hidden rolls — it tells you what to run (all honest dice
stay in dice.py / tick.py / faction_turn.py / check.py).
"""
import argparse
import os
import sys

ENG = "<mythic-gm>"   # the installed engine; resolve to its real path at runtime


def main():
    ap = argparse.ArgumentParser(description="WWN end-of-scene bookkeeping checklist.")
    ap.add_argument("campaign", nargs="?", default="<campaign>")
    ap.add_argument("scene", nargs="?", default="N")
    ap.add_argument("--control", choices=["pc", "chaotic"], help="who controlled the scene (sets Chaos +/-1)")
    ap.add_argument("--at-sea", action="store_true")
    ap.add_argument("--exploring", action="store_true")
    a = ap.parse_args()
    c, n = a.campaign, a.scene
    skill = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    bridge = os.path.join(skill, "bridge")

    print(f"=== WWN BOOKKEEPING — scene {n} ===\n")
    cf = "  Chaos: " + (
        f"PC in control → `{ENG}/scripts/state.py chaos -1 {c}`" if a.control == "pc"
        else f"world/chaotic → `{ENG}/scripts/state.py chaos +1 {c}`" if a.control == "chaotic"
        else "PC in control → chaos -1 ; chaotic → chaos +1  (`state.py chaos ±1 <campaign>`)")
    steps = [
        "1. CHAOS FACTOR\n" + cf,
        f"2. WORLD-TICK (fire due subsystems)\n   `python3 {ENG}/scripts/tick.py {bridge} {n}`\n"
        f"   → FACTION MOVE every scene: `python3 scripts/faction_turn.py {c}/factions.md --move auto --out same` — one faction acts and advances its clock (no economy). Run the FULL Faction Turn (`faction_turn.py {c}/factions.md`) at the weekly cadence. SURFACE the move/any filled clock as a sign now / a Random Event or Turning Point next beat (world-model.md §3).\n"
        f"   → NEW FACTION if play surfaced a power not on the board: `python3 scripts/worldgen.py faction --name <X> --campaign {c}` and add it.\n"
        "   → Major-Project clocks advance with the move/turn.",
        "3. EFFORT & STRAIN\n   Return scene-committed Effort; on a night's rest return day-Effort and −1 System Strain (and heal level/HD HP). Frail recover neither.",
        ("4. EXPLORATION CLOCKS\n   Supplies/light spent this watch/day; wandering-encounter check if exploring (saves.md / exploration-survival.md)."
         if (a.exploring or a.at_sea) else
         "4. EXPLORATION CLOCKS\n   (none active — running in a settled scene)"),
        ("5. NAVAL\n   Day at sea → roll `naval` (Seafaring Event / Ship Crisis)." if a.at_sea else None),
        f"6. LISTS (JSON is the source of truth)\n   Add/weight/remove Threads & Characters with `{ENG}/scripts/state.py thread|char add|weight|remove {c}`. Refresh the seed deck (seeds.md). Do NOT hand-edit a Markdown copy.",
        ("7. FRONTIER (did play reach the edge of charted canon?)\n"
         f"   Did this scene reach the edge of charted canon, or name a new region/kingdom not in `setting-canon.md`?\n"
         f"   • If yes → queue `python3 scripts/worldgen.py geography --scale <region|kingdom> --campaign {c}` (or `ruins --kingdom <name>` / a single `settlement|court|ruin|wilderness`) for the NEXT framing; show the DRAFT CANON, then on approval fold it into `setting-canon.md`, seed its hooks as Threads & figures as Characters (`state.py`), put any new nation on the faction board, and write a node per place to `{c}/places.json` (each carries its FULL tag; re-entry is a lookup, not a reroll).\n"
         "   • Distant new content enters the Lists/seeds at LOW weight (≤1) so it never crowds the scene in front of the PC.\n"
         "   • Un-recorded new places are a soft scene — the world must persist what play discovered."),
        "8. SELF-AUDIT (gate)\n   • Was any PC task resolved by a Fate Question instead of `check.py`? → that's a FAIL; note it.\n   • Did something real move (a rolled outcome, a resource, a clock, a present threat)? If not, the scene is soft.\n   • Did NPCs/factions act to win?",
        f"9. WRITE STATE\n   Overwrite `{c}/campaign-state.md` (WWN fields). The Lists already live in threads.json/characters.json.",
    ]
    for s in steps:
        if s:
            print(s + "\n")
    print("Done → only now is the scene complete. Back to: frame the next scene.")


if __name__ == "__main__":
    main()
