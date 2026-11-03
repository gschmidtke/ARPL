# Contributing to ARPL

Thank you. Every protocol, even a failed attempt, makes the next agent better.

## What we want

- A production task you ran with an AI agent in Revit (any tool: MCP bridge, pyRevit, Dynamo, custom add-in).
- What you asked, what came out, what was wrong, how you noticed, and what finally worked.
- Professional rules from your discipline that an agent needs to know (a domain overlay).
- Failure patterns you keep seeing.

## How to submit: two ways in

Everything in the repository is read-only for contributors and is maintained by the curator. There are two ways in.

### STAR-T-GATE: comments, observations and findings (anyone)

[STAR-T-GATE](https://www.tiveritllc.com/star-t-gate.html) is the official place to comment on all TIVERIT open-source repositories (ARPL, [TIVERIT BIM Standards](https://github.com/gschmidtke/TIVERIT-BIM-STANDARDS) and [USG](https://github.com/gschmidtke/USG)). Anyone can use it; no GitHub account is needed. Pick the target (ARPL, or "Unknown" to let the curators route it), the type (observation, gap, failure, contradiction, evidence, proposal, question) and describe what you saw. Every submission lands in the curators' queue as uncurated evidence; the ARPL curator reviews the ARPL items.

AI agents use the machine entry point at [https://star-t-gate-inbox-worker.white-bar-0318.workers.dev/](https://star-t-gate-inbox-worker.white-bar-0318.workers.dev/) (manifest, schema and intake), and only with their user's permission.

### The `inbox/` folder: files and complete protocols

Use this when you have files to hand over (a filled template, logs, a zip).

1. Open [Upload to inbox](https://github.com/gschmidtke/ARPL/upload/main/inbox) (you need a free GitHub account).
2. Name the path `inbox/<your-github-name>/` and drop your files: a JSON from [the template](templates/submission.template.json), Markdown, a plain-text log or a zip. Any format is fine.
3. Click "Propose changes". GitHub forks the repository and opens the pull request for you.

**Quick path:** a few lines in a text or Markdown file are enough: *I tried X, got Y, it was wrong because Z, I noticed it by W, and this worked instead.* The curator does the rest. If you want to see what a complete submission looks like, there is a [filled example](templates/example-submission.json).

**Reproductions count.** Tried an existing pack and it worked (or didn't) in your Revit version? That is one of the most valuable contributions; see [help wanted](catalogs/help-wanted.md).

Git users can fork and open a pull request the normal way, as long as it only touches `inbox/`. Pull requests that change anything outside `inbox/` fail the automatic "Inbox only" check and are closed. Issues on this repository are for questions only; send comments and findings through STAR-T-GATE.

## Rules

- Only share what you have the right to share. No client names, addresses, project numbers, model files (`.rvt`, `.rfa`), passwords, API keys or licensed content (standards text, manufacturer data behind a login). Refer to a standard by number, part, edition and clause (for example "ISO 19650-2:2018, 5.1.4") instead of pasting its text, and do not link to private or internal locations.
- By submitting, you agree to publish under CC BY 4.0 (content) and MIT (code).
- Scripts are welcome as excerpts. They are never executed by the curator without review.

## What happens next

The curator reviews the submission (see [CURATION.md](CURATION.md)), then either files it as a new pack, merges it into an existing pack (as a new iteration or a "reproduced" confirmation), or asks you questions in the PR. Every outcome is written in the [ledger](ledger/intake-ledger.json), and you are credited in [CONTRIBUTORS.md](CONTRIBUTORS.md) with the pack ids your work went into.
