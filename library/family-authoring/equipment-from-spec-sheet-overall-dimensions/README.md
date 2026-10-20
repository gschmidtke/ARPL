# ARPL-FAM-0001: Coffee brewer from a spec sheet: overall height short

| | |
|---|---|
| Level | 2 |
| Work class | W1 |
| Workflows | family-authoring, model-context |
| Disciplines | generic |
| Project types | generic |
| Revit tested | 2024 |
| Status | candidate |

**Intent:** Model a commercial coffee brewer at LOD 200 from the manufacturer's PDF spec sheet

## Learning curve

| Version | Instruction | Result | Problem |
|---|---|---|---|
| v01 | Body modelled from the body dimension on the sheet (430 mm high) | Family built and placed | Overall height on the sheet is 483 mm; the raised warmer housings were missed |

## Lesson
Overall dimensions on a spec sheet can include parts that the main views don't label separately.

## Rule
Before modelling, reconcile every overall dimension on the source against the sum of the parts in each view.

## Validation
- Bounding box height against the sheet's overall height
