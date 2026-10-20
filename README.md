# ARPL: AI Revit Production Logic

An open, curated learning pool of **instruction packs** that teach AI agents to produce professional Revit models, documentation and data, together with the reasoning behind every instruction.

> Teach it professional practice downward until the required API action becomes obvious.

Each pack records a real production task: the intent, every iteration that was tried (what was asked, what came out, what was wrong and how it was found), and the final rule that works, with a way to prove it. Failures are kept on purpose: they are what makes the next agent faster.

## Find what you need

| You are... | Start here |
|---|---|
| A Revit user or developer looking for a technique | [catalogs/by-workflow.md](catalogs/by-workflow.md) |
| An engineer or designer in a discipline | [catalogs/by-discipline.md](catalogs/by-discipline.md) |
| Working on a building type | [catalogs/by-project-type.md](catalogs/by-project-type.md) and [project-workflows/](project-workflows/) |
| Debugging an agent that went wrong | [catalogs/by-failure-pattern.md](catalogs/by-failure-pattern.md) |
| Checking what runs in your Revit version | [catalogs/by-revit-version.md](catalogs/by-revit-version.md) |

Other entry points: [by work class](catalogs/by-work-class.md), [by phase](catalogs/by-phase.md), [by role](catalogs/by-role.md), [by level](catalogs/by-level.md).

## How it is organized

```
library/<workflow>/<pack>/     one canonical pack per technique (single source of truth)
  manifest.json                id, level, work class, facets, Revit versions tested, status, contributors
  intent.md                    what the professional wanted
  v01/ v02/ ...                each iteration: instruction.json + result.json
  final/rule.json              the lesson, the rule, the validation
domains/<discipline>/          discipline overlays (rules a pattern needs in that discipline)
project-workflows/             Level 4: packs composed into a full project deliverable
patterns/failure-patterns.json recurring ways agents fail (FP01...)
vocabularies/                  the controlled lists every facet must use
catalogs/                      generated indexes; never edited by hand
inbox/                         where contributions arrive
ledger/                        record of every contribution and decision
```

A pack lives in exactly one folder; the catalogs list it under every facet it carries. **Levels:** 1 primitive, 2 pattern, 3 discipline workflow, 4 project workflow. **Work classes** (W1–W8) describe what drives the result and decide what preview and proof a task needs; see [docs/model.md](docs/model.md).

**Status:** `candidate` (recorded once) → `reproduced` (worked again in another model or by another person) → `verified` (reviewed, with a validation that passes) → `deprecated`.

## Contribute

Send your protocols, prompts, failure stories and rules. You don't need to fit our structure: put what you have in `inbox/` (see [CONTRIBUTING.md](CONTRIBUTING.md)) and the curator reads, verifies, structures and files it. Every contribution is recorded in the [ledger](ledger/intake-ledger.json) and credited in [CONTRIBUTORS.md](CONTRIBUTORS.md).

## Curation

The repository is owned by Gottfried Schmidtke and curated by Claude (Anthropic) under his supervision. How contributions are reviewed: [CURATION.md](CURATION.md).

## License

Text and JSON content: [CC BY 4.0](LICENSE-DOCS.md). Code (tools, scripts): MIT, see [LICENSE](LICENSE). Revit is a trademark of Autodesk, Inc.; this project is not affiliated with Autodesk.
