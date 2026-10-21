# ARPL-CON-0002 rev 1: Residential branch circuits from a confirmed layout

_Generated from this pack's files by tools/build_catalogs.py. Edit manifest.json, intent.md, vNN/ or final/rule.json instead._

| | |
|---|---|
| Level | 3 |
| Work class | W3 |
| Status | candidate |
| Use when | electrical for a small dwelling unit or ADU: panel, receptacles, lighting, smoke alarms, circuits; placing wall and ceiling devices by API on host-wall faces and ceiling planes; creating circuits and a panel schedule by API |
| Not for | commercial distribution or three-phase systems; load calculations or code compliance sign-off (electrical engineer / AHJ); conduit or cable routing |
| Workflows | connectors-systems, family-authoring, parameters-data |
| Disciplines | electrical |
| Project types | residential |
| Revit tested | 2024 |
| API | HostObjectUtils.GetSideFaces, Document.Create.NewFamilyInstance(Reference, XYZ, XYZ, FamilySymbol), Document.Create.NewReferencePlane, ElectricalSystem.Create, ElectricalSystem.SelectPanel, PanelScheduleView.CreateInstanceView, PanelScheduleSheetInstance.Create, Application.NewFamilyDocument, ConnectorElement.CreateElectricalConnector |
| Failure patterns | FP05, FP17, FP18 |
| Contributors | Gottfried Schmidtke with Claude |

**Intent:** Electrical for a 475 sf ADU (dwelling unit, 2-burner cooktop, cooling only, 12 kW-class tankless): 100 A 120/240 V exterior load center fed from the main house, receptacles, lighting, smoke alarms and 10 circuits per NEC 2020 (Florida Building Code 8th ed.), panel schedule on the power plan sheet.

**LOD:** LOD 300 (devices and equipment as placeholders with electrical data)

## Learning curve

| Version | Instruction | Result | Problem | Found by |
|---|---|---|---|---|
| v01 | Author missing electrical families with Family Templates (no local Autodesk library: only the cloud 'Load Autodesk Family' dialog, not reachable by API) | 7 families authored, PowerBalanced connectors read back (240 V 2P 3600/11500/2400 VA, 120 V 1P) |  |  |
| v02 | Place wall devices on host-wall side faces (HostObjectUtils.GetSideFaces) with NewFamilyInstance(face reference, point, refDir, symbol); face list collected once | Receptacles and switches placed on the right faces | SEHException on the exterior light; the same call worked in isolation: face references collected before other devices were placed had gone stale after regeneration (FP18) | dry run, isolated test |
| v03 | Exterior wall light authored from 'Lighting Fixture.rft' and made work-plane-based | SEHException on face placement | Lighting Fixture template with a light source does not take face placement; rebuilt from 'Electrical Fixture.rft' with FamilyCategory switched to Lighting Fixtures | isolated test |
| v04 | Downlights (work-plane-based) placed level-based with an elevation offset | Stayed at floor level | Offset parameter ignored for that family; place on a horizontal reference plane at the ceiling (cut -Y gives normal +Z, trim below the plane) | bounding box read-back |
| v05 | Panel from the template's 208 V MLO panelboard with distribution system 120/240 Single | 'Selected distribution system type is invalid' | The family's supply connector is fixed at 208 V 3 poles; copy the family, set its connector to 240 V 2 poles, swap the type | error message, connector probe |
| v06 | Create circuits: ElectricalSystem.Create, then rating, then SelectPanel | Numbering 1/3, 2, 4 ... 11/13 as planned | Revit raised a modal 80 %-of-rating warning during Create, against the default 20 A, before the script could set the rating; the failures preprocessor did not see it, the bridge call blocked until the owner clicked OK (FP17). Also: a downlight type carried 0 VA | screenshot after a bridge timeout |

## Lesson
A residential electrical layout is a rule check first and a modelling task second; most failures came from content (template families built for commercial work) and from Revit dialogs outside the script's reach.

## Rule
1) Lay out devices in 2D first and check them against NEC 210.52 (wall spacing 1.83 m, counter 600 mm, bath basin 900 mm, front/back exterior, HVAC service receptacle 7.5 m) before modelling; the owner confirms. 2) Check what content exists; author missing families from Family Templates with PowerBalanced connectors (ARPL-CON-0001); wall-mounted ones from 'Electrical Fixture.rft' (switch category if needed), not from 'Lighting Fixture.rft'. 3) Place wall devices on host-wall side faces, fetching fresh face references for every placement (FP18); ceiling devices on a horizontal reference plane at the finished ceiling. 4) Before circuiting, probe the panel's supply connector (voltage, poles) against the distribution system; template commercial panelboards are 208 V 3-pole. Probe device loads (some types carry 0 VA). 5) Create circuits in the order of the planned numbering; for loads above 80 % of the default 20 A rating expect a modal warning during ElectricalSystem.Create (FP17): watch the screen, or create them with a temporary small load. 6) Place the panel schedule, export the sheet as an image and look at it; sync after the checks pass.

## Validation
- NEC 210.52 spacing checks pass on the 2D layout
- Every device placed within 2 mm of its face (report distance)
- Panel connector voltage/poles match the distribution system
- Circuit numbers equal the planned numbers; ratings and loads read back
- Panel schedule and sheet exported and inspected
