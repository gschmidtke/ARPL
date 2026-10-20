# ARPL-FAM-0005: Component families for a wall panel

| | |
|---|---|
| Level | 2 |
| Work class | W1 |
| Workflows | family-authoring, assemblies-fabrication |
| Disciplines | architecture, structural, construction |
| Project types | residential |
| Revit tested | 2024 |
| Status | candidate |

**Intent:** Lumber, sheet, insulation and siding families for LOD 400 wall panels

## Learning curve

| Version | Instruction | Result | Problem |
|---|---|---|---|
| v01 | Structural framing template with type parameters b and d labelled on EQ dimensions; Generic Model box with instance Width/Height and type Thickness; profile extrusion for bevel siding | All four families flex-tested and loaded |  |
| v02 | Associate the framing extrusion's material to the template's 'Structural Material' | Document regeneration failed | That parameter can't drive the extrusion material in this template |
| v03 | Own material parameter 'Lumber Material' | Works |  |

## Lesson
Parametric component families can be generated reliably when every face is locked to a labelled reference plane.

## Rule
Generate component families from templates by script, with locks on all faces, then flex-test before placing any instance.

## Validation
- Flex test of each type with measured bounding boxes
