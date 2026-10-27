# ARPL-LNK-0002 rev 1: Batch-link cloud models from a registry and link matrix, placed by shared coordinates; verify by link transform

_Generated from this pack's files by tools/build_catalogs.py. Edit manifest.json, intent.md, vNN/ or final/rule.json instead._

| | |
|---|---|
| Level | 2 |
| Work class | W7 |
| Status | candidate |
| Use when | Every model of a federated cloud project must link the others, driven by a registry and a host-by-link matrix; A batch tool generated the link matrix and its settings must be checked before the run; Link placement has to be proven after the run |
| Not for | Projects whose models do not share one coordinate system: set coordinates first (ARPL-LNK-0001); Local file links |
| Workflows | links-coordinates, coordination, model-administration |
| Disciplines | bim-vdc, generic |
| Project types | generic |
| Revit tested | 2024 |
| API | RevitLinkType.Create(Document, ModelPath, RevitLinkOptions), RevitLinkInstance.Create(Document, ElementId, ImportPlacement), ImportPlacement.Shared, RevitLinkInstance.GetTotalTransform, Transform.IsIdentity, RevitLinkType.IsLoaded, ModelPathUtils.ConvertCloudGUIDsToCloudPath, WorksetConfigurationOption.CloseAllWorksets |
| Failure patterns | FP46, FP24 |
| Contributors | Gottfried Schmidtke with Claude |

**Intent:** Link every model of a 13-model cloud campus to the other 12 (156 links) in one unattended batch, placed by shared coordinates, and prove the placement afterwards.

Measured: 13/13 hosts OK, 0 dialogs, 21 min; model opens 7-11 s each in the batch. Coordinates come from ARPL-LNK-0001; models and registry from ARPL-ADM-0003.

## Learning curve

| Version | Instruction | Result | Problem | Found by |
|---|---|---|---|---|
| v01 | Generate the host-by-link matrix from the registry with the batch tool's default export and run the batch. | Not run as generated: reading the matrix showed 'use shared coordinates' = false on all 169 rows (also load-on-open false, room bounding false). | A generated default silently contradicted the project's coordinate setup; links would have been placed origin to origin (FP46). | reading the matrix values before the run |
| v02 | Back up the matrix, set the shared-coordinates column to true on every row, close the models the batch will open, run the batch. | 13/13 hosts OK, 12 links each, 0 dialogs, 21 min. | None. | batch log and per-host reports (rows found = instances created, 0 skipped) |
| v03 | Verify placement on hosts by link transform; open hosts with all worksets closed for later checks. | All link instances have an identity total transform (all models share one coordinate system and one internal origin); all link types loaded after creation. Worksets-closed opens take about 30 s and keep the links unloaded. | None. | RevitLinkInstance.GetTotalTransform().IsIdentity on every instance |

## Lesson
A generated link configuration must be read before a batch run: defaults can contradict the project's coordinate setup. After the run, placement is proven by the link transform, not by looking.

## Rule
1. Before the run, read the generated matrix: placement by shared coordinates on every row; link type, workset, load-on-open and room bounding as the project wants. Change it on a backup copy only (FP46).
2. Close every model the batch will open; set the batch output folder explicitly.
3. After the run: every host has as many link instances as its matrix rows; when all models share one coordinate system and internal origin, every link instance's total transform is identity; otherwise compare it with the transform implied by the shared coordinates.
4. For later read-only checks, open hosts with all worksets closed so links on their own worksets stay unloaded.

## Validation
- Per host: link instances = matrix rows for that host; 0 skipped or errored.
- Every RevitLinkInstance.GetTotalTransform() equals the expected transform (identity in a common-origin federation).
