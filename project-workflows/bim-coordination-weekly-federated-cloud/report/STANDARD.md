# ARPL-RPT-0001: Weekly BIM coordination report standard

**Version 1.0 · candidate · 2026-10-28.** The report form of [ARPL-PW-0003](../manifest.json) step 8, as structure and data contract. Machine-readable: [`report-standard.json`](report-standard.json). Reference page: [`template/index.html`](template/index.html). Empty dataset files: [`datasets/`](datasets/).

Source: the weekly reports of 2026-10-27 (a 13-model campus, partial, and the 6-model Snowdon Towers sample, complete). The Snowdon report is the standard; the campus report is the same structure with sections left out.

## Principles

- Every figure, chart and table comes from a dataset or a named calculation; no number is typed into the text
- One dataset per source, keyed by ModelKey (or element pair) and snapshot week; raw outputs per run in REPORTS/<date>
- Sections keep their order and ids; a section whose source did not run stays out and is listed under 'Not collected this week'
- Week 1 is the baseline: trend rules read 'baseline'; from week 2 they compare with last week's datasets
- Recommendations name owning teams and actions, never figures; recurring causes first
- Project constants are stated on the page: coordinate authority, tolerance, LOIN target and LOIN basis

## Page structure

Top to bottom; keep order and ids.

| # | Section (id) | From | Content |
|---|---|---|---|
| 1 | Title, week and one-sentence summary (`header`) | summary, warning_types, loin_summary, clash_summary | {{PROJECT}} weekly BIM report; 'Week of …'; baseline week or trend week; the summary sentence carries only marked figures |
| 2 | Headline figures (`tiles`) | loin_summary, clash_summary, summary | LOIN completeness; hard clashes (with groups); warnings; checks passing; Revit links; views not on sheets; model groups |
| 3 | Recommendations for the team (`recommendations`) | written | ordered by impact; each: finding, owning team, action; recurring causes first; no figures in the text |
| 4 | Hard clashes by discipline pair (`clash-pairs`) | clash_pairs | bar chart |
| 5 | Clashes by team that moves (`clash-owners`) | clash_owners | bar chart; routing priority stated |
| 6 | Largest clash groups (`clash-groups`) | clash_groups | table keyed by group, with element ids |
| 7 | LOIN completeness by model and field (`loin`) | loin_by_model | model × field grid of fill rates; state the LOIN basis |
| 8 | Largest LOIN gaps by category (`loin-gaps`) | loin_by_category, loin_summary | table keyed by model, category; system and analytical instances reported separately |
| 9 | Warnings by type (`warning-types`) | warning_types | bar chart with full message in the tooltip |
| 10 | Warnings by model (`warnings-by-model`) | models | bar chart; week-over-week from week 2 |
| 11 | Rule checks by model (`checks`) | findings | table: one row per model, one column per rule; pass, fail, baseline, n/c |
| 12 | Link matrix, host by linked model (`links`) | links | host × link grid coloured by workset and placement |
| 13 | Model contents (`models`) | models | table of the health-check counts |
| 14 | Not collected this week (`gaps`) | written | every source or rule that did not run, and why |

## Datasets

Files named `<project>_<dataset>_<yyyy-mm-dd>.csv`, UTF-8, header row as in `datasets/`. Lengths in feet (Revit internal units), angles in degrees.

### `models` — one row per model per week

Key: `model`. Collected by: step 2 ZEN ACC Gate Model Health Check (counts) + step 3 read-only bridge read (position, links, identity, schedules).

