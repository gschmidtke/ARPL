# ARPL-GEO-0001 rev 1: Forms absorb model lines and break hosting

_Generated from this pack's files by tools/build_catalogs.py. Edit manifest.json, intent.md, vNN/ or final/rule.json instead._

| | |
|---|---|
| Level | 2 |
| Work class | W2 |
| Status | candidate |
| Use when | building adaptive components or forms from profiles; hosted elements lose their host after form edits |
| Not for | non-adaptive loadable families |
| Workflows | geometry, family-authoring |
| Disciplines | generic, themed-entertainment, architecture |
| Project types | generic |
| Revit tested | 2024 |
| API | AdaptiveComponentFamilyUtils, ReferencePoint, CurveByPoints, FormUtils |
| Failure patterns | FP05 |
| Contributors | Gottfried Schmidtke with Claude |

**Intent:** Adaptive façade: 4 points on an arc, stacked 5 times, lofted into a surface

## Learning curve

| Version | Instruction | Result | Problem | Found by |
|---|---|---|---|---|
| v01 | Polyline of model lines through hosted points, stacked, lofted | Surface created | The loft absorbed and re-hosted the model lines; changing the lower levels' bow broke the stack | move test |
| v02 | Stack rebuilt with reference lines (IsReferenceLine = true) | Bow on the lower levels works; stack follows |  |  |

## Lesson
Forms take ownership of model lines used as profiles.

## Rule
Use reference lines for every profile in adaptive rigs, and verify hosting by behaviour (move test), not by element ids.

## Validation
- Move test of each driver point
