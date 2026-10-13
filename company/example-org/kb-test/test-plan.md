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

**Status values:** `Pending` (not run), `Observed` (run once, result recorded), `Confirmed` (repeated or reviewed by a second person), `Parked` (cannot be tested in the pilot setup, with the reason given), `Not applicable` (the planned setup makes the case irrelevant, with the reason given), `Deferred` (it can be run, but on the pilot setup the answer would not carry over to GitHub Enterprise, so it is re-run in Phase 4, with the reason given).

## Accounts

| Role | Account | Access |
| --- | --- | --- |
| Owner and approver | `inotives` | Admin on the repository |
| Contributor 1 | `inotivesgames` | Write |
| Contributor 2 | `inotives-inoai` | Write |

## Execution order

**Done:** Phases 0 to 3 (P3-5 is not applicable), the cross-cutting cases, the confirmation reruns R-1 to R-3, P2-3, X-1 and the scratch-to-merged rehearsal (X-6 and X-7).

**Open, in the order to run:**

These come first because their answers do not depend on the GitHub plan. They are about OpenKnowledge and the workflow, and they carry over to Enterprise unchanged.

1. P1-2b, whether the sync button shows error details when clicked.
2. P3-1b, contradicting facts on different lines.
3. X-5, onboarding on a clean machine. Last, because a deployment wizard has to be designed first.

