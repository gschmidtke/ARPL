# ARPL-PLH-0001: Windows placed at sill 0

| | |
|---|---|
| Level | 1 |
| Work class | W4 |
| Workflows | placement-hosting |
| Disciplines | architecture |
| Project types | generic |
| Revit tested | 2024 |
| Status | candidate |

**Intent:** Place windows in walls

## Learning curve

| Version | Instruction | Result | Problem |
|---|---|---|---|
| v01 | NewFamilyInstance with the window family on the wall | Windows at sill height 0 | Hosted placement ignores the family's default sill |
| v02 | Set INSTANCE_SILL_HEIGHT_PARAM explicitly after placement | Correct sill |  |

## Lesson
API placement doesn't apply UI defaults.

## Rule
Set every placement-relevant instance parameter explicitly.

## Validation
- Sill heights read back
