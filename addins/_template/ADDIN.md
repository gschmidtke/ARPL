# <Add-in name> (<Vendor>)

| | |
|---|---|
| Vendor | <vendor, link to public site> |
| Add-in | <name as on the ribbon tab> |
| Assembly version observed | <from the ribbon inventory> |
| Revit versions observed | <e.g. 2024.3> |
| Public documentation | <link to help / manual, or "none"> |
| Help on F1 | <yes / no> |
| Last observed | <YYYY-MM-DD> |
| Learned by | <steps of LEARNING-PROTOCOL used, highest evidence level reached> |
| Contributors | <names> |

## What it is for

<One or two sentences, in the vendor's terms where possible (E1-docs).>

## Commands

Full inventory: [commands.json](commands.json). Commands used in ARPL work so far:

### <Command label> (`<panel>`)

- **Command id:** `<id>`
- **Reads:** <files, model data>
- **Writes:** <files and where; model changes>
- **Dialogs:** <in order, with their defaults>
- **Does not:** <what it explicitly does not do, and how that is known>
- **Evidence:** <E1/E2/E3/E4, version, date>

## Lessons

| # | Lesson | Workaround | Evidence | Failure pattern |
|---|---|---|---|---|
| 1 | <what surprised the agent> | <what worked instead> | <E3, version, date> | <FPnn or "new"> |

## Packs that use this add-in

- <ARPL-XXX-0000: title>
