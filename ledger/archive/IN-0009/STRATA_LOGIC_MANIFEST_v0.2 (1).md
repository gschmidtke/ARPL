# STRATA LOGIC MANIFEST v0.2

**Project context:** 3XFF · USG · ARPL · dll2llm / API Navigator · Revit AI Bridge  
**Date:** 2026-10-25  
**Status:** Architectural manifest  
**Supersedes:** STRATA LOGIC MANIFEST v0.1

---

# 1. Purpose

This manifest defines the logical strata through which an AI-assisted production task is framed, resolved, implemented, executed, learned from, and improved over time.

The architecture is based on controlled descent:

```text
Reality Frame
    ↓
Problem / Purpose
    ↓
Production Representation
    ↓
Software Capability
    ↓
Runtime Execution
```

Each stratum has a distinct responsibility.

The system should always:

> **See the larger frame, operate at the lowest sufficient stratum, and preserve the upward link to why the task exists.**

The user owns the goal.

The system is not required to accept the user's proposed method, scale, representation, environment, or level of detail without examination.

---

# 2. System Overview

```text
[3XFF]
Reality frame / stratum adequacy
        ↓
[USG]
Problem / purpose / required depth
        ↓
[ARPL STRATUM]
Production representation / reuse / authority / governance
        ↓
[dll2llm + API Navigator]
Capability lookup / API provenance / path selection
        ↓
[Revit AI Bridge]
Runtime execution / dependency re-check / read-back
        ↓
[Terminal Alignment]
Local validation + retained purpose checksum
```

The normal flow is downward.

Upward movement is intentionally thin.

Operational learning moves sideways into the ARPL knowledge pool.

---

# 3. Two Meanings of ARPL

The name ARPL is used in two related but distinct ways.

## [ARPL STRATUM]

The current-run production reasoning layer.

It determines:

- what should exist,
- how it should be represented,
- what should be reused,
- what information it should carry,
- what authority applies,
- what production rules and known failure defences should constrain execution.

## [ARPL KNOWLEDGE POOL]

The cross-run institutional memory.

It contains:

- instruction packs,
- failed attempts,
- corrected methods,
- validation methods,
- recurring failure patterns,
- version evidence,
- production rationale,
- curated operational learning.

The knowledge pool can be consumed by **multiple strata**, not only the ARPL stratum.

```text
ARPL KNOWLEDGE POOL

frame lessons ───────────────→ 3XFF
purpose/workflow lessons ────→ USG
production packs ────────────→ ARPL
capability lessons ──────────→ Navigator
runtime failure patterns ────→ Bridge
```

The pool is a shared memory system.

The stratum is a current-run reasoning role.

---

# 4. STRATUM 1 — [3XFF]

## Purpose

3XFF establishes the reality frame in which the request should be understood.

It determines whether the requested operating stratum is appropriate relative to the larger purpose.

3XFF should be continuously frame-aware but only intervene when a material mismatch exists.

## Core Questions

- Where are we?
- Who or what is observing?
- What is being considered?
- What reality frame is active?
- At what stratum is the user asking to operate?
- What assumptions define the current frame?
- What larger purpose gives this frame meaning?
- Is the requested scope proportional to the intended outcome?
- Is the requested resolution necessary?
- Is the requested environment appropriate?
- What may the user be missing by framing the task here?
- What evidence could invalidate the frame?

## Frame Signature

```text
observer:
subject:
purpose:
boundary:
excluded:
assumptions:
stratum:
parent_frame:
uncertainty:
```

## Frame-Challenge Activation Triggers

3XFF should challenge the requested frame only when one or more material triggers are present.

```text
SCOPE MISMATCH
Requested effort is radically larger than the apparent purpose.

RESOLUTION MISMATCH
Very high detail is requested while purpose is unclear or low-resolution.

ENVIRONMENT MISMATCH
The requested host/tool is poorly matched to the goal.

CONSEQUENCE MISMATCH
High-cost, irreversible, or high-impact action with unclear purpose or authority.

ASSUMPTION GAP
The requested method depends on an unstated assumption that can materially alter the result.

FRAME CONFLICT
Available evidence contradicts the frame implied by the request.
```

