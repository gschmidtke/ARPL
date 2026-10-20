# ARPL-ADM-0001 rev 1: An exception inside an open Transaction crashed Revit

_Generated from this pack's files by tools/build_catalogs.py. Edit manifest.json, intent.md, vNN/ or final/rule.json instead._

| | |
|---|---|
| Level | 1 |
| Work class | W5 |
| Status | candidate |
| Use when | any scripted change that starts its own Transaction, especially inside a TransactionGroup; a bridge or add-in runs agent-written C# against a live model |
| Not for | read-only scripts that open no transaction |
| Workflows | model-administration, model-change |
| Disciplines | generic |
| Project types | generic |
| Revit tested | 2024 |
| API | Transaction, TransactionGroup, IDisposable, Transaction.RollBack |
| Failure patterns | FP14, FP11 |
| Contributors | Gottfried Schmidtke with Claude |

**Intent:** replace a placeholder roof by script, using own transactions inside the bridge's TransactionGroup (mode "group").

**Incident:** 2026-10-20 18:52, Revit 2024.3 fatal error; recovery files saved. Journal: journal.0074.txt. Full record: docs/incidents/2026-10-20-revit-fatal-error.md

## Learning curve

| Version | Instruction | Result | Problem | Found by |
|---|---|---|---|---|
| v01 | new Transaction(...) ; tr.Start(); ... doc.Create.NewFootPrintRoof(...) (threw ArgumentNullException) ; no using/try, so tr stayed open when the exception left the snippet; bridge then aborted its TransactionGroup | Revit fatal error: 'Revit has experienced a fatal error and cannot continue' | Journal: 'Missing transaction marker before abort transaction group', 'Undo phases not properly nested', 'A Transaction object or the document itself got destroyed while executing a call', then 'Pure Virtual Function Call!!! Go to crash protection'. The open sub-transaction was destroyed under the aborting group. | Revit journal (journal.0074.txt) read after restart |
| v02 | Same script with every Transaction in a using block and the body in try/catch returning the failing step | The exception rolled back cleanly; the script reported step 'create' and the real cause (see ARPL-CHG-0002). No crash. |  | dry run |

## Lesson
In Revit 2024 an exception that leaves a scripted Transaction open while an enclosing TransactionGroup is aborted can crash Revit, not just fail the script. The first visible error (ArgumentNullException) was harmless; the crash came from the unclosed transaction.

## Rule
Wrap every own Transaction (and SubTransaction) in using(...) so it is rolled back during exception unwinding, before any enclosing group is aborted. Wrap the script body in try/catch and return the failing step. Dry-run every new API call first. Bridges should run 'group' mode snippets so that unwinding happens before the group is rolled back.

## Validation
- Dry run of the guarded script returns the error and step instead of crashing
- Journal shows no 'Undo phases not properly nested' warnings
