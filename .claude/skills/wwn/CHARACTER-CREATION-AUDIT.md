# WWN Skill — Character-Creation Audit & Fix Plan

Findings from a full review of WWN character creation (rulebook vs. the skill's scripts/data), prompted by
trying to build a **Partial Warrior / Partial Healer** Adventurer with the **One Point Strike Style** focus —
a legal PC the tooling currently **cannot** generate. Companion deliverable: the new
`references/rules/character-creation-compendium.md` (all skills, backgrounds, classes, traditions, foci in one file).

Severity: **🔴 blocks legal builds · 🟠 correctness/fidelity · 🟡 cosmetic/docs.**

---

## Findings

### 🔴 A1 — `chargen.py` can't build Healer or Vowed PCs
`chargen.py` `TRADS = ["High Mage", "Necromancer", "Elementalist"]` (line ~665) **omits Healer and Vowed** — the
two *partial-only* traditions, and among the most character-defining. `--class healer` errors out; there is no
path to a magical-healer or martial-mystic PC.

### 🔴 A2 — No way to choose a tradition
Tradition is `random.choice(TRADS)` (line ~671). There is **no `--tradition` flag**, so even the three known
traditions can't be selected deliberately. Building a specific caster is impossible from the script.

### 🔴 A3 — Effort formula is hardcoded and wrong for some traditions
Effort is always `1 + Magic level + better Int/Cha` (lines ~808–821, ~1054). This is **incorrect** for:
- **Healer** → `Heal skill level + better of Int/Cha` (uses **Heal**, and has **no leading +1**).
- **Vowed** → `order's chosen skill level + best attribute mod`.

### 🔴 A4 — Atlas foci exist in neither `foci.json` nor `chargen.py`
`foci.json` has 47 core foci; chargen's `FOCI` dict mirrors them. **None** of the ~46 Atlas foci are present:
- **Maqqatban Knight Styles** (8): Ghost Archer, All Directions Edge, **One Point Strike**, Pyre of Heaven, Catalytic Soul, Wrathful Mountain, Righteous Iron, World Tree Lance.
- **Amundi Godblood Foci** (8): Master Tracker, Night Walker, Danger Sense, Pack Beast, Folie a Deux, Provident Crafter, Wildtongue, Walk Like Wind.
- **Arcane Secret Foci** (5): Atlantean Divination, Iteral Pacting, Nagadi Hemomancy, Old Empire Sigilism, Vothite Mind-Sorcery.
- **Non-Human Origin Foci** (~21): Choeru, Ghoul, !Man, Guer, Accipiter/Harbinger/Aristoi Anak, Hua, Kitsune, Deepfolk, Manu, Nahu, Oni, Pichi, Piren, Still Cities Undead, Sui, Tanuki, Tengu, Usagi, Zakathi.

Result: `lookup.py focus "One Point Strike Style"` and `chargen --focus "One Point Strike Style"` both fail.
These foci also carry **gating** the data must encode (Maqqatban: Warrior/Partial-Warrior only, one per PC;
Godblood: Expert/Partial-Expert; Arcane Secret: Mage/Partial-Mage).

### 🟠 B1 — Healer L1 package not modeled
Even with the tradition added, Healer needs: **Heal** as a bonus skill (level-0, or level-1 if already held —
the stack that makes *Physician + Healer = Heal-1*); auto **Healing Touch** + **one chosen Art**; **casts in
armor**; **no spell slots**.

### 🟠 B2 — Partial casters get no spells/Arts assigned
`_setup_tradition` prints `# TODO verify spell lists` (line ~675). `spells.json` (137 records, incl. all Healer
Arts and High Magic) is available but unused — generated casters get an empty kit.

### 🟠 B3 — Book OCR is scrambled (backgrounds & Atlas)
`02-Character-Creation.md` background tables are munged and offset; the **authoritative** background data lives
in `chargen.py BACKGROUNDS` (verified correct — e.g. **Physician → Heal**, **Scholar → Know**; the OCR offset
made these look swapped). The Atlas foci file is interleaved (Level-2 bullets displaced between styles). The new
compendium reconstructs both; the raw book files remain unreliable for direct quoting.

### 🟡 B4 / C1 / C2 — Smaller items
- **B4:** `--class adventurer` silently resolves to *Partial-Expert/Partial-Warrior* with no notice.
- **C1:** chargen prints **STEP 3 (Class) before STEP 1 (Attributes)** — confusing order.
- **C2:** the lean `character-creation.md` card and `SKILL.md` don't point to the compendium or flag the Atlas/Healer tooling gaps.

---

## Fix plan (phased)

### Phase 1 — Data & docs  ·  low risk, high value
1. **Add all Atlas foci to `foci.json`** with `level_req`, `level_1`/`level_2` text, `page`, and a `gating`
   field (allowed classes + "one per PC" where applicable). Sourced from the compendium (⚠️-flagged L2s noted).
2. **Register Healer & Vowed** as lookup-able traditions (Arts already in `spells.json`).
3. **Wire pointers:** add the compendium to `SKILL.md`'s reference table and a one-line note in
   `character-creation.md`. ✅ *(compendium already written this pass)*

### Phase 2 — `chargen.py`  ·  moderate risk (shared script), behind review
4. **`--tradition <name>`** flag; extend `TRADS` to all five with per-tradition metadata (caster-type,
   Effort basis, armor rule, partial-only flag).
5. **Per-tradition Effort + L1 package** — fix A3/B1: Healer (Heal-based Effort, Heal-skill stack, Healing Touch
   + 1 Art, armor-OK, no spells); Vowed (order-skill Effort, auto three Arts).
6. **Assign starting spells/Arts** from `spells.json` (fix B2).
7. **Recognize Atlas foci with gating** in chargen's `FOCI` (fix A4 for generation); validate class eligibility.
8. **Reorder output** (Attributes → Class → …) and print an `adventurer`→Pe/Pw notice (C1/B4).

### Phase 3 — Optional hardening
9. A `build_foci.py`-style step so `foci.json` regenerates from a single source.
10. Round-trip test: generate a Pm/Pw Healer with One Point Strike Style end-to-end from the CLI.

**Recommendation:** do **Phase 1 now** (pure data/docs — unblocks `lookup.py` and gives every future PC the full
focus list). Hold **Phase 2** for explicit go-ahead since it edits the shared generator. Shake can be finalized
by hand from the compendium in the meantime.
