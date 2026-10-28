# ARPL-PAR-0003 rev 1: LOIN instance schedule per discipline: mirror category values into project parameters and give every instance a contractor key (discipline, element code, room or level, number)

_Generated from this pack's files by tools/build_catalogs.py. Edit manifest.json, intent.md, vNN/ or final/rule.json instead._

| | |
|---|---|
| Level | 2 |
| Work class | W7 |
| Status | candidate |
| Use when | A client or project requires an information delivery per discipline (LOIN, ISO 19650 / ISO 7817-1) and a weekly dataset is read from one standard instance schedule per model; Contractors, bidders or site staff need to name one instance unambiguously (this door, not the door type); The multi-category schedule cannot show a category-specific value (voltage, flow, fire rating, element id) |
| Not for | Type identification: Type Mark stays the type key (see ARPL-PAR-0004); Asset tagging for operations, where the client gives its own asset code scheme |
| Workflows | parameters-data, schedules-quantities, validation-qaqc |
| Disciplines | bim-vdc, architecture, structural, mechanical, electrical, plumbing, generic |
| Project types | generic |
| Revit tested | 2024 |
| API | ViewSchedule.CreateSchedule, ScheduleDefinition.GetSchedulableFields, InstanceBinding, GroupTypeId.IdentityData, Document.GetRoomAtPoint, RevitLinkInstance.GetTransform, FamilyInstance.Room, FamilyInstance.MEPModel, ElectricalSystem, BuiltInParameter.RBS_ELEC_VOLTAGE, SynchronizeWithCentralOptions |
| Failure patterns | FP06, FP22, FP55, FP57 |
| Contributors | Gottfried Schmidtke with Claude |

**Intent:** Deliver one uniform dataset per model each week that carries what the assumed LOIN requires per discipline, and give every instance a readable key a contractor can use on site, without overwriting keys once given.

## Learning curve

| Version | Instruction | Result | Problem | Found by |
|---|---|---|---|---|
| v01 | Derive per-discipline information requirements from ISO 7817-1 (purpose, milestone, actor, object; identification and information content) into a workbook (fields, schedule per discipline, requirement per stage, decisions); project prefix SNOW_; classification by both Uniformat (Assembly Code) and OmniClass. | Workbook with fields per discipline; 25 project parameters defined; built-in values that the multi-category INSTANCE PARAMETERS schedule cannot show (category-specific built-ins, element id, unique id, phase created) mapped to mirror parameters. |  |  |
| v02 | Bind the project parameters as instance parameters to the categories of each discipline; rebuild each model's INSTANCE PARAMETERS schedule from the field list; fill mirrors and the key SNOW_InstElemId = <discipline>-<element code>-<room number or level>-<nnn>; location: the element's own room (FamilyInstance room / to-room / from-room), then a room of the model at the element point, then a room of the architectural link at the transformed point, then its level; first room found wins; skip any element that already has a key. | 17,928 instances keyed across six models, synced and closed. Facades first produced NOLEVEL keys on face-hosted generic models; fixed before sync by taking the host's level, then the level below the element. | Face-hosted families report no level of their own. The Architectural fill commit ran about 3 minutes and outlived the 60 s call (FP22). | reading keys back before sync; screenshot of 'Committing Transaction' |
| v03 | Export the schedules with ZEN ACC Gate and check the CSVs: headers, keyed rows, duplicate keys, fill rate per field. | Headers correct in all six. Architectural showed 3 duplicate keys: each a multi-level stair exported twice with the same element id (FP55), not a real duplicate. Electrical voltage 0% (the value lives on the circuit, FP57); HVAC space number 0% (spaces not enclosed, see ARPL-CRD-0002). Unkeyed rows: nested components, sub-elements and systems. | Counting rows instead of unique ids overstates duplicates. | grouping duplicate keys by element id |
| v04 | Fill voltage from the element's power circuit (ElectricalSystem voltage), load from the family's own Apparent Load / Load or the sum of the panel phase loads. | Electrical voltage filled on 1,404 of 1,558 instances (circuit 1,389, family 15), load on 1,329; the rest are data devices and uncircuited elements. |  |  |

## Lesson
The schedule shows only what the instance itself holds: mirror the values the data needs into project parameters, key every instance once, and count the export by unique id.

## Rule
1. Write the assumed LOIN per discipline first (ISO 7817-1 structure), with the stage each field is required at; the client's table replaces it when it exists.
2. Keep one INSTANCE PARAMETERS schedule per model with the fields of its discipline, Category, Family, Type, the key and the unique id first.
3. Mirror into project-prefixed instance parameters every value the multi-category schedule cannot show: element id, unique id, phase created, category-specific built-ins; electrical values come from the circuit, not the family.
4. Instance key: <discipline letter>-<element code>-<location>-<nnn>; location = room number of the first room found (own room, model room at point, architectural link room at transformed point), else the level name as written in the model, else the host level, else the level below.
5. Number per discipline, code and location from the next free number; never overwrite a key that exists; nested components and sub-elements get none (they belong to their parent).
6. Run fills in batches (about 2,000 elements, a 25 s budget per call) and check state after any timeout before running again; sync with a comment only after a clean commit, relinquish, close.
7. When reading the export, count unique ids, not rows; report nested, subcategory and system rows separately.

## Validation
- Keys in the model are unique (count by element).
- Every keyed row in the export has a unique id; duplicate rows share it.
- Fill rate per field and discipline reported against the LOIN table, with the assumption stated.
