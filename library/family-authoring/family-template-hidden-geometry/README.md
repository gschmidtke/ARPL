# ARPL-FAM-0003: Template with hidden geometry

| | |
|---|---|
| Level | 1 |
| Work class | W1 |
| Workflows | family-authoring |
| Disciplines | generic |
| Project types | generic |
| Revit tested | 2024 |
| Status | candidate |

**Intent:** Build a base cabinet family

## Learning curve

| Version | Instruction | Result | Problem |
|---|---|---|---|
| v01 | Family built from the Metric Casework template | Bounding box 900 mm larger than modelled | The template carries default geometry |
| v02 | Built from Metric Generic Model, then OwnerFamily.FamilyCategory set to Casework | Clean bounding box |  |

## Lesson
Some family templates carry hidden default geometry.

## Rule
Build from the Generic Model template and set the category; check the bounding box after building.

## Validation
- Bounding box against the modelled size
