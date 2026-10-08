---
title: "Phase 1 Summary: Branch Protection and Review"
description: Summary of every Phase 1 test, what was observed, the decisions it led to, and the items still open. Read this first; the three detailed reports hold the evidence.
type: report
status: draft
owner: inotives
created_at: 2026-10-08
created_by: inotives
ai_assisted: true
derived_from:
  - 2026-10-08-phase-0-1-sync-behaviour
  - 2026-10-08-phase-1-ruleset-and-review
  - 2026-10-08-phase-1-required-check
---
# Phase 1 Summary: Branch Protection and Review

Run on 2026-10-08 on free GitHub accounts, in a public repository with dummy content. Cases are defined in the [test plan](../test-plan.md). Evidence is in the [sync behaviour report](./2026-10-08-phase-0-1-sync-behaviour.md), the [ruleset and review report](./2026-10-08-phase-1-ruleset-and-review.md) and the [required check report](./2026-10-08-phase-1-required-check.md). This page repeats no new numbers or claims. Where it adds a result, that result is marked and added to the plan.

## Verdict

**GitHub's controls hold. OpenKnowledge's sync does not fit the contract.** Branch protection, required review, the required CI check and stale-approval dismissal all behaved as designed, including for the repository admin. The editor's sync command is the weak point: it pushes to `main` by name, hides failures and can lose edits after a branch switch. In this setup the editor writes pages and plain git publishes them.

The verdict applies to one run on free accounts with one person operating all three. It is not yet **Confirmed**, and it says nothing about GitHub Enterprise.

## What was tested

The ruleset `phase-1-protect-main` (id `24690905`) grew in three steps during the phase:

| Step | Rules on `main` |
| --- | --- |
| 1. Created | Pull request with 1 approval, force-push blocked, deletion blocked, no bypass actors |
| 2. After P1-4 to P1-10 | Added a required status check, `check` (the `validate-docs` job) |
| 3. After P1-13 | Turned on `dismiss_stale_reviews_on_push` |

## Results by theme

### The editor and sync (P0-1 to P0-4, P1-1 to P1-3, P1-2b, P1-8 to P1-10)

| Observation | Case |
| --- | --- |
| Nothing reaches GitHub on its own. Timed auto-sync was off. A manual `ok sync` on an unprotected `main` pushed straight to it | P0-3, P0-4 |
| Under the ruleset the push was rejected with `GH013`. The CLI still printed success. The error was only in a server log | P1-1, P1-2 |
| OpenKnowledge did not create a branch or a pull request | P1-3 |
| The editor UI showed a spinner for about a second after the rejected sync, then returned to `! Sync paused`, with no error and no reason. The tooltip said only `sync paused`. Auto-sync was already off before any rejection, so the UI shows the same state either way | P1-2b (new result, recorded after the summary was first written) |
| With a feature branch checked out, `ok sync` still committed to local `main`, tried `main -> main`, was rejected and switched itself off | P1-8, P1-9 |
| After branch switches under a running server, five edits were logged as applied but never reached disk. A server restart fixed it | P1-10 |
| Plain `git commit` and `git push` of a feature branch worked | P1-8 |

### Review and merge rules (P1-4 to P1-7, P1-5b, P1-5c, P1-6, P1-15)

| Observation | Case |
| --- | --- |
| `validate-docs` runs on a pull request | P1-4 |
| The owner cannot approve their own pull request | P1-5 |
| The owner cannot merge before any approval | P1-5b |
| The owner cannot override with `gh pr merge --admin`: `At least 1 approving review is required by reviewers with write access` | P1-5c (new result, added to the plan with this summary) |
| A contributor's approval satisfies the rule and the owner can then merge | P1-6 |
| A write-access, non-admin author can merge their own approved pull request: `inotives-inoai` merged pull request 8 after `inotivesgames` approved | P1-15 (new result, recorded after the summary was first written) |
| A non-admin cannot push to `main` | P1-7 |

