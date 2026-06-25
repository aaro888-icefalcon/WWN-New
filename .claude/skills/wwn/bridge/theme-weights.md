# Theme Weights — Latter Earth   (hook: themes; FIXED for the whole campaign)

## Operative
EVERY adventure uses this **fixed Theme priority order** — Action ▸ Social ▸ Tension ▸ Personal ▸
Mystery — via `adventure_crafter.py themes --style wwn --campaign <dir>` (the `wwn` style is the default;
running `themes` with no `--style` yields the same order). This is a deterministic order, not a weighted
draw: Action leads (the lethal fights and decisive moves), then Social (faction and court play), Tension
(attrition and grit), Personal (kept present but not dominant in a disposable-adventurer world), and
Mystery last (the ancient ruins and Deeps).

# Deterministic 1st..5th Theme priority for every adventure (style 'wwn').
order: [Action, Social, Tension, Personal, Mystery]
first_priority: Action
# The order is fixed in adventure_crafter's fixed_orders['wwn']; the weights below are only a
# fallback if a non-fixed style is ever used.
Action: 5
Social: 4
Tension: 3
Personal: 2
Mystery: 1