## 3XFF Outcomes

```text
FRAME ACCEPTED
→ descend silently.

FRAME ADJUSTMENT SUGGESTED
→ expose the mismatch before descent.

FRAME INCOMPLETE
→ surface the missing higher-level question before descent.
```

## Example

```text
User:
"Create Manhattan in Revit at LOD 400."

Potential triggers:
scope mismatch
resolution mismatch
unknown purpose

Action:
Ask what this effort is intended to achieve
before accepting Revit + LOD 400 as the operating stratum.
```

## Ownership

3XFF owns:

- observer position,
- frame selection,
- frame adequacy,
- stratum selection,
- proportionality challenge,
- frame assumptions.

## Downward Handoff Condition

Descend when the frame is sufficiently clear and the selected operating stratum is reasonable.

---

# 5. STRATUM 2 — [USG]

## Purpose

USG resolves what problem is actually being solved and how far that problem must be developed.

USG should enter its chain at the **lowest sufficient stage**, rather than restarting from purpose every time.

## Resolution Chain

```text
purpose
→ actors
→ functions
→ capacity
→ relationships
→ physics
→ context
→ regulation
→ performance
→ form
→ systems
→ elements
→ validation
```

## Core Questions

- What problem are we solving?
- Why does it matter?
- Who are the actors?
- What functions are required?
- What capacity is required?
- What relationships matter?
- What physical constraints apply?
- What context matters?
- What regulations apply?
- What performance is required?
- Does form need to be resolved?
- Which stages are already settled?
- Which stages can be skipped safely?

## Output

```text
Resolved problem definition
Required depth of development
Purpose
Constraints
Required form/system direction
Acceptance invariants
```

## Ownership

USG owns:

- problem definition,
- purpose,
- functional need,
- required depth,
- transition from purpose toward form and systems.

## Downward Handoff Condition

Descend when the problem is sufficiently resolved for production representation.

---

# 6. STRATUM 3 — [ARPL STRATUM]

## Purpose

ARPL determines what should exist in the production environment and under what governance.

It applies accumulated production knowledge from the ARPL knowledge pool.

## Core Questions

- What should exist in the production environment?
- Does it already exist?
- Can governed content be reused?
- What is the correct semantic identity?
- What information must it carry?
- What authority governs the decision?
- What project or firm standards apply?
- What representation is correct?
- What prior ARPL packs or failure patterns apply?
- What known failures should be pre-armed against?
- What can be deterministic?
- What still requires AI reasoning?
- What must be validated?

## Output

```text
Production-ready intent
Representation strategy
Reuse decision
Required information
Authority state
Known failure defences
Execution requirements
Validation requirements
```

## Authority States

```text
AUTO
CONFIRM
USER_APPROVAL
DISCIPLINE_APPROVAL
PROHIBITED
```

Knowing how to perform an action does not imply authority to perform it.

## Ownership

ARPL owns:

- production representation,
- reuse hierarchy,
- semantic correctness,
- information correctness,
- authority,
- project/firm governance,
- production validation,
- current-run use of accumulated production knowledge.

## Downward Handoff Condition

Descend when ARPL has resolved what should be done operationally and under what authority.

---

# 7. STRATUM 4 — [dll2llm + API NAVIGATOR]

## Purpose

This stratum narrows the host application's capability field.

```text
dll2llm
= generate the API map

API Navigator
= navigate the API map
```

The Navigator should not decide what production representation is correct.

It finds the smallest relevant host capability that can implement the ARPL decision.

## Core Questions

- Which host application?
- Which version?
- What operation does ARPL require?
- Which API domain contains that capability?
- Which classes and types are relevant?
- Which methods or constructors apply?
- What inputs are required?
- What objects are returned?
- What inheritance relationships matter?
- What dependencies matter?
- What known constraints apply?
- What is the provenance of this capability knowledge?
- What is the smallest verified API path?

## Capability Provenance

```text
EXTRACTED
DOCUMENTED
CURATED
INFERRED
HISTORICALLY_OBSERVED
OBSERVED_CURRENT
```

## Output

```text
Narrowed API search field
Selected capability
Relevant classes/methods
Required parameters
Dependencies
Capability provenance
Candidate execution path
```

