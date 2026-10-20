# ARPL-CHG-0002 rev 1: Changing a footprint roof's outline by API in Revit 2024

_Generated from this pack's files by tools/build_catalogs.py. Edit manifest.json, intent.md, vNN/ or final/rule.json instead._

| | |
|---|---|
| Level | 2 |
| Work class | W5 |
| Status | candidate |
| Use when | changing the outline, overhangs or type of an existing footprint roof by script; replacing a placeholder roof with a real roof type while walls are attached to it |
| Not for | extrusion roofs; roofs edited by hand in sketch mode; Revit versions where wall attachment and roof sketch editing are available in the API (check before applying) |
| Workflows | model-change, geometry |
| Disciplines | architecture, construction |
| Project types | residential, generic |
| Revit tested | 2024 |
| API | FootPrintRoof, Document.NewFootPrintRoof, ModelCurveArray, SketchEditScope, FootPrintRoof.set_Offset, CompoundStructure |
| Failure patterns | FP05, FP14, FP10 |
| Contributors | Gottfried Schmidtke with Claude |

**Intent:** replace the placeholder shed roof (Generic 9", uneven overhangs) with a real build-up (standing seam, 3/4in plywood, 2x8 rafters, 241.4 mm) and even 450 mm overhangs, keeping the four exterior walls attached.

**Targets:** edges at x -4476.3 / 8534.1, y -1666 / 2988.1 mm; 5 deg slope from the north edge; roof bottom 2456.8 at the north edge (rafter bottom line through the north plate's outer top edge at 2500).

## Learning curve

| Version | Instruction | Result | Problem | Found by |
|---|---|---|---|---|
| v01 | SketchEditScope.Start(roof sketch id) to move the footprint lines | ArgumentException: Sketch does not support editing | Footprint roof sketches are not editable through SketchEditScope in Revit 2024 | exception on dry run |
| v02 | FootPrintRoof.set_Offset(edge, delta) per edge to push the outline | No change to the outline; only the elevation shifted by 3 mm | The per-edge offset is not a horizontal move of the footprint for sketched roofs | bounding box read back in dry run |
| v03 | Delete old roof + NewFootPrintRoof(ca, level, type, out mca) + Wall.AddAttachment | Wall.AddAttachment does not exist in the 2024 API (compile error); the next version without it threw ArgumentNullException in NewFootPrintRoof and crashed Revit (see ARPL-ADM-0001) | The out ModelCurveArray must be instantiated before the call; the unclosed transaction turned the exception into a crash | compile error; Revit journal after the crash |
| v04 | var mca = new ModelCurveArray(); NewFootPrintRoof(...) in a guarded using-transaction; slope on the north edge (SlopeAngle = tan 5 deg); base offset corrected by measuring the bounding box (-43.2 mm); old roof kept, hidden in the 3D view; walls pre-selected for the user | New roof exactly on target: bb -4476.3,-1666,2456.8 to 8534.1,2988.1,3106.3 | Walls still attached to the old roof; attachment must be done in the UI (Attach Top/Base), then the old roof deleted | bounding box read back |

## Lesson
Revit 2024's API cannot edit a footprint roof's sketch or attach walls to a roof. Changing the outline means a new roof, and the wall attachment is a user step.

## Rule
Create the new roof beside the old one (instantiate the out ModelCurveArray first), set slope and base offset, verify by bounding box, hide the old roof, pre-select the walls and ask the user to Attach Top/Base; delete the old roof only after the walls are attached to the new one.

## Validation
- Roof bounding box equals target edges and heights
- Every wall reports WALL_TOP_IS_ATTACHED = 1 and a top that follows the new roof
- Old roof deleted only after attachment
