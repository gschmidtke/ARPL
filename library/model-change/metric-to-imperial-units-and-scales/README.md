# ARPL-CHG-0003 rev 1: Switch a project from metric to imperial: units, dimension types, notes and view scales

_Generated from this pack's files by tools/build_catalogs.py. Edit manifest.json, intent.md, vNN/ or final/rule.json instead._

| | |
|---|---|
| Level | 2 |
| Work class | W5 |
| Status | candidate |
| Use when | a project set up in metric must show feet and inches; dimensions show two values (metric with imperial alternate) and should show one; view scales must change to the nearest imperial scale |
| Not for | converting geometry: the model stays as built; only display and annotation change |
| Workflows | model-change, documentation |
| Disciplines | generic, architecture |
| Project types | residential |
| Revit tested | 2024 |
| API | Units, FormatOptions, SpecTypeId.Length, UnitTypeId.FeetFractionalInches, DimensionType.SetUnitsFormatOptions, View.Scale, View.GetNonControlledTemplateParameterIds, Viewport.GetBoxOutline |
| Failure patterns | FP26, FP23, FP67 |
| Contributors | Gottfried Schmidtke with Claude |

**Intent:** Change a cm-based residential project to feet and inches to 1/16", show one value per dimension, convert every mm value in detail notes, and move all view scales to the nearest imperial architectural scale.

## Learning curve

| Version | Instruction | Result | Problem | Found by |
|---|---|---|---|---|
| v01 | Project length units to ft-in; leave dimension types | Detail dimensions still showed mm with ft-in alternates | dimension types with their own units do not follow the project | dimension inventory |
| v02 | Set those types to ft-in, Alternate Units 0, clear prefix/suffix | One value per dimension |  |  |
| v03 | Leave view scales | Imperial units on metric scales (1:5, 1:25) | owner wants imperial scales | owner |
| v04 | Scales 1:25 -> 1:24, 1:100 -> 1:96, 1:10 -> 1:12, 1:5 -> 1:4 (templates first, then views not controlled by a template) | All views changed; one perspective view refuses a scale |  |  |
| v05 | Sheets after the scale change | One viewport overlap (A4-04) and one viewport into the title strip; detail notes no longer stacked | geometry grows, annotation does not (FP67) | viewport overlap check, image export |

## Lesson
A unit switch is three separate changes: project units, every dimension type that does not use project settings, and text that states values. A scale switch moves geometry relative to paper-sized annotation, so sheets and note layouts must be re-checked.

## Rule
1. Project: Length FeetFractionalInches, accuracy 1/192 ft (1/16"), SuppressLeadingZeros true (shows 5 11/16" below one foot); Area SquareFeet, Volume CubicFeet.
2. Every linear/arc-length DimensionType whose FormatOptions are not UseDefault and are metric, or whose Alternate Units parameter is not 0: set ft-in, Alternate Units 0, clear the alternate prefix/suffix, rename types that name metric units.
3. Text: inventory notes with metric values (regex for mm, m2, 'NN x NN'); rewrite them with nominal lumber sizes plus actual sizes, inch fractions, and recomputed areas; never convert by blind string replacement.
4. Scales: nearest imperial architectural scale by ratio (1:2, 1:4, 1:8, 1:12, 1:16, 1:24, 1:32, 1:48, 1:96, 1:192). Change view templates first; skip views whose template controls the scale; perspective views take no scale.
5. After the scale change: check every sheet for viewport overlaps and viewports outside the drawing area (title strip), re-run annotation layout in changed detail views (ARPL-DOC-0004), and update scale mentions in notes.
6. Sync with a comment; export PDFs and look at them.

## Validation
- No dimension type with alternate units or metric format remains
- Notes scan finds no 'mm' in the changed views
- Viewport overlap and fit check on all sheets: 0 findings
- PDF review