## Ownership

The Navigator owns:

- capability lookup,
- API vocabulary,
- API-version awareness,
- capability provenance,
- implementation-path selection.

It does not own production meaning or execution authority.

---

# 8. PROVENANCE × CONSEQUENCE × AUTHORITY

Execution permission depends on three independent dimensions.

```text
CAPABILITY PROVENANCE
How well do we know the software capability?

CONSEQUENCE
What can the operation do?

AUTHORITY
Who is permitted to authorize it?
```

The decision sequence is:

```text
Navigator provides:
Capability Provenance

ARPL provides:
Consequence Class
Authority State

        ↓

Execution Policy

        ↓

Bridge enforces:
Allowed Execution Mode
```

## Consequence Classes

```text
READ
No model mutation.

REVERSIBLE_WRITE
Model mutation that can be meaningfully validated and reversed.

DESTRUCTIVE_OR_HIGH_IMPACT_WRITE
Deletion, major propagation, high-impact change, or operation with difficult recovery.
```

## Binding Examples

| Provenance | Consequence | Authority | Result |
|---|---|---|---|
| OBSERVED_CURRENT | READ | AUTO | execute |
| DOCUMENTED | REVERSIBLE_WRITE | AUTO | execute + read-back |
| INFERRED | REVERSIBLE_WRITE | CONFIRM | test/confirm before commit |
| CURATED | DESTRUCTIVE_OR_HIGH_IMPACT_WRITE | USER_APPROVAL | approval + dependency recheck + commit |
| OBSERVED_CURRENT | DESTRUCTIVE_OR_HIGH_IMPACT_WRITE | PROHIBITED | do not execute |

## Governing Rule

> **Capability confidence never grants authority. Authority can restrict capability, but capability confidence cannot override authority.**

---

# 9. STRATUM 5 — [REVIT AI BRIDGE]

## Purpose

The Bridge executes an already-resolved operation safely inside Revit.

Its job is runtime execution, not problem definition.

## Core Questions

- Is the operation permitted?
- Is the correct document active?
- Is the operation read-only or write?
- Is a Transaction required?
- Is a known deterministic handler available?
- Is generated code required?
- Which execution mode is allowed?
- Are the required objects still valid?
- Are dependency keys still valid?
- Can the operation be executed idempotently?
- What failure handling is required?
- What happened after execution?
- Does read-back confirm the intended result?

## Execution Modes

```text
READ-ONLY PROBE
Inspect state without mutation.

PREVIEW
Reason about the intended action without model mutation.

ROLLBACK TEST
Execute in a transaction scope and roll back,
where meaningful rollback is supported.

SANDBOX TEST
Execute against a disposable or copy environment.

COMMIT
Execute against the authoritative model.
```

## Commit-Boundary Rule

Immediately before COMMIT:

> Re-verify the critical dependency keys on which the operational conclusion depends.

Examples:

```text
document_guid unchanged
required element still exists
FamilySymbol still exists
host element still exists
category unchanged
authority still valid
```

If a dependency changed:

```text
invalidate only the dependent operational conclusions
```

Do not automatically return to higher strata.

## Output

```text
Execution result
Read-back evidence
Validation evidence
Warnings
Errors
Operational observations
```

---

# 10. STRATUM OWNERSHIP

Each question belongs to one stratum.

```text
"Are we interpreting the problem at the right reality frame?"
→ 3XFF

"What problem are we actually solving?"
→ USG

"Should this be a FamilyInstance or DirectShape?"
→ ARPL

"Which NewFamilyInstance overload applies?"
→ API Navigator

"Can this execute safely in the active Document?"
→ Revit AI Bridge
```

Lower strata should not silently answer questions owned by higher strata.

Example:

```text
"DirectShape is easy to create."
```

does not imply:

```text
"DirectShape is the correct production representation."
```

---

# 11. NORMAL FLOW — CONTROLLED DESCENT

```text
[3XFF]
Frame the task
    ↓
[USG]
Resolve the problem
    ↓
[ARPL]
Resolve production representation
    ↓
[Navigator]
Resolve software capability
    ↓
[Bridge]
Execute
```

