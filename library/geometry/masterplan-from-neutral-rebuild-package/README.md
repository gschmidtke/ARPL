# ARPL-GEO-0005 rev 1: Masterplan from a neutral rebuild package: floors, DirectShape envelopes and domain-based grids

_Generated from this pack's files by tools/build_catalogs.py. Edit manifest.json, intent.md, vNN/ or final/rule.json instead._

| | |
|---|---|
| Level | 2 |
| Work class | W4 |
| Status | candidate |
| Use when | A neutral package of levels, floor profiles and exact envelopes must become native Revit elements; Exact source mass geometry (triangle face loops) has to enter Revit as DirectShape; Grids must be created for many buildings at once, including rotated wings and curved (arc) buildings; A payload is too large to embed in a code-execution call |
| Not for | Reading or interpreting the original source model (upstream intake, USG); Structural design: grid intersections are column-centreline candidates only; Workshared central models |
| Workflows | geometry, model-context, validation-qaqc |
| Disciplines | architecture |
| Project types | healthcare |
| Revit tested | 2024 |
| API | Level.Create, ViewPlan.Create, Floor.Create (multiple disjoint CurveLoops), HOST_AREA_COMPUTED, SubTransaction, TessellatedShapeBuilder, TessellatedShapeBuilderTarget.AnyGeometry, TessellatedShapeBuilderFallback.Mesh, TessellatedShapeBuilderResult.Outcome, TessellatedShapeBuilderResult.GetGeometricalObjects, DirectShape.CreateElement, DirectShape.SetShape, DirectShape.SetName, Grid.Create(Document, Line), Grid.Create(Document, Arc), Arc.Create, Document.Delete, ViewPlan.CropBoxActive, Document.ExportImage, ImageExportOptions |
| Failure patterns | FP05, FP31, FP40, FP41, FP42 |
| Contributors | Gottfried Schmidtke with Claude |

**Intent:** Rebuild a 13-building masterplan in an empty Revit project from a compact, tool-neutral rebuild package (8 levels, 22 floor-profile prototypes placed as 48 floors, 13 exact mass envelopes as triangle face loops), then create reference grids per building, without re-reading the original source model and without inventing walls, rooms or structure.

Builds on ARPL-GEO-0004 (staging, idempotent tags, visual gate), adapted for a masterplan: stages are levels, floors, envelopes, grids. The upstream reading of the source belongs to USG, not ARPL.

Measured (Revit 2024, laptop): 8 levels 0.3 s; 48 floors 2.1 s; 12 envelopes 0.05 s; one 5,907-triangle envelope 0.37 s; 361 grids including the delete of the old set 1.3 s.

## Learning curve

