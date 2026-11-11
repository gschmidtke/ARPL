# ARPL-LNK-0003 rev 2: Restore a cloud link to the state its link matrix defines: identity by cloud GUID, re-place by shared coordinates, no dialogs

_Generated from this pack's files by tools/build_catalogs.py. Edit manifest.json, intent.md, vNN/ or final/rule.json instead._

| | |
|---|---|
| Level | 2 |
| Work class | W7 |
| Status | candidate |
| Use when | A repair run must bring every link of a host back to the link matrix: found by cloud identity, at the shared position, associated with the shared site, pinned, on its workset; A link was moved, rotated, unloaded, removed, duplicated or put on another workset; The run is unattended (batch over many hosts) and must not stop on a dialog |
| Not for | Models that do not share one coordinate system: set coordinates first (ARPL-LNK-0001); Local file links (identity there comes from the file path); Links placed origin to origin on purpose |
| Workflows | links-coordinates, coordination, model-administration |
| Disciplines | bim-vdc, generic |
| Project types | generic |
| Revit tested | 2024 |
| API | RevitLinkInstance.GetLinkDocument, Document.GetCloudModelPath, ModelPath.GetModelGUID, ModelPath.GetProjectGUID, RevitLinkType.GetExternalResourceReferences, ExternalResourceReference.GetReferenceInformation, RevitLinkType.GetExternalFileReference, RevitLinkType.IsLoaded, RevitLinkType.Load, RevitLinkType.LoadFrom, RevitLinkInstance.Create(Document, ElementId, ImportPlacement), ImportPlacement.Shared, Element.Pinned, ProjectLocation.GetProjectPosition, RevitLinkInstance.GetTotalTransform, IFailuresPreprocessor, FailuresAccessor.DeleteWarning, SubTransaction, WorksetConfigurationOption.OpenAllWorksets |
| Failure patterns | FP68, FP69, FP70, FP71, FP11, FP50, FP41 |
| Contributors | Gottfried Schmidtke with Claude |

**Intent:** a repair run brings every link of a host back to its link matrix row, the way linking created it: the right cloud model, exactly once, at the shared position, associated with the shared site, pinned, on its workset. Nothing is left for a person to clean up, and no dialog stops an unattended batch (owner rule, 2026-11-10).

Tested 2026-11-10 in Revit 2024.3 on the Snowdon Towers sample federation (ACC). Cases: link moved 11-28 m and rotated, link type removed, link unloaded, link on another workset, duplicate instance, Overlay/Attachment change, a wrong model GUID in the matrix, several deviations at once. Each case ran twice; the second run had to change nothing.

## Learning curve

| Version | Instruction | Result | Problem | Found by |
|---|---|---|---|---|
| v01 | Find the existing link by RevitLinkType.GetExternalFileReference().GetPath() GUIDs, else by link name = model key | Loaded ACC links not found when the file name differs from the model key; the repair tried to create them again: 'document already contains a linked model' | GetExternalFileReference throws for ACC cloud links (loaded and, as found later, unloaded) (FP70) | owner test |
| v02 | Identity from the loaded link document: RevitLinkInstance.GetLinkDocument().GetCloudModelPath() project and model GUID; name only when no identity | Loaded links matched by GUID; a moved link was moved back by RotateElement/MoveElement and verified | The moved link sat exactly at the shared position but its instance name read 'location <Not Shared>'; links re-created by shared coordinates read 'location SNOWDON' (FP69) | owner, from the link instance names |
| v03 | Re-place instead of move: delete the instance, RevitLinkInstance.Create(doc, typeId, ImportPlacement.Shared), apply workset, pin | Position and shared-site association restored | Revit showed a modal warning 'All instances of link ... have been deleted, but the model itself is still loaded' with a Remove Link button: an unattended batch would stop there (FP11) | owner screenshot |
| v04 | Create the new instance first, then delete the old one; register an IFailuresPreprocessor on every repair transaction that deletes warnings and lists them in the report | No dialog; four links re-placed in one run | An unloaded link was not found again ('already contains a linked model'): GetExternalFileReference throws for unloaded ACC links too (FP70) | owner test |
| v05 | Identity fallback for unloaded ACC links from ExternalResourceReference.GetReferenceInformation(): LinkedModelProjectId, LinkedModelModelId, LinkedModelRegion; then RevitLinkType.Load() before the placement check. Batch: open all worksets | Local cases all pass with a clean second run. Batch with only the link worksets open failed to load links: 'The element ... is in a closed workset' (the link TYPE's workset) and 'loaded into multiple documents and cannot be reloaded' (another open document had the link loaded) (FP71) | Batch fix (open all worksets) built; retested in v06 | bridge-run test, report file |
| v06 | Batch repair opens the host with all worksets (WorksetConfigurationOption.OpenAllWorksets), then the same identity, load, re-place and warning handling as v05; no other document of the federation open in the session | Electrical host (link moved 15 m and rotated 20 degrees, three links '<Not Shared>'): 4 re-placed by shared coordinates, 1 matched, 0 errors, synchronized; open 114 s. Rerun (host reopened from the cloud): 5 matched, nothing changed. Two further hosts in one batch: both 5 matched, open 62-69 s each. |  | bridge-run test, report files |

## Lesson
A cloud link can be in the right place and still not be in the state linking produced: Revit records the shared-site association only when it places a link by shared coordinates, and the API cannot set it on an existing instance. Identity of ACC links is not available through the file reference at all. A repair that is to leave nothing behind must identify by cloud GUID, re-create rather than move, and absorb every warning.

## Rule
1. Identity: loaded link -> GetLinkDocument().GetCloudModelPath() GUIDs; unloaded ACC link -> ExternalResourceReference.GetReferenceInformation() LinkedModelProjectId / LinkedModelModelId (observed 2024.3); file reference only for file-based links; name only when no identity can be read, and never over a link whose identity is known to be another model.
2. Load governed links before checking placement (RevitLinkType.Load); in a batch open all worksets, because a link type on a closed workset cannot be loaded; run with no other open document that has the same links loaded.
3. Placement by shared coordinates = at the shared position AND associated (instance name ends with the site name, not '<Not Shared>'). If either fails: create the new instance with ImportPlacement.Shared FIRST, apply workset and room bounding, pin, verify, then delete the old instance; do it in a SubTransaction and roll back if the check fails.
4. Count annotations that go with the old instance (GetDependentElements filtered to annotation categories) and report them; Delete() also returns internal elements of every link instance.
5. Register an IFailuresPreprocessor on every repair transaction (delete warnings, list them in the report); a run with anything unfixable reports 'OK with N row errors', never plain OK.
6. Run the repair twice: the second run must change nothing.

## Validation
- Every link instance name ends with the shared site name and the instance is pinned
- Every link's total transform places it at the shared position (compare ProjectLocation.GetProjectPosition of host and link at two points)
- No modal dialog during the run; warnings listed in the report
- Second run: all rows matched, nothing created, re-placed, moved or removed
