# ARPL-SCH-0003 rev 1: BOM from governed instance data: deduplicated QTO grouped by a category rule table, every line traced to its model elements (implements ARPL-BOM-0001)

_Generated from this pack's files by tools/build_catalogs.py. Edit manifest.json, intent.md, vNN/ or final/rule.json instead._

| | |
|---|---|
| Level | 2 |
| Work class | W7 |
| Status | candidate |
| Use when | A GC or estimator needs quantities to buy against from a federation that exports a standard instance-parameter schedule with instance keys; A quantity must be traced back to the model elements that make it up |
| Not for | Procurement quantities (waste, purchase units, suppliers): those need the GC item table; Projects without instance keys or unique ids in the export: run ARPL-PAR-0003 first |
| Workflows | schedules-quantities, parameters-data |
| Disciplines | bim-vdc, construction, generic |
| Project types | generic |
| Revit tested | 2024 |
| API | ViewSchedule.Export, Element.UniqueId |
| Failure patterns | FP55, FP06, FP49 |
| Contributors | Gottfried Schmidtke with Claude |

**Intent:** Give the GC a bill of materials it can buy against, built from the same instance-parameter export the coordinator already collects every week, with every line traceable to the model elements behind it, and nothing counted twice or lost.

## Learning curve

| Version | Instruction | Result | Problem | Found by |
|---|---|---|---|---|
| v01 | Prototype on the six Snowdon exports of 2026-10-28 14:50: deduplicate by SNOW_UniqueId, group pipes by system class, material and size, framing by section and material, doors and fixtures by Type Mark. | Plumbing pipe: Domestic Cold Water copper 1" 5,348 LF, 1/2" 1,288 LF; framing 16K6 5,758 LF, W18x55 3,554 LF; WATERCLOSET-001 36 EA; DOOR-027 25 EA. All 3,056 pipe lengths parse from Revit's feet-inch text. | Structural framing holds steel (LF) and concrete beams (CY); plumbing and lighting fixtures are modelled in two models; Facades is phase Existing. Grouping by category alone would mix units, double count and buy existing work. | inspecting quantities per category and model |
| v02 | Category rule table (47 rules: category, source discipline, material condition, quantity basis, unit, field, grouping, required fields), purchase-phase filter, reference builder standards/bom/build_bom.py with reconciliation. | 17,783 unique elements: 16,713 traced into 486 BOM lines (334 EA, 86 SF, 45 LF, 21 CY), 1,070 exceptions with reasons (559 counted from the other discipline's model, 256 existing phase, 205 no rule: site, planting, parking, 45 curtain panels without area, 5 non-concrete structural floors). Every line equals the sum of its trace; elements read = traced + exceptions. |  | reconciliation built into the builder |

## Lesson
A BOM is a deterministic grouping of deduplicated instance data under a governed category rule table; anything that does not fit becomes a named exception, never a guess.

## Rule
1. Input: the INSTANCE PARAMETERS export of every model, with instance key and unique id (ARPL-PAR-0003).
2. Deduplicate by unique id before counting (FP55).
3. Keep only the purchase phases (default New Construction); existing work is an exception.
4. Take quantity basis, unit, quantity field, grouping and required fields only from the category rule table of ARPL-BOM-0001; match on category, source discipline (first letter of the instance key) and material condition.
5. A category modelled in two disciplines is counted from the discipline the table names; the other rows are exceptions.
6. Convert units explicitly: Revit feet-inch text to feet, CF to CY.
7. Write the BOM, a trace row per element and an exceptions list with a reason per element; reconcile before handing anything over.
8. Leave procurement quantities (waste, purchase units, suppliers, packages) to the GC item table; do not invent them.

## Validation
- No unique id twice in the trace
- Elements read = traced + exceptions
- Each line's quantity = sum of its trace
- Rules marked proposed are flagged until the BIM manager and GC confirm them
