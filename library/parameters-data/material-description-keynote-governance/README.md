# ARPL-PAR-0001 rev 1: Governed material Descriptions and Keynotes

_Generated from this pack's files by tools/build_catalogs.py. Edit manifest.json, intent.md, vNN/ or final/rule.json instead._

| | |
|---|---|
| Level | 2 |
| Work class | W7 |
| Status | candidate |
| Use when | A Revit material schedule contains blank, incomplete or contradictory Description values.; Materials need Keynote values for material tags or sheet keynote legends.; Material data is exported to CSV, AI-reviewed and read back into Revit.; A Revit Bridge reads material properties, requests an AI proposal, previews the proposal and commits approved changes. |
| Not for | Inventing manufacturer, product, grade, performance or specification properties that are not supported by the source data.; Replacing an approved office or project keynote database without explicit authorization.; Treating appearance assets as authoritative physical specifications.; Automatically describing analytical, phase, poche, default or other graphic/system materials as construction materials unless the user explicitly wants them documented.; Merging, deduplicating, renaming or deleting Revit materials as a side effect of metadata enrichment. |
| Workflows | parameters-data, documentation, model-administration |
| Disciplines | architecture, bim-vdc |
| Project types | generic |
| Revit tested | 2024 |
| API | Material, AppearanceAssetElement, Asset, AssetProperty, KEYNOTE_PARAM, KeynoteTable, KeynoteEntry, Parameter.Set, Transaction, ExternalEvent |
| Failure patterns | FP03, FP06, FP07 |
| Contributors | Gottfried Schmidtke |

**Intent:** Normalize Revit Material Description and Keynote data so an AI agent can improve incomplete material metadata without inventing unsupported technical information, while preserving deterministic Revit round-trip behavior and producing keynote values suitable for material tags and sheet legends.

## Learning curve

| Version | Instruction | Result | Problem | Found by |
|---|---|---|---|---|
| v01 | Export Revit materials and use AI to fill missing or inconsistent material descriptions from Name, Class, existing Description and appearance data. | AI produced normalized descriptions for physical materials and corrected several contradictions. | The first description grammar also carried dimensions from material names into Description, for example panel and tile sizes. | Human review of the edited material schedule in Excel showed that dimensions made the Description less reusable and duplicated type/name information. |
| v02 | Refine the material Description standard. | Description was redefined as a dimension-free human-readable identity: base material, product/form, finish/treatment, color, pattern/texture, and supported grade/performance terms. | Appearance data can contain plausible but non-authoritative product information, and existing descriptions can conflict with Name or appearance. | Examples showed conflicting colors and finishes between material Name, Description and Appearance Asset. |
| v03 | Create logic for assigning Material Keynotes used by Revit tags and legends. | Keynote was separated from Description: Description identifies the material variant; Keynote is the documentation identity. Existing keys remain authoritative. A new local suffix system may be generated only when the user explicitly requests creation of a new project keynote set. | The alphabetic suffix after a classification section is not inherently an official semantic code and must not be treated as one without an authoritative keynote table. | Existing material schedules contained repeated section-based keys with local suffixes that did not expose a universal letter meaning. |
| v04 | Adversarially review the governance logic for places where a human-readable rule could be misread by an autonomous agent. | The logic was tightened by naming actors, adding classification criteria and proposal states, anchoring family equivalence to approved mappings, quarantining suspicious keynotes, forbidding completion-looking placeholders, specifying a sidecar proposal schema, and requiring runtime API/keynote resolution checks. | Several rules were individually sound but left implicit authority boundaries or undefined terms such as equivalent family, valid keynote, direct commit, and proposal storage. | External model review (Mistral) tested the rule set under adversarial reading and identified ambiguities that did not require restructuring but did require explicit machine-readable constraints. |

## Lesson
Separate the four identities of a Revit material: Name is the BIM identifier, Description is the human-readable material identity, Keynote is the documentation/tagging identity, and Appearance is the visual identity. AI reasoning may be rich and probabilistic; production BIM data must remain authorized, deterministic and verifiable.

