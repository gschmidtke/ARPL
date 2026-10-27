# Proposal: deliverable acceptance contract

**Status: proposal, not adopted.** Nothing in the schema, the vocabularies or the packs changes until the owner decides. Sources: community feedback on deliverable validation (IN-0005, anonymized) and a note on the DesConOps white paper (IN-0007), both in `ledger/archive/`.

## The problem

A Revit action is not finished when the API call returns. It is finished when the intended model state is verified against a requirement, with evidence. ARPL already has the pieces, but they are not connected:

| Piece | Where it lives today |
|---|---|
| Preview before commit, proof of done | Work classes ([docs/work-classes.md](../work-classes.md)) |
| Deliverable intent, sequence, user decisions, discipline authority | Level 4 project workflows (`project-workflows/`) |
| Rule validation | `final/rule.json` → `validation` |
| Executable, read-only checks | `final/checks/`, `validation_checks` |
| Run evidence: pack + revision, environment, pass/fail, checks run | Usage reports (`ledger/usage/`) |
| Evidence level | `candidate` → `reproduced` → `verified` |

## The proposal

Connect them into one contract per deliverable (most naturally per Level 4 workflow step):

1. **Purpose**: what the deliverable is for.
2. **Expected state**: the Revit model state that counts as done.
3. **Constraints and invariants**: what must stay true (counts, identities, relationships, untouched elements).
4. **Tolerances**: numeric limits per invariant.
5. **Required checks**: which `final/checks/` scripts or read-backs prove each invariant.
6. **Pass/fail criteria**: `PASS`, `REVIEW` or `FAIL`, and who decides `REVIEW`.
7. **Execution report**: the usage report, extended with the result per invariant.

Replaying the same contract against another model, agent, bridge or Revit version would make drift measurable instead of anecdotal ("unit testing for deliverables").

## Relationship to USG

USG ([gschmidtke/USG](https://github.com/gschmidtke/USG)) already hands `acceptance_invariants` to ARPL in its output contract (`docs/handoff-to-arpl.md`): what must be true for the result to satisfy the purpose. The split would be:

- **USG** owns purpose-level invariants (what must exist, what it separates, required performance, approximate vs exact values).
- **ARPL** owns the representation-level contract above: expected Revit state, tolerances, checks and the execution report. It must not silently drop or weaken a USG invariant.

## Decisions for the owner

- Adopt the contract, and if so, as a new optional manifest field or as a section of Level 4 workflow steps?
- Extend the usage-report template with per-invariant results?
- Name the field to match USG (`acceptance_invariants`) so the handoff maps one-to-one?
