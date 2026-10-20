# Curation

**Owner:** Gottfried Schmidtke (repository owner, final authority).
**Curator:** Claude (Anthropic), working in sessions under the owner's supervision.

The curator keeps the library consistent so it stays useful as it grows. The owner reads the protocols and decides on anything that changes the structure or the rules.

## Review process for each submission

1. **Record intake.** Add a ledger entry: who, when, what files, source (PR or issue). Status `received`.
2. **Safety check.** Look for client data, personal data, secrets (keys, tokens, passwords), model files and licensed content. Anything found is removed or the submission is held, and the contributor is asked.
3. **Script check.** Contributed code is read, never run, until reviewed. Destructive or network calls are flagged.
4. **Understand.** Identify the intent, the iterations and the final rule. Ask the contributor if something essential is missing.
5. **Deduplicate.** Search the catalogs for the same technique:
   - same technique and same result → add the contributor to the pack and raise status to `reproduced`;
   - same technique with a new failure or fix → add an iteration to the existing pack;
   - new technique → create a new pack.
6. **Structure.** Write manifest, intent, iterations and final rule; assign facets from the controlled vocabularies only. New vocabulary values are proposed to the owner, not added silently.
7. **Validate.** Run `python tools/validate.py`, then `python tools/build_catalogs.py`.
8. **Close.** Update the ledger entry (decision, resulting pack ids), credit the contributor in CONTRIBUTORS.md, reply in the PR or issue with thanks and links, and move the raw submission to `ledger/archive/<entry-id>/`.

## Status rules

| Status | Meaning | Who sets it |
|---|---|---|
| candidate | Recorded once, as submitted | Curator |
| reproduced | Worked again in another model, by another person or in another Revit version | Curator, with evidence |
| verified | Reviewed by the owner or a named discipline reviewer; validation passes | Owner |
| deprecated | Superseded or no longer valid (API change); kept for history | Curator, recorded in the ledger |

## Protocols for the owner

After each curation session the curator writes a short report to `ledger/reports/YYYY-MM-DD.md`: submissions received, decisions, new or changed packs, contributors to thank, and questions waiting for the owner. That report is the owner's reading list.

## What the curator does not decide

Changes to the vocabularies, the schema, the licence, `verified` status, removing a contributor's credit, and anything about discipline adequacy (structural, code compliance). These go to the owner.
