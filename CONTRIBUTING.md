# Contributing to ARPL

Thank you for adding to the pool. You don't need to build an agent — one problem, honestly recorded, is a contribution.

## What to contribute
- A **learning chain**: the intent, each instruction version as executed, what Revit produced, the problem, and the lesson or rule at the end.
- A **failure pattern** you've seen more than once.
- A **reproduction** of an existing chain in another Revit version or with another tool — this is how entries move from `candidate` to `reproduced`.

## How
1. Copy [`templates/learning-chain.template.json`](templates/learning-chain.template.json).
2. Pick the work class (`W1`–`W8`) — see the README. If a chain spans several classes, use the class of the step where the lesson was learned and list the others in `related_classes`.
3. Fill in the chain. Keep the failed iterations.
4. Tag failure patterns from [`patterns/failure-patterns.json`](patterns/failure-patterns.json) (propose a new one if none fits).
5. Add the chain to the `learning_chains` array of the matching file in [`categories/`](categories/) and open a pull request.

Validate against [`schema/learning-chain.schema.json`](schema/learning-chain.schema.json) if you can.

## Rules
- **Record what actually ran** — JSON, prompts, scripts or conversation decisions. Short excerpts are fine; link full scripts if they're long.
- **State the environment**: Revit version, bridge or tool, compiler or runtime, model fixture.
- **No client or proprietary data**: no project names, client information, model files (`.rvt`, `.rfa`) or licensed content.
- **Status**: new entries start as `candidate`. Maintainers raise the status when an entry has been reproduced; frequency alone never raises it.

## Licence of contributions
By contributing you agree that documents and learning chains are published under CC BY 4.0 and code under MIT.
