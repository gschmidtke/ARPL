# ARPL-CRD-0001 rev 1: Weekly clash run inside Revit by solid intersection across open cloud models; penetrations separated, clashes grouped, owner by routing priority

_Generated from this pack's files by tools/build_catalogs.py. Edit manifest.json, intent.md, vNN/ or final/rule.json instead._

| | |
|---|---|
| Level | 2 |
| Work class | W8 |
| Status | candidate |
| Use when | A federated project needs a weekly clash number per discipline pair and the cloud project has no clash service (no Model Coordination module); Clash results must carry element unique ids so next week's run can report new and resolved clashes; A quick hard-clash check before publishing models for formal coordination |
| Not for | Clearance (soft) clashes: needs inflated solids, not recorded yet; Walls and floors against services when the service openings are not modelled: every crossing would count; Models that do not share one internal origin and shared position: transform one side by the link transform first; Replacing a coordination service where one is available: use its tracked clash groups instead |
| Workflows | coordination, validation-qaqc, links-coordinates |
| Disciplines | bim-vdc, mechanical, plumbing, electrical, structural, architecture |
| Project types | generic |
| Revit tested | 2024 |
| API | BooleanOperationsUtils.ExecuteBooleanOperation, BooleanOperationsType.Intersect, BoundingBoxIntersectsFilter, ElementMulticategoryFilter, Options.DetailLevel, GeometryInstance.GetInstanceGeometry, Solid.ComputeCentroid, WorksharingUtils.GetUserWorksetInfo, WorksetConfiguration.Open, OpenOptions.SetOpenWorksetsConfiguration, ModelPathUtils.ConvertCloudGUIDsToCloudPath, ProjectLocation.GetProjectPosition, Document.Close |
| Failure patterns | FP47, FP48, FP38 |
| Contributors | Gottfried Schmidtke with Claude |

**Intent:** Give the weekly coordination report one clash number per discipline pair, with element ids, when the cloud project offers no clash service: open the discipline models in one Revit session, intersect their solids pairwise, separate planned penetrations from clashes, group clashes that share an element, and name the team that moves.

## Learning curve

| Version | Instruction | Result | Problem | Found by |
|---|---|---|---|---|
| v01 | Open HVAC and Structural cloud models with link worksets closed; confirm both report the same shared position and the link transform is identity; intersect every duct and duct fitting with structural framing and columns (bounding-box prefilter, then solid intersection, volume > 0.0001 cf). | 2,050 duct elements tested in 7 s; 14 hard clashes, all small (0.0007 to 0.0075 cf): duct tees and fittings touching W18x55 beams and joists. |  |  |
| v02 | Open the other three models; run the full matrix (MEP against structure, MEP against MEP, MEP against architectural ceilings) in two calls; one CSV per pair with both unique ids, levels, volume and centroid. | 9 pairs in about 3 minutes (longest pair 53 s, plumbing against ceilings); 365 raw intersections. The second call outran the bridge's 60 s reply wait but completed; progress was read from the run log. | About a quarter of the ceiling hits were vertical pipes, ducts and conduits dropping through the ceiling to fixtures and outlets: planned penetrations, not clashes (FP47). The long call returned a timeout although it finished (FP38 family: reply wait shorter than the work). | reading the clash list by orientation of the running element |
| v03 | Classify: a vertical run through a ceiling is a penetration; everything else a clash. Group clashes that share an element (union of element pairs). Owner = the side with lower routing priority (structure and ceilings stay; then gravity drainage, ducts, pressure pipes, conduits). | 282 hard clashes in 74 groups; 83 penetrations reported separately. Three quarters of the clashes are services running inside the ceiling layer at L2 to L5: one ceiling-plenum decision per level, not hundreds of fixes. Structure: 17 small touches. Owners: Electrical 112, HVAC 85, Plumbing 85. | Fittings at the drop points (elbows) are still counted as clashes because a fitting has no run direction; ceiling figures are slightly high. | reviewing the largest groups |

## Lesson
A clash number is only useful per discipline pair, grouped, with owners and stable element ids; a raw intersection count mixes planned penetrations with real conflicts and jumps whenever one run is rerouted.

## Rule
1. Agree the clash matrix with the team first: category pairs, hard or clearance, routing priority (who moves).
2. Open every model in one session with link worksets closed; check that all report the same shared position (ProjectLocation.GetProjectPosition at the origin) and that link transforms are identity. Otherwise transform the second model's solids by the link transform.
3. Per pair: bounding-box prefilter, then BooleanOperationsUtils intersection; count a clash when the intersection volume exceeds a small threshold (0.0001 cf used). Cache solids; walk GeometryInstance with GetInstanceGeometry.
4. Write one row per element pair: both unique ids and element ids, categories, family and type, levels, volume, centroid. Keep it under the bridge's reply limit by splitting pairs across calls and appending to a run log; on a timeout read the log, never rerun blindly.
5. Classify: vertical runs through ceilings (and later through walls or floors with modelled openings) are penetrations, reported separately.
6. Group clashes that share an element (union-find); report groups, not only clashes. Owner by routing priority.
7. Close the opened models without saving (Document.Close(false)); they were only read.
8. Next week: match by the pair of unique ids to report new, resolved and still open.

## Validation
- Every model reports the same shared position; every link transform is identity (or the transform was applied).
- Run log lists every pair of the agreed matrix with a count and duration.
- Penetrations + clashes = raw intersections; each clash has a group and an owner.
- Opened models closed unchanged (no sync).
