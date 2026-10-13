---
title: Scratch
description: "Your personal, local working space for drafts and rough notes, arranged however you like. Nothing here is shared, reviewed, scanned or backed up."
---
# Scratch

## Purpose

Your own working space for drafts and rough notes, and a place for your agent to draft. It is local to your machine. Anything worth keeping is promoted into a curated folder by pull request.

## What goes here

| Goes here | Does not go here (put it in) |
| --- | --- |
| Rough notes, drafts and agent drafts that are not ready to share | A page others should rely on: promote it into a curated folder, see [Where does this go?](../AGENTS.md#where-does-this-go) |
| Throwaway experiments and test pages | A password, token or key, or personal data about an individual: nowhere in this repository, and nothing here is scanned for them |
| | Anything you need to keep safe: scratch is not backed up |

## Layout and naming

Arrange it however you like: flat, or a subfolder per topic. There are no naming rules, and you do not need a folder of your own, because `_scratch/` is local to your clone and each clone belongs to one person. OpenKnowledge may add a `.gitkeep` file to a new folder, and Git ignores it.

## Frontmatter for this folder

Give every note a **`title` and a `description`**. That is the same minimum a folder README carries, and the contract says OpenKnowledge requires it. Nothing else is needed while drafting. This is a convention: the docs check skips this folder, so nothing enforces it, and a rough note never blocks a commit. When you promote a note, add the rest of the fields in [AGENTS.md](../AGENTS.md#frontmatter); the docs check then names any that are missing.

## Review and ownership

Nothing here is reviewed and nobody owns it but you. Only a promoted page goes through a pull request, a passing `validate-docs` check and an approval from a code owner other than its author. On a clone you share with someone else, leave notes you did not write alone.

## How to use it

1. Draft here, with your agent if you like. OpenKnowledge search finds scratch notes.
2. When a note should last, move it into a curated folder with the OpenKnowledge `move` tool on a branch. Do not copy it and leave the original.
3. Fill in the frontmatter, then open a pull request and mark it ready for review.
4. Delete drafts you no longer need.

The commands are in [INSTRUCTIONS.md](../INSTRUCTIONS.md). A run of the whole path is in the [rehearsal report](../memo/test-knowledge-share/results/2026-10-12-rehearsal-scratch-to-merged.md).

## Rules for this folder

- **It is local only.** Nothing here is committed or backed up. Deleting your clone deletes it.
- **Nothing here is scanned for secrets.** The pre-commit hook and CI read staged and committed files only, and scratch is never staged. Keep secrets out anyway.
- **Scratch is indexed.** OpenKnowledge reads it for search. Keep semantic search off, because it would send scratch text to an outside provider. See the [X-1 report](../memo/test-knowledge-share/results/2026-10-12-x1-scratch-search.md).
- **Promote or delete.** Scratch is not a shared place and not an archive.

## Related

[memo](../memo/README.md), [AGENTS.md](../AGENTS.md), [INSTRUCTIONS.md](../INSTRUCTIONS.md)
