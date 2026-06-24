# Bridge manifest — Worlds Without Number

This companion supplies the **Worlds Without Number** ruleset (2d6 skills, d20 tactical combat with Shock and mortal wounds, saving throws, Effort/Arts magic, foci & classes), the **Latter Earth** setting, the WWN-native **Faction Turn** and domain subsystems, an on-demand **worldgen** subroutine, and a full **generator** suite. The mythic-gm engine supplies the scene loop, oracle, honest dice, and discipline. Hooks not listed here fall through to the engine default.

```json
{
  "companion": "wwn",
  "engine": "mythic-gm>=2",
  "overrides": [
    "resolve",
    "generate:character",
    "generate:element",
    "meaning",
    "chaos",
    "themes",
    "world-tick",
    "seeds"
  ],
  "files": {
    "system_profile": "system-profile.md",
    "interpretation": "interpretation.md",
    "chaos": "chaos-tendency.md",
    "themes": "theme-weights.md",
    "generators": "generators/registry.md",
    "subsystems": "subsystems.md",
    "seeds": "seeds.md",
    "canon": "setting-canon.md",
    "world_model": "world-model.md",
    "adventures": "adventures/"
  },
  "generators_map": {
    "character": { "mode": "conjunction", "table": "generators/npc_role.json",
                   "note": "Flesh every NEW NPC as a Latter Earth native — tie to a setting-canon faction and the current region, and act per interpretation.md (competent, self-interested). For a major/recurring NPC, also roll character_tags." }
  }
}
```

**Notes for the engine/agent**
- Resolution precedence (the oracle ladder): WWN rule → WWN generator → engine Fate Question. See `system-profile.md`.
- All WWN randomness routes through `<mythic-gm>/scripts/dice.py` (directly, or via the WWN `scripts/*` that wrap it).
- `world-tick` fires WWN subsystems (Faction Turn, project / Effort / strain / supply clocks) via `<mythic-gm>/scripts/tick.py <bridge> <scene#>`; see `subsystems.md`.
- `setting-canon.md` is the **live** committed world; it starts from Latter Earth and is grown at the frontier by `scripts/worldgen.py`.
