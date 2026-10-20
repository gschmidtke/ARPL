# ARPL-PLH-0001 rev 1: Windows placed at sill 0

_Generated from this pack's files by tools/build_catalogs.py. Edit manifest.json, intent.md, vNN/ or final/rule.json instead._

| | |
|---|---|
| Level | 1 |
| Work class | W4 |
| Status | candidate |
| Use when | placing windows, doors or other hosted families by script |
| Not for | - |
| Workflows | placement-hosting |
| Disciplines | architecture |
| Project types | generic |
| Revit tested | 2024 |
| API | NewFamilyInstance, INSTANCE_SILL_HEIGHT_PARAM |
| Failure patterns | FP05 |
| Contributors | Gottfried Schmidtke with Claude |

**Intent:** Place windows in walls

## Learning curve

| Version | Instruction | Result | Problem | Found by |
|---|---|---|---|---|
| v01 | NewFamilyInstance with the window family on the wall | Windows at sill height 0 | Hosted placement ignores the family's default sill | visual check |
| v02 | Set INSTANCE_SILL_HEIGHT_PARAM explicitly after placement | Correct sill |  |  |

## Lesson
API placement doesn't apply UI defaults.

## Rule
Set every placement-relevant instance parameter explicitly.

## Validation
- Sill heights read back
