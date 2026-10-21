# ARPL-DOC-0001 rev 3: Shop drawings: invalid references and swapped elevations

_Generated from this pack's files by tools/build_catalogs.py. Edit manifest.json, intent.md, vNN/ or final/rule.json instead._

| | |
|---|---|
| Level | 2 |
| Work class | W6 |
| Status | candidate |
| Use when | creating dimensioned shop drawings or assembly sheets; adding many dimensions by script |
| Not for | - |
| Workflows | documentation, views-graphics, assemblies-fabrication |
| Disciplines | construction, structural, architecture |
| Project types | residential |
| Revit tested | 2024 |
| API | AssemblyViewUtils, Dimension, Reference, TransactionGroup, IFailuresPreprocessor |
| Failure patterns | FP08, FP02, FP11, FP16, FP23 |
| Contributors | Gottfried Schmidtke with Claude |

**Intent:** Assembly shop drawings for three wall panels

## Learning curve

| Version | Instruction | Result | Problem | Found by |
|---|---|---|---|---|
| v01 | All dimensions in one transaction; stud chain from CenterFrontBack references | Blocking dialog 'dimension references are or have become invalid'; whole sheet rolled back | Stud centre-plane references are invalid for this family and view | dialog |
| v02 | One transaction per dimension in a TransactionGroup, rollback on error; stud chain from stud faces | 10 of 11 chains, then 11 of 11 | North sheet: 'exterior' elevation showed the inside; the assembly transform had reverted to world X | PDF review |
| v03 | Pick exterior and interior elevations by ViewDirection · exterior normal, not by the assembly transform | All three sheets correct |  |  |
| v04 | Owner: change all views and sheets to 1:25 except the site plan | 45 views at 1:25, 20 plans cropped to the building + 1.5 m with annotation crop, sections trimmed to the building, every sheet re-packed inside its drawing area; two continuation sheets (S100A, W104A) for views that no longer fit beside the others; no viewport outside its border or overlapping | At 1:25 plans came out up to 3 x 2.5 m on paper: crops larger than the building, a 71 m section mark and perspective camera markers outside the crop inflated the viewport; the first packer then moved two single plans off their own sheets | sheet fit check (viewport outline vs title block drawing area) after the scale change, and an element-by-element search for what extends past the crop |

## Lesson
Per-element transactions contain failures; implicit state (assembly transforms) can't be trusted.

## Rule
Isolate risky annotation in its own transaction and verify every sheet visually. Regenerate the shop drawing whenever the assembly members are replaced: dimensions reference member faces and are deleted with them. DirectShape faces take dimension references like family geometry. Sloped faces cannot be dimensioned in an elevation chain; state the heights at both ends in a note on the view. Check the assembly frame first (FP16). When rescaling: crop plans to the building first (clear scope boxes, which override the crop), turn on annotation crop, trim section width and far clip, hide markers that a template will not let you hide by category (HideElements), then re-pack sheets and check every viewport against the drawing area. A single-view sheet is centred, never emptied; continuation sheets (<number>A) only for real overflow on multi-view sheets (FP23).

## Validation
- PDF export rendered and reviewed per sheet
- Every viewport inside the title block drawing area and no overlaps after a scale change
