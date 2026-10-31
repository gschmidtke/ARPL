# AI Cross-Repository Routing Safeguard

This rule applies when an AI enters the public AEC knowledge system through **USG**, **TIVERIT BIM Standards**, or **ARPL**.

The repository supplied by the user is an **entry point, not the authority for every question**.

## Required routing behavior

Before giving a substantive answer:

1. **Classify the user's actual question.**
   - purpose, required outcome, success criteria -> USG
   - normative requirements, permissions, roles, authority, BEP, CDE, naming, information requirements, acceptance, compliance evidence -> TIVERIT BIM Standards
   - professional Revit production technique, known failure modes, operational verification precedent -> ARPL
   - software/API capability -> authoritative API documentation or capability lookup
   - execution -> the user's authorized bridge, add-in, or runtime
   - supported governed automation, repair, or verification -> ZEN where applicable

2. **Identify the owning layer.**
   Do not answer from the entry repository merely because that is where the user started.

3. **Read the owning layer's `AGENTS.md` before answering substantively.**
   Silent routing is not complete until the target layer's operating contract has been loaded. Do not answer from memory of what that layer probably means.

4. **Answer the user directly.**
   Do not force the user to re-point the AI at another repository when the owning public source is accessible.

5. **Carry unresolved upstream items forward as explicit gaps when safe.**
   An unresolved upstream stage does not automatically block a requested downstream deliverable. If the downstream process can continue without inventing the missing fact or violating authority, record the unresolved upstream item in that process's gap queue and continue. Example: unresolved project purpose may remain an explicit BEP objective gap while BEP assembly proceeds.

6. **Preserve authority boundaries.**
   Never invent project facts, convert proposals into confirmed requirements, let API capability create permission, or let prior production success create normative authority.

7. **Surface routing only when it matters.**
   Routing should normally remain invisible to the user. Surface provenance, governing objects, repository/layer boundaries, or conflicts when:
   - the user asks where the answer came from;
   - authority is challenged;
   - sources or layers conflict;
   - uncertainty materially affects the answer; or
   - a user, project authority, curator, or professional decision is required.

## Cross-layer precedence

- Purpose does not automatically override governance.
- Governance constrains operational precedent.
- Operational precedent does not create normative authority.
- Technical capability does not establish permission or professional acceptability.
- Successful execution does not establish compliance by itself.

## Examples

| Entry point | User asks | Silent route |
|---|---|---|
| ARPL | "What sheet standards should we establish?" | TIVERIT BIM Standards |
| USG | "Who is allowed to approve the model?" | TIVERIT BIM Standards |
| TIVERIT BIM Standards | "How do I actually set up shared coordinates in Revit?" | ARPL, then API capability evidence as needed |
| Any of the three | "What are we trying to achieve with this project?" | USG |

The user should experience the three public repositories as **one coherent knowledge surface** while the correct authority boundaries remain intact in the background.
