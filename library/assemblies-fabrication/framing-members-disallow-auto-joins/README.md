# ARPL-ASM-0004 rev 1: Vertical studs pulled by auto-joins

_Generated from this pack's files by tools/build_catalogs.py. Edit manifest.json, intent.md, vNN/ or final/rule.json instead._

| | |
|---|---|
| Level | 1 |
| Work class | W3 |
| Status | candidate |
| Use when | placing vertical studs, posts or braces as structural framing; framing members end up longer or shifted after placement |
| Not for | structural columns (not framing) |
| Workflows | assemblies-fabrication, validation-qaqc |
| Disciplines | structural, construction, architecture |
| Project types | generic |
| Revit tested | 2024 |
| API | StructuralFramingUtils.DisallowJoinAtEnd, StructuralType.Brace, LocationCurve |
| Failure patterns | FP05 |
| Contributors | Gottfried Schmidtke with Claude |

**Intent:** Place 2x6 studs as vertical structural framing between plates

**LOD:** LOD 400

## Learning curve

| Version | Instruction | Result | Problem | Found by |
|---|---|---|---|---|
| v01 | NewFamilyInstance(line, 2x6, level, StructuralType.Brace); joins disallowed on beams (plates) only | 509 pieces placed and verified by position | Interference check found studs overlapping corner studs: Revit had joined the studs to the plates, extended them to the plate centrelines and pulled two end studs 89 mm onto a neighbouring plate end | clash check between assemblies |
| v02 | StructuralFramingUtils.DisallowJoinAtEnd on every framing member including braces, then LocationCurve.Curve reset to the layout line | 0 clashes; stud lengths are true cut lengths |  |  |

## Lesson
Revit framing joins change members after placement, including their position.

## Rule
Disallow joins on all framing members immediately at creation and verify positions after regeneration.

## Validation
- Interference check between all assemblies
- Stud end heights read back
