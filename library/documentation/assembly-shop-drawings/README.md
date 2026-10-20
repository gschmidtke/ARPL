# ARPL-DOC-0001: Shop drawings: invalid references and swapped elevations

| | |
|---|---|
| Level | 2 |
| Work class | W6 |
| Workflows | documentation, views-graphics, assemblies-fabrication |
| Disciplines | construction, structural, architecture |
| Project types | residential |
| Revit tested | 2024 |
| Status | candidate |

**Intent:** Assembly shop drawings for three wall panels

## Learning curve

| Version | Instruction | Result | Problem |
|---|---|---|---|
| v01 | All dimensions in one transaction; stud chain from CenterFrontBack references | Blocking dialog 'dimension references are or have become invalid'; whole sheet rolled back | Stud centre-plane references are invalid for this family and view |
| v02 | One transaction per dimension in a TransactionGroup, rollback on error; stud chain from stud faces | 10 of 11 chains, then 11 of 11 | North sheet: 'exterior' elevation showed the inside; the assembly transform had reverted to world X |
| v03 | Pick exterior and interior elevations by ViewDirection · exterior normal, not by the assembly transform | All three sheets correct |  |

## Lesson
Per-element transactions contain failures; implicit state (assembly transforms) can't be trusted.

## Rule
Isolate risky annotation in its own transaction and verify every sheet visually.

## Validation
- PDF export rendered and reviewed per sheet
