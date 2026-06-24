# WWN — Worlds Without Number, solo on the mythic-gm engine

A self-contained repository for running a **challenging, solo / GM-less campaign** in **Worlds Without
Number** (Kevin Crawford / Sine Nomine) and the **Latter Earth** setting, with **Claude Code** as the
Game Master. Claude rolls every die honestly through scripts, asks the oracle, and never softens the
outcome.

## Layout

Both halves are installed as **Claude Code skills** under `.claude/skills/`, so they auto-activate when
you ask to play:

- **`.claude/skills/mythic-gm/`** — the engine: Mythic GME 2e + The Adventure Crafter (scene loop,
  oracle, honest dice, Random Events, Turning Points, the no-softening discipline). Shared and
  content-free.
- **`.claude/skills/wwn/`** — the companion: the WWN ruleset, the Latter Earth setting, the Faction Turn,
  on-demand worldgen, and the full generator suite. Fills the engine's hooks via
  `.claude/skills/wwn/bridge/`.
- **`campaign/`** — live play state (created by Session Zero; empty until then).
- **`CLAUDE.md`** — the always-on GM orientation Claude Code loads automatically.

The engine and companion are **synced**: every overridden bridge hook carries a `## Operative` digest,
those imperatives are inlined into `.claude/skills/wwn/SKILL.md` (and surfaced by `bridge.py brief`), and
the bridge validates clean — so the WWN rules actually fire in play instead of silently losing to a Fate
Question.

## Quick start

Open this repo in Claude Code and say **"run a Worlds Without Number game."** The `wwn` skill activates
(loading the `mythic-gm` engine), and Session Zero defines the world (default: Latter Earth), rolls up a
character, and opens the first scene. To continue later, just say **"continue my campaign."**

Verify the setup at any time (from the repo root):

```
python3 .claude/skills/mythic-gm/scripts/build_data.py                              # engine self-check → VERIFICATION PASSED ✓
python3 .claude/skills/mythic-gm/scripts/bridge.py validate .claude/skills/wwn/bridge   # → Bridge valid ✓
python3 .claude/skills/mythic-gm/scripts/bridge.py brief    .claude/skills/wwn/bridge   # the operative rules Claude holds in play
```

See **`CLAUDE.md`** for the full command reference, the oracle ladder, and the discipline.

---

*Game content is reproduced from Worlds Without Number / The Atlas of the Latter Earth and Mythic 2e /
The Adventure Crafter for personal play; not for redistribution.*
