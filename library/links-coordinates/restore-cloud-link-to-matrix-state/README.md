# ARPL-LNK-0003 rev 3: Restore a cloud link to the state its link matrix defines: identity by cloud GUID, never move a shared link, re-create or keep-and-report, no dialogs

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
| API | RevitLinkInstance.GetLinkDocument, Document.GetCloudModelPath, ModelPath.GetModelGUID, ModelPath.GetProjectGUID, RevitLinkType.GetExternalResourceReferences, ExternalResourceReference.GetReferenceInformation, RevitLinkType.GetExternalFileReference, RevitLinkType.IsLoaded, RevitLinkType.Load, RevitLinkType.LoadFrom, RevitLinkInstance.Create(Document, ElementId, ImportPlacement), ImportPlacement.Shared, Element.Pinned, ProjectLocation.GetProjectPosition, RevitLinkInstance.GetTotalTransform, IFailuresPreprocessor, FailuresAccessor.DeleteWarning, SubTransaction, WorksetConfigurationOption.OpenAllWorksets, Document.PublishCoordinates, RevitLinkType.HasSaveablePositions, Element.GetDependentElements |
| Failure patterns | FP68, FP69, FP70, FP71, FP72, FP73, FP74, FP11, FP50, FP41 |
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
| v07 | Before re-creating, find out what the shared-site binding is and whether an existing instance can be bound without deletion: compare Create Shared, Create Origin + move, copy, PublishCoordinates (instance only / with link location id), AcquireCoordinates, MoveBasePointToHostBasePoint, a second host site, and the same on an ACC host; every change rolled back | The binding is stored, not positional (FP69 corrected). File links: PublishCoordinates with the link location id binds an in-place instance without deleting anything. Cloud links: refused (FP73). Moving a bound instance rewrites the linked model's site (FP72). Create Shared follows the host's active site and is refused while a bound instance exists (FP74). ACC test host reopened afterwards: version and all five links unchanged. | Re-creating (v03-v06) binds every link but deletes tags, dimensions and view settings attached to the old instance; for cloud links there is no non-destructive alternative, so keeping such instances and reporting the unresolved binding is the conservative choice | bridge-run research, rolled-back transactions, reopen check |

## Lesson
Shared-site binding is a stored relationship between a link instance and a site of the linked model, not a property of its position. Linking by shared coordinates creates it; moving never creates it, and moving a bound link rewrites the linked model's coordinates. For file links the API can bind an in-place instance (PublishCoordinates with the link location id); for cloud links it cannot, so the bound state is reachable only by re-creating the instance, which deletes what is attached to it. A repair must never move a bound link, must decide between re-creating and keeping an unbound one by what depends on it, and must report what it could not bind.

## Rule
1. Identity: loaded link -> GetLinkDocument().GetCloudModelPath() GUIDs; unloaded ACC link -> ExternalResourceReference.GetReferenceInformation() LinkedModelProjectId / LinkedModelModelId (observed 2024.3); file reference only for file-based links; name only when no identity can be read, and never over a link whose identity is known to be another model.
2. Load governed links before checking placement or binding (RevitLinkType.Load): an unloaded link always reads '<Not Shared>'. In a batch open all worksets; run with no other open document that has the same links loaded.
3. Check the host's active site first (Create Shared places relative to it, FP74). Then per instance: bound and in place -> nothing; bound and off position -> do NOT move (it would rewrite the link's site, FP72), report a host/link coordinate mismatch; unbound with nothing attached (GetDependentElements without the instance and its internal elements) -> create the new instance with ImportPlacement.Shared FIRST, apply workset and room bounding, pin, verify position AND binding, then delete the old one, in a SubTransaction; unbound with dependents -> keep the instance, move it into place if needed (safe while unbound), pin, and report the binding as unresolved; for a file link exactly in place PublishCoordinates(new LinkElementId(instance, link active location id)) can bind it, verify the link's site values unchanged.
4. Count what depends on each instance before deciding, and report what a re-creation removed.
5. Register an IFailuresPreprocessor on every repair transaction (delete warnings, list them in the report); a run with anything unfixable or unresolved says so in its status, never plain OK.
6. Run the repair twice: the second run must change nothing.

## Validation
- Every link is at the shared position and pinned; its name ends with the site name, or the report lists it as kept unbound with the reason
- No bound link was moved: HasSaveablePositions() is false on every link type after the run
- No modal dialog during the run; warnings listed in the report
- Second run: all rows matched, nothing created, re-placed, moved or removed
