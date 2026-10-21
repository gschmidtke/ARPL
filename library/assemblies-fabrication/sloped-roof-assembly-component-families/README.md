# ARPL-ASM-0006 rev 6: Sloped roof assembly from component families

_Generated from this pack's files by tools/build_catalogs.py. Edit manifest.json, intent.md, vNN/ or final/rule.json instead._

| | |
|---|---|
| Level | 2 |
| Work class | W3 |
| Status | candidate |
| Use when | framing and finishing a sloped (shed, mono-pitch) roof as an assembly of lumber, sheet and board families; placing sheet goods, insulation or trim on a sloped plane; covering rafter tails and fly rafters with fascia and barge boards |
| Not for | prefabricated trusses modelled as single families; curved roofs |
| Workflows | assemblies-fabrication, family-authoring, validation-qaqc |
| Disciplines | construction, architecture, structural |
| Project types | residential, generic |
| Revit tested | 2024 |
| API | AssemblyInstance.Create, DirectShape, Document.NewReferencePlane, ElementIntersectsElementFilter, FAMILY_ALWAYS_VERTICAL, FAMILY_WORK_PLANE_BASED, FamilyPlacementType.WorkPlaneBased, GeometryCreationUtilities.CreateExtrusionGeometry, NewFamilyInstance(Reference, XYZ, XYZ, FamilySymbol), SolidOptions, StructuralFramingUtils.DisallowJoinAtEnd |
| Failure patterns | FP02, FP04, FP05, FP06, FP15 |
| Contributors | Gottfried Schmidtke with Claude |

**Intent:** one assembly for a 5 deg shed roof: 2x8 rafters @ 24in, fly rafters and outlookers, frieze blocks, 3/4in plywood deck, standing seam panels, 1x10 fascia and barge boards covering every exposed 2x8 cut, R-19 batts, 1/2in drywall. LOD 400 geometry + BOM data.

## Learning curve

| Version | Instruction | Result | Problem | Found by |
|---|---|---|---|---|
| v01 | Reuse RB_Sheet Panel / RB_Insulation Block (level-based, always vertical) for deck, batts, barge boards | Not possible: level-based families cannot tilt to the roof slope | Family placement type decides what orientations are possible | reading FAMILY_WORK_PLANE_BASED / FAMILY_ALWAYS_VERTICAL before building |
| v02 | Work-plane-based copies (WP) saved under new names so the 509 wall pieces stay untouched; reference plane through P with direction +X and cut vector +n | Sheet placed flipped: Height ran down-slope, Thickness pointed down | Instance Z = cutVec x direction, so the sign of the cut vector decides the orientation | flex test, transform and bounding box read back |
| v03 | Cut vector -n: instance X = +X, Y (thickness) = +n, Z (height) = up-slope; barge boards: direction = up-slope u, cut vector -X gives height square to slope and thickness +X | Bounding box equal to the computed target |  | flex test |
| v04 | Full build in a dry run with an all-pairs clash check (new pieces + wall assemblies) | 241 pieces; 12 kinds of contact | Square-cut ends of sloped members shift by depth x sin(slope): rafter tails 16 mm into the fascia, plywood 1.7 mm into fascia, batts 14 mm into frieze blocks, raked plate 3 mm into the pony plate; horizontal outlookers 4 mm above the sloped deck; rafters 1.7 mm into the north wall plywood top | ElementIntersectsElementFilter over all new pieces and wall members |
| v05 | Offset every square-cut end by depth x sin(slope), lower outlookers to the uphill edge, ribs on the pan top, trim north wall plywood 2 mm; commit only if no unexpected clash remains | Committed; only intended contacts remain (outlookers notched through end rafters; batts compressed under outlookers in the two end bays). Assembly ROOF - Shed 2x8, 241 members. Fascia and barge cover every rafter, fly rafter and outlooker end (checked by coordinates) |  | clash check + coordinate check + 3D image export |
| v06 | Quantities for the BOM read from the assembly members (cut lengths, Width x Height); prices set on the new types | Fixed: deck rows 2 and 4 rebuilt with joints at rafters 1-5-9-13-17 (pieces 1103 / 2440 / 2109 mm); types repriced with unit and source in Type Comments. Sheet W104 (framing plan, deck layout, section, 3D, parts list, dimensions, BOM note). Roof material estimate approx. USD 7,100 incl. 6.5% tax (range 6,540-7,650). | 1) The odd-row stagger started at rafter 5, giving deck pieces of 3543 mm, longer than a 2440 mm sheet; the clash check could not see it. 2) Types created by Duplicate() inherited Cost and Type Comments of the source type (batts, drywall, roofing and trim all said 'USD per 4x9 sheet plywood'). | BOM step: comparing modelled piece lengths with stock sizes; reading Cost/Type Comments of every type in the assembly |
| v07 | Outlookers 2x4 flat set level (horizontal), lowered 4 mm to their uphill edge so they stay under the sloped deck | Corrected: cross-section rotation +5 deg (STRUCTURAL_BEND_DIR_ANGLE), top centre on the rafter-top plane; top face normal (0, 0.087, 0.996) equals the roof normal; no contact with the deck | Level outlookers are not how they are built: they carry the deck and must lie in the roof plane, parallel to the rafters. The 'lower it to the uphill edge' fix hid the error instead of correcting it. | owner reviewing the section (outlookers drawn as level rectangles under a sloped deck) |
| v08 | Wedge between the flat wall plates and the sloped roof (south pony wall, east/west raked infill) framed only | Added 117 pieces to the roof assembly: XPS 2in+2in+1-1/2in between cripples, 3/4in plywood, siding courses continuing the wall pattern (plus one strip closing the 74 mm gap under the rafters on all walls), 1/2in gypsum inside; all cut to the rafter line. No clashes. | The wedge had framing but none of the exterior wall layers (no insulation, sheathing, siding or gypsum): wall panels and the Revit wall type both stopped at the plate. | owner looking at the section under the roof |
| v09 | Owner: 'a wall is a wall' - would a prefab manufacturer attach wedges under the roof, or build walls that fit the roof? Rebuild the walls to fit the roof | Roof assembly reduced to roof components (208). South panel rebuilt at 2808.6 (cap on the rafter bearing, 246 pieces); East and West raked panels (69 each, sloped plates, plywood/XPS/siding cut to the rafter line as DirectShapes). All clash-free after pulling the raked plate ends back 3.5 mm (38.1 x sin 5). | East and West shared one assembly type. Swapping the members of one instance opened a Revit dialog (not a failure, so the failure preprocessor could not answer it); the bridge call hung until the owner answered, and Revit then copied the East members over the West instance. | owner (design logic); bridge timeout and owner at the Revit dialog (FP15) |

