# ARPL-ASM-0007 rev 1: Device placement follows the framing (manufacturer's standpoint)

_Generated from this pack's files by tools/build_catalogs.py. Edit manifest.json, intent.md, vNN/ or final/rule.json instead._

| | |
|---|---|
| Level | 2 |
| Work class | W3 |
| Status | candidate |
| Use when | placing receptacles, switches, lights, smoke alarms, floor boxes or other devices in framed walls, roofs or floors; layout previews for prefab wall, roof or floor panels |
| Not for | devices on concrete or masonry without framing (use slab sleeve / chase rules); deciding code compliance (the code checks still apply) |
| Workflows | assemblies-fabrication, connectors-systems |
| Disciplines | electrical, architecture, structural |
| Project types | residential, generic |
| Revit tested | 2024 |
| API | FamilyInstance.Host, LocationCurve, ElementTransformUtils.MoveElement |
| Failure patterns | FP05 |
| Contributors | Gottfried Schmidtke, Claude (Anthropic) |

**Intent:** Place receptacles, switches, lights and other devices from the manufacturer's standpoint: in the stud, rafter or joist bay where the panel shop would put them, so the drawings stay true from layout to rough-in.

**LOD:** LOD 300-400

## Learning curve

| Version | Instruction | Result | Problem | Found by |
|---|---|---|---|---|
| v01 | ADU-01 electrical: receptacles, switches, lights and smoke alarms placed from the NEC rules and the room layout; framing considered only at rough-in | Code-compliant layout confirmed by the owner and modelled | 9 of 14 ceiling devices on or next to a rafter, 4 wall boxes on a stud; every one had to be moved after modelling, and the layout preview had to be re-checked | distance check against stud and rafter axes before adding rough-in (see ARPL-CON-0002 v07) |

## Lesson
A layout that satisfies the code but ignores the framing is not buildable as drawn; the fabricator moves the device, and the drawings become wrong.

## Rule
Place every device the way the panel manufacturer would build it: the framing is part of the layout from the first preview, not a correction at rough-in. 1) Build the layout preview on top of the framing layout (studs, plates, headers, rafters or joists, blocking, sheathing joints), not on the room outline alone. 2) Walls: box beside a stud, never on it (single-gang centre 47 mm from the stud axis, 2-gang and round boxes 75 mm), on the side that keeps the cavity widest; keep clear of corner and king/jack studs, headers, plates and sheathing joints; one standard height per device type (receptacles 300 mm, counter 1,100 mm, switches 1,220 mm) unless the code or the owner says otherwise. 3) Roofs and ceilings: devices centred in the rafter or joist bay where the room allows; minimum clearance 19 mm + device radius + 10 mm from the member axis; driver and junction boxes inside the same bay. 4) Floors: floor boxes, registers and drains in the joist bay (or in planned slab sleeves), never through a joist or beam. 5) Prefer devices on prefab panels in bays that are open in the factory; group devices so one bay or one wire run serves several. 6) After moving a device for the framing, re-run the code checks (NEC spacing) before modelling.

## Validation
- Every wall box ≥ required distance from every stud axis (report the minimum)
- Every ceiling device ≥ clearance from every rafter or joist axis and inside its room
- NEC spacing checks still pass after framing moves
- Rough-in clash check: only soft layers cut
