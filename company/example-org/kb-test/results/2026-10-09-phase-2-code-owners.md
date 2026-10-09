---
title: "Phase 2 Results: Code Owners"
description: What CODEOWNERS did on pull requests with an owner by username, by email, by path, a nonexistent owner, an owner-authored pull request and a second owner, plus the CI check added to catch bad owners. Covers cases P2-0 to P2-8.
type: report
status: draft
owner: inotives
created_at: 2026-10-09
created_by: inotives
ai_assisted: true
---
# Phase 2 Results: Code Owners

Run on 2026-10-09. Cases are defined in the [test plan](../test-plan.md). Everything below was observed in this run **[V]** unless it is marked **[?]**.

Ruleset `phase-1-protect-main` started this phase with code-owner review off. It was turned on at P2-4 and stayed on. The three accounts were `inotives` (owner, admin), `inotivesgames` and `inotives-inoai` (write access).

## Summary

- GitHub reads CODEOWNERS from the **base branch**. A pull request cannot apply its own CODEOWNERS change.
- An owner by `@username` and an owner by verified email both resolve, and the last matching rule wins.
- With code-owner review on, only an owner's approval clears a path.
- A nonexistent owner is silent. GitHub flags it only in the errors API and the file view, the pull request still merges, and the path loses its owner requirement.
- A sole owner does not block their own pull request. Any approver with write access clears it.
- A CI step on `codeowners/errors` fails the check for a nonexistent owner and for a real account without write access.

## Results

| Case | Observation | Evidence |
| --- | --- | --- |
| P2-0 | The owner checked both throwaway accounts on their GitHub pages. Both emails are verified | Checked by `inotives`. Not readable through the API with the token in use |
| P2-1 | Pull request 12 added `* @inotives` from `inotives-inoai`. It requested no reviewer, because `main` had no CODEOWNERS. After it merged, pull request 13 (a blank line in a template) requested `inotives` | Pull request 12 merged as `9f14308`. Pull request 13 `reviewRequests: [inotives]`, closed without merging |
| P2-2 | After `/memo/ inotives.games@gmail.com` reached `main`, pull request 15 (a new page under `memo/`) requested `inotivesgames` and not `inotives`. The path rule replaced `*` | Rule merged as `4574d4d` through pull request 14. Pull request 15 `reviewRequests: [inotivesgames]`, closed without merging |
| P2-3 | Covered only through P2-2: the `/memo/` rule overrode `*` for that path. The `/skill/` rule in the plan was not run | As P2-2 |
| P2-4 | Pull request 15 was approved by `inotives` first and was `CLEAN`. After `require_code_owner_review` was turned on it became `REVIEW_REQUIRED` and `BLOCKED`, although the approval still showed. The owner's approval made it `CLEAN` | Ruleset read-back `require_code_owner_review: true`. Reviews `inotives: APPROVED`, then `inotivesgames: APPROVED` |
| P2-5 | The errors API reported `Unknown owner` at line 8 for `/concept/ @inotives-no-such-user-xyz`. The pull request that added it passed CI and merged. A pull request touching `concept/` requested nobody and went `CLEAN` after one approval from a non-owner | Pull request 16 merged as `9e18113`, run 37899295738 `success`. Pull request 17 `reviewRequests: []`, then `APPROVED` and `CLEAN`, closed. Cleanup pull request 18 merged as `7540670` |
| P2-6 | Pull request 19 was authored by `inotives`, the only owner of `README.md`. It requested nobody. An approval from `inotivesgames`, not an owner, made it `CLEAN`. No deadlock | Pull request 19 `REVIEW_REQUIRED`, `BLOCKED`, then `APPROVED`, `CLEAN`. Closed without merging |
| P2-7 | The premise changed, because there was no deadlock to resolve. With `* @inotives @inotivesgames`, pull request 21 by `inotives` requested `inotivesgames`. An approval from non-owner `inotives-inoai` left it `BLOCKED`. The approval from `inotivesgames` made it `CLEAN` | Second owner merged as `f57c44f` through pull request 20. Pull request 21 closed without merging |
| P2-7 (two owners) | A normal pull request requested both owners. One owner's approval was enough to merge | Pull request 22 `reviewRequests: [inotives, inotivesgames]`, approved by `inotives` only, merged as `535d88b` |
| P2-8 | A new `validate-docs` step calls `codeowners/errors` for the pull request head. A clean file passed. A nonexistent owner and `@octocat` (a real account without write access) both failed, with the same message. The failing pull request stayed `BLOCKED` after approval. After a fix, the check passed and the approval was `DISMISSED` | Control pull request 23 run 37909424399 `success`, merged as `ad28f61`. Pull request 24 run 37909526511 `failure`, then fix commit `d4dac22`, run 37909694023 `success`. Pull request 25 run 37909532109 `failure`. Failure text: `Unknown owner on line 8: make sure @... exists and has write access to the repository` |

## Deviations from the plan

- Pull request 14 was authored by `inotivesgames` and approved by `inotives`, not authored by `inotives-inoai`, because that account was not yet signed in to `gh`. Its only job was to put the rule on `main`.
- P2-6 and P2-7 were reframed after P2-6 showed no deadlock. P2-7 now tests whether a second owner restores the gate.
- P2-8 was added. It was not in the plan.

## Implications for the contract

1. Put CODEOWNERS on `main` before relying on it. The first pull request that adds it gets no automatic reviewer, so name one by hand.
2. Keep the CODEOWNERS check in `validate-docs`. Without it, a mistyped handle removes review for that path with no warning.
3. A path rule replaces `*`, so list every owner on that path.
4. Name at least two owners on any path that matters. A sole owner's own pull requests are cleared by any approver with write access.
5. Do not rely on an unverified email. Not tested here.

## Limits of this run

- One person operated all three accounts, so approvals prove the rule mechanics, not independent review.
- The reason a sole owner does not block their own pull request is not documented by GitHub. Two cases support it. The explanation is a reading, not proven **[?]**.
- Owners as teams (`@org/team`) cannot be tested on a personal repository. That belongs to Phase 4.
- An unverified email, and an owner who has an account but lacks write access in the review request itself, were not tested. The errors API did flag `@octocat`.
- `GITHUB_TOKEN` read `codeowners/errors` inside Actions for a public repository. A private repository was not tested **[?]**.
- Each case ran once, so statuses are **Observed**, not **Confirmed**.
