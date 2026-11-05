# ARPL-DOC-0004 rev 1: Detail annotation at the element: grouped notes, shoulder leaders, no crossings

_Generated from this pack's files by tools/build_catalogs.py. Edit manifest.json, intent.md, vNN/ or final/rule.json instead._

| | |
|---|---|
| Level | 2 |
| Work class | W6 |
| Status | candidate |
| Use when | annotating a drafting or detail view with text notes and leaders; a reviewer asks for notes at the element instead of a numbered legend; checking a detail for crossing leaders, leaders through dimensions or text, duplicate lines |
| Not for | tag families driven by parameters (use governed tags); deciding what a note says: content, product and engineering values stay with their owners |
| Workflows | documentation, views-graphics |
| Disciplines | architecture, generic |
| Project types | residential |
| Revit tested | 2024 |
| API | TextNote.Create, TextNote.AddLeader, TextNoteLeaderTypes, Leader.Anchor, Leader.Elbow, Leader.End, TextNote.RemoveLeaders, TextNote.LeaderLeftAttachment, Dimension.Segments, ElementTransformUtils.MoveElement |
| Failure patterns | FP26, FP62, FP64, FP65, FP22 |
| Contributors | Gottfried Schmidtke with Claude |

**Intent:** Annotate eave details (drafting views, 1:4 and 1:2) so every element note sits at its element, grouped outside the geometry, with leaders that start with a horizontal shoulder and never cross each other, text or dimensions.

## Learning curve

| Version | Instruction | Result | Problem | Found by |
|---|---|---|---|---|
| v01 | Numbered keynote legend beside the detail, number tags on the drawing | Reviewer and owner rejected it: readers cross-reference; numbers lost meaning after renumbering | legend instead of annotation at the element | owner review |
| v02 | Stack notes in a column using TextNote bounding-box height | Notes spread over several metres | a TextNote bounding box includes its leaders (FP62) | image export |
| v03 | Column positions passed to TextNote.Coord in mm | Notes metres outside the view | Revit internal units are feet (FP26) | image export of the sheet |
| v04 | Full permutation search for a non-crossing order inside one bridge call (10 notes) | Bridge timed out at 60 s; the call still completed | 10! orders; FP22 behaviour | bridge timeout, read-only state check |
| v05 | Branch-and-bound order per column, pruning on crossings | 0 leader crossings in 5 views, 8.5k nodes for 10 notes |  |  |
| v06 | Leader to a target lying behind the text column | No horizontal shoulder possible; Revit collapses the elbow | the column must sit on the side of its targets | read-only check (noShoulder) |
| v07 | Approved profile DA-04: leaders must not pass through dimensions; first test against dimension bounding boxes | Too coarse: many false hits | a dimension's box covers its witness lines and whole extent | comparison with the drawing |
| v08 | Test against dimension lines (Segments Origin/Value) and estimated text boxes; remove redundant dimensions; move remaining ones along their normal and move their witness ticks with them | 0 leaders through dimensions; witness lines kept at 4 mm paper; values unchanged |  |  |

## Lesson
A detail is read through its annotation. Revit's TextNote/Leader behaviour (bounding box includes leaders, elbow collapses when the target is behind the text, units in feet) makes a naive layout fail. Layout is an optimisation over note order with obstacles, not a placement of individual notes.

## Rule
1. One text note per element, with one leader to that element; no numbered legend for element information (owner rule R1, DA-01). General notes (units, status, dependencies, references) may stay grouped without leaders.
2. Group notes in columns outside the geometry, on the side of the elements they describe (R2, DA-02/DA-03). A column whose targets lie behind it gets no proper shoulder: move the column, never bend the shoulder.
3. Measure each note's height with its leader removed (FP62), then stack the column with a gap of about 2.8 mm paper (DA profile: >= 2 mm).
4. Choose the note order per column by branch-and-bound: cost = 1000 x leader crossings (with already placed columns too) + 1 x crossings with dimension lines, dimension text and general-note boxes + leader length; prune when the cost exceeds the best found. Place the smallest columns first.
5. Attach leaders at the top line; set Elbow to (Anchor.X +/- 6 mm x scale, Anchor.Y) so every leader starts horizontal (R4, DA-03), then the straight leg to Leader.End.
6. Dimensions (DA-08): remove a dimension whose value is already stated in a note or repeated in another detail; move a dimension still crossed by leaders along its normal to the nearest clear lane and move its witness ticks with it (FP65), so witness lines stay short.
7. Labels uppercase (DA-07); titles only below the view as the viewport title (DA-10); long calculations, precedents and review status go to a review record outside the drawing (DA-11).
8. After any scale change or text change, re-run the layout: annotation is paper-sized, geometry is not.
9. Verify with the read-only check and an image or PDF at print size (DA-12).

## Validation
- annotation_leader_check.cs: crossings 0, noShoulder 0, duplicate/buried lines 0
- Leaders through dimension lines or text: 0 (obstacle test in the layout script)
- Exported PDF reviewed at sheet size
