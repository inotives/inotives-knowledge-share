---
title: Test results
description: Dated reports of each knowledge-base test run, one file per run, never edited after the fact. Curated by pull request.
---
# Test results

## Purpose

The evidence for every status in the [test plan](../test-plan.md). One report per run, written when the run is done.

## What goes here

| Goes here | Does not go here (put it in) |
| --- | --- |
| A dated report of a run, with the steps, the observations and the limits | The cases and their status: the [test plan](../test-plan.md) |
| A summary report that supersedes the open items of earlier reports | The commands for a case: the [test steps](../test-steps.md) |

## Layout and naming

`<YYYY-MM-DD>-<slug>.md`, for example `2026-10-12-x1-scratch-search.md`. A flat folder. Keep no hand-written index; use OpenKnowledge's folder view or search.

## Frontmatter for this folder

`type: report`, `status: draft`, and `ai_assisted: true` when an agent wrote most of it. Use `derived_from` when a report summarises others. The full table is in [AGENTS.md](../../../AGENTS.md#frontmatter).

## Review and ownership

A change needs a pull request, a passing `validate-docs` check, and one approval from someone other than the author, including a code owner. Code owners are set in `.github/CODEOWNERS`. Today the owners of `*` cover every folder, so this folder has no owner of its own. A draft pull request requests no code owners, so mark it ready for review.

## How to add a report

1. Run the case and keep the exact output or commit hash.
2. Write a new dated file here with `type: report`.
3. Update the case's status in the [test plan](../test-plan.md) in the same pull request, and link the report.

## Rules for this folder

- **Never edit an earlier report after the fact.** When something changes, write a new report or a summary that supersedes it.
- Record people and accounts by handle. No secrets and no personal local paths; write `~/` instead.

## Related

[test-knowledge-share](../README.md), [test plan](../test-plan.md), [AGENTS.md](../../../AGENTS.md)
