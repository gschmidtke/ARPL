# ARPL-CHG-0004 rev 1: Swap an insulation material model-wide by type parameters; keep the old variant as a family copy

_Generated from this pack's files by tools/build_catalogs.py. Edit manifest.json, intent.md, vNN/ or final/rule.json instead._

| | |
|---|---|
| Level | 2 |
| Work class | W5 |
| Status | candidate |
| Use when | replacing one insulation (or other) material across walls and roof; the material sits in family type parameters, compound layers and DirectShapes; the old product should stay available for later use |
| Not for | rebuilding families or geometry when only material and hatch change |
| Workflows | model-change, parameters-data |
| Disciplines | architecture, construction |
| Project types | residential |
| Revit tested | 2024 |
| API | Material.Duplicate, Material.CutForegroundPatternId, FamilySymbol.Duplicate, Document.EditFamily, Document.LoadFamily, DirectShape.SetShape, TessellatedShapeBuilder, Element.GetMaterialIds |
| Failure patterns | FP03, FP40, FP66 |
| Contributors | Gottfried Schmidtke with Claude |

**Intent:** Replace extruded polystyrene with mineral wool (rock wool) in walls and roof of a framed residential model, without rebuilding families, and keep an extruded-foam variant for later use.

## Learning curve

| Version | Instruction | Result | Problem | Found by |
|---|---|---|---|---|
| v01 | Search by material name across materials, compound layers, family types, instances, DirectShapes, filled regions, notes | Foam only in 207 family instances and 54 DirectShapes in the walls; roof batts were fiberglass |  |  |
| v02 | Material.Duplicate assigned through doc.GetElement(...) | Compile error | Material.Duplicate returns a Material, not an ElementId (FP40) | compiler |
| v03 | DirectShapes rebuilt as boxes from their bounding box | Skipped all 54 | raked wall tops: not boxes | volume comparison |
| v04 | DirectShapes rebuilt from their own faces with TessellatedShapeBuilder and the new material id | 54 rebuilt, volume difference < 1e-5 cf |  |  |
| v05 | Owner: change only hatch type and parameters; duplicate the family for later foam use | Family copy via EditFamily > SaveAs > LoadFamily; material cut patterns set (rigid-foam hatch for XPS, diagonal crosshatch for mineral wool) |  | owner |

## Lesson
A material swap is a parameter change, not a rebuild: family types carry the material, the material carries the hatch. Only DirectShapes carry the material in their geometry, so they need SetShape with a copy of their own faces.

## Rule
1. Inventory every place the old material is used: materials by name, compound layers of host types (with instance counts), family type material parameters, model elements by Element.GetMaterialIds, DirectShapes, filled region types in drafting views, and text.
2. Create the new material by duplicating the old (Material.Duplicate returns the Material); set its cut pattern (hatch) and graphics colour; give the old material its proper hatch too.
3. Before changing the in-use family, keep the old variant: EditFamily > SaveAs '<family> - <old material>' > LoadFamily; set its types' material to the old one. It stays unplaced for later use.
4. Change the in-use family's type material parameters and rename the types; update instance comments that name the material. Change thickness only by type parameters, after a dry run shows which way the geometry grows.
5. DirectShapes: rebuild with TessellatedShapeBuilder from the triangulated faces of their own solid, each face with the new material id, Target Solid, Fallback Abort; compare volumes before SetShape.
6. Drafting details: change the filled region type of the old fill; update notes; re-run annotation layout (ARPL-DOC-0004).
7. Recount: no model element still uses the old material; sync with a comment.

## Validation
- Model elements using the old material: 0
- DirectShape volume difference below tolerance
- Family copy present with old material, unplaced
- Section/plan views show the new hatch
