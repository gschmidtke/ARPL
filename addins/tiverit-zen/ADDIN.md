# ZEN (Tiverit LLC)

| | |
|---|---|
| Vendor | Tiverit LLC, https://www.tiveritllc.com/ |
| Add-in | ZEN (ribbon tab "ZEN": Federation, Data & Health, Project Standards, Families) |
| Assembly version observed | ZEN 1.0.0.0 (the help site documents manual 1.2.0) |
| Revit versions observed | 2024.3 (24.3.60.12) |
| Public documentation | https://www.tiveritllc.com/zen-help.html |
| Help on F1 | Yes: F1 with the pointer on a ZEN command opens the help page at that command's panel |
| Last observed | 2026-11-03 |
| Learned by | Protocol steps 1–4: public help, ribbon inventory, read-only model and file checks, observed runs; from 2026-11-03 also vendor verification (`V`) by the developer against ZEN release 1.2.0. No code is published here. |
| Contributors | Gottfried Schmidtke with Claude |

## What it is for

A Revit plug-in suite for BIM management at production scale: federated cloud linking from a model registry and link matrix, sheet, schedule, workset and material standards exchanged with Excel/CSV, model health checks, PDF printing driven by a workbook, and ACC batch runs (ACC Gate) over many cloud models (E1-docs).

## Commands

Full inventory, 53 entries with command ids, tooltips and expanded tooltips: [commands.json](commands.json) (E2-inventory, 2026-11-03).

Most commands sit inside split buttons: the ribbon shows one label per group, and the commands are in the dropdown under it. Use the inventory, not the visible ribbon, to know what exists.

### Export Print Intel (Data & Health, under Print PDF)

- **Command id:** `CustomCtrl_%CustomCtrl_%CustomCtrl_%ZEN%Data & Health%ZenPrintPdf%CmdExportPrintIntelWorkbook`
- **Reads:** the active model's worksets, Revit links, print sets (`ViewSheetSet`, with sheet counts and numbers), cloud identity.
- **Writes:** `<ModelTitle>_PrintIntel.xlsx` with sheets Worksets, Links, PrintSets, PrintJobs, ModelInfo, into a folder the user picks. Overwrites a workbook of the same name without asking. Model is not changed.
- **Dialogs:** "Browse For Folder" (starts at Desktop); completion window with counts of worksets, links and print sets, and a reminder to fill in PrintJobs.
- **Does not:** create or change print sets. PrintSets is reference data read from the model (E1-docs; E3-observed: model print sets identical before and after a run, 2026-11-03).
- **Evidence:** E3-observed, ZEN 1.0.0.0, Revit 2024.3, 2026-11-03.

### Print PDF (Data & Health)

- **Command id:** `CustomCtrl_%CustomCtrl_%CustomCtrl_%ZEN%Data & Health%ZenPrintPdf%CmdPrintPdfFromRegistry`
- **Reads:** the PrintJobs sheet of a Print Intel workbook (PrintSetName required; PdfSetupName and BaseFileName optional), and the named print sets in the active model.
- **Writes:** one combined PDF per PrintJobs row, `<ModelTitle>_<PrintSetName>.pdf`, into one output folder for the whole run. With PdfSetupName blank: ZEN default profile (each sheet at its own paper size, vector, colour, sheet-number order).
- **Dialogs:** "Select Print Intel workbook" (file dialog; the File name box accepts a full path); "Browse For Folder" for the output ("Select an output folder for N print job(s)"); progress in Revit's status bar; completion window "Print by Registry" listing PDFs written and sheets per job.
- **Does not:** print elements on worksets closed in the session (E1-docs). Does not create print sets.
- **Evidence:** E3-observed twice on 2026-11-03: Concept Set, 16 pages; ADU-01-current, 29 pages; page counts equal to the sets.

### Sheets (Project Standards): Export Sheets, Import Sheets, Batch Import

The sheet-list standard as a CSV: export the model's sheet list, edit it in Excel, push it back into one model or many. The three commands share one CSV format (see [File formats](#file-formats)). Evidence for this section: `V` against ZEN 1.2.0 and `E3` on Revit 2024.3, 2026-11-03, unless a line says otherwise.

**Before you use any of them, know the matching rule.** Import Sheets and Batch Import find a sheet **by its sheet number, exactly** (case and spaces count after trimming the ends). A matching number gets its name updated; a number not found **creates a new sheet**. Nothing is ever deleted, and nothing is renumbered. So:

