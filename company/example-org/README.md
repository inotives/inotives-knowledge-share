---
title: Example org
description: "The pilot organisation's folder: the pilot roster and the knowledge-base test project. Curated by pull request."
---
# Example org

## Purpose

The stand-in organisation for the pilot. It holds the pilot roster and the project that tests this knowledge base. It holds dummy content only.

## What goes here

| Goes here | Does not go here (put it in) |
| --- | --- |
| Pages about the example organisation, in one subfolder per project | Reusable reference for everyone: [concept](../../concept/README.md) |
| The pilot roster, `pilot-roster.md` | Unsettled shared notes: [memo](../../memo/README.md) |
| | Material about another organisation: its own folder under [company](../README.md) |

## Layout and naming

`company/example-org/<project>/` for a project, and loose pages for organisation-wide records such as the roster. The one project today is [kb-test](./kb-test/README.md). Lowercase kebab-case.

## Frontmatter for this folder

The usual `type` is `reference` for the roster and `report` or `spec` for project pages. The full table is in [AGENTS.md](../../AGENTS.md#frontmatter).

## Review and ownership

A change needs a pull request, a passing `validate-docs` check, and one approval from someone other than the author, including a code owner. Code owners are set in `.github/CODEOWNERS`. Today the owners of `*` cover every folder, so this folder has no owner of its own. A draft pull request requests no code owners, so mark it ready for review.

## How to add a page

1. Draft in `_scratch/`.
2. Branch `<handle>/<topic>`.
3. Move the page here, or into a project subfolder, and fill the frontmatter.
4. Open a pull request and mark it ready for review.

A new project folder follows [Add a new folder](../../workflow/new-folder/workflow.md). The commands are in [INSTRUCTIONS.md](../../INSTRUCTIONS.md).

## Rules for this folder

- Dummy content only. Nothing here is real company or client material.

## Related

[company](../README.md), [kb-test](./kb-test/README.md), [AGENTS.md](../../AGENTS.md)
