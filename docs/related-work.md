# Related work

Survey of projects close to ARPL, so future work starts from what exists. Searched 2026-10-20: English sources, a short pass in Chinese, Japanese and German, the REVIT_MCP_study repository read in full, construction knowledge-management literature, and agent-security research. Remaining gaps: work inside firms, commercial vendors' private systems, LinkedIn-only posts, Korean sources. Update this page when new projects appear.

## Summary

**ARPL is not the first shared, reviewed collection of Revit lessons for AI agents.** REVIT_MCP_study (below) has run one since March 2026, with outside contributors, monthly community meetings, workflow procedures, an append-only lessons file and a carefully designed "anti-lessons" collection. Say so openly.

What no public project combines is ARPL's particular set: **independent of any bridge** (usable from any MCP server, add-in or chat AI), **failure evidence as the core unit** (every iteration, how the problem was found, the final rule and its validation), an **evidence lifecycle** (candidate → reproduced → verified, with revisions and Revit versions tested), a **machine-readable index with a lookup protocol for agents**, and **professional framing** (work classes, disciplines, project types). The pieces exist separately:

| Need | Closest existing work | Gap ARPL fills |
|---|---|---|
| Revit workflow knowledge for agents | REVIT_MCP_study (domain SOPs, skills, lessons, anti-lessons) | Bound to one bridge and its tools; Taiwanese code focus; no evidence levels, Revit versions per lesson or machine index |
| Shared agent learning mechanism | mozilla-ai/cq (knowledge units, confirm/flag, human review) | Generic coding agents; no AEC content or professional framing |
| Failures turned into tests | ORP (lesson + eval + guardrail) | Local only; not shared; not AEC |
| Agent access to Revit | Many MCP bridges; Autodesk Assistant (Revit 2027) | Tools without shared memory |

## Closest in content

