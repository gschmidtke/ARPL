# Contributing to ARPL

Thank you. Every protocol, even a failed attempt, makes the next agent better.

## What we want

- A production task you ran with an AI agent in Revit (any tool: MCP bridge, pyRevit, Dynamo, custom add-in).
- What you asked, what came out, what was wrong, how you noticed, and what finally worked.
- Professional rules from your discipline that an agent needs to know (a domain overlay).
- Failure patterns you keep seeing.

## How to submit

**Option A, pull request (preferred):**
1. Fork the repository.
2. Copy [templates/submission.template.json](templates/submission.template.json) to `inbox/<your-github-name>/<short-title>.json` and fill in what you know. Markdown, plain-text logs or a zipped protocol in the same folder are fine too.
3. Open a pull request. Don't edit `library/`, `catalogs/` or `ledger/`: the curator does that.

**Option B, issue:** open an issue with the "Contribution" label and paste or attach your protocol.

## Rules

- Only share what you have the right to share. No client names, addresses, project numbers, model files (`.rvt`, `.rfa`), passwords, API keys or licensed content (standards text, manufacturer data behind a login).
- By submitting, you agree to publish under CC BY 4.0 (content) and MIT (code).
- Scripts are welcome as excerpts. They are never executed by the curator without review.

## What happens next

The curator reviews the submission (see [CURATION.md](CURATION.md)), then either files it as a new pack, merges it into an existing pack (as a new iteration or a "reproduced" confirmation), or asks you questions in the PR. Every outcome is written in the [ledger](ledger/intake-ledger.json), and you are credited in [CONTRIBUTORS.md](CONTRIBUTORS.md) with the pack ids your work went into.