Each stratum searches only until it can hand the next stratum a sufficiently constrained task.

---

# 12. BOUNDED PROBES

A higher stratum may need a fact from a lower stratum before completing its own decision.

This is a **bounded probe**, not committed descent.

Example:

```text
ARPL:
Reuse before creation.

Question:
Does the required family already exist?
```

Flow:

```text
ARPL
  ↓ bounded probe
Navigator
  ↓
Bridge READ
  ↓
fact returned
  ↑
ARPL continues deciding
```

## Probe Rules

- read-only by default,
- bounded to an explicit fact,
- non-committing,
- cached while dependencies remain valid,
- aggregated where possible,
- limited in nesting depth,
- failed probe returns `UNKNOWN`, not `FALSE`,
- uncontrolled probe loops must not monopolize the Revit main thread.

---

# 13. UPSTREAM LOOP — PREMISE CONTRADICTION

Failures do not automatically move upward.

Most lower-stratum failures are local.

The system moves upward only when evidence contradicts a premise that a higher stratum relied on when it decided to descend.

## Governing Rule

> **Falsification propagates upward only through premises a higher stratum actually relied on.**

## Examples

### Local Runtime Failure

```text
Bridge:
API call throws.

Meaning:
Execution path failed.

Action:
Bridge / Navigator solve locally.

USG and 3XFF remain untouched.
```

### ARPL-Level Contradiction

```text
ARPL premise:
This representation can preserve required semantic information.

Evidence:
It cannot.

Action:
ARPL re-plans representation.
```

### USG-Level Contradiction

```text
USG premise:
This production object satisfies the required function.

Evidence:
It does not.

Action:
Return to USG.
```

### 3XFF-Level Contradiction

```text
3XFF premise:
This is fundamentally a BIM-production problem.

Evidence:
The actual goal is conceptual urban analysis.

Action:
Return to 3XFF.
```

## Descent Premises

Every committed descent should carry the minimum premises required to justify that descent.

```json
{
  "descent": "USG_to_ARPL",
  "depends_on": [
    "purpose_resolved",
    "production_representation_required",
    "frame_accepted"
  ]
}
```

Upper strata should premise lightly.

That protects them from lower-level operational noise.

---

# 14. INCREMENTAL RE-ENTRY

An upstream correction does not restart the entire descent.

It invalidates only conclusions that depended on the corrected premise.

The system then resumes from the highest invalidated stratum.

## Rule

> **Correct upward narrowly; re-descend incrementally.**

Example:

```text
USG purpose corrected
        ↓
ARPL representation depended on old purpose
→ invalidate

Navigator API path depended on ARPL representation
→ invalidate

Bridge operation depended on Navigator path
→ invalidate

3XFF remains valid
```

Re-entry:

```text
resume at ARPL
```

not:

```text
restart at 3XFF
```

This makes the architecture behave more like incremental compilation than repeated full reasoning.

---

# 15. SIDEWAYS LOOP — OPERATIONAL LEARNING

Operational failures, frame errors, better methods, and new validations do not need to travel upward through the logical strata in order to remain useful.

They can move sideways into the ARPL knowledge pool.

```text
New learning
    ↓
HARVEST CANDIDATE
    ↓
Sanitize / remove client, project, private, or secret data
    ↓
USER REVIEW + CONSENT
    ↓
ARPL Inbox
    ↓
Curator
    ↓
Machine-readable rule / pattern / pack
    ↓
Canonical ARPL Knowledge Pool
    ↓
Future runs
```

## Core Rule

> **Routing answers: "Who fixes this now?"  
> Harvest answers: "Who should never have to learn this again?"**

## Any Stratum Can Generate a Harvest Candidate

```text
3XFF frame error
USG purpose-resolution error
ARPL production failure
Navigator capability mistake
Bridge runtime failure
```

can all become harvest candidates.

Where a lesson is learned determines its owner.

Where it is stored does not imply routing through the hierarchy.

## Consent Rule

HARVEST does **not** mean publish.

It means:

```text
recognize reusable learning
→ package it
→ sanitize it
→ present it to the user
→ submit only with explicit consent
```

---

