# Work classes

The learning pool is organised by **work class**: the kind of production work, defined by what drives the result. Two jobs can be equally deep or complex and still need completely different methods, previews and proofs of "done".

| ID | Work class | Driven by | "Simulation" before commit | Proof of done |
|---|---|---|---|---|
| W1 | Component family authoring | Source document + LOD | Flex test | Measured geometry, test placement |
| W2 | Adaptive / form-driven geometry | Rig of points and hosts | Motion / move test | Hosting behaves under movement |
| W3 | Layout-driven assembly production | Layout rule applied many times | 2D layout preview from the rule | Every piece matches the rule; no clashes |
| W4 | Building model authoring | Program + system families | Code and circulation checks | Warnings, rooms, swings, code |
| W5 | Model change and propagation | One changed fundamental | Re-preview affected layouts | Re-run checks of every affected class |
| W6 | Documentation production | Views and sheets | — | Exported sheets reviewed visually |
| W7 | Information and data | Parameters, standards, quantities | — | Schedules read back, totals cross-checked |
| W8 | Analysis and review | Questions about an existing model | — | Evidence for every finding |

Each category file in `categories/` holds, for its class:
- `decisive_questions`: what must be answered before building;
- `reference_method`: the method that has worked;
- `verification_profile`: the checks that prove the result;
- `learning_chains`: recorded chains of instruction → result → problem → next instruction → lesson → rule.

A real job combines classes. Example: LOD 400 wall panels were W1 (component families) → W3 (layout and assembly) → W5 (a door lowered to fit a header) → W6 (shop drawings) → W7 (BOM and cost). Record each lesson under the class of the step where it was learned and list the others in `related_classes`.

Failure patterns (`patterns/failure-patterns.json`) cut across classes and are used as tags.
