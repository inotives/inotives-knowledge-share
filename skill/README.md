---
title: Skill
description: "Custom agent skills: atomic capabilities that define how to perform one specific task. Each skill is a folder with a SKILL.md. Curated by pull request, and reviewed closely because skills execute."
---
# Skill

## Purpose

A skill is an **atomic capability that defines how to perform a specific task**: convert a table to a chart, check a frontmatter block, summarise a PDF. It does one thing and does not decide what happens next.

A [workflow](../workflow/README.md) is an **orchestrated sequence of decisions and actions that defines how to achieve a broader, end-to-end objective**. A workflow tends to invoke several skills while it runs.

| | Skill | Workflow |
| --- | --- | --- |
| Defines | How to perform one specific task | How to achieve an end-to-end objective |
| Scope | Atomic, single purpose | Broader, orchestrated |
| Contains | Instructions for one capability, plus its scripts | Ordered decisions and actions, hand-offs, and the skills it invokes |
| Relationship | Called by workflows, or directly by an agent | Usually invokes multiple skills |
| Example | Render a markdown table as an HTML chart | Turn an evaluation into a shareable HTML report |

If a skill starts to need decisions or a sequence of steps, split it: keep the atomic capability here and move the orchestration to `workflow/`.

## What goes here

| Goes here | Does not go here (put it in) |
| --- | --- |
| One atomic capability, with its scripts and references | A sequence of steps or decisions: [workflow](../workflow/README.md) |
| | Background knowledge: [concept](../concept/README.md) |
| | Generated copies in `.claude/skills/`, which are gitignored |

## Layout and naming

```text
skill/<skill-name>/
  SKILL.md        # required; frontmatter has name and description
  scripts/        # optional
  references/     # optional
```

- The folder name equals the `name` in the frontmatter: lowercase letters, digits and hyphens.
- `description` says **when to use** the skill. It is what an agent reads to decide whether to load it, so write it for that.
- Keep `SKILL.md` short. Put depth in `references/`.
- **A skill folder has no README of its own.** Every other folder needs one, because a README is how a folder says what it is for and what its rules are. For a skill, `SKILL.md` does exactly that, so a second file would only repeat it and drift out of date. The docs check therefore fails a skill folder without a `SKILL.md`, and skips the README rule for `skill/<name>/` and everything inside it, including `scripts/`, `references/` and `assets/`. This page is the README for the `skill/` folder itself.

To list the skills, use OpenKnowledge's folder view or search. This page keeps no hand-written index, because every new skill would edit it and two people adding skills at once would conflict.

## Frontmatter for this folder

A skill's `SKILL.md` uses `type: skill` and the fields in [AGENTS.md](../AGENTS.md#frontmatter), plus `name` and `description`. A new page starts at `status: draft`.

## Review and ownership

A change needs a pull request, a passing `validate-docs` check, and one approval from someone other than the author, including a code owner. The contract asks for the closest review here because a skill can run commands. **GitHub does not enforce more today.** There is no `/skill/` rule in `.github/CODEOWNERS`, so any owner of `*` can approve a skill change. A `/skill/` rule naming one or two owners would make only their approval count (see the [P2-3 report](../company/example-org/kb-test/results/2026-10-12-p2-3-skill-path-rule.md)). This is not decided. A draft pull request requests no code owners, so mark it ready for review.

## How to add a skill

1. Draft in `_scratch/`.
2. Branch `<handle>/<topic>`.
3. Create `skill/<skill-name>/SKILL.md` and fill the frontmatter.
4. Open a pull request and mark it ready for review.

The commands are in [INSTRUCTIONS.md](../INSTRUCTIONS.md). Author skills through OpenKnowledge, not by hand-editing copies in `.claude/skills/`.

## Rules for this folder

- No credentials in a skill. Point to where a secret lives.
- A skill that needs decisions or ordered steps is a workflow.

## Related

[workflow](../workflow/README.md), [concept](../concept/README.md), [AGENTS.md](../AGENTS.md)