# 16. HARVEST

HARVEST is the seventh system mechanic.

```text
1. FRAME SIGNATURE
2. STRATUM OWNERSHIP
3. COMMITTED DESCENT
4. BOUNDED PROBE
5. DEPENDENCY / INVALIDATION
6. PREMISE-GATED UPSTREAM ROUTING
7. HARVEST
```

## Harvest Triggers

Harvest when the run produces:

- a previously unknown failure,
- a contradicted premise that taught something reusable,
- a correction to an existing rule,
- a better or cheaper production method,
- evidence that an existing pack worked in a new environment,
- evidence that an existing pack failed,
- a useful new validation method,
- a recurring agent or bridge failure pattern,
- a new frame-level lesson,
- a new bounded-probe or execution defence.

## Harvest Lifecycle

```text
RAW EXPERIENCE
→ HARVEST CANDIDATE
→ USER REVIEW / SANITIZATION / CONSENT
→ ARPL INBOX
→ CURATION
→ canonical ARPL evidence lifecycle
```

The manifest does not replace ARPL's own canonical evidence/status lifecycle.

---

# 17. DEPENDENCY AND INVALIDATION

Conclusions should declare what they depend on.

Example:

```json
{
  "conclusion": "reuse FamilySymbol 483721",
  "depends_on": [
    "document_guid",
    "family_symbol_483721_exists",
    "family_symbol_483721_category",
    "project_standard_revision"
  ]
}
```

If an unrelated wall moves:

```text
dependencies unchanged
→ conclusion remains valid
```

If the family is deleted:

```text
dependency changed
→ only dependent conclusions invalidate
```

The system should invalidate narrowly.

It should never recompute the entire hierarchy unless a higher premise was actually contradicted.

---

# 18. TERMINAL ALIGNMENT / PURPOSE CHECKSUM

The system should not re-run 3XFF or USG after every successful operation.

However, purely local success is not enough.

The retained parent purpose should provide a cheap final alignment condition.

## Flow

```text
RESULT
   ↓
LOCAL VALIDATION
Did the Bridge produce what ARPL asked for?
   ↓
PURPOSE CHECKSUM
Does the result still satisfy the retained USG
acceptance invariant / parent-purpose condition?
```

This is not a full upstream reasoning loop.

It is a stored assertion check.

## Example

```text
USG purpose:
Provide an accessible route.

ARPL task:
Move door 200 mm.

Bridge result:
Door moved 200 mm.

Local validation:
PASS

Purpose checksum:
Required clear width still maintained?

PASS
→ finish.
```

If the checksum fails:

```text
a retained higher-level premise has been contradicted
→ use premise-gated upstream routing
```

## Rule

> **Keep upward reasoning thin, but never lose the reason the local action exists.**

---

# 19. APPLICATION PROFILES

The core manifest should remain domain-neutral.

Domain-specific engineering logic belongs in application profiles that cite this manifest.

Examples:

```text
STRATA LOGIC MANIFEST
        ↓
Electrical Application Profile
Structural Application Profile
Architectural Fabrication Application Profile
MEP Coordination Application Profile
Documentation Application Profile
Model QA Application Profile
```

Each profile should declare:

```text
based_on_manifest:
STRATA_LOGIC_MANIFEST v0.2
```

Application profiles may define:

- domain-specific USG constraints,
- ARPL production representations,
- deterministic kernels,
- domain authorities,
- validation contracts,
- Bridge verification requirements.

They should not redefine the core strata.

---

# 20. HAND-OFF CONTRACT DECLARATION

Every stratum boundary should carry a defined contract.

The detailed JSON schemas are a separate implementation artifact, but every contract should contain the same core fields.

## Common Contract Fields

```text
required_input
optional_context
resolved_assumptions
parent_frame_reference
descent_premises
dependency_keys
confidence / provenance
authority
unresolved_questions
acceptance_invariants
output_schema
```

## Boundaries

```text
3XFF → USG
USG → ARPL
ARPL → Navigator
Navigator → Bridge
Bridge → Terminal Alignment
```

## Probe Channel

A bounded probe should use a separate minimal contract:

