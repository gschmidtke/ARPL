# ARPL-ASM-0003 rev 1: Revit Parts for wall layers: a dead end

_Generated from this pack's files by tools/build_catalogs.py. Edit manifest.json, intent.md, vNN/ or final/rule.json instead._

| | |
|---|---|
| Level | 2 |
| Work class | W3 |
| Status | candidate |
| Use when | splitting wall layers into separate fabrication pieces; considering Revit Parts (PartUtils.CreateParts) for panels or BOM |
| Not for | Parts for simple area takeoffs or visual layer display |
| Workflows | assemblies-fabrication, family-authoring |
| Disciplines | architecture, structural, construction |
| Project types | residential |
| Revit tested | 2024 |
| API | PartUtils, AssemblyInstance |
| Failure patterns | FP03, FP11 |
| Contributors | Gottfried Schmidtke with Claude |

**Intent:** Make plywood and siding from the wall type's layers using Revit Parts

**LOD:** LOD 400

## Learning curve

| Version | Instruction | Result | Problem | Found by |
|---|---|---|---|---|
| v01 | PartUtils.CreateParts on the exterior walls | 0 parts, then a modal dialog 'Can't make Parts out of these Elements' blocked the bridge | Vertically compound wall type with integral sweeps; no error reachable through the API | bridge timeout, screenshot |
| v02 | Research: how do AGACAD Wood Framing and StrucSoft MWF do it? They place lumber and sheathing families and group them into assemblies; the user's own method is the same | Method changed: component families + assemblies |  |  |

## Lesson
The 'native' Revit route isn't always the production route; established tools are precedents.

## Rule
For fabrication panels use component families plus assemblies, not Parts. Check how established tools solve a task before choosing a method.

## Validation
- Method review against two commercial tools
