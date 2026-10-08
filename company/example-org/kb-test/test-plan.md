---
title: Knowledge Base Test Plan
description: The test cases for the knowledge base workflow, grouped by phase, with steps, expected results and the current status of each. Results live in dated report files beside this page.
type: spec
status: draft
owner: inotives
created_at: 2026-10-08
created_by: inotives
ai_assisted: true
---
# Knowledge Base Test Plan

This page lists what we test and what each result means. Evidence for every result is in a dated report in the `results/` folder beside this page. A case changes status here only when a report supports it.

**Markers:** **[V]** observed first-hand in a run with evidence in a report. **[?]** not yet observed.

**Status values:** `Pending` (not run), `Observed` (run once, result recorded), `Confirmed` (repeated or reviewed by a second person), `Parked` (cannot be tested in the pilot setup, with the reason given).

## Accounts

| Role | Account | Access |
| --- | --- | --- |
| Owner and approver | `inotives` | Admin on the repository |
| Contributor 1 | `inotivesgames` | Write |
| Contributor 2 | `inotives-inoai` | Write |

## Execution order

1. Phase 1 follow-ups: make `validate-docs` a required check (P1-11, P1-12), then P1-5b and P1-2b. Contributor 2 authors the pull requests for P1-11 and P1-12.
2. Phase 2 prerequisites (P2-0), then P2-1 to P2-7.
3. Phase 3 and the cross-cutting cases.
4. Confirmation reruns R-1 to R-3.
5. Phase 4 when GitHub Enterprise is available.

## Phase 0: baseline, no protection

| ID | Case | Steps | Expected | Status |
| --- | --- | --- | --- | --- |
| P0-1 | `ok init` leaves tracked files alone | Run `ok init --scope project --no-skills`, then `git status` | No tracked change | Observed **[V]** |
| P0-2 | An editor write stays local | Write a page through the OpenKnowledge `write` tool | File on disk, nothing committed | Observed **[V]** |
| P0-3 | Timed auto-sync | Wait 140 seconds after a write | Documented behaviour: pull every ~30s, push every ~60s | Observed **[V]**: no sync, server mode `off` |
| P0-4 | Manual `ok sync` on unprotected `main` | Run `ok sync` | Commit and push to `main` | Observed **[V]** |

## Phase 1: ruleset on `main` (PR and 1 approval, no bypass)

The ruleset as first created does not require `validate-docs`, so a failing check would not block a merge. `AGENTS.md` says the check must pass, so P1-11 and P1-12 close that gap.

| ID | Case | Steps | Expected | Status |
| --- | --- | --- | --- | --- |
| P1-1 | Ruleset blocks the editor's push | Write a page, run `ok sync` | Push rejected | Observed **[V]** |
| P1-2 | The user is told it failed | Read the CLI output after P1-1 | A clear error | Observed **[V]**: the CLI printed success. UI not checked **[?]** |
| P1-2b | The editor UI shows the failure | After a deliberately rejected sync, open the page with `ok open <doc>` and read what the UI shows. Done by the owner, because the UI cannot be driven from the CLI | A visible error. If nothing is shown, checking `git status` becomes mandatory in the contract | Pending |
| P1-3 | OpenKnowledge moves work to a branch or opens a PR | Look for a new branch or PR after P1-1 | Either, or neither | Observed **[V]**: neither |
| P1-4 | `validate-docs` runs on a PR | Open a PR, read the checks | The check runs and reports | Observed **[V]**: passed in 16s |
| P1-5 | The owner cannot approve their own PR | Approve as `inotives` | Blocked | Observed **[V]**: approval refused |
| P1-5b | The owner cannot merge before any approval | Open a PR as `inotives`, then run `gh pr merge` with no approval | Blocked by the ruleset | Observed **[V]**: refused, `base branch policy prohibits the merge` |
| P1-5c | An admin cannot override the ruleset | Run `gh pr merge --admin` on a low-stakes PR with no approval. Run by the owner, because it tries to override a review rule | Refused, since the ruleset has no bypass actors **[?]**. If it merges, "no bypass" does not hold | Observed **[V]**: refused, `At least 1 approving review is required by reviewers with write access` |
| P1-6 | A contributor's approval satisfies the rule | Approve as `inotivesgames`, then merge as `inotives` | Merge allowed | Observed **[V]**: merged as `b15c96e` |
| P1-7 | A non-admin cannot push to `main` | Push directly to `main` as `inotivesgames` | Rejected | Observed **[V]**: rejected |
| P1-8 | Editor on a feature branch | Switch to a branch, write, run `ok sync` | Pushes the branch, no `main` change | Observed **[V]**: branch not pushed, sync still targeted `main` and switched itself off. Plain git push of the branch worked |
| P1-9 | Where the editor commits | After P1-8, run `git log origin/main..main` | Nothing, if the editor respects the checked-out branch | Observed **[V]**: an `Auto-save` commit sat on local `main` |
| P1-10 | Editor after a branch switch | Switch branches under a running server, then edit a page it already had open | The edit reaches disk | Observed **[V]**: five edits reported applied but never reached disk. A server restart fixed it |
| P1-11 | A failing check blocks the merge once it is required | Add `validate-docs` (job `check`) as a required status check. As `inotives-inoai`, open a PR with broken frontmatter | CI fails and the merge is blocked even after approval | Observed **[V]**: approved but `BLOCKED`, merge refused |
| P1-12 | Fixing the failure allows the merge | Push a fix to the same PR, get approval, merge | CI passes and the merge is allowed | Observed **[V]**: CI passed, merged as `4713188` |
| P1-13 | An approval survives a later push | After approval, push a content change to the same PR | Whether the approval stands depends on `dismiss_stale_reviews_on_push` | Observed **[V]**: approval stood, because the setting is off |
| P1-14 | Dismiss stale approvals on push | Turn on `dismiss_stale_reviews_on_push`, approve a PR, then push another commit | The approval is dismissed and the PR needs a new review | Observed **[V]**: approval became `DISMISSED`, PR `REVIEW_REQUIRED` and `BLOCKED`. The state before the push was not captured, so repeat with both reads |

