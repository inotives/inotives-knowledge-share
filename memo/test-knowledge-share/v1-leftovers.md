---
title: v1 leftovers
description: "What is still open on the knowledge base after the onboard.py wizard merged on 2026-10-13: remaining work, decisions waiting on others, untested areas and housekeeping. Read this to pick up where v1 stopped."
type: note
status: draft
owner: inotives
created_at: 2026-10-13
created_by: inotives
ai_assisted: true
---
# v1 leftovers

State on 2026-10-13: `main` is at the merge of PR 61 (`onboard.py`), no pull requests are open, the docs check passes. The team uses Macs only, so Windows and Linux are out of scope for v1.

## Remaining work for v1

| Item | What it needs |
| --- | --- |
| X-5 clean-machine test | A clean Mac or a new macOS user account (Apple Silicon or Intel). Run `uv run onboard.py`, fix each TODO, rerun until it ends with `Ready.`, then record a dated report in [results](results/README.md) |
| v1 summary page | A page listing what v1 covers and the known gaps below |
| Tidy | Update the root README status, and move the answered cases out of the "Open cases" sections of [test-steps.md](test-steps.md) (P2-3, X-1 and others) |
| `v1.0.0` tag | The owner's go-ahead, after the items above |

## Waiting on a decision or someone else

| Item | Waiting on |
| --- | --- |
| Hosting: GitHub Enterprise or self-hosted GitLab | The company. The ruleset, Actions, `gh` and the code-owner API are GitHub-specific. The docs check, hook, conventions and OpenKnowledge workflow carry over |
| Phase 4 and the eight admin questions | The Enterprise account being set up. The questions are in [test-steps.md](test-steps.md) |
| Deferred cases P2-2 and P3-3 | The hosting decision, then rerun |
| Skill and workflow owners | An owner decision. See Open decisions in [AGENTS.md](../../AGENTS.md) |
| An `archived` status | Not needed yet. Retire pages with `status: deprecated` |
| Semantic search with an approved provider | Stays off. Allowing it later is open |

## Not tested

- Install commands in [SETUP.md](../../SETUP.md) (marked as unchecked there).
- The wizard on a clean machine (X-5), on an Intel Mac, and on any other plan or account type.
- P1-2b and P3-1b, which need a person watching the editor.
- The Calendar-connector meeting pull.
- The wizard's `ok init` check is a guess from editor config files, and its semantic-search check reads the settings files directly, not `ok config`.
- Why review-request lists were empty on some non-draft pull requests (52, 53) while the approval still counted.

## Housekeeping

- Delete the archived throwaway repo `inotives/kb-private-test-delete-me`. The token lacks `delete_repo`: run `gh auth refresh -h github.com -s delete_repo`, then `gh repo delete inotives/kb-private-test-delete-me --yes`.
- Two other clones are behind or on old branches: `inotivesgames` is on `inotivesgames/rehearsal-cleanup`, and `inotivesinoai` is on `main` but behind. Another clone's OpenKnowledge server has seven attached clients, so do not force-stop it.
- Send the eight admin questions to IT once the Enterprise account exists.

## Related

[Test plan](test-plan.md), [test steps](test-steps.md), [results](results/README.md), [SETUP.md](../../SETUP.md)
