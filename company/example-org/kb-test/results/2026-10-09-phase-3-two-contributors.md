---
title: "Phase 3 Results: Two Contributors"
description: Results of P3-1 to P3-4, two contributors editing one page on different lines and on the same line, how attribution looked afterwards, and what an agent working through OpenKnowledge catches compared with plain files and git. P3-5 is parked.
type: report
status: draft
owner: inotives
created_at: 2026-10-09
created_by: inotives
ai_assisted: true
---
# Phase 3 Results: Two Contributors

Run on 2026-10-09. Cases are defined in the [test plan](../test-plan.md). **Phase 3 is done except P3-5, which is parked.** This page covers P3-1 to P3-4. Fixes are not decided yet and are not part of this page. Everything below was observed in this run **[V]** unless it is marked **[?]**. Earlier phases are in the [Phase 1 summary](./2026-10-08-phase-1-summary.md) and the [Phase 2 summary](./2026-10-09-phase-2-summary.md).

The two authors were `inotivesgames` and `inotives-inoai`. `inotives` approved and merged every pull request. The test page was `concept/note__p3-shared-page.md`, created by pull request 26 with three sections of three facts each. Ruleset state: pull request with 1 approval, code-owner review on, `validate-docs` required, approvals dismissed on push, `strict_required_status_checks_policy: false`.

## Summary

- Edits on different lines of one page merge cleanly, and the second pull request stays mergeable after the first lands.
- Edits to the same line give a visible conflict. GitHub never picks a side, and the second author has to resolve it.
- A resolving push clears the earlier approval, so the pull request needs a fresh review.
- Commit author, pull request author and the clone's git identity agree. That identity comes from `git config`, not from who typed the edit.
- Nothing checks `ai_assisted`. The page says `false` although an agent wrote every commit.
- CI passes on a conflicting or contradictory edit, because it checks structure and not meaning.
- OpenKnowledge helps while an agent writes: it warned about a broken link in the `write` reply, found an orphan page and recorded the editor as an agent. It did not validate frontmatter and did not catch a false attribution.
- The pre-commit hook and CI are the only checks that refused bad frontmatter and a broken link. They did not flag an orphan page or a false `ai_assisted`.
- `ok lint` ran no checks, because no lint rules are enabled in this project.

## Results

| Case | Observation | Evidence |
| --- | --- | --- |
| P3-1 | Pull request 27 (`inotivesgames`, Section A, the refunds line) and pull request 28 (`inotives-inoai`, Section B, the guest line) were opened against the same base. After 27 merged, 28 was still `MERGEABLE`, and it merged without a rebase. Both edits are on `main`. The edits did not contradict each other, so a factual clash was not tested | 27 merged as `d05192f`, 28 as `9fcab2d`. Base `3a4f34c`. Ruleset `strict_required_status_checks_policy: false` |
| P3-2 | Pull requests 30 (06:00 to 07:00, `inotivesgames`) and 31 (06:00 to 05:30, `inotives-inoai`) changed the same line. Both passed CI and were `MERGEABLE` alone. After 30 merged, 31 became `CONFLICTING` and `DIRTY`, and `main` kept 07:00. A local merge of `main` into the branch stopped with `CONFLICT (content)` and markers around `05:30` and `07:00` | 30 merged as `63ccd47`. 31 `mergeable: CONFLICTING`, `mergeStateStatus: DIRTY` |
| P3-2 (resolve) | With 31 approved and conflicting, the resolving merge was pushed. The approval became `DISMISSED` and the pull request `REVIEW_REQUIRED`. It became `MERGEABLE` and merged after a new approval. This is also the clean repeat of P1-14 | Before: `reviewDecision: APPROVED`, `DIRTY`. After: `REVIEW_REQUIRED`, `MERGEABLE`, `inotives: DISMISSED`. Merged as `e5ecff2` |
| P3-3 | For pull requests 26, 27, 28, 30 and 31, the git author equalled the pull request author and the clone's `git config`. The committer was `GitHub`. The merger appears only on the pull request. The page's `created_by` is `inotives-inoai`, which matches the author of its creating commit. Its `ai_assisted` is `false` | Authors `inotives-inoai <inotives.inoai@gmail.com>` and `inotivesgames <inotives.games@gmail.com>`. Merged by `inotives` on each pull request |
| P3-3 (history) | The squash commit of pull request 31 is titled "inoai moves the daily report to 05:30", but its diff is `07:00` to `07:00, after late rows land`. GitHub used the first branch commit for the title | `e5ecff2`, `git show` diff |

## P3-4: an agent with and without OpenKnowledge

Two agents of the same model wrote the same three pages with four planted defects. The **plain agent** used a file-write tool, git, the pre-commit hook and `check_docs.py`, in the `inotives-inoai` clone. The **OpenKnowledge agent** used the OpenKnowledge MCP tools and CLI in the owner's clone, from a written handoff, on a throwaway branch. It returned a report and an evidence folder. The main session checked the report against the evidence: the branch held one commit and `main` was unchanged, the committed page hashes matched the evidence copies, the reflog showed no `ok sync` and no push, and `check_docs.py`, `ok lint` and `ok audit` gave the same results when re-run.

The server had been restarted at 2026-10-09T10:08:50Z, before the agent switched branches (P1-10 trap). Every write was confirmed on disk.

