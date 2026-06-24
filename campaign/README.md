# campaign/ — live play state

This folder holds the **active campaign's** state. It is empty until **Session Zero** populates it.

When you start a new game (see `../CLAUDE.md` → *Start a NEW game*), Session Zero writes here:

- `campaign-state.md` — the source of truth (party, Effort, System Strain, faction board, world ledger,
  frontier, Chaos Factor). Its presence is what tells the GM a game is in progress.
- `CLAUDE.md` — the always-on per-campaign directives (copied from
  `../wwn/assets/templates/campaign-CLAUDE.md`).
- `character-sheet.md` — the PC.
- `threads.json` / `characters.json` / `adventure.json` — the engine's Lists and Theme order (the
  source of truth; `state.py` reads and rolls them). Scaffold with
  `python3 ../mythic-gm/scripts/state.py init campaign` (run from the repo root:
  `python3 mythic-gm/scripts/state.py init campaign`).
- `seeds.md` — the 30–40 card seed deck, refreshed each bookkeeping.

To keep more than one campaign, give each its own subfolder (`campaign/<name>/`) and point the
`--campaign` flag at it.
