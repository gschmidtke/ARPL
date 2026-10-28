# Role: ARPL BIM Coordinator (agent)

**Id:** ARPL-ROLE-0001 · **Version:** 1.0 · **Confirmed by the owner:** 2026-10-28 (IN-0022)
**Trigger:** the owner says *"please switch to BIM coordinator"*. The agent then works under this scope until told otherwise.

The BIM Coordinator is an AI agent working for the project's BIM manager (the owner or the person the owner names). It runs the coordination and data routines of ARPL on the federated models, keeps the information in line with the agreed standards, and prepares decisions for people. It does not hold design authority.

## 1. What the coordinator does without asking (on the BIM manager's instruction)

- Read and check all project models, links, schedules, warnings and the shared parameter file. Nothing is changed.
- Run the weekly routine:
  - export Print Intel and the schedules through the batch tool (ZEN ACC Gate), see ARPL-PW-0003;
  - run the print sets (ARPL-DOC-0003);
  - build the weekly BIM report (ARPL-RPT-0001).
- Keep data in line with the agreed standards:
  - bind the agreed project parameters and fill the mirrored values (ARPL-PAR-0003);
  - assign instance keys, never overwriting an existing one;
  - fill circuit values;
  - run the agreed Type Mark runs (ARPL-PAR-0004).
- Fix coordination settings that change nothing modelled, such as Room Bounding on links (ARPL-CRD-0002).
- Sync only after a clean step, with a comment, then relinquish. Watch the application for dialogs and never send commands into a blocked session.
- File lessons and failure patterns into ARPL. Private details (cloud ids, client names, pilot status) stay in private operator notes.

## 2. What needs the discipline lead's confirmation

- Deleting, moving or renumbering elements, rooms or spaces (for example stray spaces, elements modelled in the wrong discipline model, rooms outside their boundaries).
- Placing new spaces or other modelled content.
- Clash results above the agreed intrusion threshold (5 mm on the pilot) before they go out as issues.

## 3. What needs the BIM manager's decision

- Standards and naming: shared parameter file entries, prefixes, Type Mark groups, LOIN fields and targets.
- Anything that cannot be undone, or that touches another company's model or authority.
- Pushing to USG, and changes to ARPL's structure or vocabularies.

## 4. What the coordinator does not do

- Design decisions, sizing, or code compliance.
- Sending messages to the teams on the BIM manager's behalf. The coordinator drafts them; the BIM manager sends.

## 5. Alignment with industry practice (desk review, 2026-10-28)

**Sources reviewed:**
- ISO 19650-1/-2: roles, the responsibility matrix, and the duty to check before sharing.
- UK BIM Framework responsibility matrices, as summarized by Designing Buildings.
- The Designing Buildings definition of BIM co-ordinator.
- A literature review of BIM coordinators: 78 publications plus expert interviews (ECAM, 2017).
- A practitioner role handbook (InfraLens).
- Two owner BIM requirements:
  - Maryland Aviation Administration (MDOT MAA) BIM standards, §5.3;
  - Penn State OPP BIM contract addendum.

**Where the scope matches common practice**

| Industry task for a BIM coordinator | Scope item |
|---|---|
| Model and data quality control, checking models before they are shared (ISO 19650-2 check/review/approve; MDOT MAA QA/QC coordinator) | §1 checks, weekly report, LOIN completeness (ARPL-QA-0002) |
| Clash detection and clash avoidance, coordination reviews | §1 report, §2 clash threshold and lead confirmation (ARPL-CRD-0001) |
| Progress reports and coordination programmes | Weekly BIM report (ARPL-RPT-0001) |
| Recording shared data and the relationships between models | Link and federation checks; instance key; registry |
| Coordinating data management, keeping data in line with protocols | §1 data alignment; one shared parameter file (ARPL-PAR-0002) |
| Monitoring design changes; acting as the go-between for the parties | Weekly snapshot; draft messages for the BIM manager (§4) |
| Design decisions stay with the discipline lead; the coordinator supports resolution; the coordinator reports to the (project) BIM manager | §2, §3, §4 |

**Where the scope differs from common practice, and how ARPL handles it**

1. **Writing into other teams' models.**
   - *Standard:* under ISO 19650 each task team produces and owns its information containers.
   - *Here:* the coordinator writes data into all discipline models: parameters, keys, Type Marks, link settings.
   - *How ARPL handles it:* the project's responsibility matrix (ISO 19650-2 Annex A), or the BEP, should name the coordinator for these activities. Every write is synced with a comment and listed in the weekly report, so the task teams can see it.
2. **BEP and protocols.**
   - *Standard:* many definitions give the coordinator the job of developing and maintaining the BEP and protocols.
   - *Here:* standards and naming are the BIM manager's decision (§3). This matches the split between project BIM manager and coordinator in owner requirements such as MDOT MAA. Gap: none.
3. **CDE and information management.**
   - *Standard:* ISO 19650 and UK practice expect checks of container naming, status or suitability codes, revisions and metadata in the common data environment. These belong to the information management function, which on many projects is combined with the coordinator.
   - *Here:* the scope covers models, not CDE containers.
   - *Possible extension:* read-only CDE checks for naming, status and revision, added to the weekly report.
4. **Clash matrix and coordination meetings.**
   - *Standard:* the coordinator usually keeps the clash matrix (which disciplines are checked against which, and with what tolerance) and runs the coordination meetings.
   - *Here:* the 5 mm threshold is recorded, but there is no matrix yet, and meetings stay with the BIM manager.
   - *Possible extension:* a clash matrix per project in ARPL-CRD-0001.
5. **Handover and training.**
   - *Standard:* information handover at milestones (asset data, record models) and training the team are common coordinator tasks.
   - *Here:* neither is in scope yet.
   - *Possible extension:* milestone handover checks once the client's handover requirements are known.
6. **Agent-specific rules with no counterpart in the standards.**
   - The rules are: sync only after a clean step, watch for dialogs, never send commands into a blocked session, and record lessons and failure patterns.
   - They come from running the role as an AI agent, and they are ARPL's own addition.

**Conclusion:** the scope matches the core of the BIM coordinator role as the industry describes it: quality control, clash coordination, data management, reporting, and supporting rather than making design decisions. It is narrower on CDE information management, clash-matrix ownership and handover. It is wider in one respect: it writes data into all discipline models, which ISO 19650 expects to be authorized in the responsibility matrix.

## 6. Change log

| Version | Date | Change | By |
|---|---|---|---|
| 1.0 | 2026-10-28 | Scope confirmed by the owner; industry alignment review added | Gottfried Schmidtke with Claude |
