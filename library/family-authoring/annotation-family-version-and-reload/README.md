# ARPL-FAM-0004: Annotation family from a newer Revit version

| | |
|---|---|
| Level | 2 |
| Work class | W1 |
| Workflows | family-authoring, model-administration |
| Disciplines | bim-vdc |
| Project types | generic |
| Revit tested | 2024 |
| Status | candidate |

**Intent:** Load and restyle a QAQC annotation family

## Learning curve

| Version | Instruction | Result | Problem |
|---|---|---|---|
| v01 | Load QAQC.rfa into the Revit 2024 project | Load refused | The family was saved in Revit 2025 (BasicFileInfo.Format) |
| v02 | Rebuild the family in 2024; save as QAQC_R2024.rfa and load | Loaded as a new family 'QAQC_R2024' | Family name comes from the file name, so it didn't replace the existing family |
| v03 | Save the 2024 copy as R2024\QAQC.rfa and reload with overwrite; capture ids before loading | Family replaced | Objects captured before the reload were invalidated (new Family element) |

## Lesson
File version, file name and reload behaviour all decide whether a family update succeeds.

## Rule
Check BasicFileInfo before loading; keep the file name equal to the family name; capture element ids (not objects) before a reload. Labels in annotation families can't be created or retyped by the API, only moved.

## Validation
- Family name and id read back after reload