- To **rename** sheets: change column B, keep column A. Works.
- To **add** sheets: add rows with new numbers. Works.
- To **renumber** sheets: **not possible with these commands.** A changed number in column A creates a second, empty sheet and leaves the old one as it was. Renumber in Revit (sheet properties) or from a bridge (`ViewSheet.SheetNumber`), then use ZEN to align names.

#### Export Sheets

- **Command id:** `CustomCtrl_%CustomCtrl_%CustomCtrl_%ZEN%Project Standards%ZenSheets%CmdExportSheetsToExcel`
- **Needs:** a sheet schedule named `SHEET LIST` (any letter case). Other sheet schedules are ignored. If none exists the command stops with a message and writes nothing.
- **Writes:** `<model> - SHEET_LIST.csv` (spaces in the model name become `_`), UTF-8. Overwrites a file of the same name without asking. The model is not changed.
- **Content:** exactly what the `SHEET LIST` schedule shows: its visible columns in its order, its column headings as the first row (a blank row may follow), then one row per sheet in the schedule's sort order, then any footer rows. For the CSV to import cleanly, the schedule's first two columns must be Sheet Number and Sheet Name.
- **Dialogs:** "Browse For Folder" ("Select folder for ZEN Sheet List export."), preselected on the model's folder for a local model and on Desktop for a cloud model; then a completion window with folder and file name.
- **Cancel does not cancel:** closing the folder dialog with Cancel still exports, to the preselected folder (`V`).

#### Import Sheets (active model)

