---
title: Knowledge base test
description: "The project that tests this knowledge base workflow: the test plan, the commands for each case, and a dated report per run. Curated by pull request."
---
# Knowledge base test

## Purpose

The project that tests whether the rules in the contract hold: the branch protection, code owners, the hook and CI, two contributors, and OpenKnowledge itself. Start with the [test plan](./test-plan.md).

## What goes here

| Goes here | Does not go here (put it in) |
| --- | --- |
| The [test plan](./test-plan.md): every case, its steps, expected result and status | A fact the team should rely on: [concept](../../../concept/README.md) |
| The [test steps](./test-steps.md): the exact commands to run a case | A decision: its own `decision` page |
| Dated reports of each run, in [results](./results/README.md) | |

## Layout and naming

```text
company/example-org/kb-test/
  test-plan.md     # the cases and their status
  test-steps.md    # the commands for each case
  results/         # one dated report per run
```

## Frontmatter for this folder

The plan and the steps use `type: spec`. Reports use `type: report`. The full table is in [AGENTS.md](../../../AGENTS.md#frontmatter).

## Review and ownership

A change needs a pull request, a passing `validate-docs` check, and one approval from someone other than the author, including a code owner. Code owners are set in `.github/CODEOWNERS`. Today the owners of `*` cover every folder, so this folder has no owner of its own. A draft pull request requests no code owners, so mark it ready for review.

## How to add a result

1. Run the case and keep the exact output or commit hash as evidence.
2. Add a new dated report in [results](./results/README.md). Never append to an earlier report.
3. Update the case's status in the test plan in the same pull request, and link the report.

## Rules for this folder

- A case changes status in the plan only when a report supports it.
- Mark a claim `[V]` only when it was observed first-hand, and `[?]` when it was not.

## Related

[example-org](../README.md), [results](./results/README.md), [AGENTS.md](../../../AGENTS.md)
