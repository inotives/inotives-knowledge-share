---
title: Concept
description: Glossary, terminology and distilled technical knowledge. Curated by pull request.
---
# Concept

## Purpose

One canonical page per subject: glossary entries, terminology and distilled technical reference. Link to a concept page instead of copying it.

## What goes here

| Goes here | Does not go here (put it in) |
| --- | --- |
| Glossary, terminology, technical reference, distilled knowledge | Unsettled notes: [memo](../memo/README.md) |
| | Work about one client or project: [company](../company/README.md) |
| | Agent capabilities: [skill](../skill/README.md) |

## Layout and naming

One page per subject, lowercase kebab-case. Group related pages in a subfolder (for example `data/`) once there are more than a handful.

## Frontmatter for this folder

The usual `type` is `glossary` or `reference`. The full table is in [AGENTS.md](../AGENTS.md#frontmatter).

## Review and ownership

A change needs a pull request, a passing `validate-docs` check, and one approval from someone other than the author, including a code owner. Code owners are set in `.github/CODEOWNERS`. Today the owners of `*` cover every folder, so this folder has no stricter review. A draft pull request requests no code owners, so mark it ready for review.

## How to add a page

1. Draft in `_scratch/`, or promote a stable page from `memo/`.
2. Branch `<handle>/<topic>`.
3. Move the page here and fill the frontmatter.
4. Open a pull request and mark it ready for review.

The commands are in [INSTRUCTIONS.md](../INSTRUCTIONS.md).

## Rules for this folder

- One canonical page per subject. Before adding, search for an existing page and extend it.
- Link to a concept page rather than restating it. When restating is unavoidable, record `derived_from`.

## Related

[memo](../memo/README.md), [company](../company/README.md), [AGENTS.md](../AGENTS.md)
