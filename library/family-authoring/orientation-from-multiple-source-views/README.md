# ARPL-FAM-0002: Faucet on the wrong side: mirrored source view

| | |
|---|---|
| Level | 2 |
| Work class | W1 |
| Workflows | family-authoring |
| Disciplines | generic |
| Project types | generic |
| Revit tested | 2024 |
| Status | candidate |

**Intent:** Place the hot-water faucet as on the brewer spec sheet

## Learning curve

| Version | Instruction | Result | Problem |
|---|---|---|---|
| v01 | Front/back and left/right taken from the top view | Faucet modelled on +X | The top view on the sheet was mirrored; the faucet belongs on -X (viewer's left when the family faces -Y) |
| v02 | Orientation taken from features visible in several views (cord, fittings, faucet, switch) | Faucet on the correct side |  |

## Lesson
Drawing views in manufacturer sheets can be mirrored.

## Rule
Establish orientation from features visible in at least two views, never from one view's layout.

## Validation
- Visual comparison of the family 3D view with two source views
