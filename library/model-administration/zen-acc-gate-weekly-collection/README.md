# ARPL-ADM-0004 rev 3: ZEN ACC Gate as the weekly collection batch: health, links and worksets, schedule exports; what each output contains and how to drive it from a bridge

_Generated from this pack's files by tools/build_catalogs.py. Edit manifest.json, intent.md, vNN/ or final/rule.json instead._

| | |
|---|---|
| Level | 2 |
| Work class | W8 |
| Status | candidate |
| Use when | The ZEN add-in (Tiverit LLC) is installed and a project has a ZEN model registry; A weekly coordination run needs per-model health, link placement and schedule data without opening each model by hand; An agent drives ZEN commands from a Revit bridge |
| Not for | Projects without ZEN: collect the same data with read-only bridge scripts (ARPL-PW-0003 lists the fields); Cloud file sizes: they need ZEN's Refresh Sizes with APS credentials |
| Workflows | model-administration, validation-qaqc, links-coordinates |
| Disciplines | bim-vdc, generic |
| Project types | generic |
| Revit tested | 2024 |
| API | UIApplication.PostCommand, RevitCommandId.LookupCommandId, ModelPathUtils.ConvertCloudGUIDsToCloudPath |
| Failure patterns | FP43, FP46, FP50, FP51, FP53, FP59 |
| Contributors | Gottfried Schmidtke with Claude |

**Intent:** Use ZEN's ACC Gate as the unattended collection batch of the weekly coordination run (ARPL-PW-0003): Model Health Check, PBP + Worksets report and Export Schedules over all registry models, with outputs the report can join reliably. ZEN is a custom Revit add-in, not part of Revit; these lessons are recorded here so later sessions do not relearn them.

## Learning curve

| Version | Instruction | Result | Problem | Found by |
|---|---|---|---|---|
| v01 | From Revit Home with no model open, start ACC Gate by PostCommand; choose the registry CSV, select the models, tick Model Health Check and PBP + Worksets report; set the output folder explicitly. | 12 of 12 models OK, 0 failures; opens 8 to 11 s per model; health part about 2 minutes. Health uses the full single-model Field/Value schema, one CSV per model at <output>\ModelHealth\<Model>_HEALTH CHECK.csv, with 'Top Warning' lines when warnings exist and one 'Revit Link Status – <status>' line per status present. PBP workbook: one sheet per host, with host and link project and model GUIDs. | Health and PBP read links as opened by the batch (unloaded, in closed worksets): status 'InClosedWorkset', placement 'Not checked (unloaded)', instance names 'location <Not Shared>' (FP50). The output folder dialog offered another project's folder (FP51). | comparing the batch report with the same links loaded in one model |
| v02 | Second project (6 models): ACC Gate Model Health Check + PBP, then Export Schedules (INSTANCE PARAMETERS, PROJECT-INFO, SHEET LIST) to REPORTS/<date>/Schedules; join health to the registry by model name. | 6 of 6 models OK; 435 warnings with top five types per model; schedule CSVs per model fed the LOIN snapshot (ARPL-QA-0002). | Health CSVs carry no ModelKey or GUID; the join goes by Model Name (= registry ModelName) or through the batch log (title to project and model id). | building the report dataset |
| v03 | Same 6-model project: post ACC Gate from Revit Home with no model open; action 'Print PDFs from Print Intel workbooks'; workbook folder with one Print Intel workbook per model; output folder typed as <workbook folder>/<date>. | Batch opened the models one by one and wrote PDF/<Model>_<Set>.pdf; the first two booklets matched their print sets page for page (27 and 12 pages). The remaining models were not observed before the session paused. | Posted from Home, the command did nothing until Home was left (FP53). The output folder came pre-filled with an earlier run's folder (FP51). | screenshots after posting; PDF page count against the workbook |

## Lesson
ZEN's ACC Gate collects most of the weekly data in one unattended batch, but its reports describe the models as the batch opened them (links unloaded), and every dialog default must be read, not trusted.

## Rule
1. Start ZEN commands from the bridge with UIApplication.PostCommand(RevitCommandId.LookupCommandId(id)); the command runs after the bridge call returns, and only once Revit is idle (move the mouse over Revit if it waits). Ids: ACC Gate CustomCtrl_%CustomCtrl_%ZEN%Federation%CmdAccGate; Cloud GUIDs CustomCtrl_%CustomCtrl_%CustomCtrl_%ZEN%Federation%ZenRegistry%CmdDumpCloudModelGuids; Export Cloud Link Matrix CustomCtrl_%CustomCtrl_%CustomCtrl_%ZEN%Federation%ZenLinkMatrix%CmdGenerateCloudLinkMatrixFromRegistry; Import Schedule Definitions CustomCtrl_%CustomCtrl_%CustomCtrl_%ZEN%Project Standards%ZenSchedules%CmdImportStandardScheduleDefinitions.
2. While a ZEN dialog is open the bridge does not answer: take a screenshot, finish the dialog, then continue.
3. Run ACC Gate with no model open; close or ask about models the user has open. A command posted while Revit Home is showing does not run until Home is left (FP53): leave Home with the back arrow or click the ribbon button, and screenshot after posting.
4. Type the output folder every time (REPORTS/<date>); the dialog remembers other projects' folders.
5. Model Health via ACC Gate = full Field/Value schema per model (ModelHealth/<Model>_HEALTH CHECK.csv); pivot the dynamic 'Revit Link Status – <status>' lines; read 'Top Warning' lines for warning types; join by Model Name.
6. Do not judge link placement from the batch health or PBP report: links are unloaded there. Check placement by link transform with links loaded (ARPL-LNK-0002).
7. Export Schedules writes one CSV per schedule and model; the instance-parameter schedule feeds the LOIN snapshot (ARPL-QA-0002). Import Standard Schedules asks for a SOURCE .rvt that already holds the schedules, not the definitions workbook.
8. Export Cloud Link Matrix defaults UseSharedCoordinates, LoadOnOpen and RoomBounding to FALSE: edit a backup copy before linking (FP46). Cloud GUIDs takes Project Information > Building Name as model key: set it first; the template placeholder text counts as a value (FP43).
9. Cloud file size reads 'n/a' unless Refresh Sizes (APS credentials) ran first.
10. Print PDFs from Print Intel workbooks prints every PrintJobs row of each model's <Model>_PrintIntel.xlsx (matched by cloud GUID), opening each model with all worksets open; output PDF/<Model>_<Set>.pdf plus ZEN_Batch_PrintPdf.xlsx. The print sets themselves are Revit print sets made once per model: ARPL-DOC-0003.

## Validation
- Batch log: every selected model OK, failures listed.
- One health CSV per model; every registry model matched by name.
- Output written to the folder of this project and date.
