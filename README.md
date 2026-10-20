# ARPL: AI Revit Production Logic

_Not related to other projects named ARPL (Advanced Redpill Loader, Adversarial Reciprocal Points Learning)._

An open, curated learning pool of **instruction packs** that teach AI agents to produce professional Revit models, documentation and data, together with the production rationale and evidence behind every instruction: why a method was chosen, what failed, how the failure was found and how the correction was verified.

> Teach it professional practice downward until the required API action becomes obvious.

Each pack records a real production task: the intent, every iteration that was tried (what was asked, what came out, what was wrong and how it was found), and the final rule that works, with a way to prove it. Failures are kept on purpose: they are what makes the next agent faster.

## What a pack looks like

An AI framed wall panels in Revit. Every stud was placed exactly where the layout said, and the check passed. Then a clash check found two end studs had moved 89 mm: Revit's automatic framing joins had changed them *after* placement. The API call "succeeded"; the model was wrong.

[ARPL-ASM-0004](library/assemblies-fabrication/framing-members-disallow-auto-joins/) records both attempts, how the problem was found, and the rule that fixed it: disallow joins on every framing member at creation, then verify positions after regeneration. The next AI that frames a wall reads that first and doesn't repeat it.

## Use it from your AI

If your AI works in Revit through a bridge or MCP server, tell it:

> Before this Revit task, check the ARPL knowledge pool for an established workflow: read https://raw.githubusercontent.com/gschmidtke/ARPL/main/AGENTS.md and follow it.

More options (system prompt, a lookup tool for bridges and MCP servers): [docs/agent-setup.md](docs/agent-setup.md).

The agent searches [index.json](index.json), applies the matching rules, tells you which packs it used, and afterwards says when it found something better or missing, so you can upload it and nobody has to learn it twice.

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

**Status:** `candidate` (recorded once) → `reproduced` (worked again in another model or by another person) → `verified` → `deprecated`. The definitions in [vocabularies.json](vocabularies/vocabularies.json) are authoritative. Each pack also has a `revision`, raised whenever its rule changes, so results can cite exactly which version was used.

Want to help? See [help wanted](catalogs/help-wanted.md): packs waiting for reproduction and disciplines not covered yet. Scope, limits and the deprecation policy: [docs/scope.md](docs/scope.md). How ARPL relates to other projects: [docs/related-work.md](docs/related-work.md). Where ARPL stands and where it should go: [docs/position-paper.md](docs/position-paper.md).

## Contribute

Everyone can read, download and fork ARPL. Contributions go through **one inbox**: [upload your protocol to `inbox/`](https://github.com/gschmidtke/ARPL/upload/main/inbox) (see [CONTRIBUTING.md](CONTRIBUTING.md)). You don't need to fit our structure; the curator reads, verifies, restructures and files it. Nothing outside the inbox is edited by contributors. Every contribution is recorded in the [ledger](ledger/intake-ledger.json) and credited in [CONTRIBUTORS.md](CONTRIBUTORS.md).

## Run it locally

```
pip install jsonschema
python tools/validate.py          # check every pack against schema and vocabularies
python tools/build_catalogs.py    # regenerate catalogs, pack READMEs and index.json
python tools/arpl_search.py "place studs in a wall panel" --index index.json
```

## Curation

The repository is owned by Gottfried Schmidtke. It is maintained by an AI-assisted curator under his supervision (currently Claude by Anthropic); ARPL itself is model-independent and works with any AI. How contributions are reviewed: [CURATION.md](CURATION.md).

## License

Text and JSON content: [CC BY 4.0](LICENSE-DOCS.md). Code (tools, scripts): MIT, see [LICENSE](LICENSE). Revit is a trademark of Autodesk, Inc.; this project is not affiliated with Autodesk.
