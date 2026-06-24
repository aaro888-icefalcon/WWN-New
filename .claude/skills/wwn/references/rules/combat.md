# Combat — tactical card

> Use this when: any fight, or to adjudicate a combat action, Shock, a mob, or a downed character. WWN combat is lethal and positional — heroes have **no plot armor**. Run it straight.

**All rolls via `<mythic-gm>/scripts/dice.py roll …` and shown.** Pre-commit the stakes, roll, then narrate.

## The round
- **Initiative:** each side `1d8 + best Dex mod`; highest side acts first (own order), PCs win ties. Re-cycle each round. (Optional: individual init.)
- **Surprise:** if plausible, opposed **Wis/Notice vs Dex/Sneak**; winner gets a full free round. May force a Morale check.
- Each turn: **1 Main**, **1 Move**, free **On-Turn** acts, unlimited **Instant** (usable even off-turn, even after dice are seen).

## Attack & damage
- **Hit roll:** `1d20 + combat-skill level + class attack bonus + attribute mod (+ situational)` vs target **AC**. Untrained weapon = −2.
- **Damage:** weapon die **+ attribute mod + magic/Focus**. Subtract from HP.
- **0 HP:** unnamed NPC dies; PC / named NPC is **Mortally Wounded** (see healing card). Non-lethal intent → unconscious, revives at 1 HP in 10 min.
- A "hit" is abstract (luck/position/stamina); only the last is the real wound.

## Shock — the tactical floor
Weapons list **Shock N/AC**. On a **miss** against a target whose **AC ≤ that value**, still deal **N** damage (+ attribute & magic bonuses; *not* other damage bonuses). A hit never deals less than its Shock. Heavily-armored targets (AC above the value) are immune. Shields negate the **first** Shock each round. → unarmored swarms and lightly-armored foes bleed even on misses; armor and positioning matter.

## Hit modifiers (cumulative, GM guideline)
Distant prone target −2 · adjacent prone target +2 · target half in cover −2 · nearly full cover −4 · melee-attacking while prone −4 · thrown while in melee −4 · **bow while in melee: not allowed** (one-handed/thrown at −4). No penalty for shooting *into* a melee.

## Signature actions (the tactical menu)
- **Swarm Attack** (Main) — up to 4 assailants pile on; the last attacks at **+2 hit / +1 dmg per other attacker** (cap **+6/+3**). Bonus damage can't exceed the weapon's normal max, **but the Shock always lands** — through high AC, shields, even Shock-immunity. The mob's answer to a tough lone foe.
- **Screen an Ally** (Move) — block for an ally within 10 ft; enemies attacking them make an opposed Str/Dex combat check vs you or have the attack **redirected to you**. Screen a number of foes = your combat-skill level.
- **Total Defense** (Instant; costs your Main) — **+2 AC** and **immune to Shock** (incl. swarms) until next turn.
- **Fighting Withdrawal** (Main) — disengage from melee without granting free attacks (then Move clear; leaving melee otherwise grants every adjacent enemy a free Instant attack).
- **Snap Attack** (Instant; spends your Main) — attack at **−4**, resolves simultaneously with other snaps. (PCs / named foes only.)
- **Charge** (Move+Main) — up to 2× move straight in, **+2 hit**, **−2 AC** that round.
- **Execution Attack** — 1 full minute setup vs an unaware foe; melee auto-hits (ranged Dex/Shoot vs 6/8/10). On hit, target makes a Physical save at **−(attacker's combat skill)** or is Mortally Wounded; on success still takes max damage. Unconscious target → auto Mortally Wounded.
- **Shatter a Shield** (Main) — axe/mace/etc.: hit, then opposed Str/Stab (defender +1); win → shield broken (not magical ones).
- **Dual-wield** (needs Stab-1): **+2 damage** (not Shock), **−1 hit**; one attack/round.
- Also: Make Ranged Attack, Cast a Spell (fails if you took HP damage this round), Hold an Action, Delay, Go Prone, Ready/Stow, Reload, Stand Up.

## Grapple / shove
Hit for no damage, then opposed **Str/Punch** (grapple) or **Str/Punch or Str/Exert** (shove → 10 ft back or prone). Grappled: no move, unarmed only, takes each grappler's unarmed damage each round. Size mismatch −2/−4.

## Morale & breaking
After first loss / a fright / being overmatched, roll **2d6 vs Morale**; over → flee/parley. **NPCs act to win** — they focus fire, screen, retreat, take Total Defense, bargain when losing. Never play them dumb to spare the PC (engine Creed).

Source: `book/Worlds-Without-Number-Deluxe/04-The-Rules-of-the-Game.md` (L117–386).
