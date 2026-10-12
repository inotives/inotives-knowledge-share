---
title: Workflow
description: Orchestrated sequences of decisions and actions that achieve a broader, end-to-end objective, and usually invoke several skills. Curated by pull request.
---
# Workflow

## Purpose

A workflow is an **orchestrated sequence of decisions and actions that defines how to achieve a broader, end-to-end objective**, for example turning an evaluation into a shareable report. It tends to invoke several [skills](../skill/README.md) as it runs.

## What goes here

| Goes here | Does not go here (put it in) |
| --- | --- |
| An ordered procedure with decisions and hand-offs, and the skills it invokes | An atomic capability that defines how to perform one specific task: [skill](../skill/README.md) |
| | Background knowledge: [concept](../concept/README.md) |

## Layout and naming

```text
workflow/<workflow-name>/
  workflow.md     # the objective, the ordered decisions and actions, the hand-offs, and the skills it invokes
  resources/      # optional
```

Lowercase kebab-case folder names.

## Frontmatter for this folder

The usual `type` is `playbook` or `runbook`. A new page starts at `status: draft`. The full table is in [AGENTS.md](../AGENTS.md#frontmatter).

## Review and ownership

A change needs a pull request, a passing `validate-docs` check, and one approval from someone other than the author, including a code owner. Code owners are set in `.github/CODEOWNERS`. Today the owners of `*` cover every folder, and there is no `/workflow/` rule, so a workflow change has no stricter review. A path rule would give workflows their own owner (see the [P2-3 report](../company/example-org/kb-test/results/2026-10-12-p2-3-skill-path-rule.md) for how a path rule behaves). A draft pull request requests no code owners, so mark it ready for review.

## How to add a workflow

1. Draft in `_scratch/<handle>/`.
2. Branch `<handle>/<topic>`.
3. Create `workflow/<workflow-name>/workflow.md` and fill the frontmatter.
4. Open a pull request and mark it ready for review.

The commands are in [INSTRUCTIONS.md](../INSTRUCTIONS.md).

## Rules for this folder

- Name the skills a workflow invokes, and link to them.
- If a step is a single atomic capability, make it a skill and call it from the workflow.

## Related

[skill](../skill/README.md), [concept](../concept/README.md), [AGENTS.md](../AGENTS.md)
