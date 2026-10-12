---
title: Generated output
description: Generated, shareable deliverables (HTML reports, PDFs, slide decks) rendered from markdown sources. Curated by pull request.
---
# Generated output

## Purpose

Shareable renderings of work that lives in markdown. This folder is never the place a fact is edited.

## What goes here

| Goes here | Does not go here (put it in) |
| --- | --- |
| HTML reports, PDFs and slide decks rendered from markdown sources | The source pages and the facts: [company](../company/README.md), [concept](../concept/README.md) or [memo](../memo/README.md) |
| | Large binaries, which bloat Git history |

## Layout and naming

A flat folder. Name files `<subject>-<kind>-<YYYY-MM-DD>.<ext>`, for example `platform-eval-summary-2026-10-06.html`. Keep each file self-contained and small.

## Frontmatter for this folder

HTML and PDF files carry none. Any markdown page in this folder follows [AGENTS.md](../AGENTS.md#frontmatter).

## Review and ownership

A change needs a pull request, a passing `validate-docs` check, and one approval from someone other than the author, including a code owner. Code owners are set in `.github/CODEOWNERS`. Today the owners of `*` cover every folder, so this folder has no stricter review. A draft pull request requests no code owners, so mark it ready for review.

## How to add an output

1. Update or confirm the source markdown page first.
2. Branch `<handle>/<topic>`.
3. Render the file here with the naming above.
4. Open a pull request, link the source page in the description, and mark it ready for review.

The commands are in [INSTRUCTIONS.md](../INSTRUCTIONS.md).

## Rules for this folder

Also in [AGENTS.md](../AGENTS.md):

- Every figure and claim traces to a line in a source markdown page.
- No new numbers. Keep the `[V]` and `[?]` markers and the draft framing.
- Fix the source and regenerate. Never edit only the output.
- Keep files self-contained and small.

## Related

[company](../company/README.md), [concept](../concept/README.md), [memo](../memo/README.md), [AGENTS.md](../AGENTS.md)
