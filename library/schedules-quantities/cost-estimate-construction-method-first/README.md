# ARPL-SCH-0001: Cost estimate priced the wrong construction

| | |
|---|---|
| Level | 2 |
| Work class | W7 |
| Workflows | schedules-quantities, model-context |
| Disciplines | architecture, construction |
| Project types | residential |
| Revit tested | 2024 |
| Status | candidate |

**Intent:** Material cost of a small house

## Learning curve

| Version | Instruction | Result | Problem |
|---|---|---|---|
| v01 | Walls priced as poured concrete because the wall type was named 'Concrete 8"' | Estimate delivered | The intended construction was CMU (common in Florida); about $2,200 difference |
| v02 | Ask the construction method; re-price with CMU | Estimate corrected |  |

## Lesson
Type names describe a material, not a construction method.

## Rule
Ask the construction method before any cost or structural work.

## Validation
- Quantities from HOST_VOLUME_COMPUTED and HOST_AREA_COMPUTED
