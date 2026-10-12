---
title: "P2-3: A Path Rule for skill/"
description: Report of case P2-3. A /skill/ code owner rule that names an account outside the * owners requested only that account, and only that account's approval unblocked a skill/ pull request. A draft pull request requested nobody.
type: report
status: draft
owner: inotives
created_at: 2026-10-12
created_by: inotives
ai_assisted: true
derived_from:
  - 2026-10-09-phase-2-code-owners
---
# P2-3: A Path Rule for skill/

Run on 2026-10-12. The case is in the [test plan](../test-plan.md). It completes the part of P2-3 that the [Phase 2 report](./2026-10-09-phase-2-code-owners.md) left open: the `/memo/` rule showed that the last matching rule wins, but the `/skill/` rule itself was never run. Everything below was observed in this run **[V]**.

## Summary

- A path rule **replaces** the `*` owners for that path. With `/skill/ @inotives-inoai`, a pull request touching `skill/` requested only `inotives-inoai`. An owner of `*` had no say there.
- The rule is **enforced**. An approval from `inotives`, who owns `*` but not `/skill/`, left the pull request `BLOCKED`. The approval from `inotives-inoai` made it `CLEAN`.
- The reverse holds on a path with no rule. On `concept/`, an approval from `inotives-inoai` did not unblock it and an approval from `inotives` did.
- A **draft** pull request requested nobody. Reviewers were requested only once it was marked ready for review.

## How it was run

The three test accounts were operated by one person, each through its own login. `inotivesgames` authored every pull request, `inotives` and `inotives-inoai` approved, and `inotives` merged.

The test steps name `@inotivesgames` as the `/skill/` owner. `inotivesgames` already owns `*`, so a `skill/` pull request and a `concept/` one would have looked alike. The rule used here names `@inotives-inoai`, who is not an owner of `*`. `*` is `@inotives @inotivesgames`.

## Results

| Step | Observation | Evidence |
| --- | --- | --- |
| Rule pull request 42 adds `/skill/ @inotives-inoai` to `CODEOWNERS` | `check` passed. It requested `inotives`, the `*` owner who is not the author. The `codeowners/errors` API reported no errors. Merged after `inotives` approved | Merged as `c1db212` |
| Probe pull request 43 touches `skill/README.md`, opened as a draft | **No reviewer was requested** | `reviewRequests` empty, `isDraft` true |
| Control pull request 44 touches `concept/README.md`, opened as a draft | **No reviewer was requested** | `reviewRequests` empty, `isDraft` true |
| Mark 43 and 44 ready for review | 43 requested `inotives-inoai` only. 44 requested `inotives` only. Neither requested the author `inotivesgames` | 43 `requests=inotives-inoai`. 44 `requests=inotives` |
| Approve 43 as `inotives` (owner of `*`, not of `/skill/`) | **Still blocked** | `BLOCKED`, `REVIEW_REQUIRED`, review `inotives: APPROVED` |
| Approve 43 as `inotives-inoai` (owner of `/skill/`) | **Unblocked** | `CLEAN`, `APPROVED`, `check` `SUCCESS` |
| Approve 44 as `inotives-inoai` (not an owner of `*`) | **Still blocked** | `BLOCKED`, `REVIEW_REQUIRED` |
| Approve 44 as `inotives` (owner of `*`) | **Unblocked** | `CLEAN`, `APPROVED` |

## Clean-up

- Pull requests 43 and 44 were closed without merging, and their branches deleted.
- The temporary rule was removed by pull request 45, merged as `a1603df`. `CODEOWNERS` on `main` is back to its two original rules, and the errors API reports none.
- The branch of pull request 42 was not deleted automatically after its merge, and was deleted by hand. GitHub's API returned a few transient `502` replies during the run. They did not change any result.

## What this shows

1. **Path rules protect what the plan needs them to.** A skill path can be given its own owner, and `*` owners cannot approve it. That matches the contract's "closest review" for skills, once a real `/skill/` owner is named.
2. **There is no `/skill/` rule on `main` today.** The rule was temporary. Until the owner adds one, any `*` owner can approve a change to a skill. This is a decision for the contract owner.
3. **A draft pull request is not reviewed.** No code owner is requested on a draft, so the review request never reaches anyone until the author marks it ready. Use drafts for work in progress only, and say so in the contract.
4. **The author is never requested.** In both pull requests the author was left out of the requests, even where the author owned the path via `*`. This agrees with the sole-owner finding in P2-6.

## Limits

- One person operated all three accounts, so the approvals prove the rule mechanics, not independent review.
- The repository is public and on free accounts. Owners as teams are untested here.
- The case ran once, so its status is **Observed**, not **Confirmed**.
