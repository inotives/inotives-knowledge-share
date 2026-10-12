---
title: Memo
description: Shared notes, research and decisions that are not yet settled enough to live in concept/ or company/. Curated by pull request.
---
# Memo

## Purpose

Shared captures that need review but are not yet canonical. A memo is a staging place: once it is stable, it moves to its permanent home.

## What goes here

| Goes here | Does not go here (put it in) |
| --- | --- |
| Shared notes, research and decisions that are not yet settled | Personal drafts: `_scratch/` |
| Meeting notes, internal or external: [meetings](./meetings/README.md) | Notes of a client meeting, or notes that hold a client's material: `company/<name>/<project>/meetings/` |
| | Stable reference or glossary: [concept](../concept/README.md) |
| | Anything about one client or project: [company](../company/README.md) |

## Layout and naming

A flat folder, with one subfolder: [meetings](./meetings/README.md) for meeting notes, internal or external. Lowercase kebab-case, for example `onboarding-checklist.md`. Use a date prefix (`2026-10-06-slug.md`) only for a record tied to a time, such as a decision.

## Frontmatter for this folder

The usual `type` is `note`, `research` or `decision`, and a new page starts at `status: draft`. The full table is in [AGENTS.md](../AGENTS.md#frontmatter). This folder has a `note` template with the fields filled in.

## Review and ownership

A change needs a pull request, a passing `validate-docs` check, and one approval from someone other than the author, including a code owner. Code owners are set in `.github/CODEOWNERS`. Today the owners of `*` cover every folder, so this folder has no stricter review. A draft pull request requests no code owners, so mark it ready for review.

## How to add a page

1. Draft in `_scratch/`.
2. Branch `<handle>/<topic>`.
3. Move the page here and fill the frontmatter.
4. Open a pull request and mark it ready for review.

The commands are in [INSTRUCTIONS.md](../INSTRUCTIONS.md).

## Rules for this folder

- Promote, do not copy. When a memo is stable, move it to `concept/` or `company/<name>/<project>/` on a branch and update its `status`. Leave no copy behind.

## Related

[concept](../concept/README.md), [company](../company/README.md), [AGENTS.md](../AGENTS.md)
