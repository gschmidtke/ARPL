# ARPL-ASM-0002 rev 1: Door too tall for a header

_Generated from this pack's files by tools/build_catalogs.py. Edit manifest.json, intent.md, vNN/ or final/rule.json instead._

| | |
|---|---|
| Level | 2 |
| Work class | W3 |
| Status | candidate |
| Use when | framing a wall with openings where headers must fit under top plates; a door or window rough opening is close to the plate height |
| Not for | openings in non-framed walls (masonry, concrete) |
| Workflows | assemblies-fabrication, model-change |
| Disciplines | architecture, structural |
| Project types | residential |
| Revit tested | 2024 |
| API | FamilyInstance, StructuralType.Beam |
| Failure patterns | FP07 |
| Contributors | Gottfried Schmidtke with Claude |

**Intent:** Frame a 6.1 m sliding door opening in a 2.50 m wood-frame wall

**LOD:** LOD 400

**Decisive questions:**
- Lower the door, raise the walls, or frame without a header? (user: lower the door)
- Structural adequacy of a 2x6 header over 6.1 m: flagged for the engineer

## Learning curve

| Version | Instruction | Result | Problem | Found by |
|---|---|---|---|---|
| v01 | Standard opening framing: king and jack studs, 2-ply header above the rough opening, double top plate | 2D plan preview flagged the conflict | Rough opening top 2505 mm is above the underside of the top plates (2424 mm); no header fits | layout rule check shown in the 2D preview |
| v02 | User decision: lower the door (new type 7'-5"); header moves tight under the plate when the gap is under 150 mm | Header fits with a 4 mm shim |  |  |

## Lesson
Conflicts between the architecture and the framing rule surface in the layout computation; they are design decisions, not things to fix silently.

## Rule
Report every opening whose rough opening plus header doesn't fit under the plates as a decision for the user; never move a header into the top plates.

## Validation
- Rough opening and header heights dimensioned on the shop drawing
