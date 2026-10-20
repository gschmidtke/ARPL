# ARPL-PW-0001: ADU exterior wall fabrication package

Level 4 project workflow: a sequence of canonical packs, each step tagged with its work class.

| Step | Work class | What | Packs |
|---|---|---|---|
| 1 | W1 | Build and flex-test component families (lumber, sheet panel, insulation block, siding board) | ARPL-FAM-0005, ARPL-FAM-0003 |
| 2 | W3 | Write the layout rule (studs 16in o.c., 3-stud corners, double top plate lapped, openings with king/jack/header/sill/cripples, sheets on stud centres, siding courses, foam per cavity) | ARPL-ASM-0001, ARPL-ASM-0002 |
| 3 | W8 | 2D preview from the rule: studs in plan, sheet and board joints in elevations; user confirms or corrects the rule | ARPL-QA-0001 |
| 4 | W5 | Resolve design conflicts found by the preview as user decisions (door lowered to fit a header) and re-preview | ARPL-ASM-0002 |
| 5 | W3 | Replay the rule in 3D per wall; disallow joins on all framing; verify every piece; group into assemblies | ARPL-ASM-0003, ARPL-ASM-0004, ARPL-ASM-0005 |
| 6 | W6 | Assembly shop drawings: framing and sheathing elevations, plan section, 3D, part list; trade dimension style; PDF review | ARPL-DOC-0001, ARPL-DOC-0002, ARPL-VIEW-0001 |
| 7 | W7 | Quantities and cost from the model; governed BOM parameters | ARPL-SCH-0001, ARPL-SCH-0002 |

**Decisions that belong to the user:** Member sizes and spacing; Insulation material; Sheet size (4x8 + blocking or 4x9 cut); Minimum remnant width; Conflicts at openings (door height vs. wall height); Siding grade for pricing.

**Discipline authority:** Header sizing over wide openings: structural engineer.
