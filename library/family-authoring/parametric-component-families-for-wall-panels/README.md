# ARPL-FAM-0005 rev 1: Component families for a wall panel

_Generated from this pack's files by tools/build_catalogs.py. Edit manifest.json, intent.md, vNN/ or final/rule.json instead._

| | |
|---|---|
| Level | 2 |
| Work class | W1 |
| Status | candidate |
| Use when | building parametric component families for lumber, sheets, insulation or cladding; families that must flex reliably before mass placement |
| Not for | - |
| Workflows | family-authoring, assemblies-fabrication |
| Disciplines | architecture, structural, construction |
| Project types | residential |
| Revit tested | 2024 |
| API | ReferencePlane, FamilyItemFactory.NewAlignment, FamilyManager, Extrusion |
| Failure patterns | FP05 |
| Contributors | Gottfried Schmidtke with Claude |

**Intent:** Lumber, sheet, insulation and siding families for LOD 400 wall panels

## Learning curve

| Version | Instruction | Result | Problem | Found by |
|---|---|---|---|---|
| v01 | Structural framing template with type parameters b and d labelled on EQ dimensions; Generic Model box with instance Width/Height and type Thickness; profile extrusion for bevel siding | All four families flex-tested and loaded |  |  |
| v02 | Associate the framing extrusion's material to the template's 'Structural Material' | Document regeneration failed | That parameter can't drive the extrusion material in this template | commit failure |
| v03 | Own material parameter 'Lumber Material' | Works |  |  |

## Lesson
Parametric component families can be generated reliably when every face is locked to a labelled reference plane.

## Rule
Generate component families from templates by script, with locks on all faces, then flex-test before placing any instance.

## Validation
- Flex test of each type with measured bounding boxes
