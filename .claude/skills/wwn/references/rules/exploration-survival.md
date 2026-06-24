# Exploration & Survival — overland travel, the dungeon turn, supplies

> Use this when: the party crosses wilderness, explores a hex, delves a site, or runs low on food/water/fire. This is the clock that grinds heroes down — run the privation and encounter checks straight; the wilds answer to logic, not the party's level.

**Dice via `<mythic-gm>/scripts/dice.py roll <NdM>` and shown.** Wandering-encounter & privation cadence fire at the world-tick (`bridge/subsystems.md`).

## Overland travel
Travel ~10 hours/day. **Miles per hour by terrain** (cross-multiply the modifiers):

| Terrain | mi/hr | | Modifier | × |
|---|---|---|---|---|
| Plains / savanna | 3 | | Road through it | ×2 |
| Light forest / desert | 2 | | Foul weather, mud, heavy rain | ×0.5 |
| Dense forest / rugged hills | 1.5 | | Deep snow | ×0.1 |
| Swamp / marsh | 1 | | | |
| Mountains / *arratu* wastes | 0.5 | | | |

- **Sea:** ~6 mi/hr under sail (round the clock if far from coast); galleys row 8 hrs/day. Sea encounter checks are `1d10` or `1d12` (see `references/setting`/naval).
- **Lightly exploring one 6-mile hex** for points of interest = a full day's scouting (×2–3 in rugged/concealing terrain). Catches major sites, not small features.

## The dungeon turn (site exploration)
Inside a ruin/Deep, track **turns** ≈ 10 min ≈ one scene; each PC does one significant thing/turn. **Order of play each turn:** (1) secret Wandering-Encounter check; (2) PCs declare; (3) resolve & describe; (4) repeat until they withdraw. Move between rooms of interest = 1 turn. Fleeing: pursuers' best **opposed Dex/Exert** vs party's (slowest member −2; +1 if PCs are fewer). Searching a stated spot finds hidden things automatically; otherwise best **Wis/Notice**. Locks/traps: 1 turn, **Dex/Sneak** vs diff 8+ (panicked = a Main Action at +2 diff, failure jams it).

## Light & timekeeping
Torch or lantern lights a **30-ft radius**. **Torch lasts 6 turns; a filled lantern 24 turns.** Outside the light, the Deep is too dark to make out. (Simplified play assumes the adventuring-gear bundle covers light; don't itemize torches unless lost.)

## Supplies & encumbrance (Enc per item)
Fire / water / shelter / food are the four needs. **Readied = Str/2 (round down); Stowed = full Str.** Carrying +2 Readied / +4 Stowed drops Move to 20 ft; another tier drops it to 15 ft.

| Supply | Enc | | Pack loads (Enc carried) | |
|---|---|---|---|---|
| 1 day food *or* water | 1 | | Riding/warhorse, laden rider | 5 |
| 1 week packed food | 4 | | Riding/warhorse, pack only | 20 |
| 1 night's fire fuel | 4 | | Heavy pack horse | 30 |
| 1 day fodder, large beast | 4 | | Mule / donkey | 15 |
| Daily water, large beast | 8 | | Professional porter | 12 |

Butchering yields 30 days' rations (horse) / 15 (mule). **Foraging:** half- or full-day, best **Wis/Survive** vs terrain diff (Woodland 8 · Mtn/scrub/savanna 9 · Desert/badlands 12 · *arratu* 14; full day −2, repeat-hex +1). Success = `dice.py roll 1d6` + summed Survive skills (max 10) units of food/water/fire; no skill −1. One encounter check per foraging attempt.

## Privation — the squeeze
Each day a need goes unmet adds **System Strain** (no save to resist it):

| Circumstance | +Sys.Str |
|---|---|
| First day without food | +0 |
| Consecutive day without food | +1 |
| First day without water | +2 |
| Consecutive day without water | +3 |
| Night without adequate shelter/fire | +0 |
| Harsh night without shelter/fire | +1 |

If Strain would exceed maximum → **Physical save** or **die by dawn** unless rescued; on a success, **helpless** until death or rescue. While deprived, the PC can't recover Strain, gain nightly HP healing, refresh daily Committed Effort, or restore spells until a full day of food, water, and warm sleep. (Strain mechanics: `references/rules/healing-and-strain.md`.)

## Wandering encounters — the pressure
**Overland:** roll the region's check **once per day's travel and once per night's camp** (and once per foraging attempt). On a **1**, something arises at the terrain's max sight range → **opposed Wis/Notice** for who spots whom. Chances: Dangerous wilds / civil-unrest / banditry **1-in-6** · ordinary wilds or back-country **1-in-8** · ordinary trade road **1-in-8** · well-policed road **1-in-10**.

**In a site:** roll `dice.py roll 1d6` every N turns; on a **1** it lands this turn. Frequency by alertness: Alerted+organized **every 1** · unalert+organized **every 2** · no active defense **every 3** · few mobile inhabitants **every 4** · disused nook **every 6** · hidden/unknown area **no check**. Encounters fit the site's logic, not PC level. **Always make a Reaction roll (2d6)** — not every group lunges; give the PCs a chance to parley or flee. Draw contents from the site's prepared table or `wilderness_tags`/`monster_gen` (`bridge/generators/`).

Source: `book/Worlds-Without-Number-Deluxe/04-The-Rules-of-the-Game.md` (L454–693); encumbrance `03 - Equipment, Armor, and Weaponry.md` (L31–45).
