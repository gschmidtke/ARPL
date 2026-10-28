# ARPL-BOM-0001: Bill of Materials from federated Revit models

**Version:** 1.2 · **Status:** candidate (category rules: *proposed*, to be confirmed by the BIM manager and the GC) · **Recorded:** 2026-10-28 (IN-0025)
**Machine-readable:** [bom-standard.json](bom-standard.json) · **Rules:** [category-rules.csv](category-rules.csv) · **Reference builder:** [build_bom.py](build_bom.py) · **Procedure pack:** ARPL-SCH-0003

## Purpose

Turn the governed instance data of a federation into quantities a general contractor can buy against. Every BOM line can be traced back to the model elements that make it up.

## Three levels, kept apart

| Level | Question | Who owns the rules | Built from |
|---|---|---|---|
| **QTO** | What is modelled? | model | the INSTANCE PARAMETERS export |
| **BOM** | What material and product quantities are required? | this standard (category rules) | QTO grouped by the BOM item key |
| **Procurement BOM** | What is actually ordered? | the GC | BOM + the GC item table (waste, purchase units, suppliers, packages) |

ARPL defines the first two levels. The third needs GC decisions (waste factors, stick or sheet sizes, vendors, packages), and ARPL does not invent those.

## Design decisions

1. **One source.** The BOM is built from the existing INSTANCE PARAMETERS export (ARPL-PAR-0003). There is no second Revit schedule: identity, classification, location and quantity fields are already there.
2. **Commercial data stays out of the model.** Supplier, waste factor, unit cost, lead time, procurement package, subcontractor and buyout status live in the GC item table (`datasets/gc_items.csv`), keyed by `bom_item_key`. Product data that belongs to the specification (manufacturer, model, catalog number) goes into the families at type level.
3. **The governed core is one rule table** (`category-rules.csv`). Per category and source discipline it sets the quantity basis (count, length, area, volume), the unit (EA, LF, SF, CY), the quantity field, the grouping fields that define one BOM item, and the required fields. A material condition separates, for example, concrete beams (CY) from steel framing (LF). The agent never infers a quantity basis.
4. **Each category is counted from one discipline.** Where a category is modelled twice (plumbing fixtures in Architecture and Plumbing, lighting fixtures in Architecture and Electrical), the rule table names the source discipline. Rows from the other model become exceptions, not double counts.
5. **Only the phases that are bought count** (default: New Construction). Existing elements are listed as exceptions.
6. **A part of a family is bought with its family, unless the rule table says the nested part is its own item.** Column `nested_parts`: `with_parent` (default; for example mullions inside a window family belong to the window) or `own_item` (Furniture: tables and chairs are separate entities, so chairs nested in a table family are their own BOM items). Nested parts keep their parent's instance key, so site staff find them under the parent. `with_parent` parts have no unique id of their own and are listed as exceptions "part of <parent key>", never silently dropped. `own_item` parts get their own unique id and element id (ARPL-PAR-0003) and are counted like any element. Standalone elements such as curtain wall mullions are their own BOM items, bought by length per profile.

## Pipeline

1. Read the INSTANCE PARAMETERS exports of all models (rows with a unique id).
2. Rows with an instance key but no unique id are nested parts: exception "part of <parent key>". Deduplicate the rest by unique id: one element can appear on several rows (FP55).
3. Drop elements outside the purchase phases.
4. Find the rule: category + source discipline (first letter of the instance key) + material condition. No rule → exception.
5. Quantity from the rule's field, in fixed units: lengths in feet (Revit's feet-inch text is parsed), areas in SF, volumes converted to CY. Unreadable → exception.
6. BOM item = rule + values of the grouping fields; key `<discipline>-<code>-<6-char hash of rule and signature>`. The key is stable as long as the grouping values do not change.
7. Aggregate per item: model quantity, instance count, elements missing a required field, breakdown by level.
8. Trace: one row per element (item key, model, unique id, instance key, level, room or space, quantity).
9. Reconcile: elements read = elements traced + exceptions; each line's quantity = the sum of its trace.

## Datasets (`datasets/`, header rows only)

| File | One row per | Columns |
|---|---|---|
| `bom.csv` | BOM item | bom_item_key, discipline, category, rule_id, item_signature, unit, model_quantity, instance_count, missing_required, by_level |
| `bom_trace.csv` | model element in a BOM line | bom_item_key, source_model, snow_uniqueid, snow_instelemid, level, room_or_space, quantity |
| `bom_exceptions.csv` | element not in the BOM | source_model, snow_uniqueid, category, reason |
| `gc_items.csv` | BOM item (GC-owned) | bom_item_key, bom_description, spec_section, manufacturer, model, catalog_no, purchase_unit, purchase_size, waste_factor, supplier, procurement_package, subcontractor, unit_cost, lead_time_days, buyout_status |

The procurement quantity is computed by the GC: `model_quantity × (1 + waste_factor)`, rounded up to `purchase_size` in `purchase_unit`. ARPL does not compute it without a filled GC item table.

The project prefix (`SNOW_` on Snowdon) is a parameter of the builder (`--prefix`).

## Validation

- No unique id appears twice in the trace.
- Elements read = elements traced + exceptions, and every exception has a reason.
- Each BOM line's quantity equals the sum of its trace rows.
- Lines with `missing_required` > 0 are listed for the owning discipline.
- Every category in the export has a rule or a deliberate exception reason.
- Category rules marked `proposed` are not used for buyout until the BIM manager and the GC confirm them.

## Open decisions (BIM manager / GC)

- Confirm or change the category rules, in particular: quantity basis for mullions, railings and steel columns (length is not exported today, so they are counted); concrete in CY; site, planting and parking (no rule yet).
- Which classification groups the procurement packages (Uniformat, OmniClass, MasterFormat / spec sections).
- Which product fields become required at type level (manufacturer, model, catalog number).

## Change log

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-10-28 | First recorded (IN-0025) |
| 1.2 | 2026-10-28 | Owner: tables and chairs are separate entities. Rule column `nested_parts` (with_parent / own_item); Furniture own_item; nested chairs get their own ids (IN-0027) |
| 1.1 | 2026-10-28 | Owner: window mullions are part of the window; curtain wall mullions are standalone. Curtain wall mullions bought by length (SNOW_Length bound and filled); nested parts listed as "part of <parent key>" instead of silently dropped; Flex Ducts code FX (IN-0026) |
