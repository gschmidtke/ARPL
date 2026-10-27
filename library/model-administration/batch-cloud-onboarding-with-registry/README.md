# ARPL-ADM-0003 rev 1: Batch-onboard local models to the cloud and register each one: verify by document state, handle posted-command dialogs

_Generated from this pack's files by tools/build_catalogs.py. Edit manifest.json, intent.md, vNN/ or final/rule.json instead._

| | |
|---|---|
| Level | 2 |
| Work class | W7 |
| Status | candidate |
| Use when | An agent uploads or registers a series of local models to one cloud project folder; A bridge call outlasts the bridge's reply wait (cloud save, enable worksharing, sync); An add-in command started by PostCommand opens file pickers, confirmation prompts or result dialogs; Some models may already exist in the cloud folder, uploaded earlier by someone else |
| Not for | Single interactive uploads done by a person; Batch tools that already run headless without dialogs: use those and skip the screen handling |
| Workflows | model-administration, links-coordinates |
| Disciplines | bim-vdc, generic |
| Project types | generic |
| Revit tested | 2024 |
| API | Document.SaveAsCloudModel, Autodesk.Revit.Exceptions.RevitServerModelAlreadyExistsException, Document.EnableCloudWorksharing, Document.IsModelInCloud, Document.IsWorkshared, Document.PathName, Document.GetCloudModelPath, ModelPath.GetModelGUID, ModelPath.GetProjectGUID, Document.GetHubId, Document.GetProjectId, Document.GetCloudFolderId, ModelPathUtils.ConvertCloudGUIDsToCloudPath, UIApplication.OpenAndActivateDocument, UIApplication.PostCommand, RevitCommandId.LookupCommandId, ProjectInfo.BuildingName, Document.SynchronizeWithCentral, RelinquishOptions, OpenOptions.DetachFromCentralOption |
| Failure patterns | FP22, FP32, FP41, FP43, FP45 |
| Contributors | Gottfried Schmidtke with Claude |

**Intent:** For each of 13 local per-building models: set its identity in Project Information, save it as a workshared cloud model into one shared cloud folder, run an add-in command that appends the model's cloud GUIDs to a registry CSV, and sync. Some models had already been uploaded by a person earlier, without the agent knowing which.

First model about 15 minutes with several surprises; the stable routine about 3-4 minutes per model, mostly cloud wait. Related: ARPL-LNK-0001 (coordinates and split before this), ARPL-LNK-0002 (linking after this).

## Learning curve

| Version | Instruction | Result | Problem | Found by |
|---|---|---|---|---|
| v01 | Open the local model, set Project Information, SaveAsCloudModel + EnableCloudWorksharing in one bridge call. | The call timed out on the agent side (60 s) but finished in Revit; while 'Enable Worksharing' ran, further bridge calls also timed out. | A timeout says nothing about success; resending would try a second upload (FP22). | wait, then read IsModelInCloud / IsWorkshared / GetCloudModelPath().GetModelGUID() in a short call |
| v02 | Run the registry add-in command on a sibling uploaded earlier, before its Building Name was set. | The registry key came out as the literal text 'Building Name'. | The template's placeholder in Project Information is not empty, so the tool did not ask for a key and used the placeholder (FP43). | reading the registry CSV |
| v03 | Upload a model whose name already existed in the cloud folder. | SaveAsCloudModel threw RevitServerModelAlreadyExistsException after about 58 s; on one model after the 60 s wait, so the agent never saw it. | Afterwards PathName showed 'Autodesk Docs://<project>/<name>.rvt' although nothing was saved: IsModelInCloud false, IsModified true; EnableCloudWorksharing then failed with 'does not have a central location' (FP45). | reading IsModelInCloud and GetCloudModelPath() instead of PathName |
| v04 | Find which models already exist: web viewer, desktop sync folder, then the application's own cloud-open view. | Web viewer not signed in; sync folder not synced; the cloud-open view listed the folder after pressing its refresh (the first view was cached). | Without GUIDs, existing cloud models cannot be opened through the API. | screenshot of the cloud-open view after refresh |
| v05 | Open each pre-existing cloud model through the UI and check it before changing anything. | ProjectPosition and element counts compared with the split report; one model had been uploaded before its split was corrected, and the check confirmed the cloud copy held the corrected version. | A model uploaded by someone else may predate a local fix. | counts and coordinates against the known-good split report |
| v06 | Post the registry command right after the bridge call. | Nothing appeared until the mouse moved over the application; then a file picker, the OS 'already exists, replace?' prompt and a result dialog. While they were open the bridge did not answer. Once the chat window was in front and would have received the typing. | PostCommand runs only when the application is idle and receives input (FP32); keyboard input lands in whatever window has focus (FP41). | screenshots after each step |
| v07 | Handle the dialog chain by keyboard: click into the file-name field, Ctrl+A, type the file name, Enter, Alt+Y, then close the result dialog. | Stable for all remaining models; the tool appended a row each time (verified by reading the CSV, backup taken first). | None once the click into the field always came first. | zoom on the result dialog showing the key; final CSV check: 13 rows, unique keys and GUIDs |
| v08 | Make a local copy of a cloud model as a source file (OpenOptions.DetachFromCentralOption on a cloud path). | ArgumentException: detach option is not valid for cloud model (Revit 2024 API). | Cloud models cannot be detached to a local file through this API; build the source from a local file instead. | the exception |

## Lesson
In a batch of cloud uploads, the bridge reply is not the result: long calls time out, failures can arrive late and leave a misleading PathName, and posted commands open dialogs that block the bridge. Verify each step by document state, keep each call short, and drive dialogs by keyboard with a focus guard.

## Rule
Per model:
1. Open the local file and set identity fields (Building Name = model name, Project Name) in one short call; never leave template placeholder text (FP43); close other documents.
2. Read hub, project and folder ids from an already uploaded sibling (GetHubId, GetProjectId, GetCloudFolderId). Cloud save + enable worksharing in one call; expect a timeout and do not resend (FP22). Wait 60-90 s, then read IsModelInCloud, IsWorkshared and GetCloudModelPath().GetModelGUID() in a short call. Never judge by PathName (FP45).
3. If IsModelInCloud is false, the name already exists in the folder: open that cloud model (cloud-open UI after refresh, or by GUID) and check its coordinates and element counts before touching it.
4. Post the registry command, move the mouse over the application so it runs (FP32), screenshot.
5. Click into the dialog's input field first, then type and confirm by keyboard (FP41); confirm an overwrite prompt only if the tool is known to append and a backup exists.
6. Read the result dialog (key and GUID), close it, then sync with central.
After the batch: one registry row per model, unique keys and GUIDs, no placeholder values. Cloud models cannot be detached to local files through the 2024 API.

## Validation
- Every model: IsModelInCloud and IsWorkshared true, synced, Building Name equals the model name.
- Registry: row count equals model count, keys and model GUIDs unique, no template placeholder text.
- Models uploaded by others: coordinates and element counts match the source.
