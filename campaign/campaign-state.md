# Campaign State — WWN   (extends the engine's campaign-state.md)

> Use this when: this is the campaign's **source of truth** — overwrite it at each scene end (engine bookkeeping). It EXTENDS mythic-gm's `campaign-state.md` with WWN fields. The engine reads the Engine block; WWN reads the rest. See `bridge/world-model.md` for how the ledger feeds the engine's Lists.

## Engine block (mythic-gm)
*Lists are stored canonically as `threads.json` / `characters.json` (engine `state.py thread|char` / `lists.py`); the lines below mirror them for reading. `state.py init <campaign>` scaffolds the JSON; pass `--campaign <dir>` to the engine's List / Fate / Turning-Point scripts.*

- **Chaos Factor:** 7  *(floor 6; +1 scene 12 — the dusk drop went against the PC: Alys caught & taken (Fate Exc-No), his line to Akhil cut, events outrunning him)*
- **Adventure mode:** Adventure Crafter  *(Theme priority: Action ▸ Social ▸ Tension ▸ Personal ▸ Mystery)*
- **Threads & Characters Lists:** canonical in `threads.json` / `characters.json` — view with `state.py thread show` / `char show`. **Do not copy them here.**
- **Adventure Features:** …  *(if a prepared/ingested adventure)*
- **★ SAVE POINT (resume here):** **Scene 12 — the drop that wasn't.** Before dusk Shake **signed on with the veterans' brotherhood** (the memorial-ground diggers job) under old serjeant **Aldhelm** — but the purse came from **Warden Osric**, the Low Quarter's risen, evasive official (a man who buries those who know his past; *Ambition: erase all who know his origins*). Then to the **dusk drop** at the cistern court behind the counting-house. **Alys never came.** Fate **Exceptional No** (98): she was **caught thieving the second book that afternoon** — the guild in theft-paranoid lockdown all week (the Claim consolidating, criminals biting its wealth) — and **taken inside**. Shake read it from the signs (overturned draw-bucket, dragged heels, her **cracked wax tally-slate**) and a frightened scullery boy: *"They took the counting-girl in… thieving out the book… they're funny about the book this week."* *(GM-side, UNEARNED by the PC: Alys is **alive, held, being squeezed** — the Factors will want who put her up to it → points at Garin & the outside healer.)* **Akhil's trail is cut at the front door; the girl and the book are both behind under-factor Reynaud's bolted, lamplit door.** Shake's still **unmarked** (scene 11 Fate No) — but moving on the Factors now risks that. HP 6/6 · Effort 3/3 · purse ~56 sp · Chaos 7. **Open beats:** *learn if Alys lives / where she's held · go back to Garin (whose ward was just taken — and who lied to his face) · move on the Factors (risks marking himself) · or cut losses to the diggers job & bare survival.*
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
- **The Lord Protector's Party** (Almeric) — F3 C5 W2 · HP 15/15 · *Make the Regency Permanent* **2/8** *(moved scene 12: Move Asset — consolidating in Aurholt; bg: a superior repaid him a favor)* · holds Aurholt & the boy.
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
- **The diggers job** (signed scene 12) — Shake has **taken the brotherhood's grave-work**: clear the night-diggers from the veterans' **memorial-ground past the west gate**. Front face (serjeant **Aldhelm**): honor the war-dead, stop the grave-robbers. True engine (patron **Warden Osric**, GM sign): Osric uses the bled-white veterans as **brute muscle** and means to **bury whoever can name his past** — the "diggers" may be after exactly that. Night-work, queued. *(Not yet a List thread; promote when he starts it.)*
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
7. Marie and Gruith's Bloc Against the Crown
8. The Worm-Cult Rises in the West
9. The Search for Akhil (his brother)  _(weight 2)_
10. The Secret Wystan Left — the seal & the true boy-king  _(weight 2)_
11. The Unaccounted New Yorkers (Jason, Jessica & the lost)
12. Find Garin's ward Alys (taken by Master Corvin, Factors' Guild)  _(weight 3)_
_Σ weighted slots = 25_

## Characters List — generated snapshot of characters.json (do not hand-edit)
1. Boy-King Phillipe  _(weight 3)_
2. Lord Protector Almeric  _(weight 3)_
3. Countess Marie  _(weight 2)_
4. Count Heinrich of Altdobern
5. Countess Deidre of Verzeille
6. Count Carloman of Hermsdorf
7. Count Gruith of Briach
8. Count Qasim of Shakal
9. Count Chilperic of Monze
10. Vörniss the Crowned Worm
11. Despot Amiya of Mishar
12. Reza (Shake's apprentice)
13. The man in the good coat (caravan survivor, watchful)
14. Maela (Mauressac landlady — secret backers)
15. Father Garin (Bleeding God priest, employer)
16. Tanya (Bronx FDNY medic — leader of the Factors' rift-folk stock)
17. Alys (the Factors' coerced ledger-girl; Garin's ward)
18. Under-Factor Reynaud (holds Alys & the second book)  _(weight 2)_
19. Warden Osric (Low Quarter — risen, buries his past)
_Σ weighted slots = 25_

<!-- LISTS:END -->
