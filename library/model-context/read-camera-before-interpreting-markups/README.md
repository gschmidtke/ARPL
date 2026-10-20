# ARPL-MCX-0001: Markup read without checking the camera

| | |
|---|---|
| Level | 1 |
| Work class | W8 |
| Workflows | model-context, validation-qaqc |
| Disciplines | generic |
| Project types | generic |
| Revit tested | 2024 |
| Status | candidate |

**Intent:** Place a door where the user marked it on a 3D screenshot

## Learning curve

| Version | Instruction | Result | Problem |
|---|---|---|---|
| v01 | Assumed the default 3D orientation | Door placed on the south wall | The marked wall faced the viewer from another direction |
| v02 | Read View3D.GetOrientation() and determine which walls face the viewer | Door on the correct wall |  |

## Lesson
A screenshot carries no orientation unless you read it from the view.

## Rule
Read the camera before interpreting any 3D markup.

## Validation
- Orientation read back
