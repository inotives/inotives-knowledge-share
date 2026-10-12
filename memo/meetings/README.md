---
title: Meetings
description: "Notes from internal team meetings: what was discussed, decided and assigned. One page per meeting. Curated by pull request."
---
# Meetings

## Purpose

A record of internal team meetings: what was discussed, what was decided and who owns each action. Meeting notes are records, so they stay here. Decisions that matter are pulled out into their own pages.

## What goes here

| Goes here | Does not go here (put it in) |
| --- | --- |
| Notes from an internal or cross-cutting team meeting | A meeting about one client or project: `company/<name>/<project>/meetings/`, because client material stays in that client's folder |
| | A decision that others must rely on: its own `decision` page in [company](../../company/README.md) or [concept](../../concept/README.md), linked from the meeting note |
| | Personal notes: `_scratch/<handle>/` |

## Layout and naming

`memo/meetings/YYYY-MM-DD-<topic>.md`, for example `2026-10-14-dwh-vendor-sync.md`. One page per meeting, in a flat folder. Lowercase kebab-case topic. Two meetings on one day get two topics.

This page keeps no index of meetings. Use OpenKnowledge's folder view or search, so that a new meeting does not edit a shared file.

## Frontmatter for this folder

`type: note`, `status: draft`, `owner` and `created_by` set to the note-taker's handle, and `tags: [meeting]`. Set `ai_assisted: true` when an agent wrote or summarised the page. Add `project` when it applies. Put the attendees, as handles, in the body. The full table is in [AGENTS.md](../../AGENTS.md#frontmatter).

This folder has a `meeting` template with the fields and headings filled in.

## Review and ownership

A change needs a pull request, a passing `validate-docs` check, and one approval from someone other than the author, including a code owner. Code owners are set in `.github/CODEOWNERS`. Today the owners of `*` cover every folder, so this folder has no stricter review. A draft pull request requests no code owners, so mark it ready for review.

The note-taker owns the page. Others propose changes by pull request instead of editing in parallel.

## How to add a meeting

1. Draft in `_scratch/<handle>/`.
2. Branch `<handle>/<topic>`.
3. Create the page here from the `meeting` template.
4. Open a pull request and mark it ready for review.

The commands are in [INSTRUCTIONS.md](../../INSTRUCTIONS.md).

## Rules for this folder

- Record people by handle, not by name, and leave out personal remarks. No personal data about individuals.
- No passwords, tokens or keys. Point to where a secret lives.
- Everyone with repository access can read this folder. Do not put client material here.
- A real decision gets its own page, linked from the note. Do not leave it only inside the meeting record.
- Keep an agent summary's `ai_assisted: true`, and read it before it goes up for review.

## Related

[memo](../README.md), [company](../../company/README.md), [concept](../../concept/README.md), [AGENTS.md](../../AGENTS.md)
