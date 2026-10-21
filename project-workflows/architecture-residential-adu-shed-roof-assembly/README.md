# ARPL-PW-0002: ADU shed roof assembly

Level 4 project workflow, recorded on ADU-01 (Revit 2024) on 2026-10-20. Builds on [ARPL-PW-0001](../architecture-residential-adu-fabrication-package/) (exterior wall panels).

Replace a placeholder shed roof with a real build-up and turn it into one roof assembly: 2x8 rafters @ 24in, pony wall on the high side, raked end infill, frieze blocks, outlookers and fly rafters, 3/4in plywood deck, standing seam roofing, 1x10 fascia and barge boards covering every exposed rafter cut, batts and drywall inside the wall lines, shop drawing and BOM with cost.

| Step | Work class | What | Packs |
|---|---|---|---|
| 1 | W8 | Read the roof as modelled before planning: type, slope, footprint, overhangs, height gap between flat wall plates and the sloped roof underside, neighbouring elements (e.g. a trellis under the eave) | ARPL-MCX-0001 |
| 2 | W4 | Ask the decisions that belong to the user: structure (rafters + pony wall vs trusses), member size (engineer flag), roofing for the slope (5 deg excludes asphalt shingles), overhangs, trim, soffit, insulation, assembly grouping | ARPL-SCH-0001, ARPL-ASM-0002 |
| 3 | W8 | 2D preview from the layout rule: framing plan, sheathing plan, section; check every view direction; look at the exported images | ARPL-QA-0001, ARPL-VIEW-0002, ARPL-VIEW-0001 |
| 4 | W5 | Replace the placeholder roof: new footprint roof with the real layers (Revit 2024 cannot edit roof sketches or attach walls by API), user re-attaches the walls, then delete the old roof; guard every transaction | ARPL-CHG-0002, ARPL-ADM-0001 |
| 5 | W1 | Component families: lumber types 2x8 / 2x4 flat; work-plane-based copies of sheet and insulation families; flex-test the plane orientation | ARPL-FAM-0005, ARPL-ASM-0006 |
| 6 | W3 | Build from one layout rule in a dry run with an all-pairs clash check; offset square-cut ends by depth x sin(slope); commit only with allow-listed contacts; trim must cover every exposed cut; insulation only inside the exterior wall lines | ARPL-ASM-0006, ARPL-ASM-0004, ARPL-ASM-0003 |
| 7 | W3 | Create the assembly after Regenerate; name it after commit | ARPL-ASM-0005 |
| 8 | W7 | BOM from the model: check every piece against its stock size; reset Cost and Type Comments on duplicated types; price with source and date; stock conversion, waste, tax, range | ARPL-SCH-0002, ARPL-ASM-0006 |
| 9 | W6 | Shop drawing: framing plan with deck hidden, deck layout, section along the slope, 3D, parts list, dimensions one per transaction, BOM note; export and look at the sheet | ARPL-DOC-0001, ARPL-DOC-0002 |

**Rules from the owner:**
- Insulation only inside the exterior wall lines; overhangs (eaves and rakes) are not insulated
- Exposed rafter and fly-rafter cuts are covered by fascia and barge boards
- Choose the cheapest build that meets the requirements, and flag what the engineer must confirm

**Decisions that belong to the user:** Structure system; Rafter size (engineer); Roofing material vs slope; Overhang depth; Fascia/barge size and drip edge; Open or closed soffit; Insulation type and ceiling; Assembly grouping.

**Discipline authority:** Structural engineer: rafter size, hurricane ties, pony wall bracing, header under the pony wall, trellis connection; Energy code: R-value of the roof insulation.

**Result:** 243 pieces in one assembly (ROOF - Shed 2x8), sheet W104, material estimate about USD 7,100 incl. tax (range 6,540-7,650).
