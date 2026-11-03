# Add-ins: what agents have learned about Revit add-ins

Revit work rarely runs on Revit alone. Firms install add-ins, many of them custom or commercial, most without a public API. An agent driving Revit through a bridge meets these add-ins with no documentation in its training and nothing in the Revit API to tell it what they do.

This folder holds what agents and their users have learned about individual add-ins, so the next agent does not have to learn the same add-in from zero. It also holds the method for learning an add-in nobody has documented yet.

## How to use this folder

1. **Your task involves an add-in command** (a ribbon tab you don't recognise, a user saying "use ZEN", "use the X tool"): look for `addins/<vendor>-<addin>/ADDIN.md` first.
2. **It exists:** read the add-in card, then the commands and lessons. Check the version and date it was observed against what is installed; the add-in may have changed since.
3. **It does not exist, or it is out of date:** follow [LEARNING-PROTOCOL.md](LEARNING-PROTOCOL.md). Then offer the user to contribute what you learned through the inbox or STAR-T-GATE (see [CONTRIBUTING.md](../CONTRIBUTING.md)).

## Layout

| Path | Content |
|---|---|
| `LEARNING-PROTOCOL.md` | The method: how an agent learns an unknown add-in, step by step, read-only first |
| `_tools/ribbon_inventory.cs` | Read-only script: lists an add-in's ribbon commands, command ids and tooltips |
| `_template/ADDIN.md` | Template for a new add-in card |
| `<vendor>-<addin>/ADDIN.md` | Add-in card: identity, versions, how it was learned, commands, lessons, links to packs |
| `<vendor>-<addin>/commands.json` | Ribbon inventory as observed (command ids, tooltips, panel), with version and date |

## Evidence levels

Every statement about an add-in carries how it is known. A lesson is only as strong as its evidence.

| Level | Source | What it can support |
|---|---|---|
| `E1-docs` | The vendor's public help, manual or tooltip | What the vendor says the command does |
| `E2-inventory` | Ribbon inventory from the running Revit | That a command exists, its id, panel and label |
| `E3-observed` | A run on a test or copied model: dialogs, files written, model state read before and after | What the command actually did in that version |
| `E4-reproduced` | E3 repeated by another user, version or project | That the behaviour holds beyond one session |
| `V-vendor-verified` | The add-in's developer checked the statement against the add-in's source | Exact behaviour, including edge cases a single run would not show (what Cancel does, matching rules, limits) |

Statements a vendor or owner makes in conversation count as `E1-docs` once they are written down by them; until then they are hearsay and are not filed.

`V-vendor-verified` is only available where the developer takes part, as for ZEN (Tiverit LLC). The card states the verified behaviour and never the code behind it. A `V` statement names the add-in version or source release it was checked against, and is still compared with one observed run (`E3`) before a command is marked complete.

## What never goes in here

The rules in [CONTRIBUTING.md](../CONTRIBUTING.md) and the source wall in [CURATION.md](../CURATION.md) apply in full, plus:

- **No add-in source code and no decompiled code**, even when the contributor owns the add-in. An add-in card describes behaviour anyone can observe. If a lesson can only be stated by quoting the code, it does not belong in ARPL.
- **No licence keys, credentials, installer files or DLLs.**
- **No circumvention:** nothing about bypassing an add-in's licensing, trial limits or protection.
- Vendor documentation is linked, not copied. Quote a tooltip or a single short line when the exact wording matters; otherwise paraphrase and link.

## Relation to GPS

GPS locates a capability in the Revit API of the installed version (see [AGENTS.md](../AGENTS.md), section 2). An add-in has no such map. The ribbon inventory and the add-in card are its equivalent: they locate what the add-in can do in the installed version. As with GPS, locating a command does not make its result correct; the result is checked against the model.
