# ARPL-ASM-0001 rev 1: Plywood slivers at openings

_Generated from this pack's files by tools/build_catalogs.py. Edit manifest.json, intent.md, vNN/ or final/rule.json instead._

| | |
|---|---|
| Level | 2 |
| Work class | W3 |
| Status | candidate |
| Use when | laying out sheathing, sheet goods or cladding boards across a wall with openings; deciding where panel joints fall relative to windows and doors |
| Not for | curtain walls; single full-height sheets without openings |
| Workflows | assemblies-fabrication, documentation, schedules-quantities |
| Disciplines | architecture, structural, construction |
| Project types | residential |
| Revit tested | 2024 |
| API | AssemblyInstance, FamilyInstance |
| Failure patterns | FP04, FP12 |
| Contributors | Gottfried Schmidtke with Claude |

**Intent:** Lay out 3/4" plywood on wood-frame walls with openings

**LOD:** LOD 400

**Decisive questions:**
- Sheet size: 4x9 cut to height (agent default; should have been asked)
- Minimum remnant: 150 mm (agent default; should have been asked)

## Learning curve

| Version | Instruction | Result | Problem | Found by |
|---|---|---|---|---|
| v01 | 4x9 sheets cut to wall height, vertical joints on stud centres from the wall end | Layout drawn in elevation preview | A joint 28 mm from the window edge would leave an unusable strip | 2D elevation preview |
| v02 | If a joint falls within 150 mm outside an opening edge, move it back one stud bay (sheet one bay shorter, following joints shift) | Rule applied | The 28 mm strip remained: the joint was inside the opening edge, a case the rule didn't cover | measuring the redrawn preview |
| v03 | Any joint within 150 mm of either side of an opening edge moves back one stud bay | Narrowest piece 219 mm; same rule fed the 3D build, shop drawings and BOM |  |  |

## Lesson
Material constraints must be part of the layout rule, not a check afterwards; and a fix needs the same preview as the original rule.

## Rule
Minimum remnant width is a parameter of the layout rule and is evaluated on both sides of every opening edge.

## Validation
- Measured joint positions in the preview
- Piece-by-piece check of the 3D build
