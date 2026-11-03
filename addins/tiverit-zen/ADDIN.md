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
| Learned by | Protocol steps 1–4: public help, ribbon inventory, read-only model and file checks, observed runs. Highest evidence: E3-observed. No source code was used. |
| Contributors | Gottfried Schmidtke with Claude |

## What it is for

A Revit plug-in suite for BIM management at production scale: federated cloud linking from a model registry and link matrix, sheet, schedule, workset and material standards exchanged with Excel/CSV, model health checks, PDF printing driven by a workbook, and ACC batch runs (ACC Gate) over many cloud models (E1-docs).

## Commands

Full inventory, 53 entries with command ids and tooltips: [commands.json](commands.json) (E2-inventory, 2026-11-03).

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

### ACC Gate (Federation)

Batch runs over cloud models without an open model, including "Print PDFs from Print Intel workbooks". See pack ARPL-DOC-0003 for the observed weekly print run.

## Lessons

| # | Lesson | Workaround | Evidence | Failure pattern |
|---|---|---|---|---|
| 1 | No ZEN command creates a print set; Export Print Intel only reports them. A user asking to "create the print set with Print Intel" needs the set made in Revit first. | Create the set in Revit (Print dialog, or `PrintManager.ViewSheetSetting.SaveAs` from the bridge), read it back (ARPL-DOC-0003 check), sync, then Export Print Intel, fill PrintJobs, Print PDF. | E3, 2026-11-03 | — |
| 2 | A Print Intel workbook is a snapshot. After sheets are renumbered or sets change, its PrintSets sheet is stale; Print PDF still prints the set by name from the model. | Re-export Print Intel after sheet or set changes and re-enter the PrintJobs rows (the export overwrites them). | E3, 2026-11-03 | FP51 (stale pre-filled folders) is related |
| 3 | "Browse For Folder" dialogs do not accept a typed folder name; "Make New Folder" leaves the folder named "New folder". | Pick an existing folder, or create the folder beforehand. | E3, 2026-11-03 | — |
| 4 | The help page is the fastest way in: F1 on a ribbon command opens the vendor help at that command. | Read the help section before the first run of a command in a session. | E3, 2026-11-03 | — |
| 5 | Commands posted while Revit Home is showing wait until Home is left; closing the document the bridge holds throws. | See ARPL-DOC-0003 rules 7 and 11. | E3, 2026-10-28 | FP53, FP54 |

## Packs that use this add-in

- ARPL-DOC-0003: Weekly print-set booklets with ZEN: one Revit print set per model, Print Intel workbook, ACC Gate Print PDFs

## Open with the vendor

- A command to create or update print sets from the PrintSets sheet of a Print Intel workbook has been proposed to the vendor (2026-11-03). Until it exists, lesson 1 applies.
