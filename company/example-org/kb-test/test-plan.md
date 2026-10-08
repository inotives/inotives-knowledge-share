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

**Status values:** `Pending` (not run), `Observed` (run once, result recorded), `Confirmed` (repeated or reviewed by a second person).

## Accounts

| Role | Account | Access |
| --- | --- | --- |
| Owner and approver | `inotives` | Admin on the repository |
| Contributor 1 | `inotivesgames` | Write |
| Contributor 2 | `inotives-inoai` | Write |

## Phase 0: baseline, no protection

| ID | Case | Steps | Expected | Status |
| --- | --- | --- | --- | --- |
| P0-1 | `ok init` leaves tracked files alone | Run `ok init --scope project --no-skills`, then `git status` | No tracked change | Observed **[V]** |
| P0-2 | An editor write stays local | Write a page through the OpenKnowledge `write` tool | File on disk, nothing committed | Observed **[V]** |
| P0-3 | Timed auto-sync | Wait 140 seconds after a write | Documented behaviour: pull every ~30s, push every ~60s | Observed **[V]**: no sync, server mode `off` |
| P0-4 | Manual `ok sync` on unprotected `main` | Run `ok sync` | Commit and push to `main` | Observed **[V]** |

## Phase 1: ruleset on `main` (PR and 1 approval, no bypass)

| ID | Case | Steps | Expected | Status |
| --- | --- | --- | --- | --- |
| P1-1 | Ruleset blocks the editor's push | Write a page, run `ok sync` | Push rejected | Observed **[V]** |
| P1-2 | The user is told it failed | Read the CLI output after P1-1 | A clear error | Observed **[V]**: the CLI printed success. UI not checked **[?]** |
| P1-3 | OpenKnowledge moves work to a branch or opens a PR | Look for a new branch or PR after P1-1 | Either, or neither | Observed **[V]**: neither |
| P1-4 | `validate-docs` runs on a PR | Open a PR, read the checks | The check runs and reports | Pending |
| P1-5 | The owner cannot approve their own PR | Approve and merge as `inotives` | Blocked | Pending |
| P1-6 | A contributor's approval satisfies the rule | Approve as `inotivesgames`, then merge as `inotives` | Merge allowed | Pending |
| P1-7 | A non-admin cannot push to `main` | Push directly to `main` as `inotivesgames` | Rejected | Pending |
| P1-8 | Editor on a feature branch | Switch to a branch, write, run `ok sync` | Pushes the branch, no `main` change | Pending |

## Phase 2: code owners

| ID | Case | Steps | Expected | Status |
| --- | --- | --- | --- | --- |
| P2-1 | Owner by `@username` resolves | Add `CODEOWNERS`, open a PR | Owner is requested as reviewer | Pending |
| P2-2 | Owner by work email resolves | Use a verified email instead | Resolves only if the email is verified on the account **[?]** | Pending |
| P2-3 | Path-specific rule, last match wins | Add a rule for `/skill/` | Contributor owns that path | Pending |
| P2-4 | Code-owner review is enforced | Turn on `require_code_owner_review` | Merge blocked without owner approval | Pending |

## Phase 3: two contributors

| ID | Case | Steps | Expected | Status |
| --- | --- | --- | --- | --- |
| P3-1 | Same page, different lines | Both edit one page on separate branches | Clean merge, facts may still disagree | Pending |
| P3-2 | Same lines | Both edit the same lines | Conflict is visible, never auto-resolved | Pending |
| P3-3 | Attribution in history | Compare commit author, `created_by` and `ai_assisted` | Author matches the account **[?]** | Pending |

## Cross-cutting

| ID | Case | Steps | Expected | Status |
| --- | --- | --- | --- | --- |
| X-1 | `_scratch/` is searchable in OpenKnowledge, writable by agents, and ignored by Git | Write and search a scratch note | Indexed, not tracked | Pending |
| X-2 | Pre-commit hook blocks bad frontmatter and a broken link | Commit a bad page | Commit refused | Pending |
| X-3 | Pre-commit and CI catch a planted fake secret | Stage a dummy key pattern | Commit refused, CI fails | Pending |

## Phase 4: Enterprise smoke test

Re-run P1-1, P1-5 to P1-7 and P2-1 on GitHub Enterprise once it is available, plus SSO and organisation-level rulesets, which free accounts cannot show.

## How to add a result

1. Run the case. Copy the exact command output or commit hash as evidence.
2. Add a new file `results/<YYYY-MM-DD>-<slug>.md` with `type: report`. Never append to an earlier report.
3. Update the status of the case here in the same pull request, and link the report.
