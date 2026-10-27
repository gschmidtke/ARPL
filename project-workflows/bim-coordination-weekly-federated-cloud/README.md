# ARPL-PW-0003: Weekly BIM coordination of a federated cloud project

Level 4 project workflow for the coordinator role: a sequence of packs, each step tagged with its work class. **Status: candidate, designed but not yet run end to end.**

| Step | Work class | What | Packs |
|---|---|---|---|
| 1 | W8 | Preflight: application idle, bridge alive, disk and cloud cache space, registry compared with the cloud folder (new or renamed models), no model open | ARPL-ADM-0002, ARPL-ADM-0003 |
| 2 | W8 | Collect in batch (unattended): per-model health export, link and workset report, schedule exports, family size report; raw outputs to REPORTS/<date> | - |
| 3 | W8 | Collect deep, read-only: warnings by type, link status and transform, ProjectPosition against the authority, Project Information keys, element counts; open each model with all worksets closed | ARPL-LNK-0002, ARPL-LNK-0001 |
| 4 | W8 | Check: one dataset keyed by model and week, compared with last week, against the rule table | - |
| 5 | W5 | Correct: safe fixes automatically (repair links to the matrix, missing building name, missing standard schedules, sync); anything that moves geometry, changes coordinates or deletes waits for the coordinator's approval | ARPL-LNK-0002, ARPL-ADM-0003 |
| 6 | W7 | Report: dashboard pages (project health, federation, model quality, data quality) and a one-page summary | - |
| 7 | W7 | Archive: append the week to history tables; never edit raw outputs; submit new lessons to the inbox | - |

## Rule table (starting thresholds)

| Check | Rule | Fix |
|---|---|---|
| Links complete | Every host has each link its matrix defines, none missing or duplicated | auto (repair from matrix) |
| Links in place | Every link instance placed by shared coordinates; when all models share one coordinate system and one internal origin, the link transform is identity | approval |
| Coordinates | Shared origin and angle equal the authority model, tolerance 0.01 ft | approval |
| Model identity | Building name equals the registry key; no template placeholder text | auto |
| Warnings | Count up more than 10% week over week, or a new warning type | report |
| File size | Over 300 MB or up more than 15% in a week | report; purge for approval |
| Families | Any family over 5 MB; in-place count rising | report |
| Parameter completeness | Required fields filled in at least 95% of instances per category | report |
| Sheets | Sheet numbers unique; sheets without views flagged | report |
| Worksets | Links on their own link worksets; elements on the default workset below a set limit | approval |
| Standards | Standard schedules and view templates present | auto |
| Registry | Every model in the cloud folder has a registry row, and the reverse | approval |

**Guardrails:** collection is read-only. The agent alone: collection, analysis, reporting, link repair to the matrix, missing building name, missing standard schedules, sync after a successful fix. Coordinator approval: re-placing links, applying coordinates, moving elements between worksets, purge, registering new models, any delete. Never automated: matrix or registry rules, the authority model, anything another user has borrowed.

**Decisions that belong to the user:** Required parameters per category for the fill-rate check; Thresholds of the rule table; Dashboard delivery (in-session dashboard or an external BI tool); Approval of every geometry, coordinate, workset or delete fix.

**Packs still to be written (help wanted):** registry-vs-cloud-folder-check, read-only-model-snapshot-worksets-closed, coordination-rule-table. Intake: IN-0016 (PR #7).
