# Treasure & Magic Items — placing a hoard

> Use this when: stocking a site, a foe, or a cache with loot, and deciding whether (and which) magic items it holds. Decide the *total* first, then split and flavor it. WWN rewards are leaner than most old-school games — that's by design; their rarity is the point.

**Dice via `<mythic-gm>/scripts/dice.py roll <NdM>`; or run the generator: `python3 scripts/gen.py treasure/"<Table>"`** (bundle `bridge/generators/treasure.json`).

## 1 — Total silver value of the site
Pick the site line, roll **`dice.py roll 2d6`**, read the column it falls in (2–3 · 4–5 · 6–8 · 9–10 · 11–12); each cell is a silver formula. (Full matrix in `treasure.json` → "Silver Piece Value"; e.g. *minor Deep* at column 6–8 = `3d6 × 1,000`, *bandit cache* at 2–3 = `1d6`.) Adjust for how picked-over the place is — PCs rarely find all of it, and missing one major trove can cost them half. **Then divide:** put **half** the total in one or two major troves (strongest foe / behind an enigma); scatter the rest across smaller finds.

## 2 — Flavor the troves
Not every trove is coins. Roll for texture and assign each item a share of the value:
- **Jewelry** `1d8` · **Valuable Objects** `1d20` (spices, textiles, art, uncut jewels, ingots…) · **Why it's especially valuable** `1d20` (contraband, unearthly material, a famous maker's mark…). All in `treasure.json`.

## 3 — Does it hold magic items?
Pick the owner/cache line, roll **`dice.py roll 1d20`** ("Chance for Magic Items"):

| Owner / trove | No items | One | Two | 3+ |
|---|---|---|---|---|
| 1 HD creature | 1–19 | 20 | — | — |
| 2–4 HD creature | 1–18 | 19 | 20 | — |
| 5–10 HD creature | 1–10 | 11–17 | 18–19 | 20 |
| 11+ HD creature | — | 1–8 | 9–16 | 17–20 |
| Minor unguarded trove | 1–18 | 19–20 | — | — |
| Major unguarded trove | 1–5 | 6–18 | 19 | 20 |
| Adventurer / noble | 1–10 | 11–19 | 20 | — |
| Veteran adventurer | — | 1–5 | 6–15 | 16–20 |
| Minor mage / shaman | 1–10 | 11–18 | 19–20 | — |
| Great wizard | — | — | 1–5 | 6–20 |

Hand-place by taste whenever it fits the story; an intelligent owner uses what they have.

## 4 — Which item? (`1d20` Type of Magic Item Found, in `treasure.json`)
1–6 **Elixir** · 7 **Exemplar or Grimoire** · 8 `1d3` **Ancient Salvage** · 9–11 **Calyx** · 12–14 **Weapon** · 15–16 **Armor** · 17 **Shield** · 18–20 **Device**.

## Kinds of magic items (how each works)
- **Weapons** — bonus to hit/damage/Shock; harms otherwise-immune magical foes. Pick **minor/major/great**, roll `1d20` for **+1/+2/+3** (minor: +1 on 1–16; great: +3 on 5–20), `1d8` original-user → favored weapon, then `1d12` for special-ability count.
- **Armor** — enchant **+1..+3** adds to base AC (always masterwork → Enc −1, not for *Armored Magic*); roll bonus and abilities as weapons. **Shields** never grant an AC bonus but **always** have one power; can't be Shattered.
- **Devices** — catch-all rings/staves/trinkets with one narrow power (Censer of Solid Dreams, Enough Rope, Congealed Paradox…). Roll on the `d100` device list or pick.
- **Elixirs** — single-use potion/salve/charm; consumed as a Main Action; one Enc when Readied. Identify by **day of Wis/Int+Magic** vs creation diff (one try each), *Apprehend the Arcane Form*, or a taste-hint. Roll `d100` for type + diff/cost. Fouled potions read as genuine until used.
- **Grimoires / Exemplars / Calyxes** (mage-only). **Grimoire** holds learnable spells (1 wk/level − Magic skill, min 1 day). **Exemplar** = a silver-valued insight (`1d20`: minor/major/great) spent to defray Working/research/crafting costs; using it up destroys it. **Calyx** = stored single-use spells, castable by anyone with **Magic ≥ spell level − 1** (else Int/Cha+Magic vs 8 + spell level, risky); calyxes can't teach.

## Random Grimoire contents (`1d20`)
| d20 | Total spells | Max level |
|---|---|---|
| 1–5 | 1 | 1 |
| 6–10 | 3 | 2 |
| 11–14 | 5 | 3 |
| 15–18 | 7 | 4 |
| 19 | 9 | 5 |
| 20 | 11 | 5 |
A *found* grimoire has ~one legible spell per level/HD of the owner (one of each castable level, then repeat from 1st). Pull the actual spells with `python3 scripts/lookup.py spell "<name>"` or `gen.py` against `bridge/generators/spells.json`; add a flaw to surprise the wizard.

Source: `book/Worlds-Without-Number-Deluxe/08-Creating-Adventures/10-Placing-Treasures.md` (L17–110); `…/13 - Magic Items.md` (weapons L238–356, armor L27–152, calyx/exemplar/grimoire L153–237, devices L530–560, elixirs L647–700).
