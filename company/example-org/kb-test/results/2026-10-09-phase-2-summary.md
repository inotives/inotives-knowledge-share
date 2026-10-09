---
title: "Phase 2 Summary: Code Owners"
description: Summary of every Phase 2 test, what was observed, the decisions it led to, and the items still open. Read this first; the detailed report holds the evidence.
type: report
status: draft
owner: inotives
created_at: 2026-10-09
created_by: inotives
ai_assisted: true
derived_from:
  - 2026-10-09-phase-2-code-owners
---
# Phase 2 Summary: Code Owners

Run on 2026-10-09 on free GitHub accounts, in a public repository with dummy content. Cases are defined in the [test plan](../test-plan.md). Evidence is in the [Phase 2 report](./2026-10-09-phase-2-code-owners.md). The [Phase 1 summary](./2026-10-08-phase-1-summary.md) covers the earlier phases. This page adds no new numbers or claims.

## Verdict

**Code owners work, but a bad owner fails open.** An owner by username or verified email is requested automatically, and with code-owner review on, only an owner's approval clears the path. The risk is silence: a mistyped owner removes review from its path with no warning on the pull request. A CI step fixes that, and it was added and tested.

The verdict applies to one run on free accounts with one person operating all three. It is not yet **Confirmed**, and it says nothing about teams as owners or GitHub Enterprise.

## What was tested

| Step | State of `main` |
| --- | --- |
| Start | No CODEOWNERS. Code-owner review off |
| P2-1, P2-2 | `* @inotives` and `/memo/ inotives.games@gmail.com` added |
| P2-4 | `require_code_owner_review` turned on |
| P2-5 | A nonexistent owner added, then removed |
| P2-7 | `* @inotives @inotivesgames` |
| P2-8 | `validate-docs` gained a CODEOWNERS owner check |

## Results by theme

### How CODEOWNERS applies (P2-1 to P2-3)

| Observation | Case |
| --- | --- |
| A pull request that adds CODEOWNERS is not covered by it. The file is read from `main` | P2-1 |
| `@username` and a verified email both resolve. A path rule replaced `*` for that path | P2-1, P2-2, P2-3 in part |

### Enforcement (P2-4, P2-6, P2-7)

| Observation | Case |
| --- | --- |
| With the setting on, an approval from a non-owner no longer cleared a path. The owner's did | P2-4 |
| A sole owner did not block their own pull request. Any approver with write access cleared it. This was not expected | P2-6 |
| A second owner is requested and required. One owner's approval is enough when two are listed | P2-7 |

### Bad owners and CI (P2-5, P2-8)

| Observation | Case |
| --- | --- |
| A nonexistent owner was reported only by the errors API and the file view. The pull request that added it passed CI and merged, and the path had no owner requirement | P2-5 |
| The new CI step failed for a nonexistent owner and for a real account without write access. A failing check beat an approval. A fix turned it green and dismissed the old approval | P2-8 |

## Decisions made

1. Keep the CODEOWNERS check as part of the `check` job, so the required context name does not change.
2. Keep `require_code_owner_review` on.
3. Do not treat a sole owner as a gate. Name at least two owners on important paths.

## Changes the contract needs

None of these is in `AGENTS.md` yet. They follow the seven from the [Phase 1 summary](./2026-10-08-phase-1-summary.md).

1. CODEOWNERS must be on `main` before it applies. Name a reviewer by hand on the pull request that adds it.
2. A path rule replaces `*`. List every owner on that path.
3. Name at least two owners on any path that matters.
4. The CODEOWNERS check in `validate-docs` must stay. It is the only thing that catches a mistyped handle.

## Open items

| Item | Why it is open | Owner |
| --- | --- | --- |
| P2-3 as written (`/skill/`) | Only covered through the `/memo/` rule | Optional |
| Unverified email | The failure case of P2-2 was not run | Confirmation reruns |
| Owners as teams | Cannot be tested on a personal repository | Phase 4 |
| Why a sole owner does not block their own pull request | Two cases support it. GitHub does not document it | To confirm **[?]** |
| `GITHUB_TOKEN` on a private repository | Tested only on a public one | Phase 4 |
| P1-14 repeat with both states captured | Done in P3-2: pull request 31 showed `APPROVED` before the push and `DISMISSED` after. See the [Phase 3 report](./2026-10-09-phase-3-two-contributors.md) | Closed |
| `require_extra_approval_for_unattributed_changes: true` | Read back from the live ruleset. Its effect is unknown | To investigate |
| `require_last_push_approval` | `false`, untested | To decide |
| `AGENTS.md` changes (seven from Phase 1, four above) | Not written | After Phase 3 |
| Nothing is Confirmed | Every case ran once | Reruns R-1 to R-3 |

## Housekeeping

- Probe pull requests 13, 15, 17, 19, 21, 24 and 25 were closed without merging, and their branches deleted.
- The probe line for the nonexistent owner was removed by pull request 18. The `/memo/` email rule and `* @inotives @inotivesgames` remain in CODEOWNERS.
- `.github/ruleset-main.json` was updated to match the live ruleset.

## Limits of Phase 2

- One person operated all three accounts, so approvals prove the rule mechanics, not independent review.
- The repository is public and on free accounts. Behaviour on GitHub Enterprise is untested.
- Every case ran once.
