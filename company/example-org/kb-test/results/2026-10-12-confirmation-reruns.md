---
title: "Confirmation Reruns R-1 to R-3"
description: Report of the three confirmation reruns. Each repeats an earlier case with a different account in a fresh clone. It gives the exact steps, how each was run, what was observed and what it proves.
type: report
status: draft
owner: inotives-inoai
created_at: 2026-10-12
created_by: inotives-inoai
ai_assisted: true
derived_from:
  - 2026-10-08-phase-0-1-sync-behaviour
  - 2026-10-08-phase-1-ruleset-and-review
---
# Confirmation Reruns R-1 to R-3

Run on 2026-10-12. The cases are defined in the [test plan](../test-plan.md) and the step-by-step commands are in [test steps](../test-steps.md). Everything below was observed in this run **[V]**. Nothing is claimed beyond it.

## Summary

| ID | Repeats | Result | Confirms |
| --- | --- | --- | --- |
| R-1 | P1-1, P1-2 | The push to `main` was rejected and the CLI still printed success | Confirmed |
| R-2 | P1-5b (part), P1-6, P1-15 | A PR by one account, approved by a second and merged by a third, passed. Two refusal cases were not repeated | Confirmed for the approve-then-merge path only |
| R-3 | P1-8, P1-9 | The branch was not pushed, and the editor's commit went to local `main` | Confirmed |

## How it was run

- **Accounts:** `inotives-inoai` (author, `Write`), `inotivesgames` (approver, `Write`), `inotives` (owner, `Admin`).
- **Clone:** a new clone of `inotives/inotives-knowledge-share` for `inotives-inoai`, over the SSH alias `github-inotivesinoai`. The clone's `user.name` is `inotives-inoai` and its `user.email` is `inotives.inoai@gmail.com`. `core.hooksPath` is `.githooks`, so the pre-commit hook was active. The clone started at `ee72e67`.
- **Operator:** one person runs all three accounts, so this shows how the rules work, not that independent review happens.
- **GitHub CLI:** each command was tied to one account with `GH_TOKEN=$(gh auth token -u <account>)`. The active `gh` account was never switched.
- **Ruleset:** `phase-1-protect-main` (id `24690905`), as left at the end of Phase 3.

## R-1: a write on `main` followed by `ok sync`

Repeats P1-1 and P1-2 with a different account in a fresh clone.

**Steps**

1. In the clone, switch to `main` and pull. `main` and `origin/main` were both at `56127f0`.
2. Run `ok init --scope project --no-skills`. `git status` stayed clean.
3. Start the server with `ok start`. It listened on port `54389`.
4. Write `concept/note__r1-confirmation.md` on disk. `git status -sb` showed it untracked and `main...origin/main` level.
5. Run `ok sync`.
6. Wait 20 seconds, run `git fetch`, then read `git status -sb`, `git log` and the server log.
7. Clean up: `git reset --hard origin/main`.

**Observed**

| Observation | Evidence |
| --- | --- |
| The CLI printed success and exited 0 | `Triggering sync via running server (port 54389)`, then `✓ sync triggered`, `exit=0` |
| A local commit was made, authored by the account | `25d6741 inotives-inoai <inotives.inoai@gmail.com> Auto-save: Updated concept/note__r1-confirmation.md` |
| The push did not reach GitHub | `git status -sb`: `main...origin/main [ahead 1]`. `origin/main` stayed at `56127f0` |
| The server classified the rejection | `class: semantic`, `subclass: protected-branch`, `retryable: false`, with `GH013: Repository rule violations found for refs/heads/main` |
| Sync switched itself off for the clone | `[sync] auto-disabled — persisting to project-local config`. `.ok/local/config.yml` then held `autoSync: enabled: false` |

**Result:** the same as P1-1 and P1-2. The ruleset blocks the push, and the only sign in the CLI is a success message. **Confirmed.**

## R-2: author, approve and merge by three accounts

Repeats P1-6 and P1-15 with the roles in a different order. P1-5b was only partly repeated.

**Steps**

1. As `inotives-inoai`, create branch `inotives-inoai/r2-confirmation` and add `concept/note__r2-confirmation.md`. The pre-commit hook reported `checked 16 files and 1 skills, 0 problems`.
2. Push the branch and open pull request 34 with `gh pr create`.
3. Read the checks, review state and review requests as `inotives`.
4. As `inotivesgames`, wait for the check to pass, then run `gh pr review 34 --approve`.
5. Read the state again.
6. As `inotives`, run `gh pr merge 34 --squash`.

**Observed**

