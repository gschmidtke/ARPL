# ARPL-PLH-0002 rev 1: Door swing reported correct without a test

_Generated from this pack's files by tools/build_catalogs.py. Edit manifest.json, intent.md, vNN/ or final/rule.json instead._

| | |
|---|---|
| Level | 2 |
| Work class | W4 |
| Status | candidate |
| Use when | placing, swapping or flipping doors; reporting door swing or hand |
| Not for | - |
| Workflows | placement-hosting, validation-qaqc, spatial-planning |
| Disciplines | architecture, interiors |
| Project types | generic |
| Revit tested | 2024 |
| API | FamilyInstance.FacingOrientation, FamilyInstance.HandOrientation, flipFacing |
| Failure patterns | FP02 |
| Contributors | Gottfried Schmidtke with Claude |

**Intent:** Check that doors swing into the right rooms

## Learning curve

| Version | Instruction | Result | Problem | Found by |
|---|---|---|---|---|
| v01 | Swing judged from FacingOrientation | Reported 'correct side' | It was wrong | user review |
| v02 | Take the swing arc midpoint in the plan view and test which room contains it | Swings verified |  |  |

## Lesson
FacingOrientation doesn't reliably predict the swing.

## Rule
Verify door swing geometrically and re-check after every door swap or move.

## Validation
- Room.IsPointInRoom on the swing-arc midpoint
