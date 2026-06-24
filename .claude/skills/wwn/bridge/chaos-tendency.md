# Chaos Tendency — Latter Earth   (hook: chaos)

## Operative
Judge the Chaos Factor HONESTLY every scene (±1, RAW): −1 ONLY if the PC was genuinely in control and
ended on their own terms; +1 if overwhelmed, failed, fled, disrupted by an Interrupt/Random Event, or
ended not on their terms; when unsure, +1. Control in the Latter Earth is hard-earned — the world is
volatile and indifferent. Apply the highest regional floor below (Deeps / active ruins / arratu /
lawless frontier ≥ 6; an Iterum ≥ 7) and never drop Chaos beneath it there. A Chaos Factor that only
falls is drift.

# Config — the ±1 step is always RAW; the values below tune the lean, floors, and flavor (not the step).
- start: 5
- volatility: normal        # ±1 each scene as the engine dictates; passivity lets it climb
- floor: |
    Most settled land has no floor (can fall to 1 in a calm, ruled town).
    Regional minimums — the world runs hotter where order thins:
      the Deeps & active ruins        >= 6
      Outsider-touched zones / arratu >= 6   (Ashblight, Blind Marsh, Iron Sky, an Iterum >= 7)
      lawless frontier / war zones     >= 6   (Ka-Adun's new city, Rebel Coast, Llaigis, reclaimer marches)
      otherwise                        none
    Apply the highest floor for the PC's current region; never drop Chaos below it there.
- flavor: standard          # standard (default, full chaos) — the Latter Earth is volatile and indifferent

# What "chaotic" looks like here: the ancient world stirs. A Deep wakes something; a decaying
# Working misfires; an arratu exhales a new horror; a warlord, faction, or Outsider seizes the
# opening the PC just made. High Chaos = the dead past and self-interested powers act first.
