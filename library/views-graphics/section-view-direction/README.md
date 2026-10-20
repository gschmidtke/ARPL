# ARPL-VIEW-0002 rev 1: Section looking the wrong way

_Generated from this pack's files by tools/build_catalogs.py. Edit manifest.json, intent.md, vNN/ or final/rule.json instead._

| | |
|---|---|
| Level | 1 |
| Work class | W6 |
| Status | candidate |
| Use when | creating sections or elevations by script; a new section or elevation looks the wrong way |
| Not for | - |
| Workflows | views-graphics, documentation |
| Disciplines | generic |
| Project types | generic |
| Revit tested | 2024 |
| API | ViewSection.CreateSection, View.ViewDirection, BoundingBoxXYZ.Transform |
| Failure patterns | FP02 |
| Contributors | Gottfried Schmidtke with Claude |

**Intent:** Section looking north through the house

## Learning curve

| Version | Instruction | Result | Problem | Found by |
|---|---|---|---|---|
| v01 | ViewSection.CreateSection with a box whose BasisZ was assumed to be the view direction towards the viewer | Section reversed | The section looks along +BasisZ of the box (ViewDirection = -BasisZ) | sheet review |
| v02 | BasisZ = direction to look; Min.Z = 0, Max.Z = depth; check ViewDirection after creating | Correct |  |  |

## Lesson
View direction conventions must be checked, not assumed.

## Rule
After creating any view, compare its ViewDirection with the intended direction.

## Validation
- ViewDirection read back
