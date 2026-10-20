# Related work

Survey of projects close to ARPL, so future work starts from what exists. Searched 2026-10-20 (English sources, public repositories and articles). Likely gaps: work inside firms, LinkedIn-only posts, non-English projects. Update this page when new projects appear.

## Summary

No public project combines what ARPL does: a **bridge-independent**, **multi-contributor**, **curated** pool of Revit production knowledge that keeps **failure evidence**, with a status lifecycle, revisions and professional framing (work classes, disciplines). The pieces exist separately:

| Need | Closest existing work | Gap ARPL fills |
|---|---|---|
| Revit workflow knowledge for agents | REVIT_MCP_study (domain SOPs, skills, lessons) | Tied to one bridge; no cross-user intake, evidence levels or version tracking |
| Shared agent learning mechanism | mozilla-ai/cq (knowledge units, confirm/flag, human review) | Generic coding agents; no AEC content or professional framing |
| Failures turned into tests | ORP (lesson + eval + guardrail) | Local only; not shared; not AEC |
| Agent access to Revit | Many MCP bridges; Autodesk Assistant (Revit 2027) | Tools without shared memory |

## Closest in content

**[REVIT_MCP_study](https://github.com/shuotao/REVIT_MCP_study)** (shuotao, Taiwan; MIT; about 100 stars, 117 forks, 580 commits). Revit MCP server with 192 tools, plus:
- `domain/`: 83 BIM workflow SOPs (building code, quantity take-off, compliance), "shared by humans and AI"; domain files take precedence over skills;
- 61 Claude skills (`.claude/skills/*/SKILL.md`), `CLAUDE.md`/`AGENTS.md`/`GEMINI.md`;
- `domain/lessons.md` and append-only session logs.

Differences: knowledge lives inside one bridge repository; Taiwanese code focus; no visible contribution review, status or Revit-version tracking.
**Status for ARPL:** most likely partner. Their lessons could become an external contribution (with permission; MIT is compatible). Not yet contacted.

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

- **Revit 2027 Autodesk Assistant** ([What's New](https://help.autodesk.com/cloudhelp/2027/ENU/Revit-WhatsNew/files/GUID-68D8FE6D-C5B0-4503-AE27-02C715BAC25B.htm), [overview](https://goto.archi/blog/post/whats-new-in-revit-2027)): tech preview, embedded MCP client; Autodesk's own Revit MCP server "coming soon". No shared agent knowledge or lessons found.
- **[Revit Gen AI: MCP, RAG and Vibe](https://blog.autodesk.io/revit-gen-ai-mcp-rag-and-vibe/)** (Jeremy Tammik, Autodesk developer blog, 2025): community projects; Revit SDK help converted to Markdown for RAG (API docs, not production experience).

**Implication:** when Autodesk's MCP server ships, every assistant needs a knowledge layer of this kind. Being the established open one before then matters.

## Skill collections

- [Archgyan: Revit automation with Claude Code skills](https://archgyan.com/revit-automation-claude-code-skills-architects/) (April 2026): six sample SKILL.md files (family auditor, schedule validator, warnings analyzer…) and a "common mistakes" list; no licence stated, no failure evidence, no contribution process.
- Skill marketplaces list generic "Revit expert" skills (e.g. theneoai/awesome-skills `revit-bim-expert`) with self-assigned scores and no test evidence.

## Research

- [Heimig-Elschner, Du, Scheuvens, Borrmann, Beetz: A modular reference architecture for MCP servers enabling agentic BIM interaction](https://arxiv.org/html/2601.00809) (RWTH Aachen, TUM, BBSR; 2026). Knowledge service for API docs, workflows and codes via vector retrieval; no learning from past runs; model validation left as future work. Tool calls succeeded in every run while model success ranged 40–100%, which is ARPL's failure pattern FP05 measured.
- [ProcMEM: learning reusable procedural memory from experience](https://arxiv.org/html/2602.01869v1): generic agent procedural memory.
- [Towards a copilot in BIM authoring tool using an LLM](https://arxiv.org/pdf/2406.16903), [Qwen-BIM](https://www.alphaxiv.org/abs/2602.20812), [BIM-Edit](https://arxiv.org/html/2606.20146v1): copilots and benchmarks, not shared experience.

## Next steps (owner decides)

1. Invite REVIT_MCP_study to collaborate; ask about contributing their lessons.
2. Evaluate cq compatibility: export packs as knowledge units.
3. Offer `arpl_search` to bridge authors (rvt-mcp, Horizun, Sam-AEC and others).
4. Watch Autodesk's Revit MCP server release.
5. Re-run this survey every few months; record new projects here.
