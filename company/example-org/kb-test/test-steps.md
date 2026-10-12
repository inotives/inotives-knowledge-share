---
title: Knowledge Base Test Steps
description: Exact commands to run the confirmation reruns R-1 to R-3 and the cases that are still open, with the expected result of each. Results go in dated reports beside the test plan.
type: spec
status: draft
owner: inotives-inoai
created_at: 2026-10-12
created_by: inotives-inoai
ai_assisted: true
---
# Knowledge Base Test Steps

The [test plan](./test-plan.md) says what each case means. This page says how to run one. A result is recorded in a new dated file in `results/`, as the plan describes.

## Setup

Run once per account. Replace `<account>` with `inotivesgames` or `inotivesinoai` for the SSH alias, and with `inotives-inoai` for the GitHub login where it differs.

1. **SSH.** `~/.ssh/config` holds one alias per account, with `IdentitiesOnly yes`. Check it with `ssh -T git@github-<account>`. Expect `Hi <login>! You've successfully authenticated`.
2. **Clone, one per account, in `~/workspaces`.**
   ```
   git clone git@github-<account>:inotives/inotives-knowledge-share.git inotives-knowledge-share-<account>
   ```
3. **Identity and hook, inside each clone.**
   ```
   git config user.name <login>
   git config user.email <login email>
   git config core.hooksPath .githooks
   ```
   Without `core.hooksPath` the clone runs no local check.
4. **GitHub CLI.** Run `gh auth login -h github.com -p https -w` once per account, signed in to that account in the browser. Check with `gh auth status`.
5. **One identity per command.** Prefix every `gh` call with `GH_TOKEN=$(gh auth token -u <login>)`. Do not run `gh auth switch`. Add `-R inotives/inotives-knowledge-share` when the command is not run inside a clone.

| Account | Role | SSH alias |
| --- | --- | --- |
| `inotives` | Owner and approver, `Admin` | the owner's own clone |
| `inotivesgames` | Contributor 1, `Write` | `github-inotivesgames` |
| `inotives-inoai` | Contributor 2, `Write` | `github-inotivesinoai` |

## Done: confirmation reruns

These were run on 2026-10-12. Results are in the [confirmation report](./results/2026-10-12-confirmation-reruns.md).

### R-1: a write on `main`, then `ok sync`

Run as `inotives-inoai`, in the clone.

1. `git checkout main && git pull --ff-only`. Note `git rev-parse --short HEAD` and `git rev-parse --short origin/main`.
2. `ok init --scope project --no-skills`, then `git status`. Expect it clean.
3. In a second terminal, run `ok start` in the clone and leave it running.
4. Write a page under `concept/` with the frontmatter from `memo/.ok/templates/note.md`. `git status -sb` should show it untracked and `main...origin/main` level.
5. `ok sync`, wait 20 seconds, `git fetch`.
6. `git status -sb`, `git log --format='%h %an <%ae> %s' -2`, `git rev-parse --short origin/main`.
7. Read the server log: `grep -i 'protected\|GH013\|auto-disabled' .ok/local/logs/server-current.jsonl`.
8. Clean up: `git reset --hard origin/main`.

**Expect:** the CLI prints success and exits 0. A local `Auto-save` commit sits on `main`. `origin/main` does not move. The log shows `protected-branch` and `GH013`, then `auto-disabled`.

### R-2: author, approve, merge

1. As `inotives-inoai`: `git checkout -b inotives-inoai/r2-confirmation`, add a page, commit, `git push -u origin HEAD`.
2. `GH_TOKEN=$(gh auth token -u inotives-inoai) gh pr create --base main --title "R-2: confirmation run" --body "..."`.
3. As `inotives`: `gh pr checks <n>`, then `gh pr view <n> --json mergeStateStatus,reviewDecision,reviewRequests`.
4. As `inotivesgames`: `gh pr review <n> --approve`, then read the state again.
5. As `inotives`: `gh pr merge <n> --squash`, then `gh pr view <n> --json state,mergeCommit,mergedBy,author`.

**Expect:** the check passes. Before approval the state is `BLOCKED` and `REVIEW_REQUIRED`. After approval it is `CLEAN` and `APPROVED`. The merge succeeds.

Not run: merge before approval (covered by P1-5b) and the owner approving their own PR (P1-5).

### R-3: a write on a feature branch, then `ok sync`

Run as `inotives-inoai`, with the server from R-1 still running.

