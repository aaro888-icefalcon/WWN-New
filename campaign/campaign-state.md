# Campaign State — WWN   (extends the engine's campaign-state.md)

> Use this when: this is the campaign's **source of truth** — overwrite it at each scene end (engine bookkeeping). It EXTENDS mythic-gm's `campaign-state.md` with WWN fields. The engine reads the Engine block; WWN reads the rest. See `bridge/world-model.md` for how the ledger feeds the engine's Lists.

## Engine block (mythic-gm)
*Lists are stored canonically as `threads.json` / `characters.json` (engine `state.py thread|char` / `lists.py`); the lines below mirror them for reading. `state.py init <campaign>` scaffolds the JSON; pass `--campaign <dir>` to the engine's List / Fate / Turning-Point scripts.*

- **Chaos Factor:** 6  *(floor 6; −1 scene 13 — Shake seized a chaotic graveyard fight, slew the relict, freed the thralls, unearthed the truth & took command of the plan; back to floor)*
- **Adventure mode:** Adventure Crafter  *(Theme priority: Action ▸ Social ▸ Tension ▸ Personal ▸ Mystery)*
- **Threads & Characters Lists:** canonical in `threads.json` / `characters.json` — view with `state.py thread show` / `char show`. **Do not copy them here.**
- **Adventure Features:** …  *(if a prepared/ingested adventure)*
- **★ SAVE POINT (resume here):** **Scene 13 — the memorial-ground, and the truth under it.** Shake **walked away** from the Alys/Akhil road (too thin, too costly) and took the brotherhood's grave-work. At the veterans' **memorial-ground** by night (with **Aldhelm** + 3 bled-white veterans), the 'ghost-hound' the old men revered was an **Outsider-relict** (Domination drive, disguised harmless) that had **enthralled the two diggers**. Shake's warning to the band **failed** (snake-eyes); it dominated **Aldhelm** mid-fight — but Shake **killed it on his blade** (16 vs AC15, 8 dmg), which **freed Aldhelm & both diggers**. The diggers — **Coll & Edrick**, local Low-Quarter men — were sent by **Warden Aldous** (Osric's rival grain-warden) to dig up proof that **Warden Osric** built his rise on a crime: Osric **murdered Captain Hroth** (a beloved war-hero) and looted his grave-hoard. Shake **read Hroth's skull** (Heal success): killed from behind, *not* in battle — **conclusive.** **Aldhelm — Hroth's own old soldier — turned utterly against Osric** (Fate Exc-Yes). **The plan (Shake's): not a clean death — ruin.** Carry the case (skull + hoard + living witnesses + Shake's forensic word + Osric's incitement to murder the diggers) to **Warden Wynne** — the one honest, unbuyable warden (Fate Exc-Yes; up from the *same* gutter as Osric, but clean). By-the-book → Osric tried, stripped, everything turned to ash; the brotherhood stays lawful. **The split (dawn near):** Shake + Aldhelm + Coll → **Wynne** (carrying the skull); Beorn + Hraf → **Aldous** (word, not proof — gauge the wolf); Ceol (healed) + Edrick → a safe hole (insurance witness). **Gap-danger:** Osric expects a first-light report; when none comes he'll send **Under-Warden Gault** (his loyal enforcer) with knives. HP 6/6 · Effort 3/3 · purse ~56 sp · Chaos 6. **Next beat:** *Shake's party reaches Warden Wynne's river-ward at dawn — survive the gap, swear the case, set Osric's ruin in motion.*
- **Last scene recap:** **Scenes 2–5 — the road west, and the catastrophe on it.** Shake left the Landing with **Hild's** westbound salt-caravan (apprentice **Reza** in tow), bound for **Mauressac** on a thin 4-month-old lead that his brother **Akhil** fell west; his first four months are now canon, and road-rumor says Mauressac's countess is *gathering rift-folk* (his hope, unconfirmed). Shake talked captain **Hild** off a first-strike against **5 Blighted** (who were *fleeing* something west and let the caravan pass). The caravan camped to wait the threat out — and **drew it**: a thing that *unmakes* what it touches turned onto the camp when a mule panicked. Fleeing on a horse with **Reza**, Shake's Evasion failed and the edge caught them (3d6=6 → **0 HP, saved only by Vital Furnace**). The horror tore a furrow and passed on; the road west is now grimly **clear**. **Dead: captain Hild and a few others**; the caravan broken and **leaderless**; Reza alive and hurt; Shake woke at 1 HP. In the aftermath he **healed himself and the wounded** (Healing Touch), **salvaged enough to limp on**, burned the dead (Hild among them), and — the survivors cohering to the one man still standing — now **leads ~11 caravaners west toward Mauressac**, the road clear, a brother's rumor ahead. The watchful **man in the good coat** lived, and is *calculating*. At the city's edge Shake **healed, named, and released the band**, read the coat-man as an opaque agent who priced him on the road, and walked the last miles into Mauressac's country with only **Reza**. *(Prior — Scene 1: saved then surrendered the king's-man Wystan to Doyle's marshals; made an enemy of his sister Aldith; heard "the seal isn't in the reliquary; the boy is true-blooded.")*
- **Open canon answers (made true in play):** The **Landing** — the Arrival's shanty in Monze, by the rift below Aurholt — is policed by **Sgt. Doyle's marshals**, who keep the camp fed by serving the **Lord Protector's** deal (handing back what wanders in). **Wystan** (a Dragon-Throne man) claims *the boy-king is true-blooded and the royal seal is not in the reliquary* — and is now in Almeric's hands. **Aldith** (his sister) blames Shake. *(Open signs: how King Urcrin died; why the rift speaks English / opened on a Working of Old Vael; where the seal truly is.)*

## Party & PCs
- **Abhishek "Shake" Rao** — Adventurer (Partial Warrior / Partial Healer) L1 · Physician · Int **18** (+2) · **HP 6/6 · AC 14 · Strain 0/11 · Effort 3/3** · Heal-1, Stab-1, Craft-0 · Foci: One Point Strike Style (attacks use Int +2), Artisan · Arts: Healing Touch, Vital Furnace · longsword **d20+4 / 1d8+3 / Shock 2-AC13** · *survived a drop to 0 in scene 5; healed up.* **Full sheet: `character-sheet.md`.**
- **Gear:** long sword · buff coat + buckler · physician's kit · backpack · throwing blades ×5 · NY relics (penlight, dead phone, badge) · **~56 sp** (25 recovered + Garin's up-front & half-on-report; a final quarter due at the dusk-drop).
- **In Mauressac, gone to ground:** lodged at **Maela's** back-quarter lodging-house (dyers/porters' district), trading healing for a room under the eaves; cover = *a healer from the lower Amundi kingdoms* (his Qasiri-passing looks sell it; his fluent Marcher is the tell). The **man in the good coat** is loose in the city. *(Maela reads as hiding something — a sign.)*
- **Companion — Reza:** 14, Bangladeshi-American, from the **Lower East Side** (Baruch Houses); 9th-grade science kid, now Shake's half-trained field-medic apprentice. Mother died at the Landing (first month); **father's fate unknown** (back on Earth? another shard? — she won't speak of it). Fiercely loyal; dragged Shake out of the unmaking. **Location:** Mauressac (RG-04).

## Effort & Strain  (per caster / PC)
- **Shake:** Effort 3/3 (none committed) · System Strain 0/11. *(Scene-Effort returns at scene end; day-Effort at dawn.)*

## Faction board  (summary; full board: `factions.md`)
- **The Dragon Throne** (Boy-King Phillipe) — F5 C2 W2 · HP 13/13 · *Free and Crown Phillipe* 0/8 · partly backed by the Arrival.
- **The Lord Protector's Party** (Almeric) — F3 C5 W2 · HP 15/15 · *Make the Regency Permanent* **3/8** *(moved scene 13: Move Asset — still consolidating Aurholt; bg sign: a trusted lieutenant of Almeric's has died or betrayed him — his grip wobbles)* · holds Aurholt & the boy.
- **The Mauressac Claim** (Marie) — F2 C3 W5 · HP 15/15 · *Press the Claim* **3/8** *(moved scene 11: Move Asset — consolidating; bg actor: criminals biting guild wealth)* · Shinbu-Anak backed.
- **The Worm-Cult of Vael** — F4 C1 W1 · HP 8/8 · *Wake the Crowned Worm* **3/8** *(moved scenes 1, 5 & 7)* · serves the dragon Vörniss.
- **The Arrival** (the New Yorkers) — F3 C2 W4 · HP 12/12 · *Find a Foothold (or the Way Home)* **1/8** *(moved scene 6)* · split; the PC is one of them.
- **Mishar's Hand** (Despot Amiya) — F3 C4 W3 · HP 14/14 · *Vassalize Auragne* 0/8 · buys the counts. *Run `faction_turn.py` at the world-tick cadence.*

