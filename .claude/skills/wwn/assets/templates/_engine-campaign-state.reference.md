# (reference pointer)

This was a convenience copy of the **engine's** base campaign-state template. To avoid drifting from
the engine (which is versioned independently — e.g. the List-term update and the JSON Lists),
read the live version from the installed engine instead:

- `<mythic-gm>/assets/templates/campaign-state.md` — the engine's base state file.

The WWN campaign uses **`wwn-campaign-state.md`** in this folder, which *extends* that engine state with
WWN fields (party/Effort/Strain, faction board, world ledger, frontier). Under the current engine the
Threads & Characters Lists live canonically in `threads.json` / `characters.json` (managed by
`state.py` / `lists.py`); the Markdown is a human-readable mirror.
