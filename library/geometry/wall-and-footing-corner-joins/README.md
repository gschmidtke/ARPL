# ARPL-GEO-0003: Footing corner notches

| | |
|---|---|
| Level | 2 |
| Work class | W4 |
| Workflows | geometry |
| Disciplines | architecture, structural |
| Project types | generic |
| Revit tested | 2024 |
| Status | candidate |

**Intent:** Continuous footings under API-created walls

## Learning curve

| Version | Instruction | Result | Problem |
|---|---|---|---|
| v01 | Wall foundations under walls meeting at centreline corners | 125 mm notches at every corner | API-created walls did not join at the corners |
| v02 | East-west walls full outer length, north-south between them; DisallowWallJoinAtEnd; footing type end extension 125 mm | Closed corners |  |

## Lesson
Wall joins assumed by the UI don't happen through the API.

## Rule
Model corner conditions explicitly; never rely on automatic joins.

## Validation
- Plan and 3D check of footing corners
