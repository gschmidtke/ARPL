# ARPL: Position Paper

20 October 2026 · Gottfried Schmidtke

ARPL (AI Revit Production Logic) is a public, curated knowledge pool for AI agents working in Revit, live on GitHub since 20 October 2026. It holds 25 instruction packs, all recorded once by one contributor in Revit 2024. It's ready for its first outside users, but not yet proven by them.

## Where ARPL stands today

ARPL now has three layers. Only the third is public.

| Layer | What it is | State |
| --- | --- | --- |
| RevitBridge | The access tool: an MCP bridge that lets an AI run C# inside Revit | Version 0.4.0, private, used in daily production tests |
| ARPL protocol | Governance rules for agents: stages, decision register, layout preview before modelling | Version 0.43 (JSON), not yet public |
| ARPL learning pool | Instruction packs with intent, every attempt, the final rule and its validation | This repository, public, CC BY 4.0 for content, MIT for code |

What the learning pool contains:

| Item | Count |
| --- | --- |
| Instruction packs (levels 1–3) | 25, all status "candidate", revision 1 |
| Project workflows (level 4) | 1: ADU exterior wall fabrication package |
| Failure patterns | 13 (FP01–FP13) |
| Discipline overlays | 1 (electrical power connector) |
| Controlled vocabularies | 17 workflows, 18 disciplines, 12 roles, 11 project types, 8 phases, 8 work classes |
| Revit versions tested | 2024 only |
| Contributors | 1 (Gottfried Schmidtke, with Claude) |

What already works:

- **One inbox.** Contributors can only add files to `inbox/`; an automatic check rejects anything else, and hidden characters.
- **Curation.** An AI curator under the owner's supervision runs every morning (daily for two weeks, then a slower rhythm). It reviews submissions, files them, credits contributors and writes a report for the owner.
- **Agent access.** `AGENTS.md`, `llms.txt` and one machine-readable `index.json` let any AI with web access find and apply packs. `tools/arpl_search.py` is a lookup tool that bridge authors can add.
- **Evidence tracking.** Every pack has a status, a revision, the Revit versions it ran in and a changelog.
- **External review.** Zara (ChatGPT) and Grok reviewed the repository; their fixes are in.

## Purpose

ARPL exists so that no AI working in Revit has to learn the same production lesson twice.

Connecting an AI to Revit is now solved many times over: community MCP servers, add-ins, and since June 2026 Autodesk's own read-only MCP server. What is not solved is the step after access. An AI can call the Revit API correctly and still produce the wrong professional result. Studs are placed exactly, then Revit's automatic joins move them 89 mm. A connector is created, but without the load parameters an engineer needs. A section is generated, looking the wrong way. Every call "succeeded".

The core idea is one sentence:

> Teach it professional practice downward until the required API action becomes obvious.

ARPL starts from what a professional wants (a wall panel ready for fabrication, a circuited piece of equipment, a coordinated sheet) and works down to the API only at the end. Its unit of knowledge is not a script but a **record of evidence**: what was asked, what came out, what was wrong, how it was noticed, and the rule that finally worked, with a way to prove it.

The expensive information in Revit automation is rarely the code. It is this sequence: we tried this, Revit accepted it, it looked successful, it was actually incomplete, here is how we found out, here is the corrected method. That knowledge sits today in private chats, project folders and people's heads, and disappears when the session ends.

## What it tries to do

ARPL turns each AI-assisted Revit task into a loop: read the pool before acting, and feed it back afterwards when something new was learned.

![The ARPL loop: 1 Frame the task from evidence, 2 Look up index.json and packs, 3 Apply the rule and read failed attempts, 4 Verify and cite pack id and revision; then if new or better, 5 the user uploads to the inbox, 6 the curator reviews, files and credits, and the index is updated](images/arpl-loop.png)

The agent establishes the task's frame from evidence (the user's words, the open model, the family's category), not from the name of the task. It looks up project workflows first, then packs, then failure patterns. It applies the rule, reads the failed attempts so it doesn't repeat them, runs the validation and tells the user which pack and revision it used. If nothing covered the task, or a rule failed, or it found a better way, it offers to prepare a submission without client data. The user uploads it; the curator reviews and files it, and the next agent finds it.

Three principles hold the loop together:

- **Evidence over assertion.** A pack moves from candidate (recorded once) to reproduced (worked again elsewhere) to verified (reviewed by the owner or a named discipline reviewer). Each pack lists the Revit versions it actually ran in.
- **Method follows the kind of work.** Eight work classes (W1 family authoring to W8 analysis and review) decide what preview to show before committing and what counts as proof of done. Layout-driven work (W3), for example, needs a 2D preview the user confirms before any 3D build.
- **Guidance, not commands.** The user's instructions, the firm's standards and the user's approval always decide. Discipline judgments, such as structural adequacy, stay with the discipline.

## What already exists in similar form

