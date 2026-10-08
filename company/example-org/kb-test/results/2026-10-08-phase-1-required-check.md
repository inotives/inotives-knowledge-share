---
title: "Phase 1 Follow-up Results: Required CI Check"
description: What happened when validate-docs became a required status check, with a deliberately invalid page authored by the second contributor. Covers P1-5b, P1-11 and P1-12, the hook evidence for X-2 and a stale-approval finding.
type: report
status: draft
owner: inotives
created_at: 2026-10-08
created_by: inotives
ai_assisted: true
---
# Phase 1 Follow-up Results: Required CI Check

Run on 2026-10-08. Cases are defined in the [test plan](../test-plan.md). Earlier results are in the [sync behaviour report](./2026-10-08-phase-0-1-sync-behaviour.md) and the [ruleset and review report](./2026-10-08-phase-1-ruleset-and-review.md). Everything below was observed in this run **[V]**.

## Change made before the tests

The ruleset `phase-1-protect-main` (id `24690905`) gained a `required_status_checks` rule for the context `check`, which is the job in `validate-docs`. `strict_required_status_checks_policy` is `false`, so a branch need not be up to date to merge. The other three rules are unchanged, there are still no bypass actors, and code-owner review is still off.

## Summary

- With the check required, a pull request whose CI fails cannot be merged even after approval. After the fix, it merges.
- The owner cannot merge a pull request that has no approval.
- The local pre-commit hook and the CI check give the same four errors for the same page.
- An approval survives a later push, so approved content can change before the merge.

## Results

| Case | Observation | Evidence |
| --- | --- | --- |
| P1-5b | `inotives` ran `gh pr merge` on pull request 3 before anyone approved it. GitHub refused | `the base branch policy prohibits the merge`. The CLI also suggested `--auto` and `--admin`, which were not used |
| X-2 (frontmatter part) | The contributor's pre-commit hook refused a normal commit of a page with invalid frontmatter. `HEAD` did not move | `missing 'type'`, `missing 'owner'`, `missing 'created_at'`, `status 'wip' not in [...]`, then `checked 11 files and 1 skills, 4 problems`. Broken-link refusal not tested |
| P1-11 | `inotives-inoai` committed the same page with `--no-verify` and opened pull request 4. CI failed with the same four errors. `inotivesgames` approved it. The state was `reviewDecision: APPROVED` with `mergeStateStatus: BLOCKED`, and the owner's merge was refused | Run 37734606700, check `check`: `fail`. Message: `the base branch policy prohibits the merge` |
| P1-12 | After a fix was pushed to the same branch, CI passed in 10 seconds and the state became `mergeStateStatus: CLEAN`. The owner then merged | Run 37734951758. Merge commit `4713188`, merged by `inotives` |
| P1-13 | The approval given before the fix was still counted after the new push, because the ruleset has `dismiss_stale_reviews_on_push: false`. `reviewDecision` stayed `APPROVED` | State read after the fix push: `reviewDecision: APPROVED`, `mergeStateStatus: CLEAN` |

## Implications for the contract

1. The ruleset now enforces the contract's rule that `validate-docs` must pass. Keep `check` as the required context name, because renaming the job would leave merges waiting for a check that never reports.
2. The pre-commit hook is a courtesy, not a control: `--no-verify` skips it. CI is the control.
3. Decide whether to dismiss approvals on new pushes. With the default, a contributor can change a page after approval and the approval stands. The cost of turning it on is a re-review after every fix.
4. Contributor 2 authored a pull request end to end without trouble, so `inotives-inoai` is confirmed to work as an author.

## Limits of this run

- One person operated all three accounts, so the approvals prove the rule mechanics, not independent review.
- `--admin` was never tried, so whether an admin can override a required check is unknown. It is tracked as P1-5c.
- Each case was run once, so statuses are **Observed**, not **Confirmed**.
