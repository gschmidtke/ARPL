# Scope, limits and policies

## What ARPL covers

Production knowledge for AI agents working in Autodesk Revit: how to turn a professional intent into correct model content, documentation and data, what goes wrong, how it is detected, and the rule that works.

## Non-goals

- **Not a replacement for firm standards.** A firm's own standards, content libraries and naming conventions take precedence over any pack. Packs describe methods; your standards decide names, parameters and graphics.
- **Not professional sign-off.** Packs never replace structural, code-compliance or other discipline review.
- **Not a code library.** Snippets illustrate methods. They are read and adapted, never run unreviewed.
- **No model files, client data or licensed content.**
- **Not tied to one AI or one bridge.** Any agent and any Revit connection can use it.

## Known limitations (October 2026)

- One founding contributor; every pack is `candidate`.
- Tested in Revit 2024 only.
- Strongest in residential wood-frame fabrication and family authoring; see [catalogs/help-wanted.md](../catalogs/help-wanted.md) for what is not covered.
- Validations are written as checks to perform, not yet as executable tests.

## Deprecation policy

A pack is deprecated when a Revit version changes the API behaviour it depends on, or a better method supersedes it.
- Status becomes `deprecated`; `superseded_by` names the replacement pack, if any.
- The pack stays in the library for history; the change is recorded in its changelog and the ledger.
- A rule that holds only up to a version keeps its pack: the version limit goes into `not_for` (e.g. "Revit 2027 and later").

## Roadmap

See also [related-work.md](related-work.md) for existing projects and partnership options.

1. Stress tests with radically different tasks (AV vs. electrical equipment, hospital MEP spaces, linked-model QA).
2. Independent reproductions; first `reproduced` and `verified` packs.
3. Executable validations: reference checks that return structured pass/fail plus evidence.
4. A controlled list for how failures are found (`found_by`), so agents can choose checks before acting.
