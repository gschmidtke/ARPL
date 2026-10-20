# ARPL-DOC-0002 rev 1: Project units round framing dimensions

_Generated from this pack's files by tools/build_catalogs.py. Edit manifest.json, intent.md, vNN/ or final/rule.json instead._

| | |
|---|---|
| Level | 1 |
| Work class | W6 |
| Status | candidate |
| Use when | dimensioning fabrication or shop drawings for a trade; dimensions round to project units and hide small values |
| Not for | - |
| Workflows | documentation, views-graphics |
| Disciplines | generic, construction |
| Project types | generic |
| Revit tested | 2024 |
| API | DimensionType, FormatOptions |
| Failure patterns | FP08 |
| Contributors | Gottfried Schmidtke with Claude |

**Intent:** Dimension a 16" o.c. stud layout in a project set to centimetres

## Learning curve

| Version | Instruction | Result | Problem | Found by |
|---|---|---|---|---|
| v01 | Default linear dimension type | 16" spacing shown as '41' | Project units cm with 0 decimals | PDF review |
| v02 | Duplicated dimension type: mm, 1 mm accuracy, alternate units ft-in below | 406 / 1'-4" |  |  |

## Lesson
Project units are set for the architecture, not for fabrication drawings.

## Rule
Shop drawings get their own dimension style matching the trade's units.

## Validation
- PDF review
