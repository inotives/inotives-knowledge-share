---
title: "X-1: Scratch Notes in OpenKnowledge and Git"
description: Report of case X-1. A note an agent wrote to _scratch/<handle>/ through OpenKnowledge was searchable and editable, stayed invisible to Git, and was skipped by check_docs. OpenKnowledge's audit does read it, and semantic search is off, so no scratch text leaves the machine.
type: report
status: draft
owner: inotives
created_at: 2026-10-12
created_by: inotives
ai_assisted: true
---
# X-1: Scratch Notes in OpenKnowledge and Git

Run on 2026-10-12 as `inotives` in the owner clone, macOS on Apple Silicon, with a local OpenKnowledge server. The case is in the [test plan](../test-plan.md). It completes the part of X-1 that the [Phase 3 report](./2026-10-09-phase-3-two-contributors.md) left open: the audit had shown that OpenKnowledge indexes a copy under `_scratch/` and that Git ignores it, but searching a scratch note and an agent writing there were not tested. Everything below was observed in this run **[V]**.

## Summary

- An agent can **write** and **edit** a note in `_scratch/<handle>/` through the OpenKnowledge tools, and the file reaches the disk.
- OpenKnowledge **search** finds the note, including text added by a later edit.
- Git **never sees it**. `git status` stays silent, `git add -A` would stage nothing from `_scratch/`, and `git check-ignore` names the rule that ignores it.
- The docs check (`check_docs.py`) **skips** `_scratch/`, so a draft there cannot block a commit.
- OpenKnowledge's **audit does read** scratch notes and warns about a dead link in one.
- **Semantic search is off** in this project, so scratch text is not sent to an embedding provider.

## Steps and observations

| Step | Observation | Evidence |
| --- | --- | --- |
| 1. Write `_scratch/inotives/x1-scratch-probe` with the `write` tool. The note held a unique phrase | The write succeeded and the file exists on disk | Reply `Written successfully`. `ls` shows `x1-scratch-probe.md` (284 bytes) |
| 2. `git status`, `git add -A --dry-run`, `git check-ignore -v` on the note | Git shows nothing and stages nothing. The ignore rule is named | `git status` printed nothing for `_scratch/`. `git check-ignore` printed `.gitignore:6:_scratch/*` and exited 0. `git ls-files _scratch` listed only `_scratch/.gitkeep` |
| 3. `search` for the unique phrase, with the default settings | One hit, the scratch note, with a snippet | `resultCount: 1`, `kind: page`, path `_scratch/inotives/x1-scratch-probe` |
| 4. The same search with `semantic: false` | The same single hit and score | Score 132.34 in both runs. The reply carried no semantic or embedding section |
| 5. `edit` the note to add a second phrase, then search for it | The edit reached disk, and search found the new text | `grep -c` of the phrase on disk returned 1. The search returned the note with the new snippet |
| 6. Re-run `git status` and `git add -A --dry-run` after the edit | Still nothing from `_scratch/` | Both printed nothing |
| 7. Run `check_docs.py` with the note present | It checked the same 22 files as before and reported 0 problems. Its own header says `_scratch/ is never checked` | `checked 22 files and 1 skills, 0 problems` |
| 8. `edit` the note to add a broken link, then run `audit` | The `edit` reply and the audit both flagged the dead link as a **warning** | `1 of 32 documents with problems`, `_scratch/inotives/x1-scratch-probe.md`, `links/dead-link` |
| 9. Read the search config | Semantic search is disabled | `search.semantic.enabled` is `false` (the provider default is OpenAI `text-embedding-3-small`) |
| 10. Delete the note | The note is gone, and `git status` is clean | `delete` reply `Deleted`. `git status` printed nothing |

## What this shows

1. **`_scratch/` works as designed.** The contract says scratch is searchable and writable by agents and not backed up by Git. All three held.
2. **Nothing in scratch reaches the pull request or CI.** The pre-commit hook scans only staged changes, and `git add -A` stages nothing from `_scratch/`. So a secret written into scratch is never scanned, and it is also never committed. It stays only on the machine.
3. **A bad scratch draft cannot block a commit.** This is a difference from the X-2 finding, where an untracked bad page in a curated folder blocked unrelated commits. `check_docs.py` does not read `_scratch/`.
4. **The OpenKnowledge audit is noisy about scratch.** It reports problems in scratch notes the same way as in shared pages, so a person's local audit can list their own drafts. This is a local view only.
5. **Semantic search is the one setting that would change the privacy picture.** Scratch is indexed, so if someone turns on `search.semantic` with a provider, their scratch text would be sent to that provider. It is off now. Treat it as a setting to keep off, or to decide on deliberately, before the real knowledge base is set up.

## Limits

- One operator and one machine, and the case ran once, so its status is **Observed**, not **Confirmed**.
- Promoting a note, by moving it from `_scratch/` into a curated folder, was not tested here.
- Search with semantic search turned on was not tested.
- Another person's scratch folder was not tested. Scratch folders are per machine, so two people do not see each other's.
- After the delete, the empty folder `_scratch/inotives/` still held a `.gitkeep` file. It is ignored by Git, and this run did not check when it was created.