The defects were D1 a broken link, D2 an orphan page, D3 invalid frontmatter (`status: wip`, no `owner`), and D4 a false attribution (`ai_assisted: false` on an agent-written page, with a `created_by` other than the committer).

| Defect | Plain agent | OpenKnowledge agent |
| --- | --- | --- |
| D1 broken link | The write tool was silent. `check_docs.py` and the hook flagged `broken link './note__p3-4-does-not-exist.md'`, and the commit was refused | The `write` reply warned `links/dead-link (warning, line 13)`. `audit` and `ok audit` flagged it, `ok audit` exited 1, and `links` listed the dead target. `lint` did not |
| D2 orphan page | Nothing flagged it | The `write` reply hinted "no backlinks yet". `links` listed the page as an orphan. `lint` and `audit` did not |
| D3 invalid frontmatter | `check_docs.py` and the hook flagged `missing 'owner'` and `status 'wip' not in [...]`, and refused the commit | Nothing flagged it. The write was accepted silently and `lint` returned `No checks ran` (`ran: []`) |
| D4 false attribution | Nothing flagged it, and the commit went through | Nothing flagged it |
| Who edited | `git log` and `git blame` show only the name and email from `git config` | `history` recorded the author `claude-code` with `agent-<uuid>@openknowledge.local` and a `contributors` entry, in OpenKnowledge's own store. The committed page and git carry no such marker |

Other things seen:

- **The hook checks the whole working tree.** With the bad page untracked in the clone, the plain agent's commit of two clean pages was refused too. It passed only after the bad page was moved out.
- **The owner clone had no hook.** `core.hooksPath` was unset in the owner's clone and set to `.githooks` in both contributor clones. The OpenKnowledge agent's commit therefore ran no hook. The hook column for that side was filled by running `check_docs.py` on its branch, which gave the same three problems as the plain side.
- **`ok lint` is a no-op here.** It reported `No checks ran`. `audit` ran only `links`. No frontmatter or markdownlint rules are enabled.
- **`write` dropped `tags: []`.** The three pages on disk had no `tags` line although the call passed it. The shared page keeps its `tags: []`.
- **`_scratch/` is indexed by OpenKnowledge and ignored by Git.** `ok audit` reported a dead link inside a copy under `_scratch/`, and `git check-ignore` confirmed the folder is ignored. Searching and agent writes were not tested separately, so X-1 is only partly observed.
- **A contract conflict surfaced.** The owner clone has `user.email` set to a personal address. `AGENTS.md` says an agent stops and asks in that case. The handoff said to proceed, so the agent proceeded and flagged it.
- **A deviation from the plan.** The agent linked page C to page A, which made A a non-orphan. `links` then listed only B as an orphan, so the default mode seems to count only pages with neither incoming nor outgoing links.

Evidence: the plain run's raw outputs are in the session scratchpad and the OpenKnowledge agent's are in `_scratch/p3-4-evidence/` of the owner's clone. Neither is committed. Page C's `created_by` and `ai_assisted` were not compared with `history` for page creation.

## What this shows about the plan

1. The two-contributor merge path works as designed. No collision was silent, and none was auto-resolved.
2. The conflict message says the lines differ, not that they are rival claims. A human has to notice that 05:30 and 07:00 disagree. Review is the control.
3. `ai_assisted` and `created_by` are honesty fields. Git identity does not tell who or what typed the change. The contract should say so.
4. Squash titles can contradict the diff. Set the squash message from the pull request title, or tell reviewers to read the diff.
5. OpenKnowledge gives feedback while an agent writes. CI and the hook are the control, because only they refused bad frontmatter and a broken link.
6. OpenKnowledge records that an agent edited, but only in its own store, so Git and the committed page do not show it. Neither tool checks that `ai_assisted` and `created_by` are true.
7. `ok lint` gives false comfort until rules are enabled. Treat "no problems" from it as "nothing was checked".
8. Hook setup is per clone. A clone without `core.hooksPath` runs no local check, including the owner's.

## Open items

| Item | Why it is open | Owner |
| --- | --- | --- |
| Enabling OpenKnowledge frontmatter and markdownlint rules | `lint` ran no checks, so D3 was invisible to it. Not tried | To decide |
| `history` for page creation, `restore_version`, `checkpoint`, behaviour after a further branch switch | Not tried in P3-4 | Optional |
| P3-5, two people on one live server | Parked. The server binds to localhost | Parked |
| Contradictory facts on different lines | P3-1 used independent edits, so a factual clash was not tested | Optional (P3-1b) |
| `require_extra_approval_for_unattributed_changes: true` | Its effect is not shown by P3-3 | To investigate |
| X-1 in full, X-3 and the reruns R-1 to R-3 | X-1 only seen through the audit. Others not run | After Phase 3 |
| Contract and setup instructions | Held until testing ends and the team has aligned | After Phase 4 |

## Limits of this run

- One person operated all three accounts, so approvals prove the rule mechanics, not independent review.
- An agent made every commit under the contributors' identities. The attribution results show how the system records identity, not who really typed.
- The repository is public and on free accounts. Behaviour on GitHub Enterprise is untested.
- Each case ran once, so statuses are **Observed**, not **Confirmed**.
- In P3-4 both agents are the same model, and each ran once. The plain side had a working hook and the OpenKnowledge side did not, so the two columns were made comparable by running the hook's script.
- The OpenKnowledge agent's report was checked against its evidence by the main session, but the evidence is not committed.