**[REVIT_MCP_study](https://github.com/shuotao/REVIT_MCP_study)** (shuotao, Taiwan; MIT; about 100 stars, 117 forks; active, last commit 2026-10-12; [knowledge site](https://shuotao.github.io/REVIT_MCP_study/)). Revit MCP server (221 tools, Revit 2022–2026) with a community knowledge layer, read in full on 2026-10-20:

- **`domain/`**: 83 workflow procedures (building code checks, quantity take-off, fire safety, parking, MEP, documentation), mostly in Traditional Chinese, with YAML frontmatter aligned to the Agent Skills spec (`name`, `description`, `metadata.version/updated/references/related/referenced_by/tags`) and staleness warnings after 12 months.
- **61 Claude skills**, each linked to a domain file; the domain file wins where they disagree.
- **`domain/lessons.md`**: 30 append-only lessons (`[L-001]`…), each a rule plus practice; maintained by a `/lessons` command. Mix of Revit API lessons (dimension references, corridor widths from boundary segments rather than bounding boxes) and bridge plumbing (WebSocket buffers, add-in deployment).
- **`domain/anti-lessons.md`**: 14 de-identified entries (`[N-001]`…) recording *what wrong information looks like*: type (TRANSIT, MISLEAD, MISJUDGE, BADDATA, EXPIRED), "what it looks like", "what it really is", **"how it was found"** (called the most reusable field) and a **"reverse exercise"** question usable as a test. Example: a non-zero outdoor-air value in a Revit space was a US software default, 10.7 times lower than the Taiwanese code requirement.
- **`tool-capability-boundary.md`**: what the tools cannot do, so the AI says so immediately instead of retrying.
- **Process**: contributions by pull request into `domain/` and `lessons.md`; code and AI instruction files are maintainer-only; monthly community meetings ("月小聚") where entries are reviewed; append-only session logs. About ten named human and AI contributors in the frontmatter.

**Overlap with ARPL:** lessons from production, "how it was found", review before acceptance, de-identification, agent instruction files.
**Differences:** knowledge is bound to that bridge's 221 tools and commands; much of it is Taiwanese building code; no status lifecycle or reproduction, no Revit version per lesson, no machine-readable index for other agents; lessons are append-only rules without the failed iterations that led to them.

**What ARPL should learn from it:**
1. Anti-lessons are a sharper idea than ARPL's failure patterns alone: record what the misleading information *looks like*, so an agent recognises it. ARPL's FP05 and FP13 are close; their TRANSIT/MISLEAD/MISJUDGE/BADDATA/EXPIRED types could become a facet.
2. The "reverse exercise" turns every lesson into a test question for agents.
3. Monthly meetings with review are what keeps contributions coming (see the lessons-learned literature below).
4. Staleness warnings after 12 months.

**Status for ARPL:** the most important project to contact, as a peer rather than a source. Options: cross-link; translate and file selected bridge-independent lessons and anti-lessons with credit (MIT allows it, but ask first); offer ARPL's index to their agents. Not yet contacted.

## Closest in mechanism

**[cq](https://github.com/mozilla-ai/cq)** (Mozilla.ai; Apache-2.0; about 1.3k stars; v0.x, breaking changes expected). "An open standard for shared agent learning": agents query knowledge units before acting, propose new ones, confirm or flag existing ones; units graduate to a shared Global Commons after human review. Local SQLite store, optional hosted or self-hosted remote. Plugin for Claude, Codex, Copilot, Cursor and others.

Mapping to ARPL: propose = inbox submission; confirm = `reproduced`; flag = deprecation request; human review graduation = curation. No AEC content.
**Status for ARPL:** complementary. Option: export ARPL packs as cq knowledge units so cq users find Revit knowledge. Not started.

**[ORP, Open Reflection Protocol](https://github.com/Fujo930/ORP)** ([article](https://dev.to/fujo_for_text/give-your-agent-a-mistake-once-orp-turns-ai-agent-failures-into-tested-lessons-llh); MIT; early). Turns a failure trace into a lesson, a regression eval and a guardrail; lifecycle candidate / active / under_review / deprecated / rejected; delivered through MCP. Local and private; not shared.
**Status for ARPL:** model for executable validations (roadmap item 3).

## Revit bridges (potential adopters of `tools/arpl_search.py`)

| Project | Notes |
|---|---|
| [bimwright/rvt-mcp](https://github.com/bimwright/rvt-mcp) | Revit 2022–2027, about 220 tools, C# escape hatch; "ToolBaker" saves personal tools locally (not shared) |
| [HorizunGroup/horizun-revit-mcp](https://github.com/HorizunGroup/horizun-revit-mcp) | Re-reads every write after commit, audits with pass/fail, plan rollback; has AGENTS.md and llms.txt; methodology kept in a separate "Horizun Hub" (not found publicly) |
| [hungpixi/revit-mcp](https://github.com/hungpixi/revit-mcp) | MCP server + C# bridge, Revit 2024+ |
| [Sam-AEC/aec-model-bridge](https://github.com/Sam-AEC/Autodesk-Revit-MCP-Server) | Human approval on every change |
| [LuDattilo/revit-mcp-server](https://github.com/LuDattilo/revit-mcp-server) | 80+ tools, Revit 2023–2026 |
| [antonhofstader/Revit-2026-MCP-Server](https://github.com/antonhofstader/Revit-2026-MCP-Server) | Revit 2026 |
| [luoyuke/RevitAgenticAICompanion](https://github.com/luoyuke/RevitAgenticAICompanion) | Revit 2026 add-in, bounded planning and execution |
| [APS Revit Automation MCP samples](https://github.com/autodesk-platform-services/aps-sample-mcp-server-revit-automation/) | Autodesk samples for cloud models via Automation API |

## Autodesk

- **[Revit Public MCP Server](https://www.autodesk.com/blogs/aec/2026/06/17/revit-public-mcp-server/)** (announced 2026-06-17, tech preview): separate add-on for **Revit 2027**, local over stdio, **read-only** with seven tools (running instances, query model, element data, select, zoom, open view, export view). A separate write server is planned. Runs alongside community servers. No knowledge base, skills or agent guidance mentioned. (An earlier overview, [goto.archi](https://goto.archi/blog/post/whats-new-in-revit-2027), still called it "coming soon"; the Autodesk post supersedes it.)
- **Revit 2027 Autodesk Assistant** ([What's New](https://help.autodesk.com/cloudhelp/2027/ENU/Revit-WhatsNew/files/GUID-68D8FE6D-C5B0-4503-AE27-02C715BAC25B.htm)): tech preview with an embedded MCP client.
- **[Revit Gen AI: MCP, RAG and Vibe](https://blog.autodesk.io/revit-gen-ai-mcp-rag-and-vibe/)** (Jeremy Tammik, Autodesk developer blog, 2025): community projects; Revit SDK help converted to Markdown for RAG.

**Implication:** Autodesk now ships the access layer (read-only so far) and leaves knowledge to others. When the write server arrives, every assistant creating content will need production knowledge of the kind ARPL and REVIT_MCP_study hold.

## Human knowledge pools (sources, not competitors)

Twenty years of Revit API knowledge exists, written for people rather than agents:
- **The Building Coder** (Jeremy Tammik's blog since 2008, with the `tbc` sample code), the **Autodesk Revit API forum**, **revitapidocs.com**, the **pyRevit** and **Dynamo** forums.
- **[Rvt_Docs_MCP](https://glama.ai/mcp/servers/kaitpw/Rvt_Docs_MCP)** and the Autodesk RAG script make the API reference available to agents; that covers *what the API offers*, not *what happened in production*.

ARPL should cite these when a pack's rule rests on them, and could invite their authors to contribute.

## Lessons-learned systems in construction (why such pools fail)

Construction has decades of lessons-learned databases and post-project reviews; most were under-used. Findings that apply directly to ARPL:
- Top barriers to capturing lessons: **lack of employee time, lack of resources, lack of clear guidelines**; lack of management support ranked lowest ([Shokri-Ghasabeh and Chileshe 2014, *Construction Innovation*](https://pure.uj.ac.za/en/publications/knowledge-management-barriers-to-capturing-lessons-learned-from-a/)).
- Knowledge is lost through **delayed capture**, staff turnover and reluctance to share; it should be captured **live**, during the work, in a form that supports reuse ([*Live capture and reuse of project knowledge in construction organisations*, KMRP 2006](https://iaorifors.com/paper/57766)).
- See also [PMI: Capitalizing from past projects](https://www.pmi.org/learning/library/business-benefits-value-lessons-learned-7116) and the reviews of [knowledge management in construction](https://www.researchgate.net/publication/362972947_Knowledge_management_in_construction_industry_projects_A_review_of_the_literature).

**How ARPL answers this:** capture happens live, by the agent, at the end of the task it just did (AGENTS.md "give back"), which removes the time barrier; the template and the curator remove the guidelines barrier; reuse happens automatically through the index. The open risk is the one REVIT_MCP_study solved socially: regular meetings and visible credit.

## Other languages

Short passes in Chinese, Japanese and German found further bridges, e.g. [xml.Revit.MCP (ZedMoster)](https://glama.ai/mcp/servers/@ZedMoster/revit-mcp/blob/7d3769bf7b20975ef1855bf76f547cf7612a5e3f/README.md) and [AchyErrorJ/RevitMCP](https://glama.ai/mcp/servers/AchyErrorJ/RevitMCP), but no further knowledge pools. REVIT_MCP_study remains the only comparable one found.

## Security research relevant to ARPL

Shared instruction files are an attack surface. A [Cloud Security Alliance briefing (May 2026)](https://labs.cloudsecurityalliance.org/research/briefing-csa-research-note-skill-md-agent-context-poisoning/) reports a Snyk audit in which 36.8% of 3,984 public agent skills had security flaws and 76 contained malicious payloads, including instructions hidden in invisible Unicode characters. Research: [SkillJect](https://arxiv.org/html/2602.14211v1), [Skill-Inject (NeurIPS 2026)](https://neurips.cc/virtual/2026/poster/139261). ARPL's response: [docs/scope.md, Security](scope.md#security).

## Skill collections

- [Archgyan: Revit automation with Claude Code skills](https://archgyan.com/revit-automation-claude-code-skills-architects/) (April 2026): six sample SKILL.md files (family auditor, schedule validator, warnings analyzer…) and a "common mistakes" list; no licence stated, no failure evidence, no contribution process.
- Skill marketplaces list generic "Revit expert" skills (e.g. theneoai/awesome-skills `revit-bim-expert`) with self-assigned scores and no test evidence.

## Research lineage: case-based reasoning and agent memory

ARPL is not a new mechanism. It applies an old one to a new kind of evidence, and it should be read that way.

- **Case-based reasoning.** [Aamodt and Plaza (1994)](https://doi.org/10.3233/AIC-1994-7104) describe the cycle *retrieve, reuse, revise, retain*. ARPL maps onto it directly: retrieve = index lookup (`lookup_order`); reuse = apply the pack's rule; revise = the `vNN` iterations and the validation (now partly executable, `final/checks/`); retain = inbox plus curation.
- **Skill libraries for LLM agents.** [Voyager (Wang et al., 2023)](https://arxiv.org/abs/2305.16291) stores verified code skills and retrieves them for new tasks. [Agent Workflow Memory (Wang et al., 2024)](https://arxiv.org/abs/2409.07429) induces reusable workflows from past runs. [ExpeL (Zhao et al., 2023)](https://arxiv.org/abs/2308.10144) extracts insights from successes and failures. [Reflexion (Shinn et al., 2023)](https://arxiv.org/abs/2303.11366) keeps verbal lessons from failed attempts.
- **What ARPL adds.** These systems are private to one agent, in an environment that verifies itself (a game, a website, a test suite). ARPL is shared across people, models and organizations, in a domain where "success" is judged professionally. A model can be geometrically valid and still wrong. So ARPL adds:
  - failures kept with how they were found (`found_by`)
  - an applicability envelope (`use_when`, `not_for`, Revit versions, environment)
  - an evidence status that only rises through outside reproduction
  - human curation with security checks
  - attribution

The contribution is the professional evidence format and its governance, not the retrieval loop.

## Research

- [Heimig-Elschner, Du, Scheuvens, Borrmann, Beetz: A modular reference architecture for MCP servers enabling agentic BIM interaction](https://arxiv.org/html/2601.00809) (RWTH Aachen, TUM, BBSR; 2026). Knowledge service for API docs, workflows and codes via vector retrieval; no learning from past runs; model validation left as future work. Tool calls succeeded in every run while model success ranged 40–100%, which is ARPL's failure pattern FP05 measured.
- [ProcMEM: learning reusable procedural memory from experience](https://arxiv.org/html/2602.01869v1): generic agent procedural memory.
- [Towards a copilot in BIM authoring tool using an LLM](https://arxiv.org/pdf/2406.16903), [Qwen-BIM](https://www.alphaxiv.org/abs/2602.20812), [BIM-Edit](https://arxiv.org/html/2606.20146v1): copilots and benchmarks, not shared experience.

## Next steps (owner decides)

1. Contact REVIT_MCP_study as a peer: cross-link, ask about filing selected bridge-independent lessons and anti-lessons in ARPL with credit, consider an anti-lesson facet.
2. Evaluate cq compatibility: export packs as knowledge units.
3. Offer `arpl_search` to bridge authors (rvt-mcp, Horizun, Sam-AEC and others).
4. Watch for Autodesk's write-capable Revit MCP server.
5. Invite authors of human knowledge pools (The Building Coder, forums) to contribute or be cited.
6. Re-run this survey every few months; record new projects here.
