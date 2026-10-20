# ARPL-FAM-0002 rev 1: Faucet on the wrong side: mirrored source view

_Generated from this pack's files by tools/build_catalogs.py. Edit manifest.json, intent.md, vNN/ or final/rule.json instead._

| | |
|---|---|
| Level | 2 |
| Work class | W1 |
| Status | candidate |
| Use when | modelling from orthographic views of a source drawing; deciding left/right or front/back orientation of a product |
| Not for | - |
| Workflows | family-authoring |
| Disciplines | generic |
| Project types | generic |
| Revit tested | 2024 |
| API | Extrusion |
| Failure patterns | FP02, FP09 |
| Contributors | Gottfried Schmidtke with Claude |

**Intent:** Place the hot-water faucet as on the brewer spec sheet

**LOD:** LOD 200

## Learning curve

| Version | Instruction | Result | Problem | Found by |
|---|---|---|---|---|
| v01 | Front/back and left/right taken from the top view | Faucet modelled on +X | The top view on the sheet was mirrored; the faucet belongs on -X (viewer's left when the family faces -Y) | user review |
| v02 | Orientation taken from features visible in several views (cord, fittings, faucet, switch) | Faucet on the correct side |  |  |

## Lesson
Drawing views in manufacturer sheets can be mirrored.

## Rule
Establish orientation from features visible in at least two views, never from one view's layout.

## Validation
- Visual comparison of the family 3D view with two source views
