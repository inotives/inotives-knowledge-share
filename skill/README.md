---
title: Skill
description: "Custom agent skills: atomic capabilities that define how to perform one specific task. Each skill is a folder with a SKILL.md. Curated by pull request with the closest review, because skills execute."
---
# Skill

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

## Available skills

| Skill | Use it for |
| --- | --- |
| [interactive-pitch-deck](./interactive-pitch-deck/SKILL.md) | Building a self-contained, interactive reveal.js pitch deck from a story outline |

## Layout

```text
skill/<skill-name>/
  SKILL.md        # required; frontmatter has name and description
  scripts/        # optional
  references/     # optional
```

- The folder name equals the `name` in the frontmatter: lowercase letters, digits and hyphens.
- `description` says **when to use** the skill. It is what an agent reads to decide whether to load it, so write it for that.
- Keep `SKILL.md` short. Put depth in `references/`.

## Rules

- A new skill or a change to one goes through pull request. A code owner approves, because a skill can run commands.
- No credentials in a skill. Point to where a secret lives.
- Author skills through OpenKnowledge, not by hand-editing copies in `.claude/skills/`, which are generated and gitignored.
