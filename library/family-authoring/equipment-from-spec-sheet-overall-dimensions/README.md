# ARPL-FAM-0001 rev 1: Coffee brewer from a spec sheet: overall height short

_Generated from this pack's files by tools/build_catalogs.py. Edit manifest.json, intent.md, vNN/ or final/rule.json instead._

| | |
|---|---|
| Level | 2 |
| Work class | W1 |
| Status | candidate |
| Use when | building an equipment family from a manufacturer spec sheet or drawing; overall dimensions don't match after modelling |
| Not for | - |
| Workflows | family-authoring, model-context |
| Disciplines | generic |
| Project types | generic |
| Revit tested | 2024 |
| API | Family, Extrusion |
| Failure patterns | FP09 |
| Contributors | Gottfried Schmidtke with Claude |

**Intent:** Model a commercial coffee brewer at LOD 200 from the manufacturer's PDF spec sheet

**LOD:** LOD 200

## Learning curve

| Version | Instruction | Result | Problem | Found by |
|---|---|---|---|---|
| v01 | Body modelled from the body dimension on the sheet (430 mm high) | Family built and placed | Overall height on the sheet is 483 mm; the raised warmer housings were missed | user / later comparison with the sheet |

## Lesson
Overall dimensions on a spec sheet can include parts that the main views don't label separately.

## Rule
Before modelling, reconcile every overall dimension on the source against the sum of the parts in each view.

## Validation
- Bounding box height against the sheet's overall height
