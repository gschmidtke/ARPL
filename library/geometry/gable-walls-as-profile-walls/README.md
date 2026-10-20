# ARPL-GEO-0002: Gable walls without wall attachment

| | |
|---|---|
| Level | 2 |
| Work class | W4 |
| Workflows | geometry, model-change |
| Disciplines | architecture |
| Project types | residential |
| Revit tested | 2024 |
| Status | candidate |

**Intent:** Walls that follow a 25° gable roof

## Learning curve

| Version | Instruction | Result | Problem |
|---|---|---|---|
| v01 | Attach walls to the roof | Wall.AddAttachment doesn't exist in Revit 2024 |  |
| v02 | Rebuild the gable walls as profile walls (Wall.Create with an IList<Curve>) following the roof underside | Gables follow the roof |  |

## Lesson
Profile walls replace attachment in the 2024 API, but they no longer follow levels (see W5-001).

## Rule
Use profile walls for gables and register them as dependents of the roof and the levels.

## Validation
- Section view check
