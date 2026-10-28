# ARPL-CRD-0002 rev 2: MEP spaces that exist but have no area: set the architectural (and facade) link types to Room Bounding in the MEP model

_Generated from this pack's files by tools/build_catalogs.py. Edit manifest.json, intent.md, vNN/ or final/rule.json instead._

| | |
|---|---|
| Level | 2 |
| Work class | W7 |
| Status | candidate |
| Use when | Space: Number / Space: Name are empty in MEP schedules although spaces are placed; Spaces report area 0 or 'Not enclosed' in a model that links the architecture |
| Not for | Moving, deleting or renumbering spaces: that needs the discipline lead; Overlapping space volumes (upper limit / offset): report them to the lead |
| Workflows | coordination, spatial-planning, links-coordinates |
| Disciplines | mechanical, electrical, plumbing, bim-vdc |
| Project types | generic |
| Revit tested | 2024 |
| API | RevitLinkType, BuiltInParameter.WALL_ATTR_ROOM_BOUNDING, SpatialElement.Area, FamilyInstance.Space |
| Failure patterns | FP56, FP11 |
| Contributors | Gottfried Schmidtke with Claude |

**Intent:** Let the MEP model's spaces find their boundaries in the linked architecture so equipment reports its space.

## Learning curve

| Version | Instruction | Result | Problem | Found by |
|---|---|---|---|---|
| v01 | In the Snowdon HVAC model: count spaces with area > 0 and instances with a Space; read Room Bounding on each link type. | 67 spaces, all placed, none enclosed; 0 of 1,576 instances in a space; Room Bounding = 0 on all five link types. |  |  |
| v02 | Set Room Bounding = 1 on the Architectural and Facades link types; accept the 'Space volumes overlap' warning; list the overlapping spaces; sync. | All 67 spaces enclosed; 1,383 of 1,576 instances report a space. Overlap between 101 Cafe and M100 Mezzanine Dining listed for the mechanical lead. | The commit raised a modal warning that blocked the bridge call (FP11/FP17). | screenshot after the call timed out |
| v03 | Owner decision: apply the same link setting in the Electrical and Plumbing models; read back spaces enclosed and instances with a space; sync. | Electrical: 80 of 80 spaces enclosed, 1,314 of 1,558 electrical instances in a space. Plumbing: 39 of 43 enclosed (four default-named spaces 2, 5, 12, 414 stay unenclosed, listed for the lead), 95 of 179 fixtures in a space: the plumbing model has fewer spaces than the architecture has rooms. | Fewer spaces than rooms leaves instances without a space even when every space encloses. | counting instances with a space per model |

## Lesson
A placed space with no area is usually a link that is not room bounding; fix the link type, not the spaces.

## Rule
1. Check spaces for area > 0 before reading Space fields; zero area everywhere points at the links.
2. Set Room Bounding on the link types that carry walls, floors and curtain walls (architecture, facades), not on MEP or structural links unless the lead asks.
3. Expect a 'Space volumes overlap' warning on commit; accept it and list the spaces for the lead instead of changing limits.
4. Read back: spaces enclosed, instances with a space; sync with a comment.
5. Apply the setting in every model that schedules Space fields (mechanical, electrical, plumbing); where a model has fewer spaces than the architecture has rooms, list the rooms without a space for the discipline lead instead of placing spaces.

## Validation
- Every space has area > 0 or is listed with a reason.
- Instances with a Space counted before and after.