| Column | Type | Meaning |
|---|---|---|
| `model` | string | ModelKey = registry key = Project Information > Building Name |
| `model_name` | string | model (file) title |
| `discipline` | string | discipline of the model |
| `snapshot` | date | week of the run, YYYY-MM-DD |
| `in_health_run` | yes|no | the model was in the batch health run |
| `warnings` | integer | warnings total |
| `views` | integer | views total |
| `view_templates` | integer | view templates |
| `views_not_on_sheets` | integer | views not placed on a sheet |
| `sheets` | integer | sheets total |
| `unplaced_rooms` | integer |  |
| `unplaced_areas` | integer |  |
| `cad_imports` | integer |  |
| `cad_links` | integer |  |
| `revit_links` | integer | Revit link instances in the host |
| `in_place_families` | integer |  |
| `model_groups` | integer |  |
| `detail_groups` | integer |  |
| `levels` | integer |  |
| `grids` | integer |  |
| `raster_images` | integer |  |
| `design_options` | integer |  |
| `building_name` | string | Project Information > Building Name as read |
| `project_status` | string | Project Information > Project Status as read |
| `phases` | string | the model's phase names in order, separated by '; ' |
| `site` | string | active project location (site) name |
| `shared_ew_ft` | number | shared position of the internal origin, east-west, feet |
| `shared_ns_ft` | number | north-south, feet |
| `elevation_ft` | number | elevation, feet |
| `angle_deg` | number | angle to true north, degrees |
| `links_on_own_workset` | integer | link instances on their own XX_<LinkKey> workset |
| `links_in_place` | integer | link instances placed as the matrix defines (identity transform when all models share one origin) |
| `worksets` | integer | user worksets |
| `has_instance_parameters` | yes|no | standard INSTANCE PARAMETERS schedule present |
| `has_sheet_list` | yes|no | standard SHEET LIST schedule present |

### `links` — one row per link instance per week

Key: `host,link`. Collected by: step 3 read-only bridge read with links loaded where placement is judged (ARPL-LNK-0002).

| Column | Type | Meaning |
|---|---|---|
| `host` | string | host ModelKey |
| `link` | string | linked ModelKey |
| `workset` | string | workset of the link instance |
| `workset_ok` | yes|no | on the link's own workset |
| `placement` | string | identity transform | moved: <offset> |
| `link_status` | string | loaded state as read |
| `source` | string | how it was read |

### `warnings` — top five warning types per model per week

Key: `model,rank`. Collected by: step 2 ZEN health check 'Top Warning' lines.

| Column | Type | Meaning |
|---|---|---|
| `model` | string | ModelKey |
| `rank` | integer | 1-5 |
| `count` | integer | instances of this warning |
| `message` | string | warning text as Revit writes it |

### `loin` — one row per model, category and information field per week

Key: `model,category,field`. Collected by: step 4 count over the INSTANCE PARAMETERS schedule export (ARPL-QA-0002).

| Column | Type | Meaning |
|---|---|---|
| `model` | string | ModelKey |
| `category` | string | Revit category |
| `element_kind` | family element|system / analytical | family elements count towards LOIN; system and analytical rows are reported separately |
| `field` | string | information field (schedule column) |
| `instances` | integer | instances in the category |
| `filled` | integer | instances with the field filled |

### `clashes` — one row per clashing element pair per week

Key: `uid_a,uid_b`. Collected by: step 5 clash run (ARPL-CRD-0001) or a cloud clash service export.

| Column | Type | Meaning |
|---|---|---|
| `snapshot` | date |  |
| `pair` | string | pair code, e.g. ELExCEIL |
| `discipline_a` | string | discipline of element a |
| `discipline_b` | string | discipline of element b |
| `kind` | clash|penetration | penetration = planned vertical run through a ceiling, not counted as a clash |
| `group` | string | group id; clashes sharing an element share a group |
| `owner` | string | discipline that moves, by routing priority |
| `category_a` | string |  |
| `family_type_a` | string |  |
| `level_a` | string |  |
| `id_a` | integer | element id |
| `uid_a` | string | UniqueId, stable week to week |
| `category_b` | string |  |
| `family_type_b` | string |  |
| `level_b` | string |  |
| `id_b` | integer |  |
| `uid_b` | string |  |
| `volume_cf` | number | intersection volume, cubic feet |
| `x` | number | clash point, feet, internal coordinates |
| `y` | number |  |
| `z` | number |  |

## Calculations