| Version | Instruction | Result | Problem | Found by |
|---|---|---|---|---|
| v01 | Embed the build data in the C# snippet. | Not attempted for envelopes: the largest envelope was 200 KB (5,907 triangles). | Inline payloads that large are error-prone to pass through a code tool. | payload size check before the build |
| v02 | Write the payload JSON files to a folder on the user's computer (one-time folder approval) and read them in Revit with File.ReadAllText + JObject.Parse. | Worked for all stages; 15 files, read in milliseconds. | None. | build results |
| v03 | Create 48 floors with Floor.Create in one call, each in a SubTransaction; profiles with two disjoint regions passed as two CurveLoops to one Floor.Create. | 48/48 in 2.1 s; multi-region floors as single elements; total area equals the package; max per-floor deviation 0.001 sq ft (HOST_AREA_COMPUTED vs shoelace area). | None. A Revit floor always has thickness; the owner chose a template floor type as a tagged stand-in. | area comparison in the same call |
| v04 | Build 12 envelopes with TessellatedShapeBuilder; log r.GetNumberOfIssues(); set ds.Name; read r.GetGeometricalObjects() for SetShape and again for volume. | Compile error: GetNumberOfIssues does not exist. Then runtime InvalidOperationException with no message, twice. | Method assumed from memory (FP40). GetGeometricalObjects() can be read only once per build result; the second read throws. Use SetName() rather than the Name setter. | rolled-back dry run with step markers, then a per-file dry run in try/catch |
| v05 | Read GetGeometricalObjects() once into a variable; ds.SetName(); Target AnyGeometry, Fallback Mesh. | 12 envelopes in 48 ms, the large one in 372 ms. Outcomes: 10 Solid, 2 Mesh, 1 Sheet. Bounding boxes equal the source; volumes of the 10 solids equal the source signed volume to the cubic foot. | Mesh/Sheet outcomes came from the source: 1 and 2 non-manifold edges (Mesh) and 1,069 open edges (Sheet). A Sheet's volume is not meaningful. | per-envelope Outcome, then an edge-use count on the source triangles |
| v06 | Create 261 grids from bounding boxes per building; tag each with Comments; verify by reading back grids whose Comments start with the tag. | 261 created in 0.9 s, but the read-back found 0 grids. | Grid datums have no ALL_MODEL_INSTANCE_COMMENTS; get_Parameter(...)?.Set(...) skipped every tag silently (FP42). The owner also rejected bounding-box grids: floors of three narrow wings extended 17.6-50.6 ft beyond their grids. | read-back count; floor-vs-grid coverage check in the building's grid frame |
| v07 | Replace with domain-based grids (one grid domain per wing, standard bays with rational end bays, a curved building as radial lines plus concentric arcs): delete the 261 and create 361 (357 lines, 4 arcs) in one transaction; read back by name prefix. | 361/361 in 1.3 s, one undo step; names unique; arcs are Arc curves; endpoints and radii at 0.0 ft deviation; no grid crosses another building or another wing. | Delete first in the same transaction to avoid name clashes. Grid heads crowd where wings meet; scope boxes would help but cannot be created through the API. | read-back; image export of a plan view |
| v08 | Visual check: bring Revit to the front with the desktop-control open-application call and zoom to fit. | A second, empty Revit instance started; the model stayed in the first instance. | Opening an already-running desktop application can launch a new instance instead of focusing it (FP41). | screenshot of the splash; bridge status listing two live Revit sessions |
| v09 | Visual check without the UI: Document.ExportImage of the template's ground-floor plan. | The image showed only a corner near the origin. | The template plan view had an active crop region. | the exported image; fixed with a dedicated plan view, CropBoxActive = false, no template |

## Lesson
A neutral rebuild package becomes native Revit quickly and exactly when data travels as files, every element is identified by name or Mark (not by a parameter that may not exist), envelopes are pre-checked for closure, and visual checks use API image export rather than the desktop UI.

## Rule
1. Payload: write data files next to the model and read them in Revit; do not embed large data in scripts.
2. Floors: Floor.Create accepts several disjoint CurveLoops as one floor (2024); verify HOST_AREA_COMPUTED against the source area in the same call; a Revit floor always has thickness, so tag it as a stand-in.
3. Envelopes as DirectShape: TessellatedShapeBuilder with Target AnyGeometry + Fallback Mesh; read GetGeometricalObjects() exactly once; name with SetName(); store the source id in ApplicationDataId and Mark.
4. Before building envelopes, count edge use in the source triangles: open or non-manifold edges predict Mesh/Sheet outcomes; report volume only for closed solids.
5. Grids: datums carry no Comments; identify grids by a unique name prefix and verify by name. Create arcs with Grid.Create(doc, Arc). To replace a grid set that reuses names, delete and create in one transaction.
6. Grid logic: one grid domain per building wing (standard bays with rational end bays), curved buildings as radial lines plus concentric arcs; never one grid per bounding box. Check that no grid crosses another building or another wing.
7. Parameter writes: avoid get_Parameter(...)?.Set(...) where the tag matters; a null parameter must fail loudly (FP42).
8. Visual checks: prefer Document.ExportImage of a dedicated view (no template, CropBoxActive = false) over driving the desktop; do not use open-application on a running Revit (FP41).
9. Scope boxes cannot be created through the API: report legibility of dense site views as a UI task for the user.

## Validation
- Counts per stage equal the package (levels, floors, envelopes, grids).
- Floor area equals the source area per floor (here max 0.001 sq ft).
- Envelope bounding boxes equal the source; closed envelopes' volumes equal the source signed volume.
- Grids read back by name with 0.0 ft endpoint/radius deviation; no grid crosses another building or wing.
- An exported plan image is checked before reporting.
