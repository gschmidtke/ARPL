# ARPL-SCH-0002 rev 1: Cost per type can't carry a BOM

_Generated from this pack's files by tools/build_catalogs.py. Edit manifest.json, intent.md, vNN/ or final/rule.json instead._

| | |
|---|---|
| Level | 2 |
| Work class | W7 |
| Status | candidate |
| Use when | preparing a bill of materials (BOM) or cut list from families; adding cost or quantity fields to schedules |
| Not for | - |
| Workflows | schedules-quantities, parameters-data |
| Disciplines | construction, bim-vdc |
| Project types | generic |
| Revit tested | 2024 |
| API | SharedParameterElement, ViewSchedule, ALL_MODEL_COST |
| Failure patterns | FP06 |
| Contributors | Gottfried Schmidtke with Claude |

**Intent:** Add costs to a project schedule for wall panel pieces

## Learning curve

| Version | Instruction | Result | Problem | Found by |
|---|---|---|---|---|
| v01 | Cost (type parameter) set per family type | Cost column filled | One value per type: for cut pieces it can only be a unit price (per stud, per sheet, per LF), so the column can't be totalled; family parameters (Width, Height, Length) can't be scheduled | schedule review |
| v02 | Unit and source written into Type Comments as a stopgap; BOM shared parameters proposed (component, cut length, width, height, stock size, unit price, extended cost) | Pending governance approval |  |  |

## Lesson
A BOM needs governed fields decided before the families are built.

## Rule
Define BOM fields as shared parameters in the information contract (A5) before authoring families.

## Validation
- Schedule read back
