# Campaign State — WWN   (extends the engine's campaign-state.md)

> Use this when: this is the campaign's **source of truth** — overwrite it at each scene end (engine bookkeeping). It EXTENDS mythic-gm's `campaign-state.md` with WWN fields. The engine reads the Engine block; WWN reads the rest. See `bridge/world-model.md` for how the ledger feeds the engine's Lists.

## Engine block (mythic-gm)
*Lists are stored canonically as `threads.json` / `characters.json` (engine `state.py thread|char` / `lists.py`); the lines below mirror them for reading. `state.py init <campaign>` scaffolds the JSON; pass `--campaign <dir>` to the engine's List / Fate / Turning-Point scripts.*

- **Chaos Factor:** 6  *(floor 6; scene 17 — Shake landed a ward post, a base & a revived plan: a stabilizing win, but the floor holds in a cracking realm)*
- **Adventure mode:** Adventure Crafter  *(Theme priority: Action ▸ Social ▸ Tension ▸ Personal ▸ Mystery)*
- **Threads & Characters Lists:** canonical in `threads.json` / `characters.json` — view with `state.py thread show` / `char show`. **Do not copy them here.**
- **Adventure Features:** …  *(if a prepared/ingested adventure)*
- **★ SAVE POINT (resume here):** **Scene 18 — the night the boy-king died.** Shake moved **Reza** to the cooper's (safe) with a brief, opaque parting from **Maela** (who clocked his ward-colors and recalculated — *"you've made yourself visible"* — a sign kept). Then a **Turning Point** broke the kingdom: **Boy-King Phillipe is DEAD** — fallen as the realm's armies finally crashed (mass battle); **the Dragon Throne collapses**, the succession now a brawl over an **empty chair.** Mauressac, already cracked, **erupts into open violence** (riot/factional convulsion in the river-ward). In the chaos **Osric SLIPPED Wynne's net** (Fate Yes) — ruined, name in the gutter, but **loose & fugitive with Gault** (who has Shake's face). And **the man in the good coat** — the opaque watcher from the road — **dragged himself, gut-opened and unconscious (can't speak — Fate No), to the one healer he'd tracked: Shake.** **CLIFFHANGER:** the mystery-man lies open and silent under the new ward-leech's hands, the city screaming, Reza safe behind a bolt. HP 6/6 · Effort 3/3 · purse ~56 sp · Chaos 6 *(scene-18 Chaos/tick pending at scene end)*. **Decision on the table:** *save the coat-man (and maybe learn who he is if he wakes — or from what's on him) · search him · let him die · or other — amid the eruption.*
- **Last scene recap:** **Scenes 2–5 — the road west, and the catastrophe on it.** Shake left the Landing with **Hild's** westbound salt-caravan (apprentice **Reza** in tow), bound for **Mauressac** on a thin 4-month-old lead that his brother **Akhil** fell west; his first four months are now canon, and road-rumor says Mauressac's countess is *gathering rift-folk* (his hope, unconfirmed). Shake talked captain **Hild** off a first-strike against **5 Blighted** (who were *fleeing* something west and let the caravan pass). The caravan camped to wait the threat out — and **drew it**: a thing that *unmakes* what it touches turned onto the camp when a mule panicked. Fleeing on a horse with **Reza**, Shake's Evasion failed and the edge caught them (3d6=6 → **0 HP, saved only by Vital Furnace**). The horror tore a furrow and passed on; the road west is now grimly **clear**. **Dead: captain Hild and a few others**; the caravan broken and **leaderless**; Reza alive and hurt; Shake woke at 1 HP. In the aftermath he **healed himself and the wounded** (Healing Touch), **salvaged enough to limp on**, burned the dead (Hild among them), and — the survivors cohering to the one man still standing — now **leads ~11 caravaners west toward Mauressac**, the road clear, a brother's rumor ahead. The watchful **man in the good coat** lived, and is *calculating*. At the city's edge Shake **healed, named, and released the band**, read the coat-man as an opaque agent who priced him on the road, and walked the last miles into Mauressac's country with only **Reza**. *(Prior — Scene 1: saved then surrendered the king's-man Wystan to Doyle's marshals; made an enemy of his sister Aldith; heard "the seal isn't in the reliquary; the boy is true-blooded.")*
- **Open canon answers (made true in play):** The **Landing** — the Arrival's shanty in Monze, by the rift below Aurholt — is policed by **Sgt. Doyle's marshals**, who keep the camp fed by serving the **Lord Protector's** deal (handing back what wanders in). **Wystan** (a Dragon-Throne man) claims *the boy-king is true-blooded and the royal seal is not in the reliquary* — and is now in Almeric's hands. **Aldith** (his sister) blames Shake. *(Open signs: how King Urcrin died; why the rift speaks English / opened on a Working of Old Vael; where the seal truly is.)*

