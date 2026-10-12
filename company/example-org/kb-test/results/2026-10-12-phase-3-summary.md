---
title: "Phase 3 Summary: Two Contributors"
description: Summary of Phase 3 (P3-1 to P3-5), what it showed, and the open items as they stand on 2026-10-12. It supersedes the open-items table in the Phase 3 report, which was written before the confirmation reruns.
type: report
status: draft
owner: inotives
created_at: 2026-10-12
created_by: inotives
ai_assisted: true
derived_from:
  - 2026-10-09-phase-3-two-contributors
  - 2026-10-12-confirmation-reruns
---
# Phase 3 Summary: Two Contributors

Read this first; the [Phase 3 report](./2026-10-09-phase-3-two-contributors.md) holds the evidence. Cases are in the [test plan](../test-plan.md). The earlier summaries are the [Phase 1 summary](./2026-10-08-phase-1-summary.md) and the [Phase 2 summary](./2026-10-09-phase-2-summary.md).

The open-items table in the Phase 3 report was written on 2026-10-09, before the confirmation reruns and the secret-scan runs. Dated reports are not edited after the fact, so this page records the current state instead.

## What Phase 3 showed

| Case | Result | Status |
| --- | --- | --- |
| P3-1 | Edits on different lines of one page merge cleanly, and the second pull request stays mergeable after the first lands. The two edits did not contradict each other, so a factual clash was not tested | Observed |
| P3-2 | Edits to the same line give a visible conflict that is never auto-resolved. A resolving push clears the approval, so the pull request needs a fresh review | Observed |
| P3-3 | Commit author, pull request author and the clone's git identity agree. Nothing checks `ai_assisted`, and a squash title can contradict the diff | Observed in part |
| P3-4 | OpenKnowledge warns an agent about a broken link and an orphan page while it writes. The pre-commit hook and CI are the only checks that refused bad frontmatter and a broken link. `ok lint` ran no checks | Observed |
| P3-5 | Not applicable. The planned setup is one local OpenKnowledge server per person, sharing work only through git, so two people never edit one live server | Not applicable |

## Decisions

- **P3-5 is not applicable** for the reason above. Concurrent edits are covered by P3-1 and P3-2.
- **Review is the control for a factual clash.** Git reports that lines differ, not that two claims rival each other.
- **CI and the hook, not OpenKnowledge, enforce the rules.** Treat "no problems" from `ok lint` as "nothing was checked" until rules are enabled.

## Open items as of 2026-10-12

| Item | State |
| --- | --- |
| Confirmation reruns R-1 to R-3 | Done on 2026-10-12. They confirm P1-1, P1-6, P1-8 and P1-9. See the [confirmation report](./2026-10-12-confirmation-reruns.md) |
| X-3, a planted fake secret, and X-4, a personal local path | Run on 2026-10-12 and recorded in the [X-3 and X-4 report](./2026-10-12-x3-x4-secret-and-path-checks.md). A further local-hook run is in a separate report awaiting review |
| P3-1b, contradicting facts on different lines | Not run. Added to the plan |
| `require_extra_approval_for_unattributed_changes: true` | Effect still not shown by P3-3 |
| X-1, scratch search and an agent write there | Only the audit half was seen |
| Enabling OpenKnowledge frontmatter and markdownlint rules | Not tried |
| `history` for page creation, `restore_version`, `checkpoint` | Not tried |
| Contract and setup instructions | Held until testing ends and the team has aligned. The setup notes were updated for the secret scan on 2026-10-12 |

## Limits

- One person operated all accounts, so approvals prove the rule mechanics, not independent review.
- The repository is public and on free accounts. Behaviour on GitHub Enterprise is untested.
- Most cases ran once. Only P1-1, P1-6, P1-8 and P1-9 are Confirmed.
