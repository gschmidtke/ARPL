# Role: Project manager (in ARPL)

**Id:** ARPL-ROLE-0002 · **Version:** 0.1 (draft) · **Recorded:** 2026-10-28 (IN-0029)

The project manager owns the project's milestones and states which project status (for example Design Development or Construction Documents) applies to the whole project. ARPL records the role so that decisions which belong to it are routed there instead of being guessed by an agent.

## Decision chain

1. The **project manager** sets the project status and milestone.
2. The **BIM manager** receives it and instructs the BIM coordinator.
3. The **BIM coordinator** (ARPL-ROLE-0001) brings every model of the project to that status and phase, sheets included, and reports models that do not match in the weekly BIM report (rule checks `status` and `phases`, ARPL-RPT-0001).

## In scope

- Project status and milestones for the whole federation.
- Which deliverables are due at a milestone.

## Not in scope

- Model content, standards and naming: the BIM manager.
- Design decisions: the discipline leads.

A fuller definition follows with the BIM Standards repository that the owner is building in parallel.