## Party & PCs
- **Abhishek "Shake" Rao** — Adventurer (Partial Warrior / Partial Healer) L1 · Physician · Int **18** (+2) · **HP 6/6 · AC 14 · Strain 0/11 · Effort 3/3** · Heal-1, Stab-1, Craft-0 · Foci: One Point Strike Style (attacks use Int +2), Artisan · Arts: Healing Touch, Vital Furnace · longsword **d20+4 / 1d8+3 / Shock 2-AC13** · *survived a drop to 0 (scene 5); shoulder clip (scene 15) mended (scene 17).* **Full sheet: `character-sheet.md`.**
- **Gear:** long sword · buff coat + buckler · physician's kit · backpack · throwing blades ×5 · NY relics (penlight, dead phone, badge) · **~56 sp** (25 recovered + Garin's up-front & half-on-report; a final quarter due at the dusk-drop).
- **In Mauressac, with colors now:** **ward-leech of Warden Wynne's river-ward** — a wage, standing, a warden at his back vs Gault, and the run of the ward-house's **open rolls**. New base: a **two-room let above a cooper's** in the river-ward (moving Reza here off Maela's eaves). Cover upgraded from "lower-Amundi healer" to a sworn ward-man — though **Wynne privately knows he's rift-folk.** The **man in the good coat** is still loose; **Maela** (old landlady, hides something) is owed a goodbye-or-reckoning. *(Gault & Osric's faction have Shake's face.)*
- **Companion — Reza:** 14, Bangladeshi-American, from the **Lower East Side** (Baruch Houses); 9th-grade science kid, now Shake's half-trained field-medic apprentice. Mother died at the Landing (first month); **father's fate unknown** (back on Earth? another shard? — she won't speak of it). Fiercely loyal; dragged Shake out of the unmaking. **Location:** Mauressac (RG-04).

## Effort & Strain  (per caster / PC)
- **Shake:** Effort 3/3 (none committed) · System Strain 0/11. *(Scene-Effort returns at scene end; day-Effort at dawn.)*

## Faction board  (summary; full board: `factions.md`)
- **The Dragon Throne — FALLEN** (Phillipe **dead**, scene 18) — F4 C2 W2 · HP 9/9 · a **leaderless dragon-blood remnant** (*Regroup* 0/8, defensive); may rally to a new dragon-claim or scatter. *The three-way succession is now a brawl over an empty chair.*
- **The Lord Protector's Party** (Almeric) — F3 C5 W2 · HP 15/15 · *Make the Regency Permanent* **4/8** *(moved scene 16: Move Asset; bg — Almeric secures a marriage-alliance: hunted but not finished, shoring up the regency)* · holds Aurholt & the boy.
- **The Mauressac Claim** (Marie) — F2 C3 W5 · HP 15/15 · *Press the Claim* **3/8** *(moved scene 11: Move Asset — consolidating; bg actor: criminals biting guild wealth)* · Shinbu-Anak backed.
- **The Worm-Cult of Vael** — F4 C1 W1 · HP 8/8 · *Wake the Crowned Worm* **5/8** *(moved scenes 1, 5, 7 & 15: bg — locals beg the cult's aid as the west burns; **PAST HALF**)* · serves the dragon Vörniss.
- **The Arrival** (the New Yorkers) — F3 C2 W4 · HP 12/12 · *Find a Foothold (or the Way Home)* **2/8** *(moved scene 14: Move Asset — consolidating; bg: rift-folk being suppressed by local authorities — shipped/herded amid the crisis)* · split; the PC is one of them.
- **Mishar's Hand** (Despot Amiya) — F3 C4 W3 · HP 14/14 · *Vassalize Auragne* **1/8** *(moved scene 17: Move Asset; bg — fighting a rival local power base)* · buys the counts. *Run `faction_turn.py` at the world-tick cadence.*

## World ledger — clocks & threats  (see `world-model.md`)
- **The Succession War — now OPEN** (erupted scene 18) **~7/12** — the cold three-way tension broke into **open battle**; **Boy-King Phillipe is dead** and the Dragon Throne fallen. Two claimants left (Almeric's regency · Marie's Claim) plus the vulture (Mishar), all over an **empty chair.** Touches all of Auragne.
- **The Reconquest of Old Vael — LIT** (scene 14 Turning Point) 0/10 — *no longer stalled:* with **Almeric hunted** and the regency cracking, the western marches are aflame and a claimant may move on the old empire's corpse — touches the western waste / Vörniss' Crown (R-06). *(Couples to Vörniss Wakes 3/8 — disturbance in the west.)*
- **Almeric hunted; the realm cracked** (scene 14 Turning Point) — the Lord Protector's grip was cut from under him in the night (the lost lieutenant → an open hunt); the capital's in uproar and every power lunges (Marie's Claim pounces in the west). Distant from Shake, but it's why Mauressac convulsed this dawn. *(Open: who hunts Almeric, and whether the boy-king/seal secret now surfaces.)*
- **Vörniss Wakes** **5/8** — *(PAST HALF; synced to the Worm-Cult project. The omen has now FIRED — scene 15's raving **sole survivor** of the Worm eating a whole company in the west; the cult exploits the realm-crisis, locals begging its sorcerers' aid)* advances by the Worm-Cult & disturbances at R-06 — **at 8/8 the dragon acts** (telegraph well underway → then fire).
- **Mishar's Vassalization** 0/8 — advances by Mishar's Hand — touches the bought counts (Deidre, Qasim; **Gruith's banner fell** in the western lurch, scene 15).
- **The Unmaking-thing** (scene 5) — a Destruction-driven horror that *unmakes* what it touches; tore through the caravan camp (killed Hild + several) and continued on its line, **out of the area** — the western road is now clear, but the beast still roams the western country toward Mauressac.
- **Maela's secret** (scene 6, GM sign) — Shake's Mauressac landlady is no mere landlady: a hidden identity and **veiled backers**, presently tangled with one of her patrons' "clients" who has **gone rogue**. Shake only reads her as "off." *(Surfaces when earned.)*
- **The Factors' "second book" → the river road** (scenes 9–14) — the secret ledger of where gathered rift-folk are **sent/sold**; holds **Akhil's destination**. Garin **barred the door** on his own part (Fate **Exc-No**, scene 10); Alys was caught reading it & **taken** (scene 12). **Scene 14 gave the shape of the answer:** the Factors ship the taken **out of Mauressac by water** — the **green-eye barge**, downriver toward the lowlands/sea-reach — *this* is where the unbought "don't come back" to. **Alys was shipped on it** (Shake saw her aboard, could not free her; the route is now his **live lead on Akhil**). *(Open: the barge's actual destination; who buys them there; Garin's & Corvin's parts; whether the kingdom-crisis ends or accelerates the trade.)* **Scene 16:** harbor-physician **Edme** names the destination — **Saltmere**, the marsh-mouth where river meets sea; sea-come buyers take delivery in unnamed coin ("up from the water"). An **unknown hand** slipped Edme a sealed manifest-scrap (barge-name + tide) for Shake. **Scene 16 (player choice): Shake DECLINED the river road** — handed the manifest back, let the barge go. **Akhil's only concrete lead is abandoned; the brother-trail goes cold by Shake's own call.** (Akhil stays a someday-goal — no active lead; **Saltmere** & the unknown benefactor remain on the shelf if he ever turns back.)
- **Mauressac tightens** (scene 11, faction sign) — the Claim is **consolidating / moving assets** while **criminals assault the guilds' wealth**; the quarter bristles with hired knives and night-moved stock (this lockdown is what got Alys caught).
- **The Osric takedown** (scene 13 · now a Thread) — the grave-work blew open: the memorial-ground's revered 'ghost-hound' was an **Outsider-relict** (slain by Shake; it had enthralled the two diggers). The diggers (**Coll & Edrick**) were **Warden Aldous's** catspaws, sent to prove **Warden Osric murdered Captain Hroth & looted his grave** to fund his rise — which Shake **confirmed off the skull** (killed from behind). **Aldhelm & the brotherhood have turned on Osric.** Plan: ruin him *lawfully* via honest **Warden Wynne** (witnesses + skull + hoard + Osric's incitement to murder the diggers). **Live threats:** **Under-Warden Gault** (Osric's enforcer) in the dawn gap; **Warden Aldous** (the wolf) may try to make the kill *his own* and taint the clean case. *(GM signs: Aldous uses everyone & hungers to look deserving; Wynne misses nothing & will clock Shake as rift-folk; Osric's patrons may fight the trial.)*
- **Osric warned; Shake marked** (scene 15) — Gault's dawn ambush failed and Shake faced him down at Wynne's door (bones-and-truth leverage; Gault backed off). But **Osric now knows the quiet is over** — expect him to flee with his wealth, fight the trial through patrons, or strike — and **Gault has Shake's face now** (*"clever's a thing a man can find again"*). The accusation is loose as **street rumor** in the river-ward (helps the case; fully tips Osric). The clean lawful ruin must reach **Wynne FAST.** **Scene 16: it did** — Wynne took the case + the doorstep-attack and moved hard (warrant + watch out for Osric; Gault to hang if he resists). The ruin is now **Wynne's machine, not Shake's** — open whether it catches Osric before he flees.
- **The west-gate memorial-ground** (scene 13, new canon) — Mauressac's martial dead, buried rich with war-plunder; **Captain Hroth's** desecrated tomb (now opened) and a thirty-year murder at its heart. The 'ghost-hound' legend was a lie over a buried Outsider-thing — *the locals believed something very false of it.*
- **Big Wat & the Serjeant** (declined scene 11, open hook) — a dock-thug's hidden garrison-captain friend, hiding from a guild protection-squeeze, who'd pay with an old **"humming, blue-lit" thing** (fixed-weapon components, true worth unknown). Shake passed on it; Wat may come back.
- **The Factors' Guild = the rift-folk apparatus** (scene 7) — **Master Corvin's** Factors' Guild sorts and sells the gathered rift-folk (some to Countess Marie, some to whoever pays). Garin's ward **Alys** counts them into ledgers from the inside — so finding Alys IS Shake's road to Akhil. *(GM signs: who Alys was really taken for, and why; Corvin's tie to the Mauressac Claim / Marie's "gathering.")*

## Domains / holdings
- **<Holding>** — income vs upkeep net per interval; unrest …

## World-tick clocks
- **Supplies:** days remaining … · **Wandering-encounter:** per watch/turn while exploring · **Days at sea:** …

## Committed-canon frontier  (worldgen)
- **Detailed now:** the **Kingdom of Auragne** — 7 shires (Altdobern, Verzeille, Hermsdorf, Mauressac, Briach, Shakal, Monze/**Aurholt**), 6 ruins, and Old Vael's edge — all in `campaign/places.json`; canon in `bridge/setting-canon.md`.
- **Generate on demand:** **Saltmere** (the downriver marsh-mouth river-port where the green-eye barges take the taken to sea-come buyers — generate when Shake travels the river road); the river route itself; then the rest of Amund (Qasir, Mishar, Pelegrin, Vois, Ostmark, Fidach, Nabardura), the continent of Agathon, and beyond — call `scripts/worldgen.py` when play reaches it, then fold the result into canon and the Lists.

*Overwrite each scene end. Run the engine SELF-AUDIT before sending a scene: did dice decide every uncertain outcome, were stakes pre-committed, did the world act to win, did a clock/List/Chaos move?*

<!-- LISTS:BEGIN — generated by `state.py render`; edit threads.json/characters.json, not here -->
## Threads List — generated snapshot of threads.json (do not hand-edit)
1. The Three-Way Succession for the Dragon Throne  _(weight 3)_
2. The Arrival — the City That Fell Through  _(weight 3)_
3. Vörniss Stirs Beneath Old Vael  _(weight 2)_
4. Despot Amiya Buys the Counts  _(weight 2)_
5. The Split Diaspora at the Rift  _(weight 3)_
6. The Worm-Cult Rises in the West
7. The Search for Akhil (his brother)  _(weight 3)_
8. The Secret Wystan Left — the seal & the true boy-king  _(weight 2)_
9. Bring down Warden Osric — Hroth's murderer (with Wynne, vs Gault)  _(weight 2)_
10. The Reconquest of Old Vael — the marches lit (no longer stalled)  _(weight 2)_
_Σ weighted slots = 23_

## Characters List — generated snapshot of characters.json (do not hand-edit)
1. Lord Protector Almeric  _(weight 3)_
2. Countess Marie  _(weight 2)_
3. Countess Deidre of Verzeille
4. Count Qasim of Shakal
5. Vörniss the Crowned Worm
6. Despot Amiya of Mishar
7. Reza (Shake's apprentice)
8. The man in the good coat (caravan survivor, watchful)
9. Maela (Mauressac landlady — secret backers)
10. Tanya (Bronx FDNY medic — leader of the Factors' rift-folk stock)
11. Alys (the Factors' coerced ledger-girl; Garin's ward)
12. Under-Factor Reynaud (holds Alys & the second book)  _(weight 2)_
13. Warden Osric (Low Quarter — risen, buries his past)  _(weight 2)_
14. Aldhelm (Keeper of the veterans' brotherhood; Shake's ally)
15. Warden Wynne (honest river-warden; the lawful hand)  _(weight 2)_
16. Edme (Mauressac harbor-physician; keeps the river-poor's tallies; river-road ally)
_Σ weighted slots = 22_

<!-- LISTS:END -->
