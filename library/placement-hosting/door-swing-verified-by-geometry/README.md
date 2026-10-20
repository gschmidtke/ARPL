# ARPL-PLH-0002: Door swing reported correct without a test

| | |
|---|---|
| Level | 2 |
| Work class | W4 |
| Workflows | placement-hosting, validation-qaqc, spatial-planning |
| Disciplines | architecture, interiors |
| Project types | generic |
| Revit tested | 2024 |
| Status | candidate |

**Intent:** Check that doors swing into the right rooms

## Learning curve

| Version | Instruction | Result | Problem |
|---|---|---|---|
| v01 | Swing judged from FacingOrientation | Reported 'correct side' | It was wrong |
| v02 | Take the swing arc midpoint in the plan view and test which room contains it | Swings verified |  |

## Lesson
FacingOrientation doesn't reliably predict the swing.

## Rule
Verify door swing geometrically and re-check after every door swap or move.

## Validation
- Room.IsPointInRoom on the swing-arc midpoint
