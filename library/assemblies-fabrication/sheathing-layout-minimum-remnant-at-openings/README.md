# ARPL-ASM-0001: Plywood slivers at openings

| | |
|---|---|
| Level | 2 |
| Work class | W3 |
| Workflows | assemblies-fabrication, documentation, schedules-quantities |
| Disciplines | architecture, structural, construction |
| Project types | residential |
| Revit tested | 2024 |
| Status | candidate |

**Intent:** Lay out 3/4" plywood on wood-frame walls with openings

## Learning curve

| Version | Instruction | Result | Problem |
|---|---|---|---|
| v01 | 4x9 sheets cut to wall height, vertical joints on stud centres from the wall end | Layout drawn in elevation preview | A joint 28 mm from the window edge would leave an unusable strip |
| v02 | If a joint falls within 150 mm outside an opening edge, move it back one stud bay (sheet one bay shorter, following joints shift) | Rule applied | The 28 mm strip remained: the joint was inside the opening edge, a case the rule didn't cover |
| v03 | Any joint within 150 mm of either side of an opening edge moves back one stud bay | Narrowest piece 219 mm; same rule fed the 3D build, shop drawings and BOM |  |

## Lesson
Material constraints must be part of the layout rule, not a check afterwards; and a fix needs the same preview as the original rule.

## Rule
Minimum remnant width is a parameter of the layout rule and is evaluated on both sides of every opening edge.

## Validation
- Measured joint positions in the preview
- Piece-by-piece check of the 3D build
