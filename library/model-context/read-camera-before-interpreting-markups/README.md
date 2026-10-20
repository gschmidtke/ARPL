# ARPL-MCX-0001 rev 1: Markup read without checking the camera

_Generated from this pack's files by tools/build_catalogs.py. Edit manifest.json, intent.md, vNN/ or final/rule.json instead._

| | |
|---|---|
| Level | 1 |
| Work class | W8 |
| Status | candidate |
| Use when | interpreting markups or redlines on a 3D view or screenshot; reviewing feedback given on a 3D image |
| Not for | - |
| Workflows | model-context, validation-qaqc |
| Disciplines | generic |
| Project types | generic |
| Revit tested | 2024 |
| API | View3D.GetOrientation, ViewOrientation3D |
| Failure patterns | FP02, FP13 |
| Contributors | Gottfried Schmidtke with Claude |

**Intent:** Place a door where the user marked it on a 3D screenshot

## Learning curve

| Version | Instruction | Result | Problem | Found by |
|---|---|---|---|---|
| v01 | Assumed the default 3D orientation | Door placed on the south wall | The marked wall faced the viewer from another direction | user |
| v02 | Read View3D.GetOrientation() and determine which walls face the viewer | Door on the correct wall |  |  |

## Lesson
A screenshot carries no orientation unless you read it from the view.

## Rule
Read the camera before interpreting any 3D markup.

## Validation
- Orientation read back
