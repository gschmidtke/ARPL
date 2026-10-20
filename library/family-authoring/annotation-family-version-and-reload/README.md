# ARPL-FAM-0004 rev 1: Annotation family from a newer Revit version

_Generated from this pack's files by tools/build_catalogs.py. Edit manifest.json, intent.md, vNN/ or final/rule.json instead._

| | |
|---|---|
| Level | 2 |
| Work class | W1 |
| Status | candidate |
| Use when | loading or editing annotation families (tags, labels); loading a family saved in another Revit version |
| Not for | - |
| Workflows | family-authoring, model-administration |
| Disciplines | bim-vdc |
| Project types | generic |
| Revit tested | 2024 |
| API | BasicFileInfo, Document.LoadFamily, TextElement |
| Failure patterns | FP05 |
| Contributors | Gottfried Schmidtke with Claude |

**Intent:** Load and restyle a QAQC annotation family

## Learning curve

| Version | Instruction | Result | Problem | Found by |
|---|---|---|---|---|
| v01 | Load QAQC.rfa into the Revit 2024 project | Load refused | The family was saved in Revit 2025 (BasicFileInfo.Format) | BasicFileInfo.Extract |
| v02 | Rebuild the family in 2024; save as QAQC_R2024.rfa and load | Loaded as a new family 'QAQC_R2024' | Family name comes from the file name, so it didn't replace the existing family | guard check |
| v03 | Save the 2024 copy as R2024\QAQC.rfa and reload with overwrite; capture ids before loading | Family replaced | Objects captured before the reload were invalidated (new Family element) | InvalidObjectException |

## Lesson
File version, file name and reload behaviour all decide whether a family update succeeds.

## Rule
Check BasicFileInfo before loading; keep the file name equal to the family name; capture element ids (not objects) before a reload. Labels in annotation families can't be created or retyped by the API, only moved.

## Validation
- Family name and id read back after reload
