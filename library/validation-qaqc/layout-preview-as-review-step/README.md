# ARPL-QA-0001 rev 1: Layout preview as a review step

_Generated from this pack's files by tools/build_catalogs.py. Edit manifest.json, intent.md, vNN/ or final/rule.json instead._

| | |
|---|---|
| Level | 2 |
| Work class | W8 |
| Status | candidate |
| Use when | any layout-driven build: studs, panels, cladding, tiles, ceiling grids; before committing many repeated elements in 3D |
| Not for | single elements |
| Workflows | validation-qaqc, assemblies-fabrication |
| Disciplines | architecture, construction |
| Project types | residential |
| Revit tested | 2024 |
| API | DetailCurve, FilledRegion |
| Failure patterns | FP04, FP07 |
| Contributors | Gottfried Schmidtke with Claude |

**Intent:** Confirm a stud and sheathing layout before building

## Learning curve

| Version | Instruction | Result | Problem | Found by |
|---|---|---|---|---|
| v01 | 2D preview drawn from the layout rule in plan and elevations; user confirms | Header conflict and plywood sliver found before any 3D work |  |  |

## Lesson
A preview is a review tool, not decoration.

## Rule
Every layout-driven build (W3) gets a 2D preview from the same rule and a user confirmation.

## Validation
- User confirmation
