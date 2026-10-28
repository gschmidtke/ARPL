# ARPL-SCH-0003 rev 4: BOM from governed instance data: deduplicated QTO grouped by a category rule table, every line traced to its model elements (implements ARPL-BOM-0001)

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
| Failure patterns | FP01, FP06, FP49, FP55, FP60 |
| Contributors | Gottfried Schmidtke with Claude |

**Intent:** Give the GC a bill of materials it can buy against, built from the same instance-parameter export the coordinator already collects every week, with every line traceable to the model elements behind it, and nothing counted twice or lost.

## Learning curve

| Version | Instruction | Result | Problem | Found by |
|---|---|---|---|---|
| v01 | Prototype on the six Snowdon exports of 2026-10-28 14:50: deduplicate by SNOW_UniqueId, group pipes by system class, material and size, framing by section and material, doors and fixtures by Type Mark. | Plumbing pipe: Domestic Cold Water copper 1" 5,348 LF, 1/2" 1,288 LF; framing 16K6 5,758 LF, W18x55 3,554 LF; WATERCLOSET-001 36 EA; DOOR-027 25 EA. All 3,056 pipe lengths parse from Revit's feet-inch text. | Structural framing holds steel (LF) and concrete beams (CY); plumbing and lighting fixtures are modelled in two models; Facades is phase Existing. Grouping by category alone would mix units, double count and buy existing work. | inspecting quantities per category and model |
| v02 | Category rule table (47 rules: category, source discipline, material condition, quantity basis, unit, field, grouping, required fields), purchase-phase filter, reference builder standards/bom/build_bom.py with reconciliation. | 17,783 unique elements: 16,713 traced into 486 BOM lines (334 EA, 86 SF, 45 LF, 21 CY), 1,070 exceptions with reasons (559 counted from the other discipline's model, 256 existing phase, 205 no rule: site, planting, parking, 45 curtain panels without area, 5 non-concrete structural floors). Every line equals the sum of its trace; elements read = traced + exceptions. |  | reconciliation built into the builder |
| v03 | Owner: mullions inside a window family are part of the window; curtain wall mullions are standalone. Bind SNOW_Length to Curtain Wall Mullions in the Architectural model, fill it from the element length, add it to INSTANCE PARAMETERS, set the mullion rule to LF; list nested parts instead of skipping them. | 1,425 curtain wall mullions filled (5,110 LF, 13 profile lines). 679 nested part rows now listed as 'part of <parent key>' (generic models in Architectural and Facades families, chairs in table families, structural connections). 486 BOM lines (321 EA, 86 SF, 58 LF, 21 CY), reconciled. | v02 dropped nested parts silently: the builder read only rows with a unique id, and nested parts have none, so they were outside the reconciliation. A first fix by element code flagged the 31 flex ducts wrongly, because the rule code DU did not match their key code FX. | comparing keys shared in the export (rows) with keys shared among unique elements (zero); code-versus-key check per category |
| v04 | Owner: tables and chairs are separate entities. Rule column nested_parts (with_parent / own_item), Furniture own_item; fill SNOW_UniqueId and SNOW_ElementId on the 102 nested chairs in the Architectural model (key stays the table's); export; rebuild. | Chair-Breuer 102 EA as its own line, every chair traced under its table's key; tables counted separately; 487 lines (322 EA, 86 SF, 58 LF, 21 CY), reconciled. | The table types carry Type Marks CHAIR-002 and CHAIR-003: the ZEN Type Marks run with the search string 'Chair' also matched the family 'Table-Dining Round w Chairs' (ARPL-PAR-0004 rule 4). | reading the furniture lines of the BOM |
| v05 | Railings by length per type and stairs per stair with risers and run width: new shared parameters SNOW_StairRisers / SNOW_StairWidth (created through the Revit API so Revit writes the file), SNOW_Length bound to Railings; filled in the Architectural model; schedule fields added; builder lists every row it does not use. | 131 railings by length (for example _IBC-Pipe-Plate Stringer 349.8 LF, Pipe-Wall Mount 289.7 LF); 26 stairs grouped by type, risers and width; 1,862 system rows and sub-elements now listed (circuits, wall sweeps, duct systems, stair supports); 497 lines (312 EA, 86 SF, 78 LF, 21 CY), every input row reconciled. | A railing type 'Road Striping' (20 elements) came out as 625 LF of railing: a category used for something else (FP01). Stair runs, landings and supports had been skipped silently (FP60, second observation). | reading the railing lines; counting rows read against rows in the export |

## Lesson
A BOM is a deterministic grouping of deduplicated instance data under a governed rule table. Every input row ends in a BOM line or a named exception. Parts follow the unit the trade buys. The export must carry the quantity the trade buys by. Wrong categories surface as BOM lines.

## Rule
1. Input: the INSTANCE PARAMETERS export of every model, with instance key and unique id (ARPL-PAR-0003).
2. Read every non-blank row; rows with no id and no key are system rows or sub-elements (exception). Nested parts follow the rule column nested_parts: with_parent parts (instance key, no unique id) are listed as 'part of <parent key>'; own_item parts (for example chairs in a table family) carry their own ids and are counted; deduplicate the rest by unique id before counting (FP55). No row leaves the reconciliation silently (FP60).
3. Keep only the purchase phases (default New Construction); existing work is an exception.
4. Take quantity basis, unit, quantity field, grouping and required fields only from the category rule table of ARPL-BOM-0001; match on category, source discipline (first letter of the instance key) and material condition.
5. A category modelled in two disciplines is counted from the discipline the table names; the other rows are exceptions.
6. Convert units explicitly: Revit feet-inch text to feet, CF to CY.
7. Write the BOM, a trace row per element and an exceptions list with a reason per element; reconcile before handing anything over.
8. Leave procurement quantities (waste, purchase units, suppliers, packages) to the GC item table; do not invent them.
9. The element codes in the rule table equal the codes of the instance keys (ARPL-PAR-0003); check them per category before the first run.
10. Before the first run, check that the export carries the quantity each trade buys by (length for mullions and railings, risers and width for stairs); add mirrored parameters where it does not (ARPL-PAR-0003).

## Validation
- No unique id twice in the trace
- Elements read = traced + exceptions
- Each line's quantity = sum of its trace
- Rules marked proposed are flagged until the BIM manager and GC confirm them
