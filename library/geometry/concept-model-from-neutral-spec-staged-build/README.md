# ARPL-GEO-0004 rev 1: Concept model from a neutral spec: staged, idempotent build with visual gates

_Generated from this pack's files by tools/build_catalogs.py. Edit manifest.json, intent.md, vNN/ or final/rule.json instead._

| | |
|---|---|
| Level | 2 |
| Work class | W4 |
| Status | candidate |
| Use when | An agent builds a whole concept model from a structured spec (JSON) through a code-execution bridge; A build script creates many elements of several categories in one call; Element heights depend on a host (roof, slab) that may change later; The model must show which geometry is source fact and which is an AI estimate |
| Not for | Detailed design or construction documentation (LOD 300+); Workshared central models (no sync handling covered here); Interpreting the sketch itself: that belongs to USG (see IN-0011 redirect) |
| Workflows | geometry, placement-hosting, validation-qaqc |
| Disciplines | architecture |
| Project types | residential |
| Revit tested | 2024 |
| API | Floor.Create, FloorType.IsFoundationSlab, Document.Create.NewFootPrintRoof, FootPrintRoof.set_DefinesSlope / set_SlopeAngle, ROOF_LEVEL_OFFSET_PARAM, Wall.Create, WallType ALLOW_AUTO_EMBED, SPACING_LAYOUT_VERT (1 fixed distance, 3 maximum spacing), Document.Create.NewOpening (floor), Railing.Create, RailingType.RailStructure.AddNonContinuousRail, RailingType.BalusterPlacement, StairsEditScope, StairsRun.CreateStraightRun, StairsLanding.CreateAutomaticLanding, FAMILY_TOP_LEVEL_OFFSET_PARAM, ALL_MODEL_MARK / ALL_MODEL_INSTANCE_COMMENTS, View3D.SetSectionBox, UIDocument.RequestViewChange |
| Failure patterns | FP01, FP05, FP10, FP11, FP13, FP22, FP40 |
| Contributors | Gottfried Schmidtke with Claude |

**Intent:** Generate a two-level concept model (levels, slabs, 8 columns, framed glazed facade, flat roof with overhang, terrace railing, two-flight stair, core walls) from a software-neutral JSON building spec plus the source hand sketch, using only native Revit elements, and keep every element traceable to its spec ID and evidence class.

Related: ARPL-GEO-0002 (no wall attachment in the Revit 2024 API; profile walls instead), ARPL-CHG-0002 (changing a footprint roof in Revit 2024), ARPL-QA-0001 (show the approach before building). The spec side of this build (what the neutral spec failed to carry) belongs to USG, not ARPL.

## Learning curve

| Version | Instruction | Result | Problem | Found by |
|---|---|---|---|---|
| v01 | Read-only survey: levels, length units, wall/floor/roof/column/railing/stair types, views. Then showed the user a mapping table (spec item -> evidence class -> Revit element) and the hypotheses before any write. | User corrected the upper-volume placement and glazing module before geometry existed. | None. Confirms ARPL principle: show the approach before committing. | user review of the plan |
| v02 | One run_csharp call creating levels, two types, two slabs, 8 columns, 8 curtain walls and 2 core walls. | Bridge returned 'did not respond within 60s'. A read-only follow-up also timed out. bridge_status said the session was alive. | Revit had committed everything; the call simply outlived the timeout. Re-running would have duplicated all elements. | desktop screenshot (no dialog, new level plan in the browser), then a read-only query of elements by Mark |
| v03 | Slabs created with type 'Conc 200mm' chosen by name. | Both slabs landed in Structural Foundations. | The type was a foundation slab (IsFoundationSlab = true). Type change across categories is impossible; slabs were deleted and recreated with a Floors type. | category column in the verification query |
| v04 | Attach upper walls to the roof with Wall.AddAttachment; build rails with new NonContinuousRailInfo(); commit StairsEditScope without a failures preprocessor. | Compile errors: AddAttachment / AttachmentLocation do not exist in the 2024 API; NonContinuousRailInfo has no public constructor; the bridge helper name was guessed wrong. | Code written against a remembered API, not the installed one. | Roslyn compile errors; fixed by reflecting the types (GetMethods/GetConstructors) and using RailStructure.AddNonContinuousRail and the bridge's Failures() collector |
| v05 | Upper columns placed with top constraint = roof-top level (6000). | Transaction committed with no warning. | Columns pierced the roof: the roof underside at the column positions was lower than the level. When the roof later changed from gable to flat, walls and columns had to be re-derived again. | screenshot of a dedicated review 3D view only |
| v06 | Curtain wall type with SPACING_LAYOUT_VERT = fixed distance 1500. | Each 10 m face: 6 panels of 1500 plus one 1000 remainder. | The design intent was '~1.5 m, equal panels'. Switched to maximum spacing 1500: equal panels of 1467 (8.8 m opening) and 1360 (6.8 m opening). | panel count in the result + user review |
| v07 | Glazing as free-standing full-width curtain walls. | Glass ran edge to edge. | Design shows a solid frame (corner piers, head band) with recessed glazing. Fixed with a basic wall per face plus a shorter curtain wall on the same line, type with Automatically Embed = Yes; Revit cut the opening itself. | user comparing the review view with the sketch |
| v08 | Terrace railing from the template's 1100 mm baluster type. | Vertical balusters at 275 mm. | Design shows three horizontal rails on sparse posts. Duplicated the type, added two non-continuous rails (400, 750) with a 50 x 50 profile, posts at 1500. | user review |
| v09 | Promised the user 'one transaction group, one undo' up front, then built in five stages. | Several undo steps. | Promise not kept. | transaction names in the results |

## Lesson
'Committed' is not 'correct' and 'timed out' is not 'failed'. A spec-driven build needs small idempotent stages, semantic type checks, version-checked API calls, host-derived dependent heights and a visual gate after every stage.

## Rule
1. Stage budget: each write call finishes well inside the bridge timeout (target < 20 s); order: datums + types -> hosts (slabs, walls) -> hosted/dependent (openings, roof, railing, stair).
2. Idempotent writes: find-or-duplicate for types; check for an existing element with the same Mark before creating.
3. Timeout protocol: never retry a write; query state by Mark read-only; if Revit does not answer, take a screenshot before anything else (FP11, FP22).
4. Type semantics: assert category and kind (Floors vs Structural Foundations, basic vs curtain vs stacked wall) before using a type; never choose by name (FP13, FP01).
5. API version gate: reflect the installed API before using non-trivial members (attachments, rails, stairs, failure handling).
6. Dependency re-derivation: record host -> dependant (column top -> roof underside, wall height -> roof underside, opening -> slab) and re-run dependants whenever a host changes (FP10).
7. Visual gate: after each stage, look at a dedicated review 3D view (section box to the building, annotation categories hidden) before reporting success (FP05).
8. Evidence tags: Mark = spec ID, Comments = 'USG | exact / derived / approximate'; promote to 'user-accepted (date)' only on explicit acceptance.
9. Intent-bearing settings (grid layout fixed vs maximum spacing, railing typology, facade composition) are asked or flagged, not defaulted.
10. Undo: one named transaction group per stage; tell the user the real number of undo steps.

## Validation
- After each stage, read-only: every element whose Comments start with 'USG' appears exactly once per expected Mark, in the expected category.
- For every host-derived element (column top, wall top, opening), top elevation <= host underside at its XY.
- A screenshot of the review 3D view is checked against the source sketch before the next stage starts.
