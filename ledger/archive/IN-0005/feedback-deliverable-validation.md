# IN-0005: feedback on deliverable intent and automated validation (anonymized)

The original file quoted a named third party's public comment verbatim. At the owner's request the person is not named here; the raw file was removed from the inbox on 2026-10-27. This record keeps only the professional content.

## The feedback, paraphrased

- ARPL is well structured but light on schema for **deliverable intent**: more granular definitions of what a deliverable is expected to be would focus validation.
- ARPL would benefit from **automated reporting channels** that can be iterated on: validation that works like unit tests, reporting whether actions matched expectations, to tune behaviour and catch drift as models change.

## The owner's assessment

Much of this already exists but is not tightly connected: work classes define a preview and a proof of done; Level 4 project workflows carry deliverable intent, sequence, user decisions and discipline authority; packs can carry read-only executable checks (`final/checks/`); usage reports record pack, revision, environment and pass/fail; reproduction moves a rule from candidate to reproduced to verified.

The next step is to connect these into a **deliverable acceptance contract**:

Purpose -> Expected state -> Constraints/invariants -> Tolerances -> Required checks -> Pass/fail criteria -> Execution report

so the same workflow can be replayed against other model, agent, bridge or Revit versions and drift becomes measurable: "unit testing for deliverables".

Follow-up: [docs/proposals/deliverable-acceptance-contract.md](../../../docs/proposals/deliverable-acceptance-contract.md).
