# ARPL-ASM-0008 rev 1: Slab on grade from the framing layout (anchors, recess, stub-ups)

_Generated from this pack's files by tools/build_catalogs.py. Edit manifest.json, intent.md, vNN/ or final/rule.json instead._

| | |
|---|---|
| Level | 2 |
| Work class | W3 |
| Status | candidate |
| Use when | a prefab timber building sits on a slab on grade; anchor bolts, slab recesses or plumbing stub-ups must match wall panels and fixtures |
| Not for | structural design of the slab or anchorage (engineer of record); raised floors on piers or ground screws |
| Workflows | assemblies-fabrication, geometry |
| Disciplines | structural, architecture, plumbing |
| Project types | residential |
| Revit tested | 2024 |
| API | Floor.Create, FLOOR_HEIGHTABOVELEVEL_PARAM, DirectShape, BooleanOperationsUtils, AssemblyInstance.Create, Element.GetDependentElements |
| Failure patterns | FP19 |
| Contributors | Gottfried Schmidtke, Claude (Anthropic) |

**Intent:** Model a slab on grade for a prefab timber building as a fabrication assembly whose anchor bolts, recesses and plumbing stub-ups come from the wall-panel framing and the fixture layout, so the pour matches the panels that will sit on it.

**LOD:** LOD 300-350

## Learning curve

| Version | Instruction | Result | Problem | Found by |
|---|---|---|---|---|
| v01 | Owner: compare a slab on grade with a wood floor on ground screws; the owner builds the slab himself, a GC signs off | Cost comparison (slab about $5.5-8.5k vs ground screws $17.6-30k) and a 2D layout preview: thickened edge, 27 anchors from the bottom-plate segments and stud axes, 5 stub-ups, bill of materials | Two stub-ups fell into the thickened edge, one too close to a wall; the shower, kitchen hot water and terrace level were open questions | layout preview reviewed against the edge zone and the room layout |
| v02 | South wall changed to three standard sliders with posts; owner answers: recessed curbless shower, kitchen hot-water delay accepted, terrace about 50 mm lower | Anchors recomputed from the rebuilt plate segments (2 per post, 31 total); assembly SLAB - On Grade 4in with 39 members: 4 in slab, shower recess -51 mm at full thickness, thickened edge 12 x 16 in with the recess subtracted, 31 J-bolts, 5 PVC stub-ups; terrace lowered 50 mm; placeholder floor removed after checking its dependents; sheet S100 with the layout drawing and BOM |  |  |

## Lesson
The slab is the first prefab assembly on site: everything that lands on it (plates, posts, drains, water service) is already known from the panels and fixtures, so the slab layout is derived, not drawn.

## Rule
1) Take the slab edge from the framing outer faces and the anchor lines from the bottom-plate segments of the current wall panels; at door openings there is no plate and no anchor. 2) Place anchors per plate segment: max spacing and end distance from the engineer (assumed 1219 / 305 mm), at least two per segment, clear of stud axes. 3) Keep stub-ups out of the thickened edge and record them from one slab corner. 4) A curbless shower is a slab recess with the full slab thickness below it; subtract it from the edge beam where they meet. 5) Show the 2D layout and BOM for review, then model it as one assembly (slab floor, recess floor, edge as Structural Foundation DirectShape, bolts, stub-ups) and clash-check it against the wall assemblies: bolts through bottom plates are intended. 6) Re-derive the anchors whenever a wall panel is rebuilt.

## Validation
- Anchor report per plate segment: count, max gap, end distances, min distance to a stud axis
- Stub-ups outside the thickened edge (except where intended)
- Clash check against wall assemblies: only bolt x bottom plate / insulation
- Placeholder host dependents checked before deletion
