---
title: A Private Repo on the Free Plan
description: "Report of putting this repository's setup in a private repo on a free personal account: GitHub refused the ruleset and branch protection, CI still ran and passed, and nothing was enforced, so an unapproved PR merged and a direct push to main went through."
type: report
status: draft
owner: inotives
created_at: 2026-10-13
created_by: inotives
ai_assisted: true
---
# A Private Repo on the Free Plan

Run on 2026-10-13 as `inotives`, on a free personal account, in a throwaway private repository created for the test. The question came from the plan's Phase 4: does this setup work on a private repo, given that every test so far used a public one? The cases are in the [test plan](../test-plan.md), and this run is case X-8. The exact commands are in the [test steps](../test-steps.md), so the run can be repeated, for example on an Enterprise repo. Everything below was observed in this run **[V]**.

## Summary

- **The workflow carries over, the enforcement does not.** CI, the docs checks and the Docker secret scan all ran and passed on a private repo. GitHub refused the ruleset and classic branch protection, so nothing stopped an unapproved merge or a direct push to `main`.
- **The `GITHUB_TOKEN` can read the `codeowners/errors` API on a private repo.** This was an open item in the [Phase 2 summary](./2026-10-09-phase-2-summary.md).
- **`CODEOWNERS` owners must already have write access to the repo they are named in.** A new private repo failed the owner check until the unknown owners were removed.

## Steps and observations

| Step | Observation | Evidence |
| --- | --- | --- |
| 1. Create a private repository and push this repository's `main` to it from an isolated clone | The repo is private and has the same files | `isPrivate: true`. One branch, `main` |
| 2. Apply this repository's ruleset (`.github/ruleset-main.json`) | **Refused** | `403`: `Upgrade to GitHub Pro or make this repository public to enable this feature.` |
| 3. Apply classic branch protection (one required review) | **Refused**, with the same message | `403`, the same text |
| 4. List the repository's rulesets | **Refused**, with the same message | `403`, the same text |
| 5. Open a probe pull request from a branch | The `validate-docs` workflow ran on the private repo | Run `completed` |
| 6. Read the run's steps | Checkout, Python setup and the docs check passed. The `CODEOWNERS` step **failed** and the secret scan was skipped | The step log lists `Unknown owner on line 2: make sure @inotivesgames exists and has write access to the repository`, and the same for the email owner |
| 7. Change `CODEOWNERS` to name only the account that exists in the repo, and push | The whole run passed, including the Docker `gitleaks` scan | Every step `success`, run `success` |
| 8. Read the probe pull request's merge state with no approval | Nothing is blocking it | `mergeStateStatus: CLEAN`, no review decision |
| 9. Merge it with no approval | It merged | State `MERGED` |
| 10. Push a commit straight to `main` | It was accepted | `main` moved from `85d0119` to `0e81561` |
| 11. Clean up | The repo was archived, not deleted | The token has no `delete_repo` scope. `isArchived: true` |

## What this shows

1. **A private repo on a free account has no branch protection.** The error text says GitHub Pro, or a public repository, unlocks it. So the required PR, the one approval, the code-owner review, the required check and the block on direct pushes would all be off. CODEOWNERS would only suggest reviewers.
2. **CI is not the gate there.** `validate-docs` runs and can fail, but a failing check does not block a merge without a rule that requires it.
3. **The `GITHUB_TOKEN` is not the obstacle.** The owner check worked and returned a real error list. This closes that item for a private repo.
4. **Moving the real repo needs the owners added first.** Every account named in `CODEOWNERS` must be a collaborator with write access, or `validate-docs` fails on the owner check. This is the check doing its job, and it is a setup step to put in the move plan.
5. **Docker and the Actions steps work on a private free repo.** `actions/checkout`, `actions/setup-python` and the unpinned `gitleaks` image all ran. An organisation's Actions policy could still block them, which is the Enterprise question.

## Limits

- One run on one free personal account, so the status is **Observed**, not **Confirmed**.
- GitHub Pro, Team and Enterprise were not tested. The error text names Pro for a personal account; whether a paid plan enforces the same ruleset on a private repo is the Phase 4 check.
- Actions minutes on a private free repo were not measured.
- The throwaway repo still exists, archived, and needs deleting by hand. See the pull request description for the command.