1. `git checkout -b inotives-inoai/r3-confirmation` from `main`.
2. Write a page under `concept/`.
3. Note `branch`, `HEAD`, local `main` and `origin/main`.
4. `ok sync`, wait 20 seconds, `git fetch`, read the same refs, `git log main -2`, `git ls-remote --heads origin`.
5. Clean up: delete the page, `git checkout main`, `git reset --hard origin/main`, `git branch -D inotives-inoai/r3-confirmation`.

**Expect:** the branch does not move and is not pushed. An `Auto-save` commit appears on local `main`. Only `refs/heads/main` is on the remote.

### X-3: a planted fake secret

Run as `inotives-inoai` on 2026-10-12. Results are in the [X-3 and X-4 report](./results/2026-10-12-x3-x4-secret-and-path-checks.md).

1. `git checkout -b inotives-inoai/x3-secret-probe`. Add a page under `concept/` with valid frontmatter and two lines: an AWS-shaped access key and a secret key line. Both must be fake.
2. `git add` and `git commit`. **Expect:** refused by the hook. With no scanner the hook now refuses too. Before the fix it printed `secret scan skipped` and let the commit through.
3. Push, then `gh pr create --draft`. Wait for CI, then read `gh pr checks <n>` and the `Scan for secrets` step log.
4. As `inotivesgames`, `gh pr review <n> --approve`. **Expect:** still `BLOCKED`.
5. Delete the key lines in a new commit and push. **Expect:** `check` still fails, because the scan reads history.
6. Rewrite the branch: `git reset --soft origin/main`, recommit the page without the key, `git push --force-with-lease`. **Expect:** `check` passes and the approval is dismissed.
7. `gh pr close <n> -d`. Never merge a probe.

A real secret that reached GitHub must be rotated. A rewrite does not remove it from GitHub's records.

### X-4: a personal local path

Run as `inotives-inoai` on 2026-10-12. The rule is in `.github/scripts/check_docs.py` and flags a macOS, Linux or Windows home path with a user name anywhere in a curated page, code fences included. A page that documents the rule cannot quote a real-looking path, because it would fail itself. Use `<name>` in documentation.

1. `git checkout -b inotives-inoai/x4-path-probe`. Add a page whose body has a home path once in prose and once in a code fence.
2. `python3 .github/scripts/check_docs.py`. **Expect:** one error per line and exit 1.
3. `git commit`. **Expect:** refused by the hook.
4. `git commit --no-verify`, push, `gh pr create --draft`. **Expect:** `check` fails in the step `Check frontmatter, links and skills`.
5. As `inotivesgames`, approve. **Expect:** still `BLOCKED`.
6. Replace the paths with `~`, push. **Expect:** `check` passes and the approval is dismissed.
7. `gh pr close <n> -d`.

Also check that `~/...` and an angle-bracket placeholder pass.

## Open cases

Nothing here has been run. Each one must get its own dated report before its status changes in the plan.

### P2-2: the unverified email

1. On a branch, add a `CODEOWNERS` line that names an email not verified on any account.
2. Read `gh api repos/inotives/inotives-knowledge-share/codeowners/errors`.
3. Open a PR touching that path and read the review requests.

**Expect:** an error on the line and no reviewer for the path.

### P2-3: a path rule for `/skill/`

1. Add `/skill/ @inotivesgames` to `CODEOWNERS` and merge it, because GitHub reads the file from the base branch.
2. Open a PR that touches `skill/`, then one that touches `concept/`.

**Expect:** the first requests `inotivesgames`, the second requests the owners of `*`.

### P3-1: contradicting facts

1. Two accounts edit different lines of one page, each stating a conflicting fact, on separate branches.
2. Merge both.

**Expect:** a clean merge with a page that contradicts itself, which shows that Git cannot catch a factual conflict.

### P3-3: unattributed changes

1. Read the ruleset with `gh api repos/inotives/inotives-knowledge-share/rulesets/24690905`.
2. Check whether `require_extra_approval_for_unattributed_changes` is set.
3. Make a commit whose author is not the pushing account, open a PR and read the state.

### X-1: scratch search and agent write

1. Write a note into `_scratch/<handle>/` through the OpenKnowledge `write` tool.
2. Search for a phrase from the note with the OpenKnowledge `search` tool.
3. `git status` and `git check-ignore -v _scratch/<handle>/<file>`.

**Expect:** found by search, ignored by Git.

### P1-2b: the sync button details

1. After a rejected sync, run `ok open <doc>`.
2. Click the sync button and read what it shows.

### Phase 4: GitHub Enterprise smoke test

Re-run P1-1, P1-5 to P1-7 and P2-1, then add SSO and an organisation ruleset. Free accounts cannot show these.
