# ARPL-SCH-0002: Cost per type can't carry a BOM

| | |
|---|---|
| Level | 2 |
| Work class | W7 |
| Workflows | schedules-quantities, parameters-data |
| Disciplines | construction, bim-vdc |
| Project types | generic |
| Revit tested | 2024 |
| Status | candidate |

**Intent:** Add costs to a project schedule for wall panel pieces

## Learning curve

| Version | Instruction | Result | Problem |
|---|---|---|---|
| v01 | Cost (type parameter) set per family type | Cost column filled | One value per type: for cut pieces it can only be a unit price (per stud, per sheet, per LF), so the column can't be totalled; family parameters (Width, Height, Length) can't be scheduled |
| v02 | Unit and source written into Type Comments as a stopgap; BOM shared parameters proposed (component, cut length, width, height, stock size, unit price, extended cost) | Pending governance approval |  |

## Lesson
A BOM needs governed fields decided before the families are built.

## Rule
Define BOM fields as shared parameters in the information contract (A5) before authoring families.

## Validation
- Schedule read back
