# ARPL-QA-0002 rev 1: LOIN completeness snapshot from an exported instance-parameter schedule: fill rate per model, field and category, family elements only

_Generated from this pack's files by tools/build_catalogs.py. Edit manifest.json, intent.md, vNN/ or final/rule.json instead._

| | |
|---|---|
| Level | 2 |
| Work class | W7 |
| Status | candidate |
| Use when | The client asks where the project stands on information requirements (LOIN) and every model carries the same instance-parameter schedule; A weekly report needs a completeness number and a ranked list of gaps |
| Not for | Checking values for correctness: this counts filled, not right; Type parameters that the schedule does not show per instance |
| Workflows | validation-qaqc, parameters-data, schedules-quantities |
| Disciplines | bim-vdc, generic |
| Project types | generic |
| Revit tested | 2024 |
| API | ViewSchedule, ScheduleDefinition, ViewSchedule.Export, Element.LookupParameter |
| Failure patterns | FP49 |
| Contributors | Gottfried Schmidtke with Claude |

**Intent:** Tell the client in one number, and in a short ranked list, how complete the model information is: export the same instance-parameter schedule from every model, count for each information column how many instances have a value, and report per model, field and category.

## Learning curve

| Version | Instruction | Result | Problem | Found by |
|---|---|---|---|---|
| v01 | Export the INSTANCE PARAMETERS schedule (Family, Category and the information columns Description and Type Mark; Structural also _Height and _Width) from all six models; count instances and filled values per model, category and field; rows with an empty Family are circuits, systems and analytical elements. | Overall 30.9% (13,110 of 42,396 required values) against a 95% target; by model 0.1% (Plumbing) to 51% (Architecture). Description filled on 1.5% of family elements, Type Mark on 64%; Plumbing has no Type Marks on 3,056 pipes and 2,656 fittings. 571 system and analytical instances counted separately. | No client LOIN table yet, so 'required' was assumed to be every information column of the schedule (FP49). The counting script was not kept; the method is recorded, the code is help wanted. | comparing the score with what the client actually asked for |

## Lesson
LOIN completeness is only meaningful against the client's requirement per category; until that table exists, state the assumption next to the number.

## Rule
1. Use one standard instance-parameter schedule in every model (same columns, Family and Category included); export it per model each week.
2. Count per model, category and information column: instances, and filled values (non-empty after trimming).
3. Count family elements only; rows without a family (circuits, systems, analytical elements) are reported separately, never in the score.
4. Required fields: the client's LOIN table per category and stage; until it exists, every information column, and say so beside the score.
5. Report: overall completeness (filled ÷ required values), a model × field grid, and the categories ranked by missing values (instances × unfilled fields).
6. Target per project (95% used as a placeholder); a model below it fails the LOIN rule in the weekly checks.

## Validation
- Instance totals per model equal the schedule row count.
- System and analytical rows excluded from the score and shown separately.
- The assumption about required fields is printed next to the score until a client LOIN table exists.
