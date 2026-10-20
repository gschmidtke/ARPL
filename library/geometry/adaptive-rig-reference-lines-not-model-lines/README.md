# ARPL-GEO-0001: Forms absorb model lines and break hosting

| | |
|---|---|
| Level | 2 |
| Work class | W2 |
| Workflows | geometry, family-authoring |
| Disciplines | generic, themed-entertainment, architecture |
| Project types | generic |
| Revit tested | 2024 |
| Status | candidate |

**Intent:** Adaptive façade: 4 points on an arc, stacked 5 times, lofted into a surface

## Learning curve

| Version | Instruction | Result | Problem |
|---|---|---|---|
| v01 | Polyline of model lines through hosted points, stacked, lofted | Surface created | The loft absorbed and re-hosted the model lines; changing the lower levels' bow broke the stack |
| v02 | Stack rebuilt with reference lines (IsReferenceLine = true) | Bow on the lower levels works; stack follows |  |

## Lesson
Forms take ownership of model lines used as profiles.

## Rule
Use reference lines for every profile in adaptive rigs, and verify hosting by behaviour (move test), not by element ids.

## Validation
- Move test of each driver point