- **Command id:** `CustomCtrl_%CustomCtrl_%CustomCtrl_%ZEN%Project Standards%ZenSheets%CmdImportSheetsFromExcel`
- **Close the CSV in Excel first** (the command's own tooltip says so). If the file cannot be read, the command stops with "Failed to read CSV" and changes nothing (`V`).
- **Reads:** one CSV, column A sheet number, column B sheet name; other columns ignored. A first row that looks like a header (A contains "sheet" and "no"/"number", or B contains "sheet" and "name") is skipped. Rows with both A and B empty are skipped; a row with a name but no number is skipped and reported.
- **Changes:** in one transaction ("ZEN – Import Sheets from CSV", one Undo): renames sheets whose number matches and whose name differs; creates missing numbers as new sheets with the title block chosen in the first dialog. Does not save or sync.
- **Dialogs, in this order:** "Select Title Block" (list of `Family : Type`, OK button; it appears even when no sheet will be created; closing it with × means new sheets get **no** title block); file dialog "Select Excel CSV (A: Sheet Number, B: Sheet Name)"; summary window with Created, Renamed, No Change/Skipped, duplicate numbers found in the CSV, and one line per row.
- **Duplicates in the CSV** are listed in the summary; they are still processed row by row, so a later row's name wins.

#### Batch Import (many local files)

- **Command id:** `CustomCtrl_%CustomCtrl_%CustomCtrl_%ZEN%Project Standards%ZenSheets%CmdBatchImportSheetsFromExcel`
- **For local `.rvt` files only.** For cloud models use ACC Gate's action "Import Sheets from CSV (Sheet No + Name)".
- **Same CSV and matching rule** as Import Sheets, with two differences: new sheets are created **without a title block**, and a new sheet with an empty name gets its number as name.
- **Per file:** opens it with all worksets closed, imports, then **saves (or synchronizes with central, comment "ZEN: Batch import sheets from CSV") automatically**, then closes it. There is no dry run in the released command: whatever the CSV says is written to every selected file.
- **60-second rule:** if opening a file takes longer than 60 s, the file is reported `TIMED OUT` and not changed. If the import step itself takes longer than 60 s, the file is reported `TIMED OUT` and closed **without saving**.
- **Dialogs:** file dialog for the CSV; multi-select file dialog for the target `.rvt` files; one summary window per run. A running log is appended to `ZEN_BatchImportSheetsLog.txt` on the Desktop.
- **Evidence:** `V` only (not yet run on a test set).

### ACC Gate (Federation)

Batch runs over cloud models without an open model, including "Print PDFs from Print Intel workbooks". See pack ARPL-DOC-0003 for the observed weekly print run.

## Task index

Start here when the user names a goal rather than a command.

| I want to … | Use | Prepare first | Expect |
|---|---|---|---|
| Get the model's sheet list into Excel | Export Sheets | A sheet schedule named `SHEET LIST` with Sheet Number, Sheet Name as first columns | `<model> - SHEET_LIST.csv` |
| Rename sheets from a list | Import Sheets (one model), Batch Import (local files), ACC Gate (cloud) | CSV: A unchanged numbers, B new names; CSV closed in Excel | Summary: Renamed n |
| Add sheets from a list | Import Sheets | CSV rows with new numbers; the title block type to use | Summary: Created n; one Undo for all |
| Renumber sheets | Not ZEN: Revit or a bridge | Old → new mapping, checked for clashes | Then Export Sheets to refresh the CSV |
| Print a set of sheets to PDF | Print PDF | A Revit print set (ZEN does not create one), a Print Intel workbook with a PrintJobs row | `<model>_<set>.pdf`, page count = set |
| See which print sets a model has | Export Print Intel | — | PrintSets sheet in the workbook |

## File formats

### Sheet-list CSV (Export Sheets, Import Sheets, Batch Import, ACC Gate sheet import)

| Column | Content | Required for import |
|---|---|---|
| A | Sheet number, exactly as in Revit | yes |
| B | Sheet name | yes (empty name: Import Sheets sets an empty name; Batch Import uses the number) |
| C … | Anything (Export Sheets writes the schedule's further columns) | ignored on import |

- Comma-separated; fields with commas or quotes in double quotes, quotes doubled. UTF-8.
- First row: optional header; skipped on import when it looks like one (see Import Sheets).
- Empty lines are ignored.

### Print Intel workbook (Export Print Intel, Print PDF, ACC Gate print action)

| Sheet | Columns | Who fills it |
|---|---|---|
| Worksets | workset id, name, kind | ZEN (reference) |
| Links | link name, type, workset, loaded, path | ZEN (reference) |
| PrintSets | PrintSetName, SheetCount, SheetNumbers (`;`-separated) | ZEN (reference; read from the model, never written back) |
| PrintJobs | PrintSetName (required, copied from PrintSets), PdfSetupName (optional), BaseFileName (optional) | the user, one row per PDF |
| ModelInfo | model title, cloud project and model GUIDs | ZEN (reference; ACC Gate matches workbooks by GUID) |

## Lessons

| # | Lesson | Workaround | Evidence | Failure pattern |
|---|---|---|---|---|
| 1 | No ZEN command creates a print set; Export Print Intel only reports them. A user asking to "create the print set with Print Intel" needs the set made in Revit first. | Create the set in Revit (Print dialog, or `PrintManager.ViewSheetSetting.SaveAs` from the bridge), read it back (ARPL-DOC-0003 check), sync, then Export Print Intel, fill PrintJobs, Print PDF. | E3, 2026-11-03 | — |
| 2 | A Print Intel workbook is a snapshot. After sheets are renumbered or sets change, its PrintSets sheet is stale; Print PDF still prints the set by name from the model. | Re-export Print Intel after sheet or set changes and re-enter the PrintJobs rows (the export overwrites them). | E3, 2026-11-03 | FP51 (stale pre-filled folders) is related |
| 3 | "Browse For Folder" dialogs do not accept a typed folder name; "Make New Folder" leaves the folder named "New folder". | Pick an existing folder, or create the folder beforehand. | E3, 2026-11-03 | — |
| 4 | The help page is the fastest way in: F1 on a ribbon command opens the vendor help at that command. | Read the help section before the first run of a command in a session. | E3, 2026-11-03 | — |
| 5 | Commands posted while Revit Home is showing wait until Home is left; closing the document the bridge holds throws. | See ARPL-DOC-0003 rules 7 and 11. | E3, 2026-10-28 | FP53, FP54 |
| 6 | ZEN sheet import matches by sheet number. A sheet list with changed numbers creates duplicate empty sheets instead of renumbering. | Renumber in Revit or from the bridge first; use ZEN only to rename and add. | V, E3, 2026-11-03 | — |
| 7 | Cancel in Export Sheets' folder dialog still exports (to the model folder, or Desktop for cloud models). | Pick the folder; check Desktop for a stray `SHEET_LIST.csv` if cancelled. | V, 2026-11-03 | — |
| 8 | Batch Import saves or syncs every target without a dry run, and closes a target unsaved if its import takes over 60 s. | Test the CSV with Import Sheets on one model first; read the summary for TIMED OUT. | V, 2026-11-03 | — |

## Packs that use this add-in

- ARPL-DOC-0003: Weekly print-set booklets with ZEN: one Revit print set per model, Print Intel workbook, ACC Gate Print PDFs

## Open with the vendor

- A command to create or update print sets from the PrintSets sheet of a Print Intel workbook has been proposed to the vendor (2026-11-03). Until it exists, lesson 1 applies.
