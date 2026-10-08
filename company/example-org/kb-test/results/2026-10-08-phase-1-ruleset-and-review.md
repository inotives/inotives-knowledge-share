---
title: "Phase 1 Results: Ruleset, Review and Editor Branches"
description: What the ruleset on main did to a pull request, a self-approval, a contributor approval, a direct push and the editor's sync on a feature branch. Covers cases P1-4 to P1-9.
type: report
status: draft
owner: inotives
created_at: 2026-10-08
created_by: inotives
ai_assisted: true
---
# Phase 1 Results: Ruleset, Review and Editor Branches

Run on 2026-10-08. Cases are defined in the [test plan](../test-plan.md). Earlier cases are in the [Phase 0 and 1 sync report](./2026-10-08-phase-0-1-sync-behaviour.md). Everything below was observed in this run **[V]**.

Ruleset `phase-1-protect-main`: pull request required with 1 approval, force-push and deletion blocked, no bypass actors, code-owner review off.

## Summary

- The review rule works as designed: the owner cannot approve their own pull request, a contributor's approval is enough, and a non-admin cannot push to `main`.
- The editor is the weak point. `ok sync` commits to the local `main` branch by name, even when a feature branch is checked out, then fails against the ruleset and switches itself off.
- Plain `git` publishes a feature branch without trouble. In this setup the editor writes pages and git moves them.

## Results

| Case | Observation | Evidence |
| --- | --- | --- |
| P1-4 | `validate-docs` ran on the pull request and passed in 16 seconds. Before any review the pull request showed `mergeStateStatus: BLOCKED` and `reviewDecision: REVIEW_REQUIRED` | Pull request 1, check `check`, run 37723999146 |
| P1-5 | The owner `inotives` could not approve their own pull request. A merge attempt before approval was not run | `gh pr review 1 --approve` returned `failed to create review: GraphQL: Review Can not approve your own pull request (addPullRequestReview)` |
| P1-6 | `inotivesgames` (write access, not admin) approved. The pull request became `reviewDecision: APPROVED`, `mergeStateStatus: CLEAN`. The owner then squash-merged it | Merge commit `b15c96e`, merged by `inotives` at 2026-10-08T03:51:19Z |
| P1-7 | A direct push of an empty commit to `main` as `inotivesgames` was rejected. `main` stayed at `b15c96e`. The contributor's pre-commit hook ran first (frontmatter and links, then a gitleaks scan through Docker) and passed | `GH013: Repository rule violations found for refs/heads/main. Changes must be made through a pull request.` |
| P1-8 | With a feature branch checked out, `ok sync` did not publish the branch. The working-tree edit stayed uncommitted on that branch. The push it attempted was `main -> main`, and it was rejected. OpenKnowledge then set `autoSync.enabled: false` in `.ok/local/config.yml` and logged `auto-disabled` | Log lines at 03:53:22 to 03:53:27 UTC: `Push rejected: branch is protected`, `auto-disabled: persisting to project-local config` |
| P1-9 | `ok sync` had committed the edit to the local `main` branch while the feature branch was checked out. Local `main` ended one commit ahead of `origin/main` | Commit `b59e48a`, `Auto-save: Updated memo/baseline-sync-test.md`, found with `git log origin/main..main` after switching branches |
| P1-8 (git path) | A plain `git commit` and `git push` of the feature branch worked, because only `main` is protected | Branch `inotives/p1-8-editor-branch-test`, commit `9ce0782` |

## Implications for the contract

1. Contributors commit and push branches with git, and open pull requests with `gh` or the web. They do not use `ok sync` on a repository whose `main` is protected.
2. After any `ok sync`, run `git log origin/main..main`. A commit there is stranded and must be moved to a branch before the pull request.
3. A one-approver pilot needs a second person to approve the owner's own pull requests. No bypass is required, and the owner can merge once approved.
4. The sync is switched off per clone after one rejection. A contributor who re-enables it will meet the same failure.

## Limits of this run

- One person operated all three accounts, so P1-5 and P1-6 prove the rule mechanics but not independent review.
- The owner is a repository admin. The ruleset had no bypass actors, and the owner was still blocked from self-approval, but admin behaviour on other rules was not explored.
- The editor UI was not opened, so what it shows after a rejected sync is unknown.
- Each case was run once, so statuses are **Observed**, not **Confirmed**.
