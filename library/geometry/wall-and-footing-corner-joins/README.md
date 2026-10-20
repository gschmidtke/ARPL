# ARPL-GEO-0003 rev 1: Footing corner notches

_Generated from this pack's files by tools/build_catalogs.py. Edit manifest.json, intent.md, vNN/ or final/rule.json instead._

| | |
|---|---|
| Level | 2 |
| Work class | W4 |
| Status | candidate |
| Use when | modelling foundations or footings at wall corners; relying on automatic joins at corners |
| Not for | - |
| Workflows | geometry |
| Disciplines | architecture, structural |
| Project types | generic |
| Revit tested | 2024 |
| API | WallFoundation, JoinGeometryUtils |
| Failure patterns | FP05 |
| Contributors | Gottfried Schmidtke with Claude |

**Intent:** Continuous footings under API-created walls

## Learning curve

| Version | Instruction | Result | Problem | Found by |
|---|---|---|---|---|
| v01 | Wall foundations under walls meeting at centreline corners | 125 mm notches at every corner | API-created walls did not join at the corners | plan review |
| v02 | East-west walls full outer length, north-south between them; DisallowWallJoinAtEnd; footing type end extension 125 mm | Closed corners |  |  |

## Lesson
Wall joins assumed by the UI don't happen through the API.

## Rule
Model corner conditions explicitly; never rely on automatic joins.

## Validation
- Plan and 3D check of footing corners
