---
title: Pilot Roster
description: Who may contribute during the pilot, who approves, and each person's handle. The handle is the part of the work email before the @.
type: reference
status: draft
owner: jane.doe
created_at: 2026-10-08
created_by: jane.doe
ai_assisted: true
---
# Pilot Roster

The first pilot of this knowledge base is open to **Team A** only. Handles follow the rule in [AGENTS.md](../../AGENTS.md#identity): the part of the work email before the `@`.

## Approver

| Handle | Name | Role in the pilot |
| --- | --- | --- |
| `jane.doe` | Jane Doe | Approves every pull request. Code owner for all paths (`.github/CODEOWNERS`) |

## Contributors

| Handle | Name | Group |
| --- | --- | --- |
| `alex.one` | Alex One | Team A |
| `sam.two` | Sam Two | Team A |

## Known limits of a one-approver pilot

- **One approver on purpose.** It is easier to manage during the pilot. Afterwards the approver group grows to 3 or 4 people across Team A and Team B.
- A pull request written by the approver cannot be approved by the same person. It needs an explicit bypass in the ruleset for the approver's own changes, or another person approving it.
- Everything waits on one person, so reviews can queue when the approver is away. Track review wait time as a pilot measure.
- This page lists names and handles only. Do not add personal contact details.
