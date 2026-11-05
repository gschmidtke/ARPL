# ARPL-DOC-0005 rev 1: Construction detail as a drafting view derived from the model

_Generated from this pack's files by tools/build_catalogs.py. Edit manifest.json, intent.md, vNN/ or final/rule.json instead._

| | |
|---|---|
| Level | 2 |
| Work class | W6 |
| Status | candidate |
| Use when | drawing an LOD 400 construction detail as a drafting view from model facts; rebuilding a detail in place while keeping its sheet placement; adding enlargements, airflow or air-control lines to a detail |
| Not for | callouts of model sections where the owner wants the model to carry the information; structural, wind, energy or product verification |
| Workflows | documentation, views-graphics |
| Disciplines | architecture |
| Project types | residential |
| Revit tested | 2024 |
| API | ViewDrafting.Create, DetailCurve, FilledRegion.Create, Arc.Create, Plane.CreateByNormalAndOrigin, ViewSheet.Create, Viewport.Create, ImageExportOptions, PDFExportOptions |
| Failure patterns | FP40, FP18, FP26, FP63, FP64, FP08 |
| Contributors | Gottfried Schmidtke with Claude |

**Intent:** Develop roof-eave junctions of a vented shed roof as drafting-view details from a section of the model, with enlargements on a separate sheet, and revise them through several external reviews.

## Learning curve

| Version | Instruction | Result | Problem | Found by |
|---|---|---|---|---|
| v01 | Seal symbol with new Plane(normal, origin) | Compile error | constructor not in the API (FP40); use Plane.CreateByNormalAndOrigin | compiler |
| v02 | Rebuild in place: delete every element owned by the view | InvalidObjectException | the view owns an internal element without a category (FP63); filter Category != null | exception, then a survey grouped by type |
| v03 | View name with ':' (scale in the name) | ArgumentException | prohibited characters; the scale belongs to the view scale | exception |
| v04 | Drip edge and eave trim both drawn down the fascia | Owner asked why two profiles | one piece does the job; detail and enlargement disagreed | owner review of the PDF |
| v05 | Delete collinear duplicates when they overlap >= 90 % of the shorter line | Long WRB and trellis lines deleted | coverage must be measured against the candidate's own length (FP64) | deletion report read before sync |
| v06 | Dimensions referencing short witness stubs, then geometry moved 2 mm | Clip dimension read 70 for 72 | stubs are not tied to geometry (FP65) | line-purpose review |
| v07 | Default project dimension type in a cm project | Reviewer read 45, 34, 7 | project units (FP26, ARPL-DOC-0002) | external reviewer |

## Lesson
A drafting view is free linework: nothing ties it to the model or to itself. Every line, note and dimension needs a stated purpose and a check, and the detail and its enlargements must be drawn from one geometry definition.

## Rule
1. Survey the model section first (plates, rafters, offsets, overhang) and write the detail coordinates as functions of model values (e.g. zb(y) for the rafter underside), so the detail and every enlargement use the same geometry.
2. Rebuild in place to keep the viewport: delete only view-owned elements with a category; never the view (FP63).
3. Draw each component once; when an enlargement refines a part (roof edge, seat), redraw that part in the main detail from the enlargement's definition.
4. Use one dimension type in the drawing's units (ARPL-DOC-0002); reference real edges, not stubs; move stubs with any geometry change (FP65).
5. Line-purpose review (owner rule R5): list every line by style and position; remove same-style duplicates and hidden lines buried under visible ones only when the candidate itself is >= 90 % covered (FP64); keep breaks, hidden elements, airflow and air-control lines and witness ticks with a stated purpose.
6. Annotate per ARPL-DOC-0004.
7. Image-export the view after every stage and look at it (ARPL-QA-0001); export the sheet PDF for the reviewer.
8. Keep review findings and their dispositions in a report outside the drawing (DA-11); the drawing carries short [PROV] markers only.

## Validation
- Image export after each stage
- Line inventory with no unexplained or duplicate lines
- annotation_leader_check.cs (ARPL-DOC-0004) passes
- PDF reviewed by the owner and an external reviewer
