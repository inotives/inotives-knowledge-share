---
title: "Rehearsal: From Scratch to Merged to Pulled"
description: "Report of a full run of the daily path: a contributor drafts in _scratch/, promotes the note into memo/, merges it by pull request, and a teammate pulls it and finds it in OpenKnowledge with no restart. Covers X-6, X-7 and a repeat of P1-15 under code-owner review."
type: report
status: draft
owner: inotives
created_at: 2026-10-12
created_by: inotives
ai_assisted: true
---
# Rehearsal: From Scratch to Merged to Pulled

Run on 2026-10-12 on macOS, with a local OpenKnowledge server per clone. The cases are in the [test plan](../test-plan.md): X-6 (a teammate receives merged pages), X-7 (a note is promoted from `_scratch/` into a curated folder, added with this report), and a repeat of P1-15 under code-owner review. It follows the daily path in [INSTRUCTIONS.md](../../../../INSTRUCTIONS.md). Everything below was observed in this run **[V]**.

## Summary

- The whole path works: draft in scratch, promote with the OpenKnowledge `move` tool, fill the frontmatter, merge by pull request, and a teammate who pulls finds the page.
- A teammate who runs `git pull` on the same branch **does not need to restart** the OpenKnowledge server. Search found the new page, and later stopped finding it after a deletion.
- `move` carries a draft's two frontmatter fields across unchanged. The docs check then names the four fields the page is missing, so a promoted page cannot go up unfilled.
- A contributor who is a non-admin can **merge their own approved pull request** under today's rules, with code-owner review on. This closes the gap noted in P1-15, which had only been seen before code owners existed.

## Who did what

The three test accounts were operated by one person, each through its own login.

| Role | Account | Did |
| --- | --- | --- |
| Contributor A | `inotivesgames` | Drafted, promoted, opened the pull requests, merged them |
| Code owner | `inotives` | Approved both pull requests |
| Teammate | the owner clone, as `inotives` | Pulled, then searched and read the page |

The `inotives-inoai` clone was not used as the teammate, because its server had seven other clients attached and was not forced down.

## Steps and observations

| Step | Observation | Evidence |
| --- | --- | --- |
| 1. A writes `_scratch/inotivesgames/rehearsal-note` with the `write` tool | The file exists and Git ignores it | `git status` printed nothing for it. `git check-ignore` named `.gitignore:6` |
| 2. A moves it to `memo/rehearsal-note` with the `move` tool | The old path is gone. The new file is untracked. The frontmatter is the same two fields as before | Reply `Renamed _scratch/inotivesgames/rehearsal-note -> memo/rehearsal-note`. `git status`: `?? memo/rehearsal-note.md` |
| 3. Run the docs check | It names the missing fields | `missing 'type'`, `'status'`, `'owner'`, `'created_at'`, `4 problems` |
| 4. A fills the frontmatter with `edit`, then commits | The check passes and the hook runs | `0 problems`. Hook: docs check and gitleaks, `no leaks found` |
| 5. A pushes and opens pull request 52 | CI passed | `check` `SUCCESS` |
| 6. `inotives` approves | Blocked before, clean after | `BLOCKED` and `REVIEW_REQUIRED`, then `CLEAN` and `APPROVED` |
| 7. A merges its own pull request | It merged | `mergedBy inotivesgames`, merge commit `0b2b0a7` |
| 8. Before the pull, the teammate searches for the page's unique phrase with the server running | No match | `No matches`, clone at `1df716d` |
| 9. The teammate runs `git pull` on the same branch, then searches and reads, with no restart | The page is found and read at once | Clone `1df716d` to `0b2b0a7`. One search hit. `cat` shows the page and its history, with `inotivesgames` as author |
| 10. Cleanup: A branches from `main`, deletes the page with `delete`, opens pull request 53 | The delete reached disk | `git status`: ` D memo/rehearsal-note.md`. The docs check passed |
| 11. `inotives` approves and A merges pull request 53 | Merged | `mergedBy inotivesgames`, merge commit `d68ee1f` |
| 12. The teammate pulls the deletion, with the server running | The page is gone and search no longer finds it | Clone at `d68ee1f`, `ls memo` without the page, search `No matches` |

## What this shows

1. **The daily path holds end to end.** Nothing in the path needed a workaround.
2. **A pull does not stale the server; a branch switch can.** The earlier finding (P1-10) is about switching branches under a running server. Here the teammate stayed on `main` and pulled, and the server saw both the new page and its removal. The setup notes' advice to restart after switching branches is still right, and a restart after a plain pull is not needed. This was one pull on one branch, so it is not a guarantee.
3. **Promotion is safe because the docs check catches the gap.** `move` does not add the contract's fields. The check and the hook name them, so a half-filled page cannot reach review.
4. **The merge rule is the same for a contributor as for the owner.** A non-admin author merged after one code-owner approval, as the earlier P1-15 run showed before code owners existed.
5. **One thing stayed unexplained.** At the times it was read, the review-request list on pull requests 52 and 53 was empty although they were not drafts, while earlier probe pull requests did list a requested reviewer. The approval still counted and cleared the block. It was not investigated.

## Limits

- One person operated all accounts, so the approvals prove the mechanics, not independent review.
- The teammate was the owner's clone and not a different contributor's. The teammate did not edit the pulled page.
- One pull on one branch. A pull that brings in many changes, or a pull after a branch switch, was not tested.
- Free personal accounts on a public repository. How this behaves on Enterprise is untested.
- The case ran once, so its status is **Observed**, not **Confirmed**.
