# ARPL-ASM-0005 rev 2: Assembly naming and identical panels

_Generated from this pack's files by tools/build_catalogs.py. Edit manifest.json, intent.md, vNN/ or final/rule.json instead._

| | |
|---|---|
| Level | 1 |
| Work class | W3 |
| Status | candidate |
| Use when | creating and naming Revit assemblies; several identical panels or modules need drawings |
| Not for | - |
| Workflows | assemblies-fabrication, documentation |
| Disciplines | construction, structural, architecture |
| Project types | generic |
| Revit tested | 2024 |
| API | AssemblyInstance.Create, AssemblyType, AssemblyInstance.SetTransform |
| Failure patterns | FP05, FP15, FP16 |
| Contributors | Gottfried Schmidtke with Claude |

**Intent:** One named assembly per wall

## Learning curve

| Version | Instruction | Result | Problem | Found by |
|---|---|---|---|---|
| v01 | AssemblyInstance.Create, then set AssemblyTypeName in the same transaction | Exception 'No valid type for the assembly instance'; assembly kept a default name | The assembly type exists only after the creating transaction commits | exception |
| v02 | Rename in a second transaction | Named. East and West panels share one assembly type because they're identical |  |  |

## Lesson
Revit detects identical assemblies and gives them one type.

## Rule
Name assemblies after commit; document identical assemblies once with a quantity ('build 2'). Identical panels may share one assembly type only while their geometry stays identical. When they diverge (raked end walls are mirror images, not copies), give each its own type before editing members: changing the members of one instance of a shared type opens a modal Revit dialog no script can answer and copies the change to the other instances (FP15). An assembly made with AssemblyInstance.Create gets a frame along the project axes; set it with SetTransform (BasisX along the wall, BasisY to the interior) before creating its views (FP16).

## Validation
- Assembly type names and member counts read back
