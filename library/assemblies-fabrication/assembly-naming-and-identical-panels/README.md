# ARPL-ASM-0005: Assembly naming and identical panels

| | |
|---|---|
| Level | 1 |
| Work class | W3 |
| Workflows | assemblies-fabrication, documentation |
| Disciplines | construction, structural, architecture |
| Project types | generic |
| Revit tested | 2024 |
| Status | candidate |

**Intent:** One named assembly per wall

## Learning curve

| Version | Instruction | Result | Problem |
|---|---|---|---|
| v01 | AssemblyInstance.Create, then set AssemblyTypeName in the same transaction | Exception 'No valid type for the assembly instance'; assembly kept a default name | The assembly type exists only after the creating transaction commits |
| v02 | Rename in a second transaction | Named. East and West panels share one assembly type because they're identical |  |

## Lesson
Revit detects identical assemblies and gives them one type.

## Rule
Name assemblies after commit; document identical assemblies once with a quantity ('build 2').

## Validation
- Assembly type names and member counts read back
