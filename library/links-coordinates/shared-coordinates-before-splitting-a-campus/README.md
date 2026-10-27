# ARPL-LNK-0001 rev 1: Set shared coordinates on an authority building, then split a campus model into per-building files

_Generated from this pack's files by tools/build_catalogs.py. Edit manifest.json, intent.md, vNN/ or final/rule.json instead._

| | |
|---|---|
| Level | 2 |
| Work class | W5 |
| Status | candidate |
| Use when | A campus or masterplan model has to be split into per-building models that will be linked back by shared coordinates; One building is the coordinate authority and the site location comes from a map pick (lat/long) rather than a survey file; Elements (grids, masses, floors) must be assigned to buildings automatically before a split |
| Not for | Projects with a surveyed control point or a civil/site model to acquire coordinates from: acquire from that instead; Splits where buildings share elements that cannot be assigned to one building (shared podium, site-wide topography): decide ownership first |
| Workflows | links-coordinates, model-administration, coordination |
| Disciplines | bim-vdc, architecture |
| Project types | healthcare, generic |
| Revit tested | 2024 |
| API | ProjectLocation.SetProjectPosition, ProjectPosition, ProjectLocation.GetTotalTransform, SiteLocation.Latitude, SiteLocation.Longitude, SiteLocation.TimeZone, Application.OpenDocumentFile, Document.Delete, Document.Save, Document.Close, Grid.Curve, Element.get_BoundingBox |
| Failure patterns | FP05, FP44 |
| Contributors | Gottfried Schmidtke with Claude |

**Intent:** Give one campus model with all buildings' grids, masses and floors a real-world shared coordinate system anchored on one authority building, then split it into one file per building so every child carries the same shared coordinates and can be linked back by shared coordinates.

The cloud upload and registry steps that followed are filed as ARPL-ADM-0003; the batch linking as ARPL-LNK-0002; the recurring coordination as ARPL-PW-0003.

## Learning curve

| Version | Instruction | Result | Problem | Found by |
|---|---|---|---|---|
| v01 | Shared coordinates from a map pick: pointer on the authority building gives lat/long, converted to the local state plane (US survey feet) outside Revit. SetProjectPosition(XYZ.Zero, new ProjectPosition(E - c.X, N - c.Y, 0, 0)), c = centre of the authority building's arc grid in internal coordinates; site lat/long and time zone set; dry run first. | Committed; the anchor read back through GetTotalTransform().Inverse at exactly E/N. | Sign convention is easy to flip: ProjectPosition is the shared position of the internal origin, so E - c.X, not c.X - E. A map pick is accurate to a few metres only, and grid north differs from true north by the convergence angle (about 0.13 deg here). | read-back of the anchor in shared coordinates; rolled-back dry run before commit |
| v02 | Split: copy the campus file per building, open the copy, delete grids, masses and floors of other buildings, save. Grids by name prefix, masses by name, floors by nearest mass bounding box. | 13 files; each kept the parent's ProjectPosition. | Nearest-distance assignment misfiled floors where two buildings touch: one building got 0 floors, its neighbour too many (FP44). | per-file count report against the parent total (48 floors) |
| v03 | Redo the two affected files with floors assigned by containment in the smallest grid extent that holds the floor centre. | Counts correct; 0 floors unassigned; per-file totals equal the parent. | None. | floor levels per file match each building's storeys |

## Lesson
Set shared coordinates once in the parent before splitting, so every child inherits them; assign elements to buildings by containment, never by nearest distance.

## Rule
1. Pick the authority building and an anchor point on it (for example an arc-grid centre). Compute the state-plane E/N of the anchor outside Revit.
2. In the parent: SetProjectPosition(XYZ.Zero, new ProjectPosition(E - anchor.X, N - anchor.Y, elevation, angle)); set SiteLocation latitude, longitude and time zone; dry-run, read the anchor back through GetTotalTransform().Inverse, then commit and save. Record the accuracy of the source (map pick: metres) and the grid-north convergence you did or did not apply.
3. Split only after that: copy the file per building and delete what does not belong. Grids by name prefix, masses by name, hosted/floor elements by containment in the building's own grid extent (smallest containing extent wins).
4. Guard: per-file counts must add up to the parent's counts, no element unassigned, and every child's ProjectPosition at XYZ.Zero equals the parent's.

## Validation
- The anchor reads back the intended E/N in shared coordinates.
- Every child file has the same ProjectPosition at XYZ.Zero as the parent.
- Element counts per building sum to the parent counts; 0 unassigned.
