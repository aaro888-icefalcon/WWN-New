# WWN references — index

> Use this when: deciding which card to load. **Load lean** — read one card for the task at hand, not the folder. Each card opens with `> Use this when:` and ends with a `Source:` line into `book/`. Generators are JSON rolled by scripts (`bridge/generators/`), not read here.

## rules/ — player-facing resolution (hot path)
| File | For |
|---|---|
| `resolution.md` | skill checks, difficulties, opposed/aided, skill list, advancement |
| `combat.md` | the tactical fight: action economy, Shock, swarm, screen, mortal-wound flow |
| `saves.md` | the four saves + hazards (poison, falling, suffocation) |
| `healing-and-strain.md` | mortal wounds, first aid, System Strain, rest, magical healing |
| `character-creation.md` | making a PC (also `scripts/chargen.py`); backgrounds, classes, foci, gear |
| `magic-and-effort.md` | Effort, Arts, spell slots, the caster traditions |
| `exploration-survival.md` | travel, light, supplies, watches, wandering encounters |

## gm/ — running the world
| File | For |
|---|---|
| `worldgen.md` | build & expand the world (region/nation/court/ruin); the Session-Zero scope dialog |
| `faction-turn.md` | the WWN-native Faction Turn, Major Projects, Renown, domains |
| `monsters.md` | statting & generating foes; the bestiary lookup |
| `treasure-and-items.md` | hoards, magic items, enchantments |
| `creating-adventures.md` | combat/exploration/investigation/social challenge builders |
| `gm-tools.md` | oracles, NPC/architecture/seed generators (Additional GM Tools) |

## Deeper than a card?
Each card cites the exact `book/Worlds-Without-Number-Deluxe/…` (or `…/The Atlas of the Latter Earth/…`) range. Open the book chapter only when the card is insufficient. Pull one record (a focus, spell, monster, tag) with `python3 scripts/lookup.py <kind> <name>` rather than loading a chapter.