**Deferred to Phase 4:** P2-2, P3-3 and the re-runs listed under [Phase 4](#phase-4-enterprise-smoke-test), because they depend on how identity and organisations work and the pilot's free personal accounts cannot show that.

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
| P1-1 | Ruleset blocks the editor's push | Write a page, run `ok sync` | Push rejected | Confirmed **[V]** by R-1: rejected again on a fresh clone as `inotives-inoai` |
| P1-2 | The user is told it failed | Read the CLI output after P1-1 | A clear error | Observed **[V]**: the CLI printed success. UI not checked **[?]** |
| P1-2b | The editor UI shows the failure | After a deliberately rejected sync, open the page with `ok open <doc>` and read what the UI shows. Done by the owner, because the UI cannot be driven from the CLI | A visible error. If nothing is shown, checking `git status` becomes mandatory in the contract | Observed **[V]**: the button spun for about 1 second, then returned to `! Sync paused`. No error, banner or reason. The tooltip said only `sync paused`. Whether clicking the button shows details was not checked |
| P1-3 | OpenKnowledge moves work to a branch or opens a PR | Look for a new branch or PR after P1-1 | Either, or neither | Observed **[V]**: neither |
| P1-4 | `validate-docs` runs on a PR | Open a PR, read the checks | The check runs and reports | Observed **[V]**: passed in 16s |
| P1-5 | The owner cannot approve their own PR | Approve as `inotives` | Blocked | Observed **[V]**: approval refused |
| P1-5b | The owner cannot merge before any approval | Open a PR as `inotives`, then run `gh pr merge` with no approval | Blocked by the ruleset | Observed **[V]**: refused, `base branch policy prohibits the merge` |
| P1-5c | An admin cannot override the ruleset | Run `gh pr merge --admin` on a low-stakes PR with no approval. Run by the owner, because it tries to override a review rule | Refused, since the ruleset has no bypass actors **[?]**. If it merges, "no bypass" does not hold | Observed **[V]**: refused, `At least 1 approving review is required by reviewers with write access` |
| P1-6 | A contributor's approval satisfies the rule | Approve as `inotivesgames`, then merge as `inotives` | Merge allowed | Confirmed **[V]** by R-2: PR 34 by `inotives-inoai`, approved by `inotivesgames`, merged by `inotives` as `56127f0`. Earlier: merged as `b15c96e` |
| P1-7 | A non-admin cannot push to `main` | Push directly to `main` as `inotivesgames` | Rejected | Observed **[V]**: rejected |
| P1-8 | Editor on a feature branch | Switch to a branch, write, run `ok sync` | Pushes the branch, no `main` change | Confirmed **[V]** by R-3. Earlier: branch not pushed, sync still targeted `main` and switched itself off. Plain git push of the branch worked |
| P1-9 | Where the editor commits | After P1-8, run `git log origin/main..main` | Nothing, if the editor respects the checked-out branch | Confirmed **[V]** by R-3: `Auto-save` commit `7ebb120` sat on local `main` while a feature branch was checked out. Earlier: an `Auto-save` commit sat on local `main` |
| P1-10 | Editor after a branch switch | Switch branches under a running server, then edit a page it already had open | The edit reaches disk | Observed **[V]**: five edits reported applied but never reached disk. A server restart fixed it |
| P1-11 | A failing check blocks the merge once it is required | Add `validate-docs` (job `check`) as a required status check. As `inotives-inoai`, open a PR with broken frontmatter | CI fails and the merge is blocked even after approval | Observed **[V]**: approved but `BLOCKED`, merge refused |
| P1-12 | Fixing the failure allows the merge | Push a fix to the same PR, get approval, merge | CI passes and the merge is allowed | Observed **[V]**: CI passed, merged as `4713188` |
| P1-13 | An approval survives a later push | After approval, push a content change to the same PR | Whether the approval stands depends on `dismiss_stale_reviews_on_push` | Observed **[V]**: approval stood, because the setting is off |
| P1-14 | Dismiss stale approvals on push | Turn on `dismiss_stale_reviews_on_push`, approve a PR, then push another commit | The approval is dismissed and the PR needs a new review | Observed **[V]**: approval became `DISMISSED`, PR `REVIEW_REQUIRED` and `BLOCKED`. Repeated cleanly on PR 31 in P3-2 with both reads: `APPROVED` before the push, then `REVIEW_REQUIRED` with the approval `DISMISSED` after. Also seen on PR 24 in P2-8, where a failing check was blocking too |
| P1-15 | A contributor merges their own approved PR | A non-admin author gets one approval and a passing check, then runs `gh pr merge` | Merge allowed, if write access is enough | Observed **[V]**: `inotives-inoai` merged PR 8 as `5b5dda0` after `inotivesgames` approved. Seen again with code-owner review on: `inotivesgames` merged its own PRs 52 and 53 after `inotives` approved (merge commits `0b2b0a7` and `d68ee1f`). See the [rehearsal report](./results/2026-10-12-rehearsal-scratch-to-merged.md) |

## Phase 2: code owners

| ID | Case | Steps | Expected | Status |
| --- | --- | --- | --- | --- |
| P2-0 | Prerequisite: the throwaway emails are verified on their accounts | Owner checks Settings, Emails, for `inotivesgames` and `inotives-inoai` and records the result | Both verified. If not, P2-2 can show only the failure case | Observed **[V]**: both emails verified, checked by the owner on the GitHub pages |
| P2-1 | Owner by `@username` resolves | Add `CODEOWNERS`, open a PR | Owner is requested as reviewer | Observed **[V]**: PR 12 got no reviewer, because GitHub reads CODEOWNERS from the base branch and `main` had none. After merge, PR 13 requested `inotives`. The file must be on `main` before it applies |
| P2-2 | Owner by work email resolves | Use a verified email instead | Resolves only if the email is verified on the account **[?]** | Observed **[V]**: PR 15 requested `inotivesgames` from `/memo/ inotives.games@gmail.com`, not `inotives`. The path rule replaced `*`. The failure case (unverified email) was not tested. **Deferred** to Phase 4: it needs an account with an unverified email, and the answer depends on how identity works on Enterprise. A nonexistent owner is already covered by P2-5 and P2-8 |
| P2-3 | Path-specific rule, last match wins | Add a rule for `/skill/` | Contributor owns that path | Observed **[V]**: the `/memo/` rule from P2-2 overrode `*` (last match wins). The `/skill/` rule was then run with `/skill/ @inotives-inoai`, who is not an owner of `*`. PR 43 requested only `inotives-inoai`, stayed `BLOCKED` after approval by `inotives` (owner of `*`) and went `CLEAN` after approval by `inotives-inoai`. A control PR on `concept/` behaved the other way round. A draft PR requested nobody. See the [report](./results/2026-10-12-p2-3-skill-path-rule.md) |
| P2-4 | Code-owner review is enforced | Turn on `require_code_owner_review` | Merge blocked without owner approval | Observed **[V]**: with the setting on, PR 15 went from `CLEAN` to `BLOCKED` although `inotives` had approved. Approval by the owner `inotivesgames` made it `CLEAN` |
| P2-5 | A nonexistent owner | Add a line with an account that does not exist | GitHub flags an error on the file. Whether it blocks a PR is unknown **[?]** | Observed **[V]**: the codeowners errors API reports `Unknown owner` for the line. The PR 16 that added it passed CI and merged. A PR touching the path (17) got no reviewer and went `CLEAN` after one ordinary approval. The line also replaced `*` for that path |
| P2-6 | The owner authors a PR on a path only they own | With `* @inotives` and code-owner review required, `inotives` opens a PR | Nobody can satisfy the rule, so the PR deadlocks **[?]** | Observed **[V]**: **no deadlock.** PR 19 by the sole owner `inotives` went `CLEAN` after approval by `inotivesgames`, who is not an owner. When the author is the only owner, the code-owner rule seems to be waived **[?]** |
| P2-7 | A second code owner resolves P2-6 | Add `@inotivesgames` as a second owner of the same path, then repeat P2-6 | The second owner's approval satisfies the rule **[?]** | Observed **[V]** in a reframed form: with `* @inotives @inotivesgames`, PR 21 by `inotives` requested `inotivesgames`. An approval from non-owner `inotives-inoai` left it `BLOCKED`. The approval from `inotivesgames` made it `CLEAN` |
| P2-8 | CI fails on an invalid code owner | Add a `codeowners/errors` step to `validate-docs`. Open one PR with a nonexistent owner and one with a real account that has no write access | Both fail `check` and stay blocked even after approval. A fix turns it green | Observed **[V]**: PR 24 (nonexistent `@inotives-no-such-user-xyz`) and PR 25 (`@octocat`) failed with `Unknown owner on line 8`. PR 24 stayed `BLOCKED` after approval. After a fix push `check` passed in 9s and the approval was `DISMISSED`. The control PR 23 passed, and `GITHUB_TOKEN` can read the API inside Actions |

## Phase 3: two contributors

Contributor 2 (`inotives-inoai`) and contributor 1 (`inotivesgames`) are the two authors.

| ID | Case | Steps | Expected | Status |
| --- | --- | --- | --- | --- |
| P3-1 | Same page, different lines | Both edit one page on separate branches | Clean merge, facts may still disagree | Observed **[V]**: pull requests 27 (`inotivesgames`, Section A) and 28 (`inotives-inoai`, Section B) both merged without conflict, as `d05192f` and `9fcab2d`. The second stayed `MERGEABLE` after the first landed, and the ruleset does not require an up-to-date branch. The two edits did not contradict each other, so "facts may disagree" is untested |
| P3-1b | Contradicting facts on different lines | Two accounts edit different lines of one page, each stating a conflicting fact, on separate branches. Merge both | A clean merge of a page that contradicts itself, which shows that Git cannot catch a factual conflict | Pending. P3-1 used independent edits, so this was not tested |
| P3-2 | Same lines | Both edit the same lines | Conflict is visible, never auto-resolved | Observed **[V]**: pull requests 30 (`inotivesgames`, 07:00) and 31 (`inotives-inoai`, 05:30) both passed CI and were `MERGEABLE` alone. After 30 merged as `63ccd47`, 31 became `CONFLICTING` and `DIRTY`, and `main` kept 07:00. A local merge showed conflict markers. After the resolving push, 31 went from `APPROVED` to `REVIEW_REQUIRED` with the approval `DISMISSED`, and merged as `e5ecff2` |
| P3-3 | Attribution in history | Compare commit author, `created_by` and `ai_assisted` | Author matches the account **[?]** | Observed **[V]** in part: for pull requests 26, 27, 28, 30 and 31 the git author, the pull request author and the clone's `git config` agree, and the committer is `GitHub`. The merger is only in the pull request. The page says `ai_assisted: false` although an agent wrote every commit, and nothing checks it. The squash title of 31 says 05:30 while its diff says 07:00. Whether `require_extra_approval_for_unattributed_changes` matters here is not shown. **Deferred** to Phase 4: the setting is about commits whose email is linked to no account, and that mapping differs on Enterprise, so a result on free personal accounts would not carry over |
| P3-4 | Agent edit with and without OpenKnowledge | One agent edits a page with plain files and git, another through the OpenKnowledge tools. Compare what each catches: broken links, orphan pages, frontmatter, attribution | Shows what OpenKnowledge adds beyond Git | Observed **[V]**: the plain agent's hook and `check_docs.py` refused the broken link and the invalid frontmatter. The OpenKnowledge `write` reply warned about the broken link, and `audit` and `links` found the link and the orphan page. OpenKnowledge did not flag the invalid frontmatter (`lint` ran no checks) and neither side flagged the false `ai_assisted`. `history` recorded the editor as the agent `claude-code`, which git does not show. Details are in the Phase 3 report |
| P3-5 | Two people on one live OpenKnowledge server | Two people edit the same page at the same time on one server | Not testable in the pilot setup. The server binds to localhost by default, and shared multi-user use is unverified **[?]** | Not applicable. In the planned setup each person runs OpenKnowledge on their own machine and shares work only through git, so two people never edit one live server. Concurrent edits are covered by P3-1 and P3-2 |

## Cross-cutting

| ID | Case | Steps | Expected | Status |
| --- | --- | --- | --- | --- |
| X-1 | `_scratch/` is searchable in OpenKnowledge, writable by agents, and ignored by Git | Write and search a scratch note | Indexed, not tracked | Observed **[V]**: an agent wrote and edited a note under `_scratch/<handle>/` through the OpenKnowledge tools, search found it (including text added by the edit), `git status` stayed silent and `git check-ignore` named `.gitignore:6`. `check_docs.py` skips `_scratch/`, and `ok audit` does read it and flags a dead link. Semantic search is off, so no scratch text leaves the machine. Promotion to a curated folder was not tested. See the [report](./results/2026-10-12-x1-scratch-search.md) |
| X-2 | Pre-commit hook blocks bad frontmatter and a broken link | Commit a bad page | Commit refused | Observed **[V]** for invalid frontmatter: refused with four errors. Broken link also refused in P3-4: `broken link './note__p3-4-does-not-exist.md'`, exit 1. The hook checks the whole working tree, so an untracked bad page blocks unrelated commits. The owner clone had no hook enabled |
| X-3 | Pre-commit and CI catch a planted fake secret | Stage a dummy key pattern | Commit refused, CI fails | Observed **[V]** in part: **CI** blocked PR 37 on both planted secrets (`aws-access-token`, `generic-api-key`), and approval did not unblock it. A fix commit did not clear it, because the scan reads history. A rewritten branch did. The **local hook failed open**: with no scanner the commit went through with a warning. The hook was changed to refuse, with `SKIP_SECRET_SCAN=1` as a one-time override. On the owner's machine, once a scanner was available, the hook did find the secret: with gitleaks installed it refused a staged fake token, and with gitleaks off PATH it downloaded a pinned, checksum-verified copy and refused too. A failed download or a wrong checksum is refused, and `SKIP_SECRET_SCAN=1` skips it once. The git history and the working tree scanned clean. See the [CI report](./results/2026-10-12-x3-x4-secret-and-path-checks.md) and the [local hook report](./results/2026-10-12-x3-local-hook-and-test-status.md) |
| X-4 | A personal local path is refused and must be written as `~/` | Commit a page containing a home-directory path, in prose and in a code fence. Then open a PR with it | The hook refuses the commit and `validate-docs` fails the PR. A `~/` path passes | Observed **[V]**: the hook refused with both lines named. CI failed PR 38 on both and approval did not unblock it. The fix to `~` turned the check green. A `~/` path and an angle-bracket placeholder passed. See the [report](./results/2026-10-12-x3-x4-secret-and-path-checks.md) |
| X-5 | A new contributor can set up on a clean machine | In a fresh clone, follow [INSTRUCTIONS.md](../../../INSTRUCTIONS.md): set the git identity, enable `core.hooksPath`, run `ok init`, then commit a page | The hook runs on the commit, downloads the pinned gitleaks once if none is installed, passes a good page and refuses a bad one | Pending. **Run last.** It needs a deployment wizard to be designed first, so that onboarding is one guided flow and not a list of commands |
| X-6 | A teammate receives merged pages | While a local OpenKnowledge server is running, another account's pull request is merged. Run `git pull`, then search for and open the new page through OpenKnowledge | The page appears without a restart, or the report records that a restart is needed | Observed **[V]**: after `git pull` on the same branch, with the server running, search found the new page and `cat` read it at once, and after a later pull that deleted it, search stopped finding it. No restart was needed. One pull on one branch, so not a guarantee. See the [report](./results/2026-10-12-rehearsal-scratch-to-merged.md) |
| X-7 | A note can be promoted from `_scratch/` into a curated folder | Draft in `_scratch/<handle>/`, then move it into a curated folder with the OpenKnowledge `move` tool on a branch, fill the frontmatter, and open a pull request | The old path is gone, the new file is a plain untracked file until added, and the docs check names any missing fields | Observed **[V]**: `move` removed the scratch file and left `memo/rehearsal-note.md` untracked with its two original frontmatter fields. `check_docs.py` named the four missing fields (`type`, `status`, `owner`, `created_at`). After the fields were added it passed, and the page merged by pull request. See the [report](./results/2026-10-12-rehearsal-scratch-to-merged.md) |
| X-8 | The setup works on a private repo on a free personal account | Create a private repo, push `main`, try the ruleset and classic branch protection, open a pull request and read the CI result, then try an unapproved merge and a direct push | If rulesets are available they apply as in the public repo | Observed **[V]**: the ruleset and branch protection were refused with `Upgrade to GitHub Pro or make this repository public`. CI ran and passed (docs check, `CODEOWNERS` check, Docker `gitleaks`), and the `GITHUB_TOKEN` could read `codeowners/errors`. An unapproved PR merged and a direct push to `main` was accepted, so nothing is enforced. `CODEOWNERS` owners must already have write access in the repo. See the [report](./results/2026-10-13-private-repo-free-plan.md) |

## Confirmation reruns

Run on 2026-10-12, with steps in [test steps](./test-steps.md). A full rerun is not worth the cost for a pilot. These three carry the design, so they are repeated with a different account in a fresh clone to move them from `Observed` to `Confirmed`.

| ID | Repeats | Steps | Status |
| --- | --- | --- | --- |
| R-1 | P1-1 | `inotives-inoai` writes a page in a fresh clone and runs `ok sync` on `main` | Observed **[V]**: push rejected, CLI printed success, `Auto-save` commit `25d6741` left on local `main`. Case P1-1 is now Confirmed. See the [confirmation report](./results/2026-10-12-confirmation-reruns.md) |
| R-2 | P1-5 and P1-6 | `inotives-inoai` authors a PR, `inotivesgames` approves, `inotives` merges | Observed **[V]** in part: PR 34 was `BLOCKED` before approval, `CLEAN` after, and merged as `56127f0`. The owner's own approval (P1-5) and a merge before approval were not repeated, so P1-6 is Confirmed and P1-5 stays Observed |
| R-3 | P1-8 | `inotives-inoai` writes on a feature branch and runs `ok sync` | Observed **[V]**: branch not pushed, sync targeted `main`, `Auto-save` commit `7ebb120` landed on local `main`. Cases P1-8 and P1-9 are now Confirmed |

## Phase 4: Enterprise smoke test

Waiting for the GitHub Enterprise account to be set up. The pilot runs on a public repository with free personal accounts, so it shows how the GitHub rules behave but not how identity and organisations work.

**Why some cases wait.** Rulesets, required checks and code-owner review are the same features on Enterprise, so those results should carry over. What can differ is identity: with SSO, verified company domains or managed accounts, a commit email maps to an account differently, and code owners can be teams. Two cases depend on that, so a result on free accounts would say little: P2-2 (an unverified email) and P3-3 (`require_extra_approval_for_unattributed_changes`). Cases about OpenKnowledge itself (X-1, P1-2b, X-5, X-6) do not depend on the GitHub plan, so they are run now.

**To run on Enterprise:**

- Re-run P1-1, P1-5 to P1-7 and P2-1.
- Re-run P2-3 (a path rule for `skill/`) and P1-15 (a contributor merges their own approved pull request). P1-15 was seen before code-owner review was switched on, and again under it on free accounts on 2026-10-12.
- Run the deferred cases P2-2 and P3-3.
- Test code owners that are teams.
- Test SSO and organisation-level rulesets.
- Confirm that the Actions `GITHUB_TOKEN` can still read the `codeowners/errors` API. It could on a private repo on a free account (X-8).
- Check whether secret push protection, if available, changes the X-3 result.

These rest on my expectation of how Enterprise behaves and should be checked against GitHub's current plan table **[?]**.

**Observed on a free personal account (X-8).** A private repository refuses both the ruleset and classic branch protection (`Upgrade to GitHub Pro or make this repository public`). CI still runs and passes there, but nothing is enforced: an unapproved pull request merges and a direct push to `main` is accepted. So a private repo needs a plan that enforces the ruleset before it holds real content. See the [report](./results/2026-10-13-private-repo-free-plan.md).

**Questions for the Enterprise admin.** None of these is known yet, and each one decides part of the setup.

1. Is it GitHub Enterprise Cloud or Enterprise Server, and which version? Server gets features by version. What is the host name people sign in to (`github.com`, a `*.ghe.com` subdomain, or a self-hosted server)? `gh auth login` and the setup guide need it.
2. Are repository rulesets and required status checks available on private repos in the plan, and can a ruleset be set at the organisation level?
3. What is the Actions policy? Are `actions/checkout` and `actions/setup-python` allowed, can a workflow run a Docker image, and are the runners hosted or self-hosted with Docker?
4. How do SSO and verified domains map a commit email to an account, and can a managed account push as the person? Does the `gh` token need to be authorised for single sign-on, and how?
5. Can code owners be teams, and who are the approvers for each path?
6. Does the company network allow downloads from GitHub release assets? The hook fetches `gitleaks` from there.
7. Is secret push protection available, and is it on?
8. Which collaborators and teams can be added to the repo before the move? Every account named in `CODEOWNERS` must have write access first, or `validate-docs` fails.

## How to add a result

1. Run the case. Copy the exact command output or commit hash as evidence.
2. Add a new file `results/<YYYY-MM-DD>-<slug>.md` with `type: report`. Never append to an earlier report.
3. Update the status of the case here in the same pull request, and link the report.
