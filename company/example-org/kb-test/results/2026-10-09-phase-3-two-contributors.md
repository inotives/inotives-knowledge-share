---
title: "Phase 3 Results So Far: Two Contributors"
description: Results of P3-1 to P3-3, two contributors editing one page on different lines and on the same line, and how attribution looked afterwards. Phase 3 is not finished, because P3-4 is pending and P3-5 is parked.
type: report
status: draft
owner: inotives
created_at: 2026-10-09
created_by: inotives
ai_assisted: true
---
# Phase 3 Results So Far: Two Contributors

Run on 2026-10-09. Cases are defined in the [test plan](../test-plan.md). **Phase 3 is in progress.** This page covers P3-1 to P3-3. P3-4 is pending and P3-5 is parked. Everything below was observed in this run **[V]** unless it is marked **[?]**. Earlier phases are in the [Phase 1 summary](./2026-10-08-phase-1-summary.md) and the [Phase 2 summary](./2026-10-09-phase-2-summary.md).

The two authors were `inotivesgames` and `inotives-inoai`. `inotives` approved and merged every pull request. The test page was `concept/note__p3-shared-page.md`, created by pull request 26 with three sections of three facts each. Ruleset state: pull request with 1 approval, code-owner review on, `validate-docs` required, approvals dismissed on push, `strict_required_status_checks_policy: false`.

## Summary

- Edits on different lines of one page merge cleanly, and the second pull request stays mergeable after the first lands.
- Edits to the same line give a visible conflict. GitHub never picks a side, and the second author has to resolve it.
- A resolving push clears the earlier approval, so the pull request needs a fresh review.
- Commit author, pull request author and the clone's git identity agree. That identity comes from `git config`, not from who typed the edit.
- Nothing checks `ai_assisted`. The page says `false` although an agent wrote every commit.
- CI passes on a conflicting or contradictory edit, because it checks structure and not meaning.

## Results

| Case | Observation | Evidence |
| --- | --- | --- |
| P3-1 | Pull request 27 (`inotivesgames`, Section A, the refunds line) and pull request 28 (`inotives-inoai`, Section B, the guest line) were opened against the same base. After 27 merged, 28 was still `MERGEABLE`, and it merged without a rebase. Both edits are on `main`. The edits did not contradict each other, so a factual clash was not tested | 27 merged as `d05192f`, 28 as `9fcab2d`. Base `3a4f34c`. Ruleset `strict_required_status_checks_policy: false` |
| P3-2 | Pull requests 30 (06:00 to 07:00, `inotivesgames`) and 31 (06:00 to 05:30, `inotives-inoai`) changed the same line. Both passed CI and were `MERGEABLE` alone. After 30 merged, 31 became `CONFLICTING` and `DIRTY`, and `main` kept 07:00. A local merge of `main` into the branch stopped with `CONFLICT (content)` and markers around `05:30` and `07:00` | 30 merged as `63ccd47`. 31 `mergeable: CONFLICTING`, `mergeStateStatus: DIRTY` |
| P3-2 (resolve) | With 31 approved and conflicting, the resolving merge was pushed. The approval became `DISMISSED` and the pull request `REVIEW_REQUIRED`. It became `MERGEABLE` and merged after a new approval. This is also the clean repeat of P1-14 | Before: `reviewDecision: APPROVED`, `DIRTY`. After: `REVIEW_REQUIRED`, `MERGEABLE`, `inotives: DISMISSED`. Merged as `e5ecff2` |
| P3-3 | For pull requests 26, 27, 28, 30 and 31, the git author equalled the pull request author and the clone's `git config`. The committer was `GitHub`. The merger appears only on the pull request. The page's `created_by` is `inotives-inoai`, which matches the author of its creating commit. Its `ai_assisted` is `false` | Authors `inotives-inoai <inotives.inoai@gmail.com>` and `inotivesgames <inotives.games@gmail.com>`. Merged by `inotives` on each pull request |
| P3-3 (history) | The squash commit of pull request 31 is titled "inoai moves the daily report to 05:30", but its diff is `07:00` to `07:00, after late rows land`. GitHub used the first branch commit for the title | `e5ecff2`, `git show` diff |

## What this shows about the plan

1. The two-contributor merge path works as designed. No collision was silent, and none was auto-resolved.
2. The conflict message says the lines differ, not that they are rival claims. A human has to notice that 05:30 and 07:00 disagree. Review is the control.
3. `ai_assisted` and `created_by` are honesty fields. Git identity does not tell who or what typed the change. The contract should say so.
4. Squash titles can contradict the diff. Set the squash message from the pull request title, or tell reviewers to read the diff.

## Open items

| Item | Why it is open | Owner |
| --- | --- | --- |
| P3-4, agent edit with and without OpenKnowledge | Needs the OpenKnowledge server. Not run | Next |
| P3-5, two people on one live server | Parked. The server binds to localhost | Parked |
| Contradictory facts on different lines | P3-1 used independent edits, so a factual clash was not tested | Optional (P3-1b) |
| `require_extra_approval_for_unattributed_changes: true` | Its effect is not shown by P3-3 | To investigate |
| X-1, X-3 and the reruns R-1 to R-3 | Not run | After Phase 3 |
| Contract and setup instructions | Held until testing ends and the team has aligned | After Phase 4 |

## Limits of this run

- One person operated all three accounts, so approvals prove the rule mechanics, not independent review.
- An agent made every commit under the contributors' identities. The attribution results show how the system records identity, not who really typed.
- The repository is public and on free accounts. Behaviour on GitHub Enterprise is untested.
- Each case ran once, so statuses are **Observed**, not **Confirmed**.
