---
title: Setup
description: "Set up your machine to contribute to this knowledge base: check what you have, install what is missing, sign in, configure the clone and prove the checks work. Written so that a person or their agent can follow it step by step."
---
# Setup

This page takes a machine from "cloned the repo" to "ready to contribute". It takes about fifteen minutes. You can follow it yourself, or tell your agent:

> Follow `SETUP.md` from the top. Run each step's check and compare it with the expected result before moving on. Stop at the first step that fails and tell me. Ask me before you install anything.

A wizard, `onboard.py`, checks all of this for you and does steps 5 to 8 where it is safe to. Run `uv run onboard.py` (or `python3 onboard.py` without `uv`). It never installs system tools: it prints the command for each missing one. `--check` makes it read-only. The steps below are what it does, so you can also follow them by hand.

## Rules for an agent following this page

1. Do the steps in order. After each one, run its **Check** and compare the result with what is expected.
2. **Ask the person before installing anything** or running a command that changes their machine, and show the command first. Never pipe a download straight into a shell: show the person the address and ask.
3. Install only the tools listed here.
4. Never enable OpenKnowledge's semantic search and never add an embedding API key. See [AGENTS.md](./AGENTS.md#rules-for-agents).
5. If `git config user.email` is empty or is not a company address, stop and ask for the address. Never invent one.
6. Stop at the first failed check and report it. Do not work around it. If the fix needs an account action, such as accepting an invite or signing in, say so.
7. Never write a password, token or key into this repository.

## Before you start (by hand, once)

- A GitHub account with a verified company email, and an accepted invitation to this repository with write access.
- You have already cloned the repository. That needs `git`, `gh` and a GitHub sign-in, which the [README](./README.md) explains under "Before you clone".

## Step 1: Check what you already have

Run each check. A tool that is missing or too old goes on your install list for step 2.

| Tool | Used for | Check | Expected |
| --- | --- | --- | --- |
| `git` | Branches and commits | `git --version` | `git version 2.` or later |
| `gh` | Sign-in, clone and pull requests (required) | `gh --version` | `gh version 2.` or later |
| `uv` | Runs the wizard and brings its own Python | `uv --version` | `uv 0.` and a number |
| `python3` | The docs check and the hook, if you do not use `uv` | `python3 --version` | `Python 3.9` or later |
| Node.js | OpenKnowledge, unless you use its desktop app | `node --version` | `v24` or later |
| `ok` | The OpenKnowledge command | `ok --version` | a version number |
| `claude` | Claude Code, the agent | `claude --version` | a version number |

You need `uv` **or** `python3`, not both. Docker is not needed.

## Step 2: Install what is missing

Install only what step 1 showed missing. The commands below were not run for this page, so check them against each tool's own documentation **[?]**.

| Tool | macOS | Windows | Linux |
| --- | --- | --- | --- |
| `git` | `xcode-select --install`, or `brew install git` | `winget install Git.Git` | your package manager |
| `gh` | `brew install gh` | `winget install GitHub.cli` | your package manager, or GitHub's install page |
| `uv` | `brew install uv` | `winget install astral-sh.uv` | uv's install page |
| Node.js 24 | `brew install node` | `winget install OpenJS.NodeJS` | your package manager |

OpenKnowledge and Claude Code have their own installers. Use each one's own instructions: [OpenKnowledge](https://github.com/inkeep/open-knowledge) and [Claude Code](https://code.claude.com/docs). Company laptops may need IT to approve an installer first.

**Check:** repeat step 1 for the tools you installed. Open a new terminal first, so the new commands are on your path.

## Step 3: Sign in to GitHub

```
gh auth login
```

