# ARPL — AI Revit Production Logic

**An open learning pool of tested production instructions for AI agents working in Revit — including the failed versions, the lessons and the rules that came out of them.**

Connecting an AI to the Revit API is increasingly solved: there are bridges, MCP servers and add-ins. The harder question comes next:

> *What exactly should we tell the AI to do — and how do we know the result is correct?*

ARPL collects the answers as they are actually found: the instruction that was executed, what Revit produced, what was wrong with it, the next version, and the reusable rule at the end. A successful instruction tells you what worked. A failed one tells you **why the rule exists**.

---

## What is in this repository

| Folder | Content |
|---|---|
| [`categories/`](categories/) | One JSON file per **work class** (see below). Each holds the class definition, its decisive questions, the reference method, known failures, the verification profile, and the **learning chains** recorded so far. |
| [`patterns/`](patterns/) | Cross-cutting **failure patterns** ("geometry correct — semantics wrong", "API succeeded — model wrong", …) used as tags in the learning chains. |
| [`schema/`](schema/) | JSON Schema for a learning chain, so contributions stay comparable. |
| [`templates/`](templates/) | An empty learning chain to copy when you contribute. |
| [`docs/`](docs/) | Background: the work-class model and how ARPL uses it. |

## Work classes

Production work in Revit falls into distinct kinds. They differ less in size than in **what drives the result** — and each has its own decisive questions, methods, failure modes and proof of "done".

| ID | Work class | Driven by | Example |
|---|---|---|---|
| W1 | Component family authoring | A source document and an LOD | Coffee brewer at LOD 200 and LOD 350 |
| W2 | Adaptive / form-driven geometry | A rig of points and hosts | Adaptive façade lofted through stacked points |
| W3 | Layout-driven assembly production | A rule applied many times | LOD 400 wall panels: studs, plywood, siding, foam |
| W4 | Building model authoring | A program and system families | Small house: walls, roofs, rooms, doors, windows |
| W5 | Model change and propagation | One changed fundamental | Lowering a level and everything that depends on it |
| W6 | Documentation production | Views and sheets that must be right | Sections, dimensions, shop drawings, PDF sets |
| W7 | Information and data | Parameters, standards, quantities | Schedules, BOM, cost estimates |
| W8 | Analysis and review | Questions about an existing model | Code check, circulation, model audit |

A real job usually combines several classes — the class of each **step** decides its method.

## A learning chain, in short

```
INTENT → instruction v1 → Revit result → problem found → instruction v2 → … → lesson → reusable rule
```

Example (W3, wall panelization, recorded 2026-10-19):

| Version | Instruction | Result |
|---|---|---|
| v1 | Plywood sheets 4×9, joints on stud centres | A joint 28 mm from the window edge → unusable sliver |
| v2 | Move joints that fall within 150 mm *outside* an opening edge | Sliver remained — the joint was *inside* the opening edge |
| v3 | Move any joint within 150 mm of either side of an opening edge back one stud bay | Valid layout; same rule fed model, shop drawings and BOM |

**Lesson:** material constraints must be part of the layout rule, not checked afterwards — and a fix needs the same preview as the original rule.

## Principles behind the pool

- **Record what was executed**, not a polished prompt. Instructions may be JSON, prompts, C#/Python/Dynamo scripts or decisions taken in conversation — record them as they ran.
- **Keep the failures.** Every iteration has a result and a problem.
- **State the environment** (Revit version, tool or bridge, model fixture) so others can reproduce it.
- **Popularity is not authority.** Entries carry a status — `candidate`, `reproduced`, `verified` — and only reproduced evidence raises it.
- **No client data.** Strip project names, client information and licensed content (Autodesk or manufacturer families) before contributing.

## Contributing

Small contributions are welcome — one problem, one chain. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Licence

- Code and scripts: [MIT](LICENSE)
- Documents, lessons and learning chains (Markdown and JSON content): [CC BY 4.0](LICENSE-DOCS.md)

## Origin

ARPL is developed by Gottfried Schmidtke (Tiverit LLC) as a governance layer for AI agents producing Revit content. The first learning chains come from experiments with an AI agent working in Revit 2024 through a local Revit API bridge.