## Rule
0. ACTORS AND AUTHORITY
Use three explicit actors:
- AI: interprets evidence and proposes changes. AI never performs an uncontrolled production write.
- Approver: human or pre-authorized policy that accepts, rejects, quarantines or escalates a proposal.
- Engine: performs only approved deterministic writes and verifies the result.

1. PRESERVE THE ROUND-TRIP SCHEMA
When editing an exported material CSV intended for Revit re-import, the Engine must not add, remove, rename or reorder columns. It must not rename materials. It may modify only fields explicitly authorized by the workflow, normally Description and/or Keynote. Metadata enrichment must not merge, deduplicate or delete materials.

2. CLASSIFY BEFORE ENRICHING
The AI must first classify each row as one of:
PHYSICAL | FINISH | SYSTEM | GRAPHIC | ANALYTICAL | UNKNOWN.

Classification is part of the proposal and must include evidence.
Useful deterministic hints include Revit class/category metadata and name patterns such as Default, Poche, Analytical, Phase -, Clearance and similar system/graphic terms. Name-pattern hints are evidence, not sole authority.
SYSTEM, GRAPHIC and ANALYTICAL rows must not receive invented construction descriptions or classification keynotes unless the Approver explicitly authorizes a separate internal documentation namespace.
UNKNOWN must be reviewed rather than silently promoted to PHYSICAL.

3. MATERIAL DESCRIPTION GRAMMAR
For PHYSICAL or FINISH materials, the AI may propose Description from supported evidence in this order:
Base Material -> Product/Form -> Finish/Treatment -> Color -> Pattern/Texture -> Grade/Performance.
Omit any component that is not supported.

Description describes what the material is and how it is finished. It does not describe its instance size or type dimensions.

Hard exclusions from Description:
- dimensions, thicknesses and sizes;
- model/type numbers unless they are part of the actual product identity explicitly required by the Approver;
- project codes;
- keynote numbers;
- unsupported manufacturer/product claims;
- completion-looking placeholders such as N/A, Unknown, TBD, To Be Determined or equivalent, unless the governing standard explicitly requires that literal value.

4. EVIDENCE AUTHORITY
Use Name and Class primarily for material identity.
Use an existing Description as evidence, but test it for contradictions.
Use explicit terms in Name as strong evidence.
Use Appearance Asset and appearance properties as visual evidence for attributes such as color, gloss, texture and transparency.
Do not promote an appearance texture or asset name into a physical/specification claim unless corroborated.
Appearance-only color is low-confidence visual evidence: the AI may propose it, but the Engine must not commit it into Description unless corroborated or specifically approved.
Use Keynote only as a classification hint, not as proof of physical properties.

5. CONFLICT HANDLING
If Name, Description, Class and Appearance conflict, the AI must not silently merge contradictory claims. It must record the conflict in the proposal and prefer explicit material identity over purely visual appearance.
The AI may mark an unambiguous correction as high confidence, but it does not directly commit it.
The Engine may commit only after the Approver or a documented pre-authorized approval policy permits that specific change class.

6. KEYNOTE AUTHORITY AND STATES
If an approved office/project keynote table exists, it is the governing authority.

Define keynote state as:
- VALID: key exists in the governing table and resolves to the expected entry.
- SUSPICIOUS: key exists and resolves, but conflicts with the material evidence, approved mapping or intended documentation use. Preserve it, quarantine/flag it, and do not silently replace it.
- INVALID: key is absent from the governing table or fails resolution.

The Engine must preserve existing VALID keynotes unless remapping is explicitly authorized.
The AI may flag SUSPICIOUS or INVALID keynotes but may not overwrite them without approval.
Never invent a new key because a classification number merely looks plausible.
If no reliable approved match exists, leave Keynote blank or route to review.

Match priority:
a. exact approved material/library match;
b. equivalent approved material family ONLY when equivalence is defined by a documented approved mapping table or library relationship;
c. approved keynote database/table match;
d. approved specification/classification mapping;
e. no match -> review/blank.

7. GENERATING A NEW PROJECT KEYNOTE SET
Only generate new material keynotes when the Approver explicitly requests creation of a new project keynote system and no governing table must be preserved.
Use:
<approved classification section>.<local family letter><variant number>

