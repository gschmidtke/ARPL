# ARPL-ASM-0003: Revit Parts for wall layers: a dead end

| | |
|---|---|
| Level | 2 |
| Work class | W3 |
| Workflows | assemblies-fabrication, family-authoring |
| Disciplines | architecture, structural, construction |
| Project types | residential |
| Revit tested | 2024 |
| Status | candidate |

**Intent:** Make plywood and siding from the wall type's layers using Revit Parts

## Learning curve

| Version | Instruction | Result | Problem |
|---|---|---|---|
| v01 | PartUtils.CreateParts on the exterior walls | 0 parts, then a modal dialog 'Can't make Parts out of these Elements' blocked the bridge | Vertically compound wall type with integral sweeps; no error reachable through the API |
| v02 | Research: how do AGACAD Wood Framing and StrucSoft MWF do it? They place lumber and sheathing families and group them into assemblies; the user's own method is the same | Method changed: component families + assemblies |  |

## Lesson
The 'native' Revit route isn't always the production route; established tools are precedents.

## Rule
For fabrication panels use component families plus assemblies, not Parts. Check how established tools solve a task before choosing a method.

## Validation
- Method review against two commercial tools
