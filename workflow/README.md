---
title: Workflow
description: Orchestrated sequences of decisions and actions that achieve a broader, end-to-end objective, and usually invoke several skills. Curated by pull request.
---
# Workflow

A workflow is an **orchestrated sequence of decisions and actions that defines how to achieve a broader, end-to-end objective**, for example turning an evaluation into a shareable report. It tends to invoke multiple [skills](../skill/README.md) as it runs.

An atomic capability that defines how to perform one specific task is a skill, not a workflow. Put it in `skill/`.

Each workflow is a folder containing `workflow.md` (the objective, the ordered decisions and actions, the hand-offs, and which skills it invokes) plus any `resources/`. A change to a workflow needs approval from its code owner before merge.
