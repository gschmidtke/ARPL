# ARPL-PW-0003 rev 4: Weekly BIM coordination of a federated cloud project

Level 4 project workflow for the coordinator role: a sequence of packs, each step tagged with its work class and the tool used in the recorded runs. **Status: candidate, run end to end once on two projects (2026-10-27).** First runs are baselines; trend rules start with the second run.

## Sequence

| Step | Work class | What | Tool used | Without that tool | Packs |
|---|---|---|---|---|---|
| 1 | W8 | Preflight: Revit idle at Home with no model open (ask before closing the user's work), bridge alive, disk and collaboration cache space, registry compared with the cloud folder (new or renamed models), report folder REPORTS/<date> created | RevitBridge; ZEN registry CSV | registry as a plain CSV of model name, project and model GUIDs | ARPL-ADM-0002, ARPL-ADM-0003 |
| 2 | W8 | Collect in batch (unattended): Model Health Check and PBP + Worksets report over all registry models, then Export Schedules (instance parameters, project information, sheet list); output folder typed explicitly | ZEN ACC Gate started by PostCommand | bridge script that opens each cloud model with link worksets closed and writes the same fields (warnings by type, views, sheets, links, groups, levels, grids) and the schedule rows | ARPL-ADM-0004 |
| 3 | W8 | Collect deep, read-only: shared position at the internal origin per model against the authority, link instances per host with workset and total transform (links loaded, not from the batch report), Project Information keys, standard schedules present | RevitBridge run_csharp | - | ARPL-LNK-0002, ARPL-LNK-0001 |
| 4 | W7 | LOIN snapshot: from the exported instance-parameter schedules count filled values per model, category and field (family elements only); score against the client's LOIN table, or state the assumption | schedule CSVs from step 2 | schedule export by ViewSchedule.Export from the bridge | ARPL-QA-0002 |
| 5 | W8 | Clash run: open the discipline models in one session (link worksets closed), intersect the agreed category pairs, separate penetrations, group clashes, owner by routing priority; close the models unsaved. Use the cloud clash service instead where the project has one | RevitBridge run_csharp | cloud coordination service export (tracked clash groups) | ARPL-CRD-0001 |
| 6 | W8 | Check: one dataset per source (models, links, warnings, LOIN, clashes) keyed by model or pair and week; findings per model and rule; week-over-week deltas from the second week on | report calculations | - | - |
| 7 | W5 | Correct: safe fixes automatically (repair links to the matrix, missing building name, missing standard schedules, then sync); anything that moves geometry, changes coordinates or deletes waits for the coordinator's approval | ZEN ACC Gate (Create Cloud Links, Import Standard Schedules) or bridge | bridge scripts | ARPL-LNK-0002, ARPL-ADM-0003 |
| 8 | W7 | Report: one dashboard page in the standard report form ARPL-RPT-0001 (report/STANDARD.md: headline, tiles, recommendations, clashes, LOIN, warnings, checks, link matrix, model contents, not collected) over its five datasets; every number drawn from the datasets, none typed | dashboard artifact from [report/template/index.html](report/template/index.html) | any BI tool reading the same CSVs | - |
| 9 | W6 | Print: one PDF booklet per model in the same unattended batch (ACC Gate 'Print PDFs from Print Intel workbooks'); set-up once per model: fixed print set, Print Intel workbook, PrintJobs row; check page counts against the sets and run the drift check when sheets change | Revit print dialog, ZEN Export Print Intel and ACC Gate | bridge PDF export per model with PDFExportOptions over the same print sets | ARPL-DOC-0003, ARPL-ADM-0004 |
| 10 | W7 | Archive: keep raw outputs in REPORTS/<date>; append the week's datasets to history; submit new lessons to the ARPL inbox (Revit and ZEN alike) | - | - | - |

ZEN is a custom Revit add-in (Tiverit LLC), not part of Revit. Its lessons are recorded in ARPL like Revit's (ARPL-ADM-0004) so a session can use it without relearning; every ZEN step has a bridge alternative.

## Rule table (starting thresholds)

| Check | Rule | Fix |
|---|---|---|
| Links complete | Every host has each link its matrix defines, none missing or duplicated | auto (repair from matrix) |
| Links in place | Every link instance placed by shared coordinates; when all models share one coordinate system and one internal origin, the link transform is identity | approval |
| Coordinates | Shared origin and angle equal the authority model, tolerance 0.01 ft | approval |
| Model identity | Building name equals the registry key; no template placeholder text | auto |
| Warnings | Count up more than 10% week over week, or a new warning type in a model's top five; week 1 is the baseline | report |
| Clashes | No new hard clashes in the agreed pairs; open clash groups falling week over week; penetrations reported separately | report; owners by routing priority |
| File size | Over 300 MB or up more than 15% in a week | report; purge for approval |
| Families | Any family over 5 MB; in-place count rising | report |
| LOIN completeness | Filled ÷ required values of family elements in the instance-parameter schedule at or above the project target (95% placeholder) per model; required fields from the client's LOIN table, else every information column with the assumption stated | report; recommendations name the categories with the most missing values |
| Sheets | Sheet numbers unique; sheets without views flagged | report |
| Worksets | Links on their own link worksets; elements on the default workset below a set limit | approval |
| Standards | Standard schedules and view templates present | auto |
| Registry | Every model in the cloud folder has a registry row, and the reverse | approval |

## Report form

**Standard:** [ARPL-RPT-0001 v1.0](report/STANDARD.md): page structure, the five dataset contracts ([empty CSVs](report/datasets/)), calculations, rule checks and constants, machine-readable in [report-standard.json](report/report-standard.json), with a [page template](report/template/index.html) for the Dashboard artifact type. The summary below is its outline.

One page, top to bottom. Every figure comes from a dataset or a calculation, never typed into the text; recommendations name owners but no numbers.

1. Header: project, week, baseline or trend week; one sentence with checks passed, warnings and top warning type, LOIN completeness against target, hard clashes and groups
2. Tiles: LOIN completeness, hard clashes (with groups), warnings, checks passing, Revit links, views not on sheets, model groups
3. Recommendations for the team: ordered by impact, each with the owning team and the action; recurring causes first (one decision that clears many items)
4. Clashes: bars by discipline pair, bars by team that moves, table of the largest groups (pair, level, owner, main element with id)
5. LOIN: model x field grid of fill rates; categories ranked by missing values; system and analytical elements counted separately
6. Warnings: types across models (top five per model), warnings by model
7. Checks: one row per model, one column per rule (pass, fail, baseline, not collected)
8. Link matrix: host x link heat map (placed, workset, transform)
9. Model contents: health fields per model
10. Not collected this week: every gap and every assumption, in plain words

**Datasets**

- `models`: one row per model: health fields, shared position, link and workset counts, schedules present
- `links`: host x link: instance, workset, transform, status
- `warnings`: model, rank, count, message
- `loin`: model, category, element_kind, field, instances, filled
- `clashes`: one row per element pair: pair, disciplines, kind, group, owner, categories, family and type, levels, ids and unique ids, volume, centroid

## Measured (2026-10-27)

- ACC Gate health + PBP: 12 models, about 2 min, 8-11 s per open
- ACC Gate Export Schedules: 6 models, 3 schedules each
- Clash run: 5 models opened in 33 s; 9 pairs in about 3 min; 365 intersections -> 282 clashes in 74 groups + 83 penetrations
- LOIN: 6 models, 20,327 instances, 30.9% against 95%
- Batch cloud links: 156 links in 21 min (setup week)
- Estimate per week: 45-75 min with agent and batch tool, against 6-8 h by hand.
- Print sets and Print Intel set-up: 6 models, 139 sheets, about 20 min once; booklets checked page for page against the sets (2026-10-28, ARPL-DOC-0003).

**Guardrails:** collection is read-only; models opened for checks are closed without saving. The agent alone: collection, analysis, reporting, link repair to the matrix, missing building name, missing standard schedules, sync after a successful fix. Coordinator approval: re-placing links, applying coordinates, moving elements between worksets, purge, registering new models, any delete, closing a model the user has open. Never automated: matrix or registry rules, the authority model, anything another user has borrowed.

**Decisions that belong to the user:** The client's LOIN table: required fields per category and stage, and the target; The clash matrix: category pairs, hard or clearance, routing priority; The coordinate authority model; Thresholds of the rule table; Approval of every geometry, coordinate, workset or delete fix.

**Packs still to be written (help wanted):** registry-vs-cloud-folder-check, loin-count-script (code for ARPL-QA-0002), clash-new-and-resolved-week-over-week, clearance-clashes-by-inflated-solids. Intake: IN-0016 (PR #7), IN-0017.