## Lesson
Sloped assemblies need work-plane-based component families and an explicit orientation rule; on a slope every square-cut end moves by depth x sin(slope), which is where nearly all clashes came from.

## Rule
1) Check family placement type before reuse; make work-plane-based copies under new names. 2) Flex-test the plane orientation (cut vector sign) with one instance and read back the transform. 3) Compute every sloped member from one layout rule; offset square-cut ends by depth x sin(slope); members that carry the deck (outlookers, flat blocking) are rotated to the slope (cross-section rotation = slope angle; check the sign by the top-face normal), with their top on the rafter-top plane. 4) Dry-run the whole build with an all-pairs clash check and commit only when every remaining contact is on an allow-list of intended conditions. 5) Verify that trim covers every exposed cut by comparing end-face extents with trim extents. 6) Before documenting, check every modelled piece against its stock size (no piece longer than the sheet or board it is cut from). 7) After Duplicate(), reset Cost, Type Comments and other data parameters of every new type; duplicated types inherit them silently. 8) Insulation (batts, foam) runs only inside the exterior wall lines, bearing to bearing; eaves and rake overhangs are not insulated. 9) Walls are built to fit the roof, as a prefab plant would: no wedge or pony wall. The high wall is framed taller (cap at the rafter bearing), the end walls are raked (sloped double top plate, studs cut to it), and sheathing, insulation and siding are cut to the rafter line inside the wall panels. The roof assembly holds only roof components. 10) Before changing the members of an assembly instance, check whether its type is shared by other instances; if so, build a new assembly (AssemblyInstance.Create) instead, because Revit asks a modal question no script can answer and then copies the change to every instance (FP15). Box families cannot make sloped edges: use DirectShape extrusions with material and Comments/Mark for the BOM.

## Validation
- Flex test transform equals expected axes
- Clash check: only allow-listed contacts
- End faces of all rafters, fly rafters and outlookers inside fascia/barge extents
- Assembly member count equals pieces built
- No piece longer than its stock length
- Every type in the assembly has its own Cost and unit in Type Comments
- Insulation bounding box inside the outer face of the wall framing (ADU-01: batts y -1134.1..2456.2 within -1172.7..2494.8; x -3944.9..8002.7 within -3983..8040.8)
- Top-face normal of every deck-bearing member equals the roof normal
- Every exterior face below the roof is closed: framing, insulation, sheathing, siding and gypsum reach the rafter line on all walls
