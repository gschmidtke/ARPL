# ARPL-VIEW-0002: Section looking the wrong way

| | |
|---|---|
| Level | 1 |
| Work class | W6 |
| Workflows | views-graphics, documentation |
| Disciplines | generic |
| Project types | generic |
| Revit tested | 2024 |
| Status | candidate |

**Intent:** Section looking north through the house

## Learning curve

| Version | Instruction | Result | Problem |
|---|---|---|---|
| v01 | ViewSection.CreateSection with a box whose BasisZ was assumed to be the view direction towards the viewer | Section reversed | The section looks along +BasisZ of the box (ViewDirection = -BasisZ) |
| v02 | BasisZ = direction to look; Min.Z = 0, Max.Z = depth; check ViewDirection after creating | Correct |  |

## Lesson
View direction conventions must be checked, not assumed.

## Rule
After creating any view, compare its ViewDirection with the intended direction.

## Validation
- ViewDirection read back
