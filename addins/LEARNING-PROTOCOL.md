# Learning an unknown Revit add-in

For an agent working in Revit through a bridge (with screen access for dialogs) that has to use an add-in it does not know, and that has no public API. Decided by the owner on 2026-11-03.

The steps go from cheapest and safest to most expensive. Stop as soon as you know enough for the task. Steps 1 to 3 change nothing; step 4 changes files or the model and needs the user.

## 0. Ask first

Ask the user before learning by trial:

- Is there a manual, help page or training material? Many add-ins open their help on **F1** while the pointer rests on a ribbon command.
- Has anyone in the firm used this command before, and what did they expect it to do?
- Is there an add-in card in `addins/` already? Check it before anything else.

The user's own description of what the command should produce is the test you will check the result against.

## 1. Read the vendor's documentation (`E1-docs`)

Read the help for the commands the task needs, and nothing else. Note per command: what it reads, what it writes, where (fixed folder or user choice), and what it says it does not do.

Treat documentation as the vendor's claim, not as proof. Today's help can describe a newer or older version than the one installed.

## 2. Take the ribbon inventory (`E2-inventory`)

Run [`_tools/ribbon_inventory.cs`](_tools/ribbon_inventory.cs) with the bridge, no transaction, after showing it to the user. It lists every command on the add-in's tab: panel, label, command id, control type and tooltip, plus the add-in's loaded assembly name and version.

This tells you three things the documentation may not:

- which commands exist **in this installation** (split buttons hide most of them);
- the **command id**, which a bridge can post with `UIApplication.PostCommand(RevitCommandId.LookupCommandId(id))` when clicking is unreliable;
- the **tooltip**, which is often the most precise one-line statement of what a command does.

Do not inspect the add-in's assemblies beyond their name and version. Reflection over types, decompiling or reading resources is out of scope for ARPL, whoever owns the add-in.

## 3. Read the model and the files before you run anything

Record the state the command will change, with a read-only script: the elements, settings or sets involved, their counts and names; and the folder the command writes into. This is the "before" half of every lesson.

## 4. Run once, on purpose, and watch (`E3-observed`)

With the user's consent:

1. Prefer a copy, a test model or a scratch folder. If it must run on the real model, say so and make sure the change can be undone or is wanted anyway.
2. Start the command (ribbon click or posted command id). Take a screenshot after every step: add-ins open their own dialogs, and a dialog the agent does not see blocks Revit (FP15).
3. Read each dialog fully before answering it. Note its title, the question, and the default it offers (folders often start at Desktop or at the last folder used).
4. Never send a bridge command while the add-in is running; wait for its completion window.
5. Read the result: the completion window, the files it wrote (name, size, sheets or columns), and the model state with the same read-only script as step 3. The difference is what the command did.

Run it once. If the result is wrong, stop and tell the user before trying a variation.

## 5. Write it down

Create or update `addins/<vendor>-<addin>/ADDIN.md` from [`_template/ADDIN.md`](_template/ADDIN.md):

- identity: vendor, add-in name, assembly version, Revit version, date observed;
- how it was learned (which steps, which evidence level);
- per command used: what it reads, what it writes, dialogs and their defaults, what it does not do;
- lessons: anything that surprised you, and the workaround;
- failure patterns met, by id (`patterns/failure-patterns.json`), or a new one proposed.

A complete production sequence that uses the add-in (for example a weekly print run) becomes a normal pack in `library/` that names the add-in in `use_when`; the add-in card links to it.

Submit through the inbox or STAR-T-GATE like any other contribution. The curator files it.

## What the agent may and may not conclude

- "The command does not exist" needs the ribbon inventory, not a search of the documentation.
- "The command does not do X" needs a run (step 4) or an explicit statement in the vendor's documentation. Name which one.
- "The command did X" holds for the version observed. Say which version.
- A missing capability is reported to the user as it is, with the nearest working route, and, where the vendor accepts them, as a feature request. Do not imitate a missing command with a script and present the result as the add-in's.
