# ARPL-PAR-0004 rev 1: Type Marks with ZEN Type Marks by Family: one run per family group, the search string becomes the prefix, Overwrite on for a clean re-run

_Generated from this pack's files by tools/build_catalogs.py. Edit manifest.json, intent.md, vNN/ or final/rule.json instead._

| | |
|---|---|
| Level | 2 |
| Work class | W7 |
| Status | candidate |
| Use when | A model has no or inconsistent Type Marks and the types can be grouped by a word in the family name; Type Marks must be redone after the grouping changed |
| Not for | Pipe, duct and fitting system types (no family-name group); leave them or mark them by system; Firm-specific code lists that do not follow family names: enter the code as the search string only if family names contain it |
| Workflows | parameters-data, model-administration |
| Disciplines | plumbing, generic, bim-vdc |
| Project types | generic |
| Revit tested | 2024 |
| API | RevitCommandId.LookupCommandId, UIApplication.PostCommand, BuiltInParameter.ALL_MODEL_TYPE_MARK |
| Failure patterns | FP41, FP58 |
| Contributors | Gottfried Schmidtke with Claude |

**Intent:** Give every type in use a readable sequential Type Mark per family group with ZEN, in a way that can be re-run.

## Learning curve

| Version | Instruction | Result | Problem | Found by |
|---|---|---|---|---|
| v01 | ZEN > Families > Type Marks by Family (command id CustomCtrl_%CustomCtrl_%ZEN%Families%CmdAssignTypeMarksByFamilyName) in the Snowdon Plumbing model; one run with the list Drain;Sink;Shower;Washer;WaterCloset;Hose Bib;Water Heater;BuildingConnection;Valve;Meter, start 1, Overwrite off. | Ran; result not read back. The owner pointed out that the default AUD (Audio) is the code of one run and must be replaced by the group's code per run. | A combined list in one run gives no group-wise numbering. | owner review |
| v02 | One run per search string, Overwrite on, start 1; read the ZEN summary after each run (prefix used, matched, assigned, skipped, sample updates); read Type Marks back; sync with the list of runs in the comment. | Prefix = search string in capitals with spaces removed (DRAIN-001, HOSEBIB-001). All 26 fixture, equipment and valve types in use marked, no duplicate marks; ZEN also marks unused types that match. 'Water Closet - Flush Valve' matched Valve, not WaterCloset (space in the name). | The dialog needs a click on OK and then Enter; clicks sent before the dialog appears are lost (FP41). | ZEN summary per run and read-back |

## Lesson
In ZEN Type Marks by Family the search string is the prefix: run once per group, Overwrite on, and check that family names really contain the string.

## Rule
1. List the types in use and group them by a word every family name of the group contains; agree the group strings (they become the prefixes) with the owner or discipline lead.
2. Run Type Marks by Family once per group: replace the default AUD with the group's string, start 1, Overwrite on for a re-run.
3. Read the ZEN summary of each run (prefix, matched, assigned, skipped) before the next run.
4. Watch names with spaces or other spellings ('Water Closet' vs 'WaterCloset'): the first group whose string matches takes the type.
5. Read back all Type Marks in use and check for duplicates; then sync with the runs listed in the comment.

## Validation
- Every type in use in the target categories has a Type Mark.
- No Type Mark is used by two types.
- Each prefix corresponds to an agreed group string.