## Phase 2: code owners

| ID | Case | Steps | Expected | Status |
| --- | --- | --- | --- | --- |
| P2-0 | Prerequisite: the throwaway emails are verified on their accounts | Owner checks Settings, Emails, for `inotivesgames` and `inotives-inoai` and records the result | Both verified. If not, P2-2 can show only the failure case | Pending |
| P2-1 | Owner by `@username` resolves | Add `CODEOWNERS`, open a PR | Owner is requested as reviewer | Pending |
| P2-2 | Owner by work email resolves | Use a verified email instead | Resolves only if the email is verified on the account **[?]** | Pending |
| P2-3 | Path-specific rule, last match wins | Add a rule for `/skill/` | Contributor owns that path | Pending |
| P2-4 | Code-owner review is enforced | Turn on `require_code_owner_review` | Merge blocked without owner approval | Pending |
| P2-5 | A nonexistent owner | Add a line with an account that does not exist | GitHub flags an error on the file. Whether it blocks a PR is unknown **[?]** | Pending |
| P2-6 | The owner authors a PR on a path only they own | With `* @inotives` and code-owner review required, `inotives` opens a PR | Nobody can satisfy the rule, so the PR deadlocks **[?]** | Pending |
| P2-7 | A second code owner resolves P2-6 | Add `@inotivesgames` as a second owner of the same path, then repeat P2-6 | The second owner's approval satisfies the rule **[?]** | Pending |

## Phase 3: two contributors

Contributor 2 (`inotives-inoai`) and contributor 1 (`inotivesgames`) are the two authors.

| ID | Case | Steps | Expected | Status |
| --- | --- | --- | --- | --- |
| P3-1 | Same page, different lines | Both edit one page on separate branches | Clean merge, facts may still disagree | Pending |
| P3-2 | Same lines | Both edit the same lines | Conflict is visible, never auto-resolved | Pending |
| P3-3 | Attribution in history | Compare commit author, `created_by` and `ai_assisted` | Author matches the account **[?]** | Pending |
| P3-4 | Agent edit with and without OpenKnowledge | One agent edits a page with plain files and git, another through the OpenKnowledge tools. Compare what each catches: broken links, orphan pages, frontmatter, attribution | Shows what OpenKnowledge adds beyond Git | Pending |
| P3-5 | Two people on one live OpenKnowledge server | Two people edit the same page at the same time on one server | Not testable in the pilot setup. The server binds to localhost by default, and shared multi-user use is unverified **[?]** | Parked |

## Cross-cutting

| ID | Case | Steps | Expected | Status |
| --- | --- | --- | --- | --- |
| X-1 | `_scratch/` is searchable in OpenKnowledge, writable by agents, and ignored by Git | Write and search a scratch note | Indexed, not tracked | Pending |
| X-2 | Pre-commit hook blocks bad frontmatter and a broken link | Commit a bad page | Commit refused | Observed **[V]** for invalid frontmatter: refused with four errors. Broken link not tested |
| X-3 | Pre-commit and CI catch a planted fake secret | Stage a dummy key pattern | Commit refused, CI fails | Pending |

## Confirmation reruns

A full rerun is not worth the cost for a pilot. These three carry the design, so they are repeated with a different account in a fresh clone to move them from `Observed` to `Confirmed`.

| ID | Repeats | Steps | Status |
| --- | --- | --- | --- |
| R-1 | P1-1 | `inotives-inoai` writes a page in a fresh clone and runs `ok sync` on `main` | Pending |
| R-2 | P1-5 and P1-6 | `inotives-inoai` authors a PR, `inotivesgames` approves, `inotives` merges | Pending |
| R-3 | P1-8 | `inotives-inoai` writes on a feature branch and runs `ok sync` | Pending |

## Phase 4: Enterprise smoke test

Re-run P1-1, P1-5 to P1-7 and P2-1 on GitHub Enterprise once it is available, plus SSO and organisation-level rulesets, which free accounts cannot show.

## How to add a result

1. Run the case. Copy the exact command output or commit hash as evidence.
2. Add a new file `results/<YYYY-MM-DD>-<slug>.md` with `type: report`. Never append to an earlier report.
3. Update the status of the case here in the same pull request, and link the report.