```text
probe_id
requesting_stratum
fact_requested
read_only
dependency_scope
timeout_behavior
result
certainty
```

A probe failure returns:

```text
UNKNOWN
```

not:

```text
FALSE
```

---

# 21. THE TWO LOOPS

The architecture contains two fundamentally different loops.

## Loop A — Upstream Logical Correction

Occurs inside the current run.

Triggered only by:

```text
contradicted descent premise
```

Direction:

```text
lower stratum
↑
owner of contradicted premise
```

Purpose:

```text
correct the current task
```

Re-entry after correction is incremental.

---

## Loop B — Sideways Learning

Occurs across runs.

Triggered by:

```text
new reusable learning
```

Direction:

```text
any stratum
→ HARVEST CANDIDATE
→ user review / consent
→ ARPL knowledge pool
→ future downstream work
```

Purpose:

```text
reduce future search, failure, and repeated learning
```

---

# 22. COMPLETE SYSTEM VIEW

```text
                         CURRENT RUN

                    [3XFF]
           Reality frame / stratum
                        ↓
                     [USG]
           Problem / purpose resolution
                        ↓
                [ARPL STRATUM]
       Production representation / governance
                        ↓
             [dll2llm + Navigator]
              Capability resolution
                        ↓
                [Revit AI Bridge]
                Runtime execution
                        ↓
              [Terminal Alignment]
       Local validation + purpose checksum
                        ↓
                     RESULT

                        ↑
             only when a premise
              is contradicted


                   SIDEWAYS LEARNING

      Any reusable lesson from any stratum
                        ↓
               HARVEST CANDIDATE
                        ↓
        Sanitize + USER REVIEW / CONSENT
                        ↓
                    ARPL Inbox
                        ↓
                     Curator
                        ↓
          Canonical ARPL Knowledge Pool
                        ↓
        Pre-arms applicable future strata
```

---

# 23. Compact Role Summary

```text
[3XFF]
Where are we?
Does this frame and stratum make sense?
When should the frame be challenged?

[USG]
What problem are we solving?
Why?
How far must it be resolved?

[ARPL STRATUM]
What should exist operationally?
What should be reused?
What authority applies?
What known production failures should be avoided?

[ARPL KNOWLEDGE POOL]
What has previous work already taught us?
Which strata can use that learning?

[dll2llm + API Navigator]
Where exactly is the required software capability?
How reliable is our knowledge of it?

[Revit AI Bridge]
Can this operation execute safely now?
Re-check dependencies, execute, and read back.

[Terminal Alignment]
Did the local result still satisfy the retained parent purpose?

[HARVEST]
What did this run teach that future runs should know?
```

---

# 24. Core Principles

> **Context can remain available without remaining active.**

> **Operate at the lowest sufficient stratum.**

> **Respect the user's goal, but do not blindly accept the user's proposed method or stratum.**

> **Challenge the frame only when the mismatch is material.**

> **Failures stay local unless they contradict a premise owned by a higher stratum.**

> **Correct upward narrowly and re-descend incrementally.**

> **Operational learning travels sideways into the ARPL knowledge pool rather than upward through settled strata.**

> **Any stratum can generate reusable learning.**

> **HARVEST requires sanitization, user review, and explicit consent before submission.**

> **Capability confidence never grants authority.**

> **Re-check critical dependencies at COMMIT.**

> **Keep final purpose verification cheap but explicit.**

> **The knowledge pool may pre-arm multiple strata.**

> **A local failure should improve future downstream navigation even when it never changes the larger frame.**

> **The system becomes more efficient over time because it remembers not only what worked, but why previous attempts failed.**

---

# 25. Next Implementation Artifact

The architecture is now sufficiently stable to move from architectural discovery to protocol engineering.

The next artifact should define the actual machine-readable hand-off schemas for:

```text
3XFF → USG
USG → ARPL
ARPL → Navigator
Navigator → Bridge
Bridge → Terminal Alignment
```

Those contracts should operationalize:

- frame signatures,
- descent premises,
- dependency keys,
- authority states,
- provenance,
- consequence classes,
- execution modes,
- bounded probes,
- acceptance invariants,
- terminal purpose checks,
- and harvest candidates.
