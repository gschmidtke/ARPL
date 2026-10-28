# ARPL-PAR-0002 rev 1: One shared parameter file per company: find every candidate, choose one master, edit it byte-exact, keep project parameters in a project group

_Generated from this pack's files by tools/build_catalogs.py. Edit manifest.json, intent.md, vNN/ or final/rule.json instead._

| | |
|---|---|
| Level | 2 |
| Work class | W7 |
| Status | candidate |
| Use when | Starting coordinator work on a project and the shared parameter file in use is not known; Two teams report the same parameter with different GUIDs, or schedules lose values after a family reload; A typo in a shared parameter name must be fixed without breaking existing values |
| Not for | Annotation families that carry the review stamp (QAQC note block): those are families loaded into the model, not entries in the shared parameter file; Deciding the company's parameter naming standard: that is the owner's decision |
| Workflows | parameters-data, model-administration |
| Disciplines | bim-vdc, generic |
| Project types | generic |
| Revit tested | 2024 |
| API | Application.SharedParametersFilename, DefinitionFile, ExternalDefinition.GUID, InstanceBinding, BindingMap.Insert, BindingMap.ReInsert |
| Failure patterns | FP03, FP31 |
| Contributors | Gottfried Schmidtke with Claude |

**Intent:** Make sure the company and each project use exactly one shared parameter file, so a parameter has one GUID everywhere; fix names in that file without breaking values that already exist in models.

## Learning curve

| Version | Instruction | Result | Problem | Found by |
|---|---|---|---|---|
| v01 | Search the company's ACC project files and local folders for *.txt files with the shared parameter header (*META / *GROUP / *PARAM); compare GUIDs and names against the parameters bound in the six Snowdon models; record each file in an audit CSV. | One master file in the company's R&D project files; the GUIDs bound in the models matched it. One misspelled entry (TICKNESS) in the DIMENSIONS group. |  |  |
| v02 | Rename TICKNESS to THICKNESS in the master file, keeping its GUID; add a project group with 25 project-prefixed instance parameters (SNOW_) for the LOIN schedule; back up the file first. | First write lost the file's CRLF line endings; redone byte-exact (UTF-16 LE with BOM, CRLF, tab-separated). Revit reads the edited file; the renamed parameter keeps its GUID and therefore its values. | A plain text rewrite changed the encoding and line endings of a file Revit had written. | comparing the file bytes before and after the edit |

## Lesson
A shared parameter is its GUID, not its name: keep one file, rename in place with the GUID unchanged, and write the file exactly as Revit wrote it.

## Rule
1. Before any parameter work, list every shared parameter file the company and project can reach (cloud project files, local folders, the path set in Revit) and compare GUIDs with the parameters bound in the models.
2. Choose one master file per company with the owner; record the others as superseded and stop binding from them.
3. Back up the master file (dated copy) before every edit.
4. Fix a misspelled name by renaming the entry and keeping its GUID; never delete and recreate, which makes a new parameter and orphans the values.
5. Project-specific parameters go into their own group with a project prefix (for example SNOW_ for Snowdon); company parameters keep the company groups.
6. Write the file in Revit's own format: UTF-16 LE with BOM, CRLF line endings, tab-separated columns; set USERMODIFIABLE to 0 for parameters filled by scripts.
7. Review stamps (reviewer, date, comments) belong to an annotation family and its schedule; the parameters can live in the shared file, the family is loaded separately.

## Validation
- Every GUID bound in the models is found in the master file.
- No name appears twice with different GUIDs across the files found.
- The edited file has the same encoding, BOM and line endings as the backup.
