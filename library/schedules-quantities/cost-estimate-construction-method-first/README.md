# ARPL-SCH-0001 rev 1: Cost estimate priced the wrong construction

_Generated from this pack's files by tools/build_catalogs.py. Edit manifest.json, intent.md, vNN/ or final/rule.json instead._

| | |
|---|---|
| Level | 2 |
| Work class | W7 |
| Status | candidate |
| Use when | estimating material or construction costs from a model; pricing wall, floor or roof types |
| Not for | - |
| Workflows | schedules-quantities, model-context |
| Disciplines | architecture, construction |
| Project types | residential |
| Revit tested | 2024 |
| API | ViewSchedule, ALL_MODEL_COST |
| Failure patterns | FP07, FP09, FP13 |
| Contributors | Gottfried Schmidtke with Claude |

**Intent:** Material cost of a small house

## Learning curve

| Version | Instruction | Result | Problem | Found by |
|---|---|---|---|---|
| v01 | Walls priced as poured concrete because the wall type was named 'Concrete 8"' | Estimate delivered | The intended construction was CMU (common in Florida); about $2,200 difference | user |
| v02 | Ask the construction method; re-price with CMU | Estimate corrected |  |  |

## Lesson
Type names describe a material, not a construction method.

## Rule
Ask the construction method before any cost or structural work.

## Validation
- Quantities from HOST_VOLUME_COMPUTED and HOST_AREA_COMPUTED
