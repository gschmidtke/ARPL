# ARPL-DOC-0001 rev 2: Shop drawings: invalid references and swapped elevations

_Generated from this pack's files by tools/build_catalogs.py. Edit manifest.json, intent.md, vNN/ or final/rule.json instead._

| | |
|---|---|
| Level | 2 |
| Work class | W6 |
| Status | candidate |
| Use when | creating dimensioned shop drawings or assembly sheets; adding many dimensions by script |
| Not for | - |
| Workflows | documentation, views-graphics, assemblies-fabrication |
| Disciplines | construction, structural, architecture |
| Project types | residential |
| Revit tested | 2024 |
| API | AssemblyViewUtils, Dimension, Reference, TransactionGroup, IFailuresPreprocessor |
| Failure patterns | FP08, FP02, FP11, FP16 |
| Contributors | Gottfried Schmidtke with Claude |

**Intent:** Assembly shop drawings for three wall panels

## Learning curve

| Version | Instruction | Result | Problem | Found by |
|---|---|---|---|---|
| v01 | All dimensions in one transaction; stud chain from CenterFrontBack references | Blocking dialog 'dimension references are or have become invalid'; whole sheet rolled back | Stud centre-plane references are invalid for this family and view | dialog |
| v02 | One transaction per dimension in a TransactionGroup, rollback on error; stud chain from stud faces | 10 of 11 chains, then 11 of 11 | North sheet: 'exterior' elevation showed the inside; the assembly transform had reverted to world X | PDF review |
| v03 | Pick exterior and interior elevations by ViewDirection · exterior normal, not by the assembly transform | All three sheets correct |  |  |

## Lesson
Per-element transactions contain failures; implicit state (assembly transforms) can't be trusted.

## Rule
Isolate risky annotation in its own transaction and verify every sheet visually. Regenerate the shop drawing whenever the assembly members are replaced: dimensions reference member faces and are deleted with them. DirectShape faces take dimension references like family geometry. Sloped faces cannot be dimensioned in an elevation chain; state the heights at both ends in a note on the view. Check the assembly frame first (FP16).

## Validation
- PDF export rendered and reviewed per sheet
