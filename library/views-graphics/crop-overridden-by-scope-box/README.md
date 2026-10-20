# ARPL-VIEW-0001: Crops silently ignored

| | |
|---|---|
| Level | 1 |
| Work class | W6 |
| Workflows | views-graphics, documentation |
| Disciplines | generic |
| Project types | generic |
| Revit tested | 2024 |
| Status | candidate |

**Intent:** Crop elevations and sections tightly to the house

## Learning curve

| Version | Instruction | Result | Problem |
|---|---|---|---|
| v01 | Set View.CropBox | No error; crop unchanged | The template's scope box (VIEWER_VOLUME_OF_INTEREST_CROP) overrode the crop |
| v02 | Set the scope box parameter to InvalidElementId first, then set and read back the crop | Crops applied |  |

## Lesson
Some settings override others without any error.

## Rule
Read back every crop after setting it.

## Validation
- Crop read-back
- Image or PDF review