### CI as a control (P1-11, P1-12, X-2 in part)

| Observation | Case |
| --- | --- |
| With `check` required, an approved pull request whose CI failed could not be merged. After a fix it merged | P1-11, P1-12 |
| The local pre-commit hook refused the same page with the same four errors. `--no-verify` skips it, so CI is the control and the hook is a convenience | X-2 (frontmatter only) |

### Approvals and later pushes (P1-13, P1-14)

| Observation | Case |
| --- | --- |
| With the default setting, an approval survived a later push, so approved content could change before merging | P1-13 |
| With `dismiss_stale_reviews_on_push` on, a new push turned the approval into `DISMISSED`, and the pull request went back to `REVIEW_REQUIRED` and `BLOCKED` | P1-14 (new result, added to the plan with this summary). The state before the push was not captured. The approval existed before the push, so the sequence fits, but this is the weakest result in the phase |

## Decisions made

1. Make `validate-docs` a required check, because the contract says it must pass and the first ruleset did not enforce that.
2. Dismiss approvals on every new push. Approved content must not change unreviewed.
3. Keep no bypass actors. Admin rights confer no merge shortcut, so any emergency override has to be added deliberately.
4. Publish with git, not `ok sync`.
5. Turn on automatic deletion of merged branches. Confirmed: the branch of pull request 10 was gone after its merge.

## Changes the contract needs

None of these is in `AGENTS.md` yet.

1. Work on a branch named `<handle>/<topic>`. Never run `ok sync` on `main`.
2. After any `ok sync`, run `git log origin/main..main`. A commit there is stranded and must move to a branch.
3. Do not trust the CLI's success message. Check `git status` or the pull request.
4. After switching branches, restart the OpenKnowledge server and confirm with `git status` that an edit reached disk.
5. Push all fixes before asking for review. Any push clears approvals.
6. CI is the control. The hook can be skipped.
7. A one-approver pilot needs a second person to approve the owner's own pull requests.

## Open items

| Item | Why it is open | Owner |
| --- | --- | --- |
| Whether clicking the `! Sync paused` button shows details | P1-2b only looked at the button's appearance, not what clicking it opens | Optional, `inotives` |
| P1-14 repeat with both states captured | The "before" state was missed | Next run |
| `require_extra_approval_for_unattributed_changes: true` appeared in the ruleset read-back although it was never set | Its effect is unknown | To investigate |
| `require_last_push_approval` is `false` and untested | A possible extra control on top of dismissal | To decide |
| X-2, broken-link refusal | Only the frontmatter part was run | Phase 3 or cross-cutting |
| Nothing is Confirmed | Every case ran once, with one person behind all accounts | Reruns R-1 to R-3 |
| `AGENTS.md` changes above | Not written | After Phase 2 |
| The private vault research note quoted a 30s pull and 60s push interval | This run did not show it | Correct the note |
| Enterprise behaviour | Free accounts cannot show SSO or organisation rulesets | Phase 4 |

## Housekeeping

Done after the summary was first written:

- Pull request 6 (the P1-5c probe) was closed without merging.
- All test branches were deleted. GitHub now has only `main`.
- The probe pages `memo/baseline-sync-test.md` and `memo/p1-11-broken-frontmatter.md` were removed by pull request 8. The reports mention them as plain text, so nothing links to a missing page.
- The owner's clone was reset to `origin/main`, which dropped the stranded auto-save from P1-9. The contributors' clones were tidied too.
- Automatic deletion of merged branches is on and works, as seen on pull request 10.

## Limits of Phase 1

- One person operated all three accounts, so approvals prove the rule mechanics, not independent review.
- The repository is public and on free accounts. Behaviour on GitHub Enterprise is untested.
- Every case ran once.
- The editor UI was checked for the sync button only. What clicking it shows, and anything else the UI offers, was not looked at.
