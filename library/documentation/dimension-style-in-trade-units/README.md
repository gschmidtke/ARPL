# ARPL-DOC-0002: Project units round framing dimensions

| | |
|---|---|
| Level | 1 |
| Work class | W6 |
| Workflows | documentation, views-graphics |
| Disciplines | generic, construction |
| Project types | generic |
| Revit tested | 2024 |
| Status | candidate |

**Intent:** Dimension a 16" o.c. stud layout in a project set to centimetres

## Learning curve

| Version | Instruction | Result | Problem |
|---|---|---|---|
| v01 | Default linear dimension type | 16" spacing shown as '41' | Project units cm with 0 decimals |
| v02 | Duplicated dimension type: mm, 1 mm accuracy, alternate units ft-in below | 406 / 1'-4" |  |

## Lesson
Project units are set for the architecture, not for fabrication drawings.

## Rule
Shop drawings get their own dimension style matching the trade's units.

## Validation
- PDF review