| Id | Inputs | Output | Rule |
|---|---|---|---|
| `loin_by_model` | loin | model, field, instances, filled, fill | family elements only; fill = filled / instances |
| `loin_by_category` | loin | model, category, instances, description_fill, type_mark_fill, missing | family elements only; missing = sum(instances - filled) over fields; top 15 by missing |
| `loin_summary` | loin | completeness, required_values, filled_values, system_instances | completeness = sum(filled) / sum(instances) over family elements; system instances counted once (Description rows) |
| `clash_summary` | clashes | clashes, groups, penetrations | kind = clash counts; penetrations separately |
| `clash_pairs` | clashes | pair, clashes, groups | per 'discipline_a × discipline_b', largest first |
| `clash_owners` | clashes | owner, clashes, groups | per owner (team that moves) |
| `clash_groups` | clashes | group, pair, level, owner, element, clashes | top 12 groups by clashes; most frequent level, owner and element (category, family type, id) |
| `findings` | models, loin_by_model | model + one column per rule | see rules |
| `summary` | models, findings | models, links, warnings, views_not_on_sheets, model_groups, checks_passed, checks_failed, checks_total, pass_share | sums over models; pass_share = passed / (passed + failed); baseline and n/c are not counted |
| `warning_types` | warnings | message, count, models | top-five rows of every model combined by message; numbered system names normalised ('<name> 31:' to '<name> <n>:') |

## Rule checks (`findings`)

One row per model, one column per rule. Values: `pass`, `fail`, `baseline` (first week of a trend rule), `n/c` (not collected). `checks_total` counts pass and fail only.

| Rule | Column | Pass when |
|---|---|---|
| Links complete | `links_complete` | revit_links = number of models - 1 (every host links every other model), or as the link matrix defines |
| Link worksets | `links_workset` | links_on_own_workset = revit_links |
| Links in place | `links_in_place` | links_in_place = revit_links |
| Coordinates | `coordinates` | |shared_ew_ft - authority| <= TOL_FT and |shared_ns_ft - authority| <= TOL_FT and |angle_deg - authority| < ANGLE_TOL_DEG |
| Model identity | `identity` | building_name = model (ModelKey) |
| Project status | `status` | project_status = PROJECT_STATUS; until the BIM manager sets it, = the status most models carry (a split federation fails the minority) |
| Phases | `phases` | phases = the authority model's phase list (or PHASES): same names, same order, so linked-model phase mapping works |
| Standard schedules | `standards` | has_instance_parameters = yes and has_sheet_list = yes |
| LOIN ≥ target | `loin` | model completeness >= LOIN_TARGET; n/c when the model has no LOIN rows |
| Warnings trend | `warnings` | warnings <= last week's warnings; 'baseline' in the first week |
| Health data | `health` | in_health_run = yes, else n/c |

Constants (the user decides; state them on the page):

| Constant | Default | Meaning |
|---|---|---|
| `AUTHORITY_MODEL_KEY` | none | coordinate authority model; until one is chosen, name the stand-in in 'Not collected' |
| `TOL_FT` | 0.01 | position tolerance, feet |
| `ANGLE_TOL_DEG` | 0.001 | angle tolerance, degrees |
| `LOIN_TARGET` | 0.95 | completeness target |
| `PROJECT_STATUS` | none | the one project status for the federation (the BIM manager decides) |
| `PHASES` | authority model's phases | agreed phase list (optional) |

## Using the template

1. Collect steps 2-5 of ARPL-PW-0003 into the five datasets; leave out what did not run.
2. Create a dashboard from the Dashboard artifact type, attach each CSV as a fixed file dataset (`fixed: true`, `updated` with time and source), and write `template/index.html` with the placeholders replaced. Section notes that describe one project (LOIN basis, clash scope, link setup) are rewritten for each project.
3. Write the recommendations from the datasets and the 'Not collected' list. Check that every marked figure fills.
4. From week 2: add last week's datasets and switch the `warnings` rule from `baseline` to the comparison; clashes new and resolved are matched by `uid_a, uid_b`.

Without the Dashboard type, any BI tool reading the same CSVs can follow the sections, calculations and rules; the page is the reference, not a requirement.

## Change log

| Version | Date | Change |
|---|---|---|
| 1.1 | 2026-10-28 | Rule checks `status` and `phases` added; `models` gains `project_status` and `phases`. Mixed project status or phases across discipline models is a common multi-discipline problem; the coordinator raises it every week. |
