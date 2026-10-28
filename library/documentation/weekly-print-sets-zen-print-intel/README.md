# ARPL-DOC-0003 rev 1: Weekly print-set booklets with ZEN: one Revit print set per model, Print Intel workbook, ACC Gate Print PDFs

_Generated from this pack's files by tools/build_catalogs.py. Edit manifest.json, intent.md, vNN/ or final/rule.json instead._

| | |
|---|---|
| Level | 2 |
| Work class | W6 |
| Status | candidate |
| Use when | A federated project needs one PDF booklet per model every week without opening the models by hand; The ZEN add-in (Tiverit LLC) is installed and the project has a ZEN model registry of ACC cloud models; An agent prepares print sets in Revit and drives ZEN Print Intel and ACC Gate from a bridge with screen access |
| Not for | Projects without ZEN: export PDFs per model from the bridge with PDFExportOptions instead (same content rule, same read-back); Sets that must follow the sheet list automatically: a Revit print set is a fixed list (see rule 9) |
| Workflows | documentation, model-administration |
| Disciplines | bim-vdc, generic |
| Project types | generic |
| Revit tested | 2024 |
| API | ViewSheetSet, PrintManager.ViewSheetSetting, ViewSheet.GetAllViewports, ScheduleSheetInstance, PanelScheduleSheetInstance, UIApplication.PostCommand, UIApplication.OpenAndActivateDocument, ModelPathUtils.ConvertCloudGUIDsToCloudPath, Document.SynchronizeWithCentral |
| Failure patterns | FP32, FP51, FP52, FP53, FP54 |
| Contributors | Gottfried Schmidtke with Claude |

**Intent:** Give every model of a federated cloud project one fixed print set and a ZEN Print Intel workbook, once, so that the whole project's PDF booklets print every week in one unattended ZEN ACC Gate run, without opening any model by hand. This is a BIM coordinator routine; ZEN is a custom Revit add-in, recorded here by name so later sessions do not relearn it.

## Learning curve

| Version | Instruction | Result | Problem | Found by |
|---|---|---|---|---|
| v01 | Create the print set with ZEN (Print PDF > Select Views/Sheets), then export Print Intel. | ZEN Print PDF first asks for a Print Intel workbook; with an empty PrintJobs sheet it stops with 'No print jobs found in the PrintJobs sheet'. ZEN has no command that creates a print set. | The plan put a Revit step into the add-in. The print set is a Revit print set; ZEN's Export Print Intel only reads it and Print PDF prints the PrintJobs rows (ZEN 1.2 manual). | running the command, walking the ZEN ribbon for command ids, and reading the manual on the owner's instruction |
| v02 | Decide the content with a read-only script: a sheet belongs in the set when it carries a viewport or a schedule (ScheduleSheetInstance, not the title-block revision schedule). | Architectural: 55 of 55 sheets, A602 schedule-only. The owner decided schedule-only sheets count. | Electrical sheets E300-E307 hold only panel schedules. These are PanelScheduleSheetInstance, not ScheduleSheetInstance, so the rule reported them as 'no views' and would have dropped all eight from the booklet (FP52). | comparing the dry run with the model's exported sheet list before creating the set |
| v03 | Per model: open from the registry GUIDs with worksets closed; script lists the content; Revit Print > Selected views/sheets > Select: choose the existing set that matches (or Check none and tick the sheets), Save as the common name, Save current set, Select, Close; read back; sync and relinquish; ZEN Export Print Intel to the workbook folder; one PrintJobs row. Then ACC Gate from no open model: registry, all models, 'Print PDFs from Print Intel workbooks', workbook folder, output folder typed. | 6 models, 139 sheets: every set read back with would_add 0, would_remove 0 and no non-sheet views; sync 10-14 s; opens 12-15 s; set-up of all six about 20 minutes. Each workbook lists the set with the right sheet count and the model's cloud GUIDs. ACC Gate printed the first two models before the session paused: Plumbing 27 pages, Structural 12 pages, page count equal to the set, every sheet number present, each sheet at its own size (42 x 30 in). The other four were not observed. | The posted ACC Gate command did nothing while Revit Home was showing; it ran when Home was left (FP53). Closing the document the bridge holds as doc threw InvalidObjectException (FP54). In Select Views/Sheets the link 'Create a print set' opens online help, not a command. Export Print Intel overwrites the workbook without asking and its folder browser starts at Desktop every time; the ACC Gate output folder came pre-filled with another run's folder (FP51). The PrintSets sheet counts sheets only: a set of 12 views shows 0. | watching the screen after every command, the read-back script, and counting PDF pages against the workbook |

