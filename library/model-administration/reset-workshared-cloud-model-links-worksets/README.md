# ARPL-ADM-0002 rev 1: Reset a workshared cloud model: remove all Revit links and delete user worksets with all worksets closed

_Generated from this pack's files by tools/build_catalogs.py. Edit manifest.json, intent.md, vNN/ or final/rule.json instead._

| | |
|---|---|
| Level | 2 |
| Work class | W5 |
| Status | candidate |
| Use when | batch-clean several workshared cloud (ACC/BIM 360) models before a relinking run, a demo or a standards reset; delete user worksets and move their elements to Workset1 without opening the worksets; remove every RevitLinkType and RevitLinkInstance from a host model |
| Not for | detaching or archiving models (use DetachFromCentral instead); non-workshared files; removing CAD imports or links (ImportInstance, CADLinkType) |
| Workflows | model-administration |
| Disciplines | generic |
| Project types | generic |
| Revit tested | 2024 |
| API | ModelPathUtils.ConvertCloudGUIDsToCloudPath, OpenOptions, WorksetConfiguration, WorksetConfigurationOption.CloseAllWorksets, RevitLinkType, RevitLinkInstance, WorksharingUtils.CheckoutWorksets, WorksetTable.CanDeleteWorkset, WorksetTable.DeleteWorkset, DeleteWorksetSettings, Document.SynchronizeWithCentral, RelinquishOptions |
| Failure patterns | FP15, FP19, FP24, FP25 |
| Contributors | Gottfried Schmidtke with Claude |

**Intent:** bring ten workshared ACC cloud models back to a clean start (no Revit links, only Workset1 and the shared levels/grids workset) so that a batch relinking tool can be shown creating links and worksets from scratch.

**Context:** the relinking tool itself is a third-party add-in and is not described here; this pack covers only the Revit API cleanup, which any batch relinking workflow needs.

## Learning curve

| Version | Instruction | Result | Problem | Found by |
|---|---|---|---|---|
| v01 | Open each model with default worksets, delete links, then WorksetTable.DeleteWorkset directly (no checkout, no transaction) | Links removed; every workset deletion refused | CanDeleteWorkset returned false: the worksets were not owned by the current user. Opening all worksets also made each open slower. | return values of CanDeleteWorkset |
| v02 | Open with all worksets closed (owner's instruction); CheckoutWorksets on the worksets plus Workset1; DeleteWorkset outside a transaction | CanDeleteWorkset now true; DeleteWorkset threw | 'Modification of the document is forbidden ... no open transaction': deleting a workset is a document modification and needs a Transaction even though checkout does not. | exception message |
| v03 | Same, with the delete loop inside a Transaction and the sync with relinquish after it | 10 of 10 models clean: 0 links, 2 user worksets each, synced and relinquished; about 20 s per model |  | re-open counts and the sync result |

## Lesson


## Rule
Per model, in one bridge call of at most 2-3 models (each cloud open+sync takes 15-25 s): 1) open by cloud GUIDs (ConvertCloudGUIDsToCloudPath) with WorksetConfiguration(CloseAllWorksets) and DoNotDetach; closed worksets are enough for both tasks and keep the open fast. 2) Delete all RevitLinkType and RevitLinkInstance ids in one Transaction with a failures preprocessor. 3) Collect user worksets; keep Workset1 and the shared levels/grids workset. Call WorksharingUtils.CheckoutWorksets on the worksets to delete plus Workset1 (works while they are closed); make Workset1 active. 4) In a Transaction, for each workset: DeleteWorksetSettings(MoveElementsToWorkset, Workset1), CanDeleteWorkset, then DeleteWorkset; collect failures per workset instead of aborting. 5) SynchronizeWithCentral with SaveLocalBefore and SaveLocalAfter true, RelinquishOptions(true) and a comment; skip the sync when nothing changed. 6) Close(false) in finally. Return per-model counts and timings. Check free disk space first: every cloud open fills the local collaboration cache.

## Validation
- Re-open check: RevitLinkType and RevitLinkInstance counts are 0
- User worksets are exactly Workset1 plus the shared levels/grids workset
- No elements or worksets remain borrowed after sync (relinquished)
- Sync comment visible in the cloud model's version history
