# Creating Adventures — the four challenge-builders

> Use this when: building (or improvising at the table) the meat of an adventure — a fight, a delve, a mystery, or a negotiation — and awarding XP/Renown. WWN sandboxes obey **logic, not balance**: a tribe has its forty warriors whether the PCs are level 1 or 10. Never force a challenge; always leave a way around it.

Each challenge becomes the engine's **scenes** (`bridge/world-model.md`). For a fast premise, run `python3 scripts/gen.py hook` — it fills a `fractal_seeds` premise with Enemy/Friend/Complication/Thing/Place drawn from a location tag, plus Bait + Introduction (`adventure_seeds`). All dice via `<mythic-gm>/scripts/dice.py roll <NdM>`.

## Combat challenge
Build the *facts*, not a balanced fight. (1) **List who's there** — the target + guards, minions, allies; jot stat lines. (2) **Frame the environment** — map, hazards, who hears the alarm; keep it logical (people don't live next to death-traps). (3) **Identify alternate routes** — a back door, a bribe, a social angle. There is almost never a reason to *force* a head-on brawl; an adventure of unavoidable fights gets PCs killed. (4) **Recognize consequences** — who avenges, replaces, or thanks the dead. Liven a banal fight with the complication tables (`d20` twist about the target · `d12` what they're doing now / their problems · `d12` bestial monster · urban/wilderness/Deep complications). Run foes to **win** (Morale, Reaction, self-preservation all apply).

## Exploration challenge (sites & hexcrawls)
Procedure: (1) **inhabitant framework** + (2) **site type** (`d`-tables, or `gen.py ruin --seed N`); (3) **~10–20+ rooms of interest** — assume **half hold nothing significant**; (4) **lay out** rooms (index cards, exits, loops) and add map features/level links; (5) **stock** each room — creature / treasure / enigma / distractor (no more than ⅓ have creatures; ~half of those guard treasure; ~⅙ of empty rooms still hold loot — don't gate *all* loot behind monsters). Pull residents from your framework groups + `monster_gen`; pull totals from the silver matrix (`references/gm/treasure-and-items.md`). (6) **Wandering table** of 6 entries (~⅓ events, not all hostile). (7) **Daily life** — what each group is doing, and how it reacts when disturbed. Hexcrawl: each hex is a "room," stocked from `wilderness_tags`. Run the turn/encounter clock per `references/rules/exploration-survival.md`.

## Investigation challenge — built backwards
Mysteries are hard because their scope is open; tilt the table on purpose. Build from the climax down:
1. **Resolution** — the confrontation/revelation. Prep its stats, map, and social fallout.
2. **Three Investigation scenes** — pick exactly **three facts** that together unlock the Resolution; give each its own scene, its own keeper (NPC/place), and an **obstacle** in front of it. This is the **three-clue rule** — three independent paths to the truth so no single failure stalls the case.
3. **Introduction scene** — points the PCs at all three clues with *actionable* "do this next" intelligence.
4. **Hook scene** (optional) — signals there's a mystery at all.
5. **Reaction / Failsafe** (optional) — how a noticed culprit strikes back; a Failsafe hands a missed clue to the PCs at a price (a hurt ally, a stronger enemy).

In play: be **blunt about irrelevancies** (kill dead-end red herrings), **reward effort with information** (never "you learn nothing"), **no naked skill checks** (make them describe *how* they search before any Connect/Notice roll), and **always leave one lead forward**. Decide your failure mode up front: dead-end, or get-it-at-a-price.

## Social challenge
The PCs want something an NPC holds. **Build the target** by answering: is the result possible? why won't they give it? what do they want from the PCs? what levers can the PCs pull? how can the NPC hurt them? And — **how do the PCs even hear of them?** (be generous with hooks; the meat is after they meet). In play: each PC who rolls a social skill must first **state their offer/terms**; you privately set difficulty by *offer vs. demand* (good offer ~7, risky/poor ~12+). **Success** → they accept or add a doable condition; **failure** → never a flat refusal — give a hint at a new lever or a way to change the terms. Quick target: `d4` mood · `d12` what they want · `d6` how PCs hear of them · `d8` why they refuse · `d10` weakest point · `d20` negotiation twist. Court tags (`gen.py court`) supply their context, minions, and resources.

## Rewards — Renown, money, XP
**Renown** (per session, per PC): +1 for adventuring at all; +1 for helping locals/authority; +1 for spending ≥25% of last haul on carousing/charity; *Special* for a helpful adventure done without pay (convert a fitting patron-reward to Renown, split as bonus). You don't *lose* Renown for angering rulers.
**Pay** scales by patron (peasant 50 sp → monarch/merchant-prince 50,000 sp); ×2 if paid in land/goods or for great danger, ×4 if desperate. A bribe to face real danger ≈ ×2 the patron's reward.
**XP** — pick **one** system: *default* 3 XP/session for genuine adventuring (success not required); *goal-based* (short goal 3 / long 9, +1/+3 to helpers, rotate the spotlight); *mission-based* (agreed goal → 3 each); *spending-based* (3 each only if last session's liquid cash was all spent). What you reward is what the table chases.

Source: `book/Worlds-Without-Number-Deluxe/08-Creating-Adventures/`: `05 - Creating Combat Challenges.md`, `06 - Creating Exploration Challenges.md` (L5–110), `07 - Creating Investigation Challenges.md` (L9–130), `08 - Creating Social Challenges.md`, `09 - Rewards, Renown, and Experience Points.md`.