## World ledger — clocks & threats  (see `world-model.md`)
- **The Three-Way Succession War** 0/12 — advances by faction turns & decisive moves — touches all of Auragne.
- **The Stalled Reconquest of Old Vael** 0/10 — advances when a claimant consolidates the crown — touches the western waste / Vörniss' Crown (R-06).
- **Vörniss Wakes** 3/8 — *(Worm-Cult moved scenes 1, 5 & 7; nearing half — surface a faint omen soon)* advances by the Worm-Cult's project & any disturbance at R-06 — if filled, the dragon stirs (telegraph, then fire).
- **Mishar's Vassalization** 0/8 — advances by Mishar's Hand — touches the bought counts (Deidre, Gruith, Qasim).
- **The Unmaking-thing** (scene 5) — a Destruction-driven horror that *unmakes* what it touches; tore through the caravan camp (killed Hild + several) and continued on its line, **out of the area** — the western road is now clear, but the beast still roams the western country toward Mauressac.
- **Maela's secret** (scene 6, GM sign) — Shake's Mauressac landlady is no mere landlady: a hidden identity and **veiled backers**, presently tangled with one of her patrons' "clients" who has **gone rogue**. Shake only reads her as "off." *(Surfaces when earned.)*
- **The Factors' "second book"** (scene 9 · spiked scene 12) — the secret ledger Alys was forced to keep: where the gathered rift-folk are **sent/sold** (Marie · "men who pay more and ask less" · and the **unbought who "don't come back"**). Holds **Akhil's destination**. Garin **barred the door** on his own part (Fate **Exc-No**, scene 10). **Scene 12: Alys was caught reading it for Shake and TAKEN; the book is now locked behind under-factor Reynaud's door, the trail cut.** *(GM-side: she's alive & being squeezed → the Factors will trace her backers toward Garin & Shake. Open: who buys the unbought, and where they're "taken.")*
- **Mauressac tightens** (scene 11, faction sign) — the Claim is **consolidating / moving assets** while **criminals assault the guilds' wealth**; the quarter bristles with hired knives and night-moved stock (this lockdown is what got Alys caught).
- **The Osric takedown** (scene 13 · now a Thread) — the grave-work blew open: the memorial-ground's revered 'ghost-hound' was an **Outsider-relict** (slain by Shake; it had enthralled the two diggers). The diggers (**Coll & Edrick**) were **Warden Aldous's** catspaws, sent to prove **Warden Osric murdered Captain Hroth & looted his grave** to fund his rise — which Shake **confirmed off the skull** (killed from behind). **Aldhelm & the brotherhood have turned on Osric.** Plan: ruin him *lawfully* via honest **Warden Wynne** (witnesses + skull + hoard + Osric's incitement to murder the diggers). **Live threats:** **Under-Warden Gault** (Osric's enforcer) in the dawn gap; **Warden Aldous** (the wolf) may try to make the kill *his own* and taint the clean case. *(GM signs: Aldous uses everyone & hungers to look deserving; Wynne misses nothing & will clock Shake as rift-folk; Osric's patrons may fight the trial.)*
- **The west-gate memorial-ground** (scene 13, new canon) — Mauressac's martial dead, buried rich with war-plunder; **Captain Hroth's** desecrated tomb (now opened) and a thirty-year murder at its heart. The 'ghost-hound' legend was a lie over a buried Outsider-thing — *the locals believed something very false of it.*
- **Big Wat & the Serjeant** (declined scene 11, open hook) — a dock-thug's hidden garrison-captain friend, hiding from a guild protection-squeeze, who'd pay with an old **"humming, blue-lit" thing** (fixed-weapon components, true worth unknown). Shake passed on it; Wat may come back.
- **The Factors' Guild = the rift-folk apparatus** (scene 7) — **Master Corvin's** Factors' Guild sorts and sells the gathered rift-folk (some to Countess Marie, some to whoever pays). Garin's ward **Alys** counts them into ledgers from the inside — so finding Alys IS Shake's road to Akhil. *(GM signs: who Alys was really taken for, and why; Corvin's tie to the Mauressac Claim / Marie's "gathering.")*

## Domains / holdings
- **<Holding>** — income vs upkeep net per interval; unrest …

## World-tick clocks
- **Supplies:** days remaining … · **Wandering-encounter:** per watch/turn while exploring · **Days at sea:** …

## Committed-canon frontier  (worldgen)
- **Detailed now:** the **Kingdom of Auragne** — 7 shires (Altdobern, Verzeille, Hermsdorf, Mauressac, Briach, Shakal, Monze/**Aurholt**), 6 ruins, and Old Vael's edge — all in `campaign/places.json`; canon in `bridge/setting-canon.md`.
- **Generate on demand:** the rest of Amund (Qasir, Mishar, Pelegrin, Vois, Ostmark, Fidach, Nabardura), the continent of Agathon, and beyond — call `scripts/worldgen.py` when play reaches it, then fold the result into canon and the Lists.

*Overwrite each scene end. Run the engine SELF-AUDIT before sending a scene: did dice decide every uncertain outcome, were stakes pre-committed, did the world act to win, did a clock/List/Chaos move?*

<!-- LISTS:BEGIN — generated by `state.py render`; edit threads.json/characters.json, not here -->
## Threads List — generated snapshot of threads.json (do not hand-edit)
1. The Three-Way Succession for the Dragon Throne  _(weight 3)_
2. The Stalled Reconquest of Old Vael  _(weight 2)_
3. The Arrival — the City That Fell Through  _(weight 3)_
4. Vörniss Stirs Beneath Old Vael  _(weight 2)_
5. Despot Amiya Buys the Counts  _(weight 2)_
6. The Split Diaspora at the Rift  _(weight 3)_
7. The Worm-Cult Rises in the West
8. The Search for Akhil (his brother)  _(weight 2)_
9. The Secret Wystan Left — the seal & the true boy-king  _(weight 2)_
10. The Unaccounted New Yorkers (Jason, Jessica & the lost)
11. Find Garin's ward Alys (taken by Master Corvin, Factors' Guild)  _(weight 3)_
12. Bring down Warden Osric — Hroth's murderer (with Wynne, vs Gault)
_Σ weighted slots = 25_

## Characters List — generated snapshot of characters.json (do not hand-edit)
1. Boy-King Phillipe  _(weight 3)_
2. Lord Protector Almeric  _(weight 3)_
3. Countess Marie  _(weight 2)_
4. Countess Deidre of Verzeille
5. Count Gruith of Briach
6. Count Qasim of Shakal
7. Vörniss the Crowned Worm
8. Despot Amiya of Mishar
9. Reza (Shake's apprentice)
10. The man in the good coat (caravan survivor, watchful)
11. Maela (Mauressac landlady — secret backers)
12. Father Garin (Bleeding God priest, employer)
13. Tanya (Bronx FDNY medic — leader of the Factors' rift-folk stock)
14. Alys (the Factors' coerced ledger-girl; Garin's ward)
15. Under-Factor Reynaud (holds Alys & the second book)  _(weight 2)_
16. Warden Osric (Low Quarter — risen, buries his past)  _(weight 2)_
17. Aldhelm (Keeper of the veterans' brotherhood; Shake's ally)
18. Warden Wynne (honest river-warden; the lawful hand)
_Σ weighted slots = 25_

<!-- LISTS:END -->
