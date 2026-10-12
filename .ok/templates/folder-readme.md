---
template:
  title: Folder README
  description: "The README every folder must have: purpose, what goes here, layout
    and naming, frontmatter, review and ownership, how to add, rules and related
    links."
  tags:
    - template
title: "<Folder name>"
description: "<What the folder holds, in one sentence>. Curated by pull request."
---

# <Folder name>

## Purpose

<One or two sentences: what this folder is for.>

## What goes here

| Goes here | Does not go here (put it in) |
| --- | --- |
| <Kind of page> | <Other kind of page>: <relative markdown link to that folder's README> |

## Layout and naming

<Path pattern, filename pattern and one example. Keep no hand-written index of the pages; use OpenKnowledge's folder view or search.>

## Frontmatter for this folder

<The usual `type` and the starting `status`. Add a relative markdown link to AGENTS.md#frontmatter, with the right number of `../` for this folder's depth, and do not copy its table.>

## Review and ownership

A change needs a pull request, a passing `validate-docs` check, and one approval from someone other than the author, including a code owner. Code owners are set in `.github/CODEOWNERS`. <Say here whether this folder has an owner of its own or only the owners of `*`.> A draft pull request requests no code owners, so mark it ready for review.

## How to add a page

1. Draft in `_scratch/`.
2. Branch `<handle>/<topic>`.
3. Move the page here and fill the frontmatter.
4. Open a pull request and mark it ready for review.

The commands are in <relative markdown link to INSTRUCTIONS.md>.

## Rules for this folder

- <Only rules that are specific to this folder.>

## Related

<Relative markdown links to neighbouring folders and to AGENTS.md.>
