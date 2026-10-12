---
title: X-3 Local Hook Run, Decisions and Test Status
description: What the local secret scan did with no scanner, with Homebrew gitleaks and with a pinned download; the hook change that came out of it; decisions on P3-5, Phase 4 and where the secret check is enforced; and a ranked list of what is left to test.
type: report
status: draft
owner: inotives
created_at: 2026-10-12
created_by: inotives
ai_assisted: true
---
# X-3 Local Hook Run, Decisions and Test Status

Run on 2026-10-12 as `inotives` in the owner clone (`core.hooksPath` set to `.githooks`, macOS on Apple Silicon). Cases are in the [test plan](../test-plan.md). Everything under **Observed** was seen first-hand **[V]**. This page is a companion to the separate X-3 and X-4 report from the `inotives-inoai` clone, which covers the CI half. It does not repeat that run.

## Summary

| Layer | Result |
| --- | --- |
| Local hook, no scanner installed | **Failed open.** A commit holding a fake token went through with only a warning |
| Local hook, gitleaks installed (Homebrew) | **Refused** the same commit |
| Local hook, pinned download (new) | Downloaded, verified and used the scanner; refused a staged fake token |
| Full scan with the pinned binary | Clean git history and working tree |

## Observed: local hook

| Step | Observation |
| --- | --- |
| Control run with nothing staged, no scanner | Doc checks passed. The hook printed `WARNING gitleaks and docker are not available; secret scan skipped` and exited 0 |
| Commit a page with three random fake credentials, no scanner | **Not refused.** A local commit was created, with the same warning |
| Install gitleaks 8.30.1 with Homebrew, undo the commit, retry | **Refused**, exit 1, `leaks found: 2` |
| Which rules matched | `github-pat` for the fake token and `generic-api-key` for the fake secret key. The fake AWS key ID was not matched, because the string used characters outside the real AWS key format. That is a flaw in the test string, not in the scanner |
| Clean-up | The test commit, page and branch were deleted. Nothing was pushed |

## Change: pinned gitleaks download in the hook

A data analyst may not have Homebrew, and Docker is a heavy ask. The hook now uses `gitleaks` from PATH if present. Otherwise it downloads gitleaks 8.30.1 once into `.bin/` (gitignored) and checks the SHA-256 against checksums pinned in the script. The checksums were copied from the checksum file on the official release page. A reviewer must compare them with the release page independently.

Tests with gitleaks removed from PATH, all **[V]** on macOS Apple Silicon:

| Case | Result |
| --- | --- |
| First run, nothing staged | Downloaded, verified and scanned. No leaks, exit 0 |
| Second run | Used the cached copy with no download |
| `git commit` with a staged fake token | Refused: `leaks found: 1`. No commit was created |
| Wrong pinned checksum | `checksum mismatch, commit refused`, exit 1. No binary was installed |
| Download fails (404) | Warned that the scan was skipped and let the commit through, exit 0 |

A first draft of the script only warned on a checksum mismatch, because the exit happened inside a subshell. It was fixed before the tests above.

Full scans with the pinned binary: the git history (26 commits) and the working-tree files (about 592 KB) both reported no leaks. A fake token in a temporary folder was detected (exit 1), so the scanner does detect.

**Not tested:** Linux, Intel Mac and Windows (the Linux and Intel Mac checksums are in the script and unrun; Windows has no pinned build and only warns).

## Open conflict: fail open or refuse

The `inotives-inoai` branch changes the same hook to **refuse** when no scanner is found, with `SKIP_SECRET_SCAN=1` as a one-off override. The change here **warns and skips** when the download fails. Given that CI blocked a planted secret in that run, the two can be combined: auto-download the pinned scanner, and refuse unless `SKIP_SECRET_SCAN=1` when the download is not possible. That combination is a proposal and is untested.

## Decisions recorded

- **CI is the enforced secret check.** The local hook is an early warning and need not be a required setup step. Nobody has to install Docker or Homebrew for a secret to be blocked from merging.
- **If CI flags a secret, rotate it.** A follow-up commit does not clear the failure, and a rewrite does not make the leak safe (see the X-3 and X-4 report).
- **P3-5 is not applicable.** Each person runs OpenKnowledge locally and shares work only through git, so two people never edit one live server. Concurrent edits go through git, which P3-1 and P3-2 covered.
- **Phase 4 stays parked** until the GitHub Enterprise account is set up.
- The plan and `AGENTS.md` were **not edited here**, to avoid conflicting with the `inotives-inoai` change to the same rows. The owner should update the X-3 and P3-5 rows and the contract wording.

## What is left to test, ranked

1. **P2-3, the `/skill/` path rule.** Skills execute and get the closest review, and only the `/memo/` rule was run.
2. **P1-2b, sync button details.** Whether clicking the paused sync button shows a reason was never checked. Otherwise "check `git status`" must go in the contract.
3. **Onboarding on a clean machine.** Follow the setup steps from a fresh clone and confirm the hook really runs, then confirm a teammate receives others' merged pages after a pull.
4. **P3-3, attribution.** `ai_assisted: false` on agent-written pages is checked by nothing.
5. **Lower:** P2-2 (unverified email), P3-1 (contradicting facts), X-1 (scratch search).

The full list of partial cases is in the test plan.
