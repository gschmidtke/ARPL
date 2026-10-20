# Incident: Revit fatal error during scripted roof replacement

**Date:** 2026-10-20, 18:52 (local). **Revit:** 2024.3. **Bridge:** RevitBridge 0.4.0, `run_csharp`, mode `group`. **Model:** ADU-01 (workshared cloud model). **Packs:** [ARPL-ADM-0001](../../library/model-administration/exception-in-open-transaction-crashes-revit/), [ARPL-CHG-0002](../../library/model-change/replace-footprint-roof-revit-2024/). **Failure pattern:** FP14.

## What happened

| Time | Event |
|---|---|
| 18:52:35.014 | Script "ARPL replace placeholder roof" throws `ArgumentNullException` in `Document.NewFootPrintRoof` while its own `Transaction` is open (no `using`, no try/catch) |
| 18:52:35.014 | Journal: `Missing transaction marker before abort transaction group` (UndoMgr.cpp) |
| 18:52:35.018 | Journal: `Undo phases not properly nested` |
| 18:52:35.079 | Journal: `A Transaction object or the document itself got destroyed while executing a call ... The transaction identity is: APITransactionIdentity_1` |
| 18:52:35.080 | Journal: `Pure Virtual Function Call!!! Go to crash protection.` |
| 18:52:38 | Dialog: "Revit has experienced a fatal error and cannot continue." |
| 19:08–19:10 | Recovery files saved by the user's decision: `Documents\ADU-01\ADU-01.rvt` (detached from the cloud), `TONGS Column(Recovery).rfa` |
| 19:30 | Revit restarted; recovery file opened as `ADU-01_detached`; roof recreated with the guarded pattern without error |

## Root cause

1. **Trigger:** `NewFootPrintRoof(..., out ModelCurveArray)` requires the `ModelCurveArray` to be instantiated before the call; passing an uninitialised variable throws `ArgumentNullException`.
2. **Crash:** the exception left the script's own transaction open. The bridge then aborted its enclosing `TransactionGroup` around the still-open transaction, which destroyed it mid-call. Revit treated this as unrecoverable.

My first explanation to the user (deleting a roof that walls were attached to) was wrong; the journal showed the real sequence.

## Contributing conditions

- Low free memory: about 700–800 MB available of 16 GB at crash time (Revit itself used about 0.8 GB). Not the cause, but it leaves little headroom.
- The script combined several first-time API calls (new roof, delete, attach) without a dry run of each.

## Data impact

- Cloud model ADU-01 unchanged since the last sync. Lost from the cloud session: the three annotation-only roof preview views, which are present in the recovery file.
- The recovery file is a detached local copy. Work done in it does not sync back to the cloud model.

## Corrective actions

- Rule recorded in ARPL-ADM-0001: `using` for every Transaction, try/catch reporting the failing step, dry run of every new API call.
- Bridge candidate for 0.4.1: refuse to abort a TransactionGroup while the document is still modifiable, and report it instead; document the pattern in the tool description.
- Decision for the owner: continue in the detached copy, or redo the roof in the cloud model (the scripts are recorded and repeatable).