## Lesson
The weekly booklet is three layers: a fixed Revit print set per model (made once, checked weekly for drift), a ZEN Print Intel workbook that names it in PrintJobs, and one ACC Gate run over the registry. Decide the content by script, build the set in Revit's own dialog, read it back before syncing, and count PDF pages against the workbook.

## Rule
1. The print set is a Revit print set (ViewSheetSet), one per model, with the same name in every model (for example <Project>-current). ZEN does not create it: Export Print Intel reads the model's print sets into the workbook, and Print PDF and ACC Gate print the workbook's PrintJobs rows.
2. Decide the content before creating anything, with the read-only check (final/checks/printset_readback.cs, before creation it lists the content): a sheet belongs in the set when it carries a viewport, a schedule (ScheduleSheetInstance other than the title-block revision schedule) or a panel schedule (PanelScheduleSheetInstance). Ask the user whether schedule-only sheets count; show the skipped sheets.
3. Create it in Revit: Print (Ctrl+P) > Selected views/sheets > Select. If an existing set already holds exactly the listed sheets, select it and use the 'Save as' icon (top right) with the common name. Otherwise Save as first, then Check none, untick 'Hide un-checked views/sheets', type 'Sheet:' in the filter and tick the listed sheets. Then Save current set, Select, and close the Print dialog with Close, never OK. The link 'Create a print set' only opens online help.
4. Read back with the check: set exists, would_add 0, would_remove 0, no non-sheet views. Only then synchronize with central with a comment and relinquish: ACC Gate opens the central model, and an unsynced set does not exist there.
5. Export Print Intel (ZEN > Data & Health > Print PDF split button, id CustomCtrl_%CustomCtrl_%CustomCtrl_%ZEN%Data & Health%ZenPrintPdf%CmdExportPrintIntelWorkbook) into one workbook folder per project. Check the PrintSets sheet lists the set with the expected sheet count and ModelInfo carries the cloud GUIDs (ACC Gate matches by GUID). The export overwrites an existing workbook without asking; its folder browser starts at Desktop.
6. Fill PrintJobs: one row per PDF, PrintSetName copied exactly from PrintSets, PdfSetupName blank for ZEN's default profile (each sheet at its own size, vector, colour, sheet-number order), BaseFileName optional (default <Model>_<Set>). Save and close the workbook before the run.
7. Weekly run: ACC Gate with no model open: registry CSV, all models, action 'Print PDFs from Print Intel workbooks', the workbook folder, and the output folder typed as <workbook folder>/<date> (FP51). A command posted while Revit Home is showing waits until Home is left (FP53): leave Home with the back arrow, or click the ribbon button, and take a screenshot after posting.
8. Check the output: one PDF per model in PDF/, page count equal to the set's sheet count in the workbook, every sheet number present, batch report without failures.
9. A Revit print set is a fixed list: a sheet added later is missed and a sheet emptied later stays in. Run the check weekly as a drift check and update the set (step 3) when would_add or would_remove is not 0.
10. Links unloaded in a model stay unloaded and do not print (ZEN manual); the workbook's Links sheet shows IsLoaded as of the export session. Confirm linked content on one site or overall sheet in the PDF.
11. Bridge mechanics: open each model with OpenAndActivateDocument from the registry GUIDs (worksets closed) and work on uiapp.ActiveUIDocument.Document; close the previous model by the reference captured before opening, never the document the bridge passes as doc; close the active model with PostableCommand.Close (FP54).

## Validation
- Read-back check pass in every model (would_add 0, would_remove 0, non_sheet_views 0)
- Every workbook: PrintSets lists the set with the expected sheet count; PrintJobs has the set name; ModelInfo has the model's cloud GUIDs
- One PDF per model; page count equal to the set's sheet count; every sheet number present
- Batch report and run log without failures
