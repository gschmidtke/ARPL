# ARPL-GEO-0002 rev 1: Gable walls without wall attachment

_Generated from this pack's files by tools/build_catalogs.py. Edit manifest.json, intent.md, vNN/ or final/rule.json instead._

| | |
|---|---|
| Level | 2 |
| Work class | W4 |
| Status | candidate |
| Use when | walls under gable or sloped roofs; walls that should follow a roof slope |
| Not for | - |
| Workflows | geometry, model-change |
| Disciplines | architecture |
| Project types | residential |
| Revit tested | 2024 |
| API | Wall, SketchPlane, Wall.Create (profile) |
| Failure patterns | FP05, FP10 |
| Contributors | Gottfried Schmidtke with Claude |

**Intent:** Walls that follow a 25° gable roof

## Learning curve

| Version | Instruction | Result | Problem | Found by |
|---|---|---|---|---|
| v01 | Attach walls to the roof | Wall.AddAttachment doesn't exist in Revit 2024 |  | compile/API check |
| v02 | Rebuild the gable walls as profile walls (Wall.Create with an IList<Curve>) following the roof underside | Gables follow the roof |  |  |

## Lesson
Profile walls replace attachment in the 2024 API, but they no longer follow levels (see W5-001).

## Rule
Use profile walls for gables and register them as dependents of the roof and the levels.

## Validation
- Section view check
