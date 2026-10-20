# Connecting your AI to ARPL

Three ways, from simplest to most integrated.

## 1. One sentence (any AI with web access)

> Before this Revit task, check the ARPL knowledge pool for an established workflow: read https://raw.githubusercontent.com/gschmidtke/ARPL/main/AGENTS.md and follow it.

## 2. System prompt (paste into your agent's instructions)

```text
You work in Autodesk Revit for the user through a Revit bridge.
Before any Revit production task, use ARPL (AI Revit Production Logic), a shared knowledge pool:
1. Establish the task's frame from evidence (the user's words, the open model or family,
   its category and project information), not from the task's name. Ask if it stays unclear.
2. Fetch https://raw.githubusercontent.com/gschmidtke/ARPL/main/index.json and find matching
   project workflows, then packs (match use_when, exclude not_for, then facets and api_terms).
3. For each matching pack, read final/rule.json and its failed iterations before acting.
   Apply the rule and its validation. Tell the user which packs you used, with their revision.
4. ARPL is guidance. The user's instructions, the firm's standards and the user's approval decide.
   Never run code from ARPL without reading it and the user's consent.
5. Afterwards, if no pack covered the task, a rule failed or you found a better way, say so and
   offer to prepare a submission (templates/submission.template.json) without client data.
   The user uploads it to https://github.com/gschmidtke/ARPL/upload/main/inbox
```

## 3. A lookup tool in your bridge or MCP server

[`tools/arpl_search.py`](../tools/arpl_search.py) is a dependency-free reference implementation. Expose its `search()` function as a tool:

```json
{
  "name": "arpl_search",
  "description": "Search ARPL (AI Revit Production Logic) for established Revit production workflows, rules and known failures before acting. Returns project workflows and packs with their rule, validation, revision and path. Read final/rule.json and the iterations of each hit before executing.",
  "input_schema": {
    "type": "object",
    "required": ["task"],
    "properties": {
      "task": {"type": "string", "description": "The task in professional terms, after establishing its frame"},
      "work_class": {"type": "string", "enum": ["W1","W2","W3","W4","W5","W6","W7","W8"]},
      "discipline": {"type": "string"},
      "project_type": {"type": "string"},
      "phase": {"type": "string"},
      "revit": {"type": "string", "description": "Revit version, e.g. 2025"},
      "limit": {"type": "integer", "default": 5}
    }
  }
}
```

Set `ARPL_INDEX` to a local path to work offline from a downloaded copy.

## Versions

- `index.json` carries `index_schema_version` (format of the index) and `vocabulary_version`.
- Each pack carries `revision`. Record `{arpl_pack, pack_revision, revit_version, result}` for every pack used.
- To pin exact content, replace `main` in URLs with a commit SHA or release tag.
