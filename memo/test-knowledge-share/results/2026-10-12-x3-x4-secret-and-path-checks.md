---
title: "X-3 and X-4: Secret and Local Path Checks"
description: Report of the planted-secret test (X-3) and the new local-path check (X-4), with the steps, the observed results at the hook and in CI, the problems found and the fix made.
type: report
status: draft
owner: inotives-inoai
created_at: 2026-10-12
created_by: inotives-inoai
ai_assisted: true
derived_from:
  - 2026-10-12-confirmation-reruns
---
# X-3 and X-4: Secret and Local Path Checks

Run on 2026-10-12 as `inotives-inoai` in its clone, with approvals by `inotivesgames` and reads by `inotives`. The cases are in the [test plan](../test-plan.md) and the commands are in [test steps](../test-steps.md). Everything below was observed in this run **[V]**.

## Summary

| ID | Layer | Result |
| --- | --- | --- |
| X-3 | Local hook | **Failed open.** With no scanner installed the commit went through with only a warning. Fixed in this pull request |
| X-3 | CI (`Scan for secrets`) | Blocked the PR on both planted secrets. A later fix commit did **not** clear it, because the scan reads history. Rewriting the branch did |
| X-4 | Local hook | Refused the commit and named both lines |
| X-4 | CI (`Check frontmatter, links and skills`) | Failed the PR on both paths. The fix to `~/` turned it green |

Both probes were closed unmerged and their branches deleted, so no probe content reached `main`.

## How it was run

- **Clone and identity:** the `inotives-inoai` clone, `user.email` `inotives.inoai@gmail.com`, `core.hooksPath` `.githooks`, as in the [confirmation report](2026-10-12-confirmation-reruns.md).
- **Scanner on this machine:** neither `gitleaks` nor a running `docker` was available, so the local secret scan could not run.
- **Probes:** two draft PRs from branches `inotives-inoai/x3-secret-probe` (PR 37) and `inotives-inoai/x4-path-probe` (PR 38), each with one throwaway page under `concept/` with valid frontmatter, so that only the case under test could fail.
- **Fake secret:** an AWS-shaped access key line and a secret key line. They are not real credentials and are not repeated here.
- **Fake paths:** a macOS-style home path in prose and a Linux-style home path in a code fence, both with an invented name. The report does not repeat them, because the new check would refuse the page.
- **Accounts per command:** `GH_TOKEN=$(gh auth token -u <login>)`, as in the setup.

## X-3: a planted fake secret

**Steps and observations**

| Step | Observation | Evidence |
| --- | --- | --- |
| 1. Commit the page with the fake key, hook on | The commit was **not refused** | The hook printed `WARNING gitleaks and docker are not available; secret scan skipped`. Commit `67d6436` was created |
| 2. Push and open draft PR 37 | CI ran | The check started on the PR |
| 3. Read the CI result | `check` failed in 11s, PR `BLOCKED` | Step `Scan for secrets`: `leaks found: 2` over 30 commits. `RuleID: aws-access-token`, line 13, and `RuleID: generic-api-key`, line 14, both in `concept/note__x3-secret-probe.md`, commit `67d6436`. Values were redacted |
| 4. Approve as `inotivesgames` | Approval did not unblock the PR | `["BLOCKED","APPROVED"]` |
| 5. Push a commit that deletes the key lines | `check` still failed | `leaks found: 2`, same commit `67d6436`, now 31 commits scanned. State `BLOCKED`, `REVIEW_REQUIRED` (approval dismissed by the push) |
| 6. Rewrite the branch: `git reset --soft origin/main`, recommit the page without the key, `git push --force-with-lease` | `check` passed in 10s | `30 commits scanned. no leaks found`. State `BLOCKED`, `REVIEW_REQUIRED` because the push dismissed the approval |
| 7. Close PR 37 unmerged and delete the branch | Done | `gh pr close 37 -d`. `git ls-remote --heads origin` listed only `main` |

**Result**

- **CI works.** It detected both the key pattern and the generic secret, and a required check stopped the merge even after approval.
- **The local hook does not protect a machine without a scanner.** It warned and let the commit through. A person who ignores the warning commits the secret, and only CI stops it, after the secret is already in a pushed branch.
- **A fix commit is not enough.** `gitleaks detect` scans the history of the branch, so the key in the first commit keeps failing every later run. The branch must be rewritten so no commit holds the key.
- **A rewrite does not remove the leak.** The old commit `67d6436` was pushed and was reachable through the pull request. The report did not test whether GitHub still serves it after the force-push, so treat any real secret as exposed and rotate it.

## X-4: a personal local path

**Steps and observations**

| Step | Observation | Evidence |
| --- | --- | --- |
| 1. Local probe with four pages: a path in prose, a `~/` path, a path in a code fence, a Windows path | Prose, fenced and Windows paths were flagged. The `~/` path and a placeholder path in angle brackets passed | One error per bad line, each in the form `<file>:<line>: local path '<match>', write ~/ or a relative path`. The probe page was deleted before any commit |
| 2. Commit the probe page, hook on | Refused | errors on lines 13 and 16 of `concept/note__x4-path-probe.md`, then `checked 18 files and 1 skills, 2 problems` |
| 3. `git commit --no-verify`, push, open draft PR 38 | CI ran | The check started on the PR |
| 4. Read the CI result | `check` failed in 5s | Step `Check frontmatter, links and skills`: the same two errors and `2 problems` |
| 5. Approve as `inotivesgames` | Approval did not unblock the PR | `["BLOCKED","APPROVED"]` |
| 6. Replace the paths with `~` and push | `check` passed in 11s | State `BLOCKED`, `REVIEW_REQUIRED`, because the push dismissed the approval |
| 7. Close PR 38 unmerged and delete the branch | Done | `git ls-remote --heads origin` listed only `main` |

**Result:** the rule works at both layers. It was added in pull request 36 (`fa4b4d5`), and that pull request's own CI passed, so the existing pages have no such path. The check covers prose, code fences and the Windows form.

## Problems found and what was done

| # | Problem | Action |
| --- | --- | --- |
| 1 | The pre-commit hook skips the secret scan when no scanner exists, and the commit proceeds | **Fixed** in `.githooks/pre-commit`. It now exits 1 with install instructions. `SKIP_SECRET_SCAN=1 git commit` skips it once, with a warning. A test commit with no scanner and no override was refused and `HEAD` did not move |
| 2 | A follow-up commit does not clear a CI secret finding | **Documented** in the test steps: rewrite the branch, then rotate the key. No code change |
| 3 | `AGENTS.md` says the hook scans for secrets and does not say it now refuses without a scanner, or name local paths under "never store" | **Not changed.** The contract is the owner's page. Reported for the owner |
| 4 | The CI step pulls `zricethezav/gitleaks:latest`, unpinned | **Not changed.** The workflow already carries a comment about it, to be pinned once the approved-actions policy is known |
| 5 | The local path check catches only a path form. A bare username in a clone URL or `git log` output is not caught | **Not changed.** A limit of the rule |

## Limits of this run

- One operator, one machine, three accounts.
- The local half of X-3 was run only on a machine with no scanner, so the case where the hook finds and refuses a real secret was **not** observed in this run. The earlier claim of a tested hook is not repeated here.
- The fix to the hook was tested for the refusal and for the absence of a scanner. The override path is shown by the commit of this report, which printed the override warning.
- Whether GitHub still serves a force-pushed commit was not tested.
- Free accounts only. Organisation-level secret protection on Enterprise is untested.
