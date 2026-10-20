# ARPL-FAM-0003 rev 1: Template with hidden geometry

_Generated from this pack's files by tools/build_catalogs.py. Edit manifest.json, intent.md, vNN/ or final/rule.json instead._

| | |
|---|---|
| Level | 1 |
| Work class | W1 |
| Status | candidate |
| Use when | choosing a family template for a new family; family geometry is invisible or too large after building |
| Not for | - |
| Workflows | family-authoring |
| Disciplines | generic |
| Project types | generic |
| Revit tested | 2024 |
| API | Application.NewFamilyDocument, FamilyCategory |
| Failure patterns | FP05 |
| Contributors | Gottfried Schmidtke with Claude |

**Intent:** Build a base cabinet family

## Learning curve

| Version | Instruction | Result | Problem | Found by |
|---|---|---|---|---|
| v01 | Family built from the Metric Casework template | Bounding box 900 mm larger than modelled | The template carries default geometry | bounding box measurement |
| v02 | Built from Metric Generic Model, then OwnerFamily.FamilyCategory set to Casework | Clean bounding box |  |  |

## Lesson
Some family templates carry hidden default geometry.

## Rule
Build from the Generic Model template and set the category; check the bounding box after building.

## Validation
- Bounding box against the modelled size
