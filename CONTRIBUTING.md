# Contributing to ARPL

Thank you. Every protocol, even a failed attempt, makes the next agent better.

## What we want

- A production task you ran with an AI agent in Revit (any tool: MCP bridge, pyRevit, Dynamo, custom add-in).
- What you asked, what came out, what was wrong, how you noticed, and what finally worked.
- Professional rules from your discipline that an agent needs to know (a domain overlay).
- Failure patterns you keep seeing.

## How to submit: one inbox

There is exactly one way in: **the `inbox/` folder**. Everything else in the repository is read-only for contributors and is maintained by the curator.

1. Open [Upload to inbox](https://github.com/gschmidtke/ARPL/upload/main/inbox) (you need a free GitHub account).
2. Name the path `inbox/<your-github-name>/` and drop your files: a JSON from [the template](templates/submission.template.json), Markdown, a plain-text log or a zip. Any format is fine.
3. Click "Propose changes". GitHub forks the repository and opens the pull request for you.

Git users can fork and open a pull request the normal way, as long as it only touches `inbox/`. Pull requests that change anything outside `inbox/` fail the automatic "Inbox only" check and are closed. Issues are for questions only, not for submissions.

## Rules

- Only share what you have the right to share. No client names, addresses, project numbers, model files (`.rvt`, `.rfa`), passwords, API keys or licensed content (standards text, manufacturer data behind a login).
- By submitting, you agree to publish under CC BY 4.0 (content) and MIT (code).
- Scripts are welcome as excerpts. They are never executed by the curator without review.

## What happens next

The curator reviews the submission (see [CURATION.md](CURATION.md)), then either files it as a new pack, merges it into an existing pack (as a new iteration or a "reproduced" confirmation), or asks you questions in the PR. Every outcome is written in the [ledger](ledger/intake-ledger.json), and you are credited in [CONTRIBUTORS.md](CONTRIBUTORS.md) with the pack ids your work went into.