Choose GitHub.com, choose HTTPS, and say yes when it offers to set up git credentials. That one sign-in covers `git` and `gh`, so no SSH key is needed. If you already use SSH keys and prefer them, see [INSTRUCTIONS.md](./INSTRUCTIONS.md#22-ssh-key); say no to the credentials offer in that case.

**On GitHub Enterprise** you will sign in to your company's host instead of github.com, and you may need to authorise your token for single sign-on. This page will give the exact command once the Enterprise details are known.

**Check:** `gh auth status` says you are logged in to github.com.

## Step 4: Run the wizard

```
uv run onboard.py          # or: python3 onboard.py
```

It goes through every step in one pass and prints one line each: `OK`, `FIXED` (it changed something local and safe), `TODO` (you must act, with the command) or `WARN`. It asks only for what it cannot know: your git name and email. Fix the `TODO` lines and run it again; a step that passes is skipped. `uv run onboard.py --check` changes nothing. It covers steps 5 to 8. The `ok init` step stays manual, because it wires your editors.

**Check:** the summary ends with `Ready.` Not yet tested on a clean machine (case X-5), so treat a surprising result as a bug and tell the owner.

## Step 5: Set your identity

```
git config user.name "<Your Name>"
git config user.email "<you>@<company-domain>"
```

Use your company email, verified on your GitHub account. Your **handle** is the part before the `@`, and it names your branches. A GitHub `noreply` address is not accepted.

**Check:** `git config user.email` prints your company address.

## Step 6: Turn on the hook

```
git config core.hooksPath .githooks
```

The hook runs the docs check, then scans your staged changes for secrets. It protects only people who turn it on. The check on GitHub is the one that cannot be skipped.

**Check:** `git config core.hooksPath` prints `.githooks`.

## Step 7: Set up OpenKnowledge

```
ok init --scope project --no-skills
```

This wires the OpenKnowledge tools into your editors for this project only. It changes no tracked file. Then keep semantic search off, because it would send page text to an outside provider (see [INSTRUCTIONS.md](./INSTRUCTIONS.md#24-set-up-openknowledge)).

**Check:** `git status` shows no changed tracked file, and `search.semantic.enabled` reads `false` in your OpenKnowledge settings.

## Step 8: Prove it works

1. Run the docs check:
   ```
   python3 -I .github/scripts/check_docs.py
   ```
   **Expected:** it ends with `0 problems`.
2. Run the hook once with nothing staged. The first run downloads the pinned `gitleaks` into `.bin/` (macOS and Linux):
   ```
   sh .githooks/pre-commit
   ```
   **Expected:** the docs check passes and the scan ends with `no leaks found`.
3. Confirm the hook refuses a bad page, on a throwaway branch:
   ```
   git switch -c <handle>/setup-check
   printf '# no frontmatter\n' > memo/setup-check.md
   git add memo/setup-check.md
   git commit -m "setup check"
   ```
   **Expected:** the commit is **refused** with `missing frontmatter`. Then clean up:
   ```
   git restore --staged memo/setup-check.md
   rm memo/setup-check.md
   git switch main
   git branch -D <handle>/setup-check
   ```

## Step 9: Start working

Start the OpenKnowledge server and your agent as described in [INSTRUCTIONS.md](./INSTRUCTIONS.md#part-3-start-up), then follow the daily workflow in Part 4. Draft in `_scratch/`, promote by pull request, and mark the pull request ready for review.

## If something fails

| Symptom | Likely cause | What to do |
| --- | --- | --- |
| The hook says no `gitleaks` could be found or downloaded | Offline, behind a proxy that blocks GitHub downloads, or an unsupported system such as Windows | Install `gitleaks` yourself and put it on your path. To skip the scan once, run `SKIP_SECRET_SCAN=1 git commit` and tell the owner. CI still scans every pull request |
| The hook says the checksum does not match | The download was altered or corrupted | Do not skip it. Delete `.bin/` and try again, and tell the owner if it repeats |
| `check_docs.py` names a missing README or an unknown top-level folder | A folder was added without a README, or a new top-level folder | See [Add a new folder](./workflow/new-folder/workflow.md) |
| An OpenKnowledge edit is reported as done but `git status` shows nothing | The server kept an old copy after you switched branches | Run `ok stop`, then retry. Restart the server after every branch switch |
| `git push` or `gh` says you lack access | The invite was not accepted, or the sign-in is for the wrong account | Check `gh auth status` and the invitation |