The classification section is the authoritative classification anchor.
The suffix is local project/office syntax, not an official meaning supplied by the classification standard.
The family letter groups related materials within a section.
The number distinguishes documented material variants.

For material-tag and sheet-legend workflows, default to a unique suffix when two variants must appear as separate legend entries. Variants may share a key only when they are intentionally represented by the same legend/specification entry.

A generated keynote is not complete until a matching keynote text-table entry exists and resolves correctly in Revit.

8. AI PROPOSAL SIDECAR
AI reasoning and review metadata must live outside the Revit round-trip CSV unless the governing schema explicitly provides fields for them.
Use a sidecar proposal record with at least:
{
  "material": "<existing material name>",
  "classification": "PHYSICAL|FINISH|SYSTEM|GRAPHIC|ANALYTICAL|UNKNOWN",
  "proposed_description": "<string|null>",
  "proposed_keynote": "<string|null>",
  "keynote_state": "VALID|SUSPICIOUS|INVALID|null",
  "evidence": ["<source/value/reason>"],
  "conflicts": ["<conflict>"],
  "confidence": 0.0,
  "decision": "PROPOSE|REVIEW|QUARANTINE|NO_CHANGE"
}

The sidecar is advisory/audit data. The Engine writes only approved production values into the authoritative CSV/Revit model.

9. COMMIT
CSV workflow:
Revit export -> AI sidecar proposal -> Approver/policy decision -> Engine edits only authorized existing cells -> Revit import -> read-back verification.

Bridge workflow:
Read Material -> gather governed evidence -> AI sidecar proposal -> preview/dry run -> Approver/policy decision -> approved ExternalEvent -> Transaction -> set authorized values -> regenerate/read back -> verify.

10. REVIT API WRITE AND RESOLUTION CHECKS
Do not assume that the existence of BuiltInParameter.KEYNOTE_PARAM guarantees a writable Material keynote in every target version/document.
For Revit 2024-2027, the Engine must runtime-check that the target Material exposes the expected keynote parameter, that it is writable when a write is requested, and that the storage/value behavior is as expected before calling Parameter.Set.
Use the governing KeynoteTable/KeynoteEntry data where available to validate membership and resolution.
If parameter access, writability or keynote-table resolution differs from expectation, do not substitute a guessed API path or value; flag the material/workflow for review.

11. FAIL SAFE
When evidence is insufficient, omit the unsupported Description component or leave Keynote blank.
Do not pad missing information with placeholders that merely make the record look complete.
Missing data is preferable to plausible invented BIM data.

## Validation
- CSV validation:
- row count unchanged;
- column count, names and order unchanged;
- material Name unchanged;
- no materials merged, deduplicated or deleted;
- every non-authorized cell byte/value-equivalent to the source;
- Description contains no copied dimensions/sizes;
- Description contains no banned completion placeholder unless explicitly required;
- no unsupported physical claim was introduced;
- existing VALID Keynotes remain unchanged unless remapping was authorized.
- Proposal/sidecar validation:
- every record identifies the existing material name;
- classification is one of the allowed states;
- evidence is present for every proposed non-null Description or Keynote;
- conflicts are surfaced, not silently resolved;
- appearance-only color is marked as low-confidence evidence unless corroborated;
- UNKNOWN classification cannot auto-commit;
- SUSPICIOUS or INVALID keynote state cannot auto-commit;
- equivalent-family matching cites an approved mapping relationship.
- Keynote validation:
- VALID means both governing-table membership and successful resolution;
- every selected approved key exists in the governing keynote table and resolves to the expected entry; or, for a newly authorized project keynote set, every generated key has a corresponding text-table entry;
- no single key resolves to conflicting legend text;
- distinct material variants receive distinct keys when the intended sheet legend requires separate entries;
- suffix semantics are documented as local, not represented as official classification semantics.
- Revit/API validation:
- before write, confirm the target Material exposes the expected keynote parameter and that it is writable for the requested operation;
- commit occurs inside the required Revit API transaction path;
- read back Description and Keynote after commit;
- confirm the material tag reports the expected keynote;
- place or refresh a keynote legend and confirm key and text resolve as intended;
- if read-back, parameter access or legend resolution differs from the approved proposal, roll back where possible or quarantine/flag the material for review.
