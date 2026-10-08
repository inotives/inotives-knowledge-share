---
title: "Phase 0 and 1 Results: Sync Behaviour"
description: What OpenKnowledge did with an editor write and with manual sync, first on an unprotected main and then under a ruleset requiring pull requests. Covers cases P0-1 to P0-4 and P1-1 to P1-3.
type: report
status: draft
owner: inotives
created_at: 2026-10-08
created_by: inotives
ai_assisted: true
---
# Phase 0 and 1 Results: Sync Behaviour

Run on 2026-10-08 as `inotives` (repository owner and admin), in a clone of this repository, with the OpenKnowledge server running. Cases are defined in the [test plan](../test-plan.md). Everything below was observed in this run **[V]**. Nothing is claimed beyond it.

## Summary

- Phase 0: nothing reaches GitHub on its own. A manual `ok sync` commits and pushes straight to `main`.
- Phase 1: the ruleset blocks that push. OpenKnowledge classifies the rejection as a protected branch, but the CLI still prints success, and it does not move the work to a branch or open a pull request.
- Consequence: contributors must work on a branch, because syncing on `main` strands a local commit.

## Phase 0: no protection

| Case | Observation | Evidence |
| --- | --- | --- |
| P0-1 | `ok init --scope project --no-skills` changed no tracked file. Generated files are gitignored | `git status` clean after init |
| P0-2 | A page written with the MCP `write` tool appeared on disk as an untracked file. No commit | `?? memo/baseline-sync-test.md` for 140s |
| P0-3 | No sync in 140 seconds. Local `HEAD` and remote `main` both stayed at `32987eb`. The server log reports `autoSyncMode: off` | Polled every 35s, four times |
| P0-4 | `ok sync` created a commit and pushed it to `main` in about 15 seconds | Commit `847e191`, `Auto-save: Updated memo/baseline-sync-test.md`, author from the local git config. Remote `main` moved from `32987eb` to `847e191` |

## Phase 1: ruleset on `main`

Ruleset `phase-1-protect-main` (id `24690905`): pull request required with 1 approval, force-push and deletion blocked, no bypass actors, code-owner review off.

| Case | Observation | Evidence |
| --- | --- | --- |
| P1-1 | `ok sync` made a local commit, then the push was rejected. Remote `main` stayed at `847e191` | Local commit `c57c46e`. GitHub message: `GH013: Repository rule violations found for refs/heads/main. Changes must be made through a pull request.` |
| P1-2 | `ok sync` and `ok push` printed `sync triggered` and `push triggered` and exited 0, although the push failed. The error appears only in `.ok/local/logs/server-current.jsonl`, classified `protected-branch`, `retryable: false`. Whether the editor UI shows it was not checked | CLI output and server log |
| P1-3 | No branch and no pull request was created. The local clone stayed on `main`, one commit ahead of `origin/main` | `git status -sb`: `main...origin/main [ahead 1]` |

## Implications for the contract

1. Add a rule to `AGENTS.md`: work on a branch named `<handle>/<topic>` and never run sync on `main`.
2. A contributor cannot rely on the CLI message to know whether work was published. Check `git status` or the pull request.
3. Recovery for a stranded commit: create a branch at it, point local `main` back at `origin/main`, push the branch and open a pull request. That is how this report's branch was made.
4. History cannot tell a person's edit from an agent's. The commit message is `Auto-save` and the author is the git user. Only the self-declared `ai_assisted` field marks agent work.

## Limits of this run

- One run, one machine, one account. Admin rights may change what the owner sees, so this is **Observed**, not **Confirmed**.
- The editor UI was not opened, so P1-2 covers the CLI and server log only.
- The research memo in the private vault quoted a 30s pull and 60s push interval. This run did not show it, so that claim is unconfirmed for this version.