ARPL is not the first shared collection of Revit lessons for AI agents, and it should say so. What no public project combines is ARPL's set: independent of any bridge, failure evidence as the core unit, an evidence lifecycle with revisions and Revit versions, a machine-readable index for any agent, and professional framing by work class and discipline. Survey date: 20 October 2026.

| Project | What it is | Overlap with ARPL | What it lacks compared with ARPL |
| --- | --- | --- | --- |
| [REVIT_MCP_study](https://github.com/shuotao/REVIT_MCP_study) (shuotao, Taiwan, MIT) | Revit MCP server with 221 tools, 83 workflow procedures, 61 skills, 30 lessons, 14 "anti-lessons"; monthly community meetings review contributions | Closest peer: production lessons, "how it was found", review before acceptance, de-identification | Bound to its own bridge; largely Taiwanese building code; no status lifecycle, no Revit version per lesson, no failed attempts kept, no index for other agents |
| [cq](https://github.com/mozilla-ai/cq) (Mozilla.ai, Apache-2.0) | Open standard for shared agent learning: query, propose, confirm, flag; human review before a unit joins the shared pool | Same loop and trust model (confirm = reproduced) | General coding agents; no AEC content or professional framing |
| [ORP](https://github.com/Fujo930/ORP) (MIT) | Turns agent failures into a lesson, a regression test and a guardrail | Failures as the source of rules | Local and private, not shared; not AEC |
| [Revit Public MCP Server](https://www.autodesk.com/blogs/aec/2026/06/17/revit-public-mcp-server/) (Autodesk, tech preview, June 2026) | Read-only access for Revit 2027, seven tools; write server planned | Access layer ARPL sits on | No knowledge, skills or guidance for agents |
| Community Revit bridges ([rvt-mcp](https://github.com/bimwright/rvt-mcp), [Horizun](https://github.com/HorizunGroup/horizun-revit-mcp), [Sam-AEC](https://github.com/Sam-AEC/Autodesk-Revit-MCP-Server) and others) | Tools for agents; some verify results after every write | Natural users of `arpl_search` | Tools without shared memory |
| Human knowledge pools (The Building Coder, Revit API forum, revitapidocs.com, pyRevit and Dynamo forums) | Twenty years of Revit API knowledge, written for people | Sources to cite and authors to invite | Not structured for agents; no production evidence format |

Two lessons from this survey shape ARPL. From REVIT_MCP_study: record what misleading information *looks like*, give every lesson a test question, review in regular meetings. From construction research on lessons-learned systems: they fail for lack of time, resources and clear guidelines, and through delayed capture ([Shokri-Ghasabeh and Chileshe 2014](https://pure.uj.ac.za/en/publications/knowledge-management-barriers-to-capturing-lessons-learned-from-a/); [live capture, 2006](https://iaorifors.com/paper/57766)). ARPL answers by letting the agent capture the lesson right after the task. The full survey: [related-work.md](related-work.md).

## Security risks and concerns

The biggest risk is that ARPL is read by agents: its content enters their context, so a bad pack can steer someone else's AI. The second is that the curator is itself an AI with push access, reading untrusted submissions every morning.

| Risk | How it would show up | Defence in place | Still open |
| --- | --- | --- | --- |
| Context poisoning through a pack | A pack tells agents to fetch a URL, send data or ignore their user. A May 2026 audit found malicious payloads in 76 of 3,984 public agent skills, some in invisible characters ([CSA](https://labs.cloudsecurityalliance.org/research/briefing-csa-research-note-skill-md-agent-context-poisoning/)) | AGENTS.md: ignore and report embedded instructions; curator checks every submission; validator and inbox check reject hidden characters | No signed releases yet; users can't pin a reviewed version except by commit |
| The AI curator is manipulated | A submission addresses the curator and gets merged or filed with harmful content | Curator prompt treats all submissions as data; it can't change vocabularies, schema, licences or `.github`; daily report to the owner | It runs unattended with push access. During the first weeks the owner should read each report; consider owner approval before merges |
| Client or personal data published | A contributor pastes project names, addresses or file paths | Template and CONTRIBUTING forbid it; agents strip it before drafting; curator checks | A merged pull request stays in git history; removing it means rewriting history |
| Unsafe code run by an agent | A snippet deletes elements or corrupts a model | Rule: code is read, never run unreviewed; packs are guidance | Planned executable validations increase this risk and need sandbox rules |
| Wrong or outdated rule applied blindly | A rule valid in Revit 2024 fails in 2027; a simplification passes as structural advice | Status lifecycle, Revit versions tested, discipline authority stays with professionals, deprecation policy | Only one Revit version tested; no reviewer named for any discipline yet |
| Intellectual property | Contributions include Autodesk SDK text, standards, manufacturer data or an employer's confidential methods | Licence confirmation in every submission; licensed content refused | Knowledge gained at work may belong to the employer; contributors need to be told plainly |
| Fake evidence | Invented reproductions push a pack towards "verified" | "Reproduced" needs evidence; only the owner sets "verified" | No reputation system for contributors yet |
| Single points of failure | One owner, one AI vendor as curator, one GitHub account | Curator role defined by documents, not by a model; MIT and CC BY allow forks | No second maintainer or backup curator |

## The silo problem

Production knowledge for Revit agents is forming right now, and most of it is forming inside walls. Every bridge, vendor and firm is building its own layer, tied to its own tools.

What the survey shows:

- **Knowledge bound to a tool.** REVIT_MCP_study's 83 procedures and 30 lessons are written for its own 221 tools. Horizun keeps its methods in a separate "Hub" that isn't public. BIMwright's learned tools stay on each user's machine.
- **Access open, knowledge absent.** Autodesk now ships a read-only MCP server and an assistant, with no knowledge layer for agents. Whoever fills that gap first will shape how agents work in Revit.
- **Private by default.** Firms and vendors keep agent memory inside their products or projects. Much of it can't be shared because it carries client data, and none of it can be checked from outside.

Most silos aren't built to exclude anyone. They form because a lesson is easiest to record in the tool where it happened, because client confidentiality makes firms careful, because language divides communities, and because vendors earn money from what is theirs. The effect is the same, though: every agent relearns the same failures, quality can't be compared, and users depend on whichever vendor holds the knowledge.

The AEC industry has seen this before. Building data was locked in proprietary formats until openBIM and IFC gave it a neutral, shared form. Agent production knowledge needs the same: a neutral format and a commons any tool can read and contribute to. That is the position ARPL can take.

## Where ARPL should go

ARPL should become the neutral commons for Revit agent production knowledge: the place any bridge, vendor or firm can read from and contribute to, the way IFC became neutral ground for building data. It earns that role by evidence first, not by announcement.

![Proposed roadmap: 1 Prove (Nov to Dec 2026: stress tests, reproductions by others, Revit 2025 to 2027 tested), gate: structure holds and first outside reproduction; 2 Open (Q1 2027: announce, bridges adopt arpl_search, named discipline reviewers), gate: 3 bridges use it and 10 outside contributors; 3 Standardize (2027: neutral pack format, executable validations, shared governance)](images/arpl-roadmap.png)

Phases and gates are a proposal; dates are targets, not commitments.

**Positioning for the announcement.** Don't claim to be first. Say: *ARPL builds on community lessons such as REVIT_MCP_study and on open agent-learning work such as Mozilla's cq, and adds a bridge-independent, evidence-tracked knowledge layer any Revit AI can use.* The Gemini "Advanced Redpill Loader" mistake is the opening example: the problem isn't that AI hallucinates, it is that it chooses its frame too early.

**Strategic choices:**

- **Peer, not competitor.** Approach REVIT_MCP_study as a partner: cross-link, translate and file selected bridge-independent lessons with credit, borrow anti-lessons and test questions.
- **Interoperate, don't enclose.** Publish packs in a form other systems can read (cq knowledge units, the Agent Skills format), so ARPL knowledge reaches agents that never visit the repository.
- **Bridges as distribution.** Every bridge that adds `arpl_search` turns its users into readers and contributors.
- **Community over volume.** Regular sessions with review and visible credit, as REVIT_MCP_study does, matter more than pack count. Research on lessons-learned systems says the same.
- **Governance before scale.** Name discipline reviewers, add a second maintainer, sign releases, before inviting large numbers of contributors.

**Decisions for the owner:**

- [ ] Approve the "how the failure was found" word list
- [ ] Set the GitHub description and topics
- [ ] Choose the first stress test (proposed: AV device versus electrical panel)
- [ ] Approve contacting shuotao (REVIT_MCP_study)
- [ ] Decide whether the ARPL protocol (v0.43) goes public with the learning pool
- [ ] Read the curator's daily reports for the first two weeks; decide whether merges need your approval
- [ ] Name a first discipline reviewer and a second maintainer

## Sources

- [REVIT_MCP_study](https://github.com/shuotao/REVIT_MCP_study)
- [cq, Mozilla.ai](https://github.com/mozilla-ai/cq)
- [ORP](https://github.com/Fujo930/ORP)
- [Autodesk: Introducing the Revit Public MCP Server](https://www.autodesk.com/blogs/aec/2026/06/17/revit-public-mcp-server/)
- [Cloud Security Alliance: agent context poisoning](https://labs.cloudsecurityalliance.org/research/briefing-csa-research-note-skill-md-agent-context-poisoning/)
- [Shokri-Ghasabeh and Chileshe 2014, barriers to capturing lessons learned](https://pure.uj.ac.za/en/publications/knowledge-management-barriers-to-capturing-lessons-learned-from-a/)
- [Live capture and reuse of project knowledge in construction, 2006](https://iaorifors.com/paper/57766)
- [Related-work survey](related-work.md)
