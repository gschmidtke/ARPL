# ARPL-VIEW-0001 rev 1: Crops silently ignored

_Generated from this pack's files by tools/build_catalogs.py. Edit manifest.json, intent.md, vNN/ or final/rule.json instead._

| | |
|---|---|
| Level | 1 |
| Work class | W6 |
| Status | candidate |
| Use when | setting crop boxes or scope boxes on views; exported views show more than intended |
| Not for | - |
| Workflows | views-graphics, documentation |
| Disciplines | generic |
| Project types | generic |
| Revit tested | 2024 |
| API | View.CropBox, ViewCropRegionShapeManager |
| Failure patterns | FP08, FP05 |
| Contributors | Gottfried Schmidtke with Claude |

**Intent:** Crop elevations and sections tightly to the house

## Learning curve

| Version | Instruction | Result | Problem | Found by |
|---|---|---|---|---|
| v01 | Set View.CropBox | No error; crop unchanged | The template's scope box (VIEWER_VOLUME_OF_INTEREST_CROP) overrode the crop | image export review |
| v02 | Set the scope box parameter to InvalidElementId first, then set and read back the crop | Crops applied |  |  |

## Lesson
Some settings override others without any error.

## Rule
Read back every crop after setting it.

## Validation
- Crop read-back
- Image or PDF review
