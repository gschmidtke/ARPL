# ARPL-CHG-0001 rev 1: Lowering a level: what doesn't follow

_Generated from this pack's files by tools/build_catalogs.py. Edit manifest.json, intent.md, vNN/ or final/rule.json instead._

| | |
|---|---|
| Level | 2 |
| Work class | W5 |
| Status | candidate |
| Use when | changing a level elevation or another fundamental datum; a change must propagate to walls, roofs, openings and layouts |
| Not for | - |
| Workflows | model-change, documentation |
| Disciplines | architecture |
| Project types | generic |
| Revit tested | 2024 |
| API | Level, Element.GetDependentElements |
| Failure patterns | FP10 |
| Contributors | Gottfried Schmidtke with Claude |

**Intent:** Lower L2 from 3.60 to 2.50 m and reprint the set

## Learning curve

| Version | Instruction | Result | Problem | Found by |
|---|---|---|---|---|
| v01 | Change the level elevation | Walls, roof and rooms followed | Profile gable walls and a custom Ridge level didn't; one window head ended above the new wall line | section and elevation review |
| v02 | Edit the gable sketches with SketchEditScope + CurveElement.SetGeometryCurve, commit with a failures preprocessor; also set WALL_USER_HEIGHT_PARAM (the bounding box follows it); move the Ridge level | Model consistent; sheets reprinted |  |  |

## Lesson
Constraint-driven elements follow a level; sketch-driven ones don't.

## Rule
Before changing a fundamental, list every dependent by type of constraint and plan the fix for each.

## Validation
- Sections and elevations exported and reviewed
- Window heads against the new wall top