| Step | Observation | Evidence |
| --- | --- | --- |
| Author | The commit author matched the account | `inotives-inoai <inotives.inoai@gmail.com>` |
| CI | `check` ran on the PR and passed in 8s | `gh pr checks 34` |
| Review requests | Both code owners were requested | `inotives,inotivesgames`, from `* @inotives @inotivesgames` |
| Before approval | The PR could not be merged | `BLOCKED`, `REVIEW_REQUIRED` |
| After approval | The PR could be merged | `CLEAN`, `APPROVED`, review `inotivesgames:APPROVED` |
| Merge | The owner merged it | `MERGED`, merge commit `56127f0`, merged by `inotives`, authored by `inotives-inoai` |

**Result:** an approval by a second account, with a passing check, allows a third account to merge a PR from a different author. **Confirmed for that path.**

**Not repeated, on purpose.** An attempt to merge before approval was refused by the agent's permission classifier, so no merge was tried before the review. P1-5b already covers that case. The owner approving their own PR (P1-5) was also not repeated, because this run used a non-owner author. Both stay **Observed**.

## R-3: a write on a feature branch followed by `ok sync`

Repeats P1-8 and P1-9 with a different account in a fresh clone. The server from R-1 was still running, so the branch was switched under a running server, as in P1-10.

**Steps**

1. Create branch `inotives-inoai/r3-confirmation` from `main`.
2. Write `concept/note__r3-confirmation.md` on disk.
3. Read the state: branch, `HEAD`, local `main`, `origin/main`.
4. Run `ok sync`, wait 20 seconds, run `git fetch`, then read the state, `git log` and `git ls-remote --heads origin`.
5. Clean up: delete the page, check out `main`, `git reset --hard origin/main`, delete the branch.

**Observed**

| Observation | Evidence |
| --- | --- |
| Before the sync, all refs agreed | `branch=inotives-inoai/r3-confirmation head=56127f0 main=56127f0 origin/main=56127f0` |
| The CLI printed success | `✓ sync triggered` |
| The editor's commit went to local `main`, not the checked-out branch | After: `head=56127f0 main=7ebb120 origin/main=56127f0`. `7ebb120 inotives-inoai Auto-save: Updated concept/note__r3-confirmation.md` is on `main` |
| The feature branch did not move and the page stayed untracked | `git status -sb`: `## inotives-inoai/r3-confirmation`, `?? concept/note__r3-confirmation.md` |
| The branch was not pushed | `git ls-remote --heads origin` listed only `refs/heads/main` |
| The sync still targeted `main` and then switched itself off | Server log: `protected-branch`, `GH013`, then `[sync] auto-disabled` |

**Result:** the same as P1-8 and P1-9. The editor ignores the checked-out branch, so a branch cannot be used to publish through `ok sync`. **Confirmed.**

## Findings

1. **The three design-carrying observations hold with a second account in a fresh clone.** The ruleset blocks the editor's push (R-1), the approve-then-merge path works (R-2), and the editor does not respect the checked-out branch (R-3).
2. **The failure is silent in the CLI.** Both R-1 and R-3 printed `✓ sync triggered` and exited 0. The only trace is in `.ok/local/logs/server-current.jsonl`. The contract should say: check `git status` and the pull request, never the CLI message.
3. **A feature branch does not help.** R-3 shows the commit lands on local `main`, which leaves a stranded commit that has to be reset. The contributor workflow should be plain git for branches, commits and pushes, with OpenKnowledge used for editing and search only.
4. **Sync turns itself off after one rejection.** It happened in R-1 and again in R-3, so a contributor must expect it.
5. **A clean recovery exists.** `git reset --hard origin/main` removed the stranded commit in both clones. It is safe only when the commit holds nothing worth keeping, so move the work to a branch first.
6. **The pre-commit hook cannot scan for secrets on this machine.** In step 1 of R-2 it printed `WARNING gitleaks and docker are not available; secret scan skipped`. The CI workflow has a `Scan for secrets` step, so only the local layer is affected. This matters for X-3.

## Limits of this run

- One operator, one machine, three accounts. Independent review is not shown.
- Free accounts and a personal repository, so organisation rulesets and SSO are untested (Phase 4).
- R-2 did not repeat the refusals for a merge before approval and for the owner's own approval.
- The editor UI was not opened, so P1-2b is unchanged.
- The two throwaway pages `concept/note__r1-confirmation.md` and `concept/note__r2-confirmation.md` were removed. R-1's page never reached `main`. R-2's page was merged in PR 34 and is deleted by the pull request that adds this report.
