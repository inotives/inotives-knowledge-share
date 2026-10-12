---
title: Add a new folder
description: "How to add a subfolder under memo, concept, company or generated_output: decide it is needed, create it with a README from the folder-readme template, link it from its parent, check and open a pull request."
type: playbook
status: draft
owner: inotives
created_at: 2026-10-12
created_by: inotives
ai_assisted: true
---
# Add a new folder

## Objective

A new subfolder under a curated folder (`memo/`, `concept/`, `company/`, `generated_output/`) always starts with a `README.md` built from the same template, so every folder says what it is for, what goes in it and how it is reviewed. This is a workflow because it is a sequence with decisions. It invokes no skills.

## The rule

- **Every folder under a curated folder has a `README.md`, always.** The README is how a folder explains what it is for and what its rules and conventions are, so it is never optional. The docs check fails a folder without one.
- **Create it from the `folder-readme` template.** It has the eight sections the folder READMEs use: purpose, what goes here, layout and naming, frontmatter, review and ownership, how to add, rules, related.
- **Exemptions.** The inside of a skill (`skill/<name>/`) is described by its `SKILL.md`, and the inside of a workflow (`workflow/<name>/`) by its `workflow.md`. Neither needs a README, and both files are required: the docs check fails a skill folder without a `SKILL.md` and a workflow folder without a `workflow.md`. The exemption is by position, so a `SKILL.md` or `workflow.md` placed anywhere else does not excuse a folder.
- **A new top-level folder is not covered here.** It changes the contract's folder list, so it needs the owner's decision first. The docs check fails on an unknown top-level folder, and the owner adds the new one to the list in `.github/scripts/check_docs.py`.

## When a new folder is warranted

Create a folder when one of these is true. Otherwise keep the pages where they are and use tags or a filename prefix.

1. There are more than a handful of pages on one subject (the same threshold `concept/` uses).
2. The pages share a different audience, owner or review need from their neighbours.
3. The pages are about one client or project, which the contract says stay together in `company/<name>/<project>/`.

Do not create a folder for a single page, and do not create one to hold an index. Folder names are lowercase kebab-case.

## Steps

1. **Decide.** Check the list above. If none applies, stop and add the page to the existing folder.
2. **Look for an existing home.** Search the parent folder and its README. A page about the same subject may already have a folder.
3. **Branch.** `git switch -c <handle>/<topic>`. Restart the OpenKnowledge server after the switch.
4. **Create the README from the template.** Write `<parent>/<new-folder>/README` with the OpenKnowledge `write` tool and `template: "folder-readme"`. The template is available in every folder.
5. **Fill in all eight sections.** Replace every `<placeholder>`. Say plainly what review the folder gets: today the owners of `*` cover every folder unless `.github/CODEOWNERS` names an owner for the path.
6. **Link it from the parent.** Add the new folder to the parent README's "Layout and naming" or "What goes here" section, so it can be found. Do not keep a hand-written list of the pages inside it.
7. **Add the first page,** or promote one from `_scratch/` (see [INSTRUCTIONS.md](../../INSTRUCTIONS.md)).
8. **Check.** Run `python3 -I .github/scripts/check_docs.py` and the OpenKnowledge `audit`. Both must report no problems.
9. **Open the pull request** and mark it ready for review. A draft requests no code owners.

## Hand-offs

- The reviewer is a code owner other than the author. They read the README first, because it sets the rules for everything that is added later.
- If the folder needs its own approver, say so in the pull request. A path rule in `.github/CODEOWNERS` is a separate change and a separate decision.

## Related

[workflow](../README.md), [AGENTS.md](../../AGENTS.md#folders), [INSTRUCTIONS.md](../../INSTRUCTIONS.md)
