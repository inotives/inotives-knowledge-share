# Example Team Knowledge Base -- Team Contract

One shared repository for what the team knows and decides, written by people and their AI agents together. Stack: **OpenKnowledge** as the editor and AI control panel, **GitHub** as the only host. This file is the operating contract for both people and agents.

## Using this repository as durable memory

When an agent is started from this folder, this repository is its long-term memory. It is an OpenKnowledge project, not a code project.

**Start of a session**

- Before re-deriving context, search the knowledge base with the `open-knowledge` MCP tools (`search`, `exec`). Check `company/` for the project you are working on.
- Read and write markdown only through the `open-knowledge` MCP tools, never native file tools. Load the `open-knowledge` skill if it is not already in context.

**Saving what you learn**

- Capture new durable knowledge as a draft in `_scratch/` first.
- `_scratch/` is gitignored and unbacked. When something should last, promote it (see below).

**Precedence.** For work done from this folder, this repository is the durable memory and this file is the contract. Ignore user-level instructions that point at a different knowledge vault or that default new notes to `memo/`.

## One-time setup per clone

1. `git config user.email "<you>@example.com"` and `git config user.name "<Your Name>"` (see [Identity](#identity)).
2. `git config core.hooksPath .githooks` to turn on the local pre-commit check. It runs the same frontmatter, link and skill checks as CI, and scans staged changes for secrets with gitleaks, from your PATH or from a pinned, checksum-checked copy it downloads into `.bin/` (see [INSTRUCTIONS.md](./INSTRUCTIONS.md)). Docker is not needed.
3. `ok init` to set up OpenKnowledge and the agent tool config. Those generated files are gitignored.

The guided path is [SETUP.md](./SETUP.md), which a person or an agent can follow step by step.

The pre-commit hook protects only the people who enable it. The pull-request checks on GitHub are the ones that cannot be skipped.

## Identity

Every person has one **handle**: the part of their company email address before the `@` (for `jane.doe@example.com`, the handle is `jane.doe`). It is the same email used for their GitHub account.

- **Source:** `git config user.email`. Each person sets it once to their company email, so commits, GitHub and this repository agree.
- **Used for:** `created_by`, `owner`, `human_reviewed` and branch names (`<handle>/<topic>`).
- **An agent uses the handle of the person it is working for**, never `claude` or `agent`. The person is accountable for what the agent writes.
- **If `git config user.email` is empty, or is not a company address** (for example a GitHub `noreply` address), the agent stops and asks. It never invents a handle.

## Folders

| Folder | Status | What goes here |
| --- | --- | --- |
| `_scratch/` | **Gitignored, local only.** The folder and its README exist in git; its contents never do | Your own working notes and agent drafts. Free writes, no review, no backup |
| `memo/` | Curated | Shared notes, research and decisions that are not yet settled enough for `concept/` or `company/` |
| `concept/` | Curated | Glossary, terminology, technical reference and distilled knowledge |
| `company/<name>/<project>/` | Curated | One folder per company or client, one subfolder per project. No loose files directly under `company/<name>/` once a project has more than a few pages |
| `skill/` | Curated | Skills: atomic capabilities that define how to perform one specific task. One folder per skill with a `SKILL.md`. Skills execute, so changes here get the closest review |
| `workflow/` | Curated | Workflows: orchestrated sequences of decisions and actions that achieve a broader, end-to-end objective, and usually invoke several skills |
| `generated_output/` | Curated | Generated, shareable deliverables: HTML reports, PDFs, slide decks. Rendered from markdown sources; never the place a fact is edited |

Everything outside `_scratch/` is **curated**: it changes by pull request, not by direct push.

**Every folder under a curated folder has a `README.md`, always.** It is how a folder says what it is for and what its rules and conventions are, so a folder without one is not allowed. Create it from the `folder-readme` template, which has the same eight sections in every folder: purpose, what goes here, layout and naming, frontmatter, review and ownership, how to add, rules, related. Follow [Add a new folder](./workflow/new-folder/workflow.md). The docs check fails a folder without one. The inside of a skill (`skill/<name>/`) and of a workflow (`workflow/<name>/`) is described by its `SKILL.md` or `workflow.md` and needs no README. Each skill folder must have a `SKILL.md` and each workflow folder a `workflow.md`, and the docs check enforces both by position: a stray `SKILL.md` or `workflow.md` elsewhere excuses nothing. A new top-level folder changes this list and needs the owner's decision first. The docs check fails on an unknown top-level folder, and adding one means adding it to the list in `.github/scripts/check_docs.py`.

### Where does this go?

| You have | Put it in |
| --- | --- |
| A personal draft or rough agent notes | `_scratch/`, which is local and never shared |
| A shared note, research or decision that is not settled yet | `memo/` |
| Notes from a meeting, internal or external | `memo/meetings/`. A meeting with a client, or notes holding client material, go in that client's project folder |
| Work for a client, or a project of our own organisation | `company/<name>/<project>/` |
| A decision others must rely on | A `type: decision` page next to the project it belongs to, linked from the meeting note |
| A glossary entry, terminology or stable reference | `concept/` |
| A procedure people follow: a how-to, runbook or onboarding guide | `workflow/<name>/workflow.md` |
| An atomic capability for an agent | `skill/<name>/SKILL.md` |
| A shareable report, deck or PDF | `generated_output/`, named `<subject>-<kind>-<YYYY-MM-DD>.<ext>` |
| A page that is no longer true, or has been replaced | Leave it where it is. Set `status: deprecated` and point to what replaced it. Do not move it |
| Something that fits none of these | Ask the owner. A new top-level folder is the owner's decision |
| A password, token, or personal data about an individual | Nowhere in this repository |

## Working in _scratch

- Work in `_scratch/`, arranged however you like. Each clone belongs to one person, so no per-person folder is needed. Let agents draft there, and give every note a `title` and a `description`. Nothing else is required in scratch.
- **Nothing in `_scratch/` is saved to GitHub.** If it matters, promote it.
- **Nothing in `_scratch/` is scanned for secrets,** because the hook and CI read only staged and committed files. Keep secrets and personal data out of it. The folder's rules are in [_scratch/README.md](./_scratch/README.md).
- **Promote** by moving the file into a curated folder on a branch, filling in the frontmatter, and opening a pull request. Do not copy and leave the original behind.

## Images, data files and generated outputs

- **Images and small data files** live beside the page that uses them, in an `assets/` subfolder of that page's folder, with descriptive names (not screenshot timestamps). There is no shared asset folder.
- **Generated deliverables** go in `generated_output/`, named `<subject>-<kind>-<YYYY-MM-DD>.<ext>`, for example `platform-eval-summary-2026-10-06.html`.
- **Every figure and claim in an output must trace to a line in a markdown source page.** An output introduces no new numbers, keeps the sources' confidence markers, and keeps their draft framing. When an output is wrong, fix the source page and regenerate; never edit only the output.
- Outputs go through pull request like any curated change. Keep each file self-contained and small; large binaries bloat Git history.

## Frontmatter

Every page in a curated folder needs these fields (`README.md` files need only `title` and `description`):

| Field | Rule |
| --- | --- |
| `title`, `description` | Required by OpenKnowledge |
| `type` | `note`, `research`, `decision`, `spec`, `runbook`, `playbook`, `skill`, `reference`, `glossary`, `report` |
| `status` | `draft`, `reviewed`, `verified`, `deprecated` |
| `owner` | A person's handle (see [Identity](#identity)) or a team name. Should match `CODEOWNERS` |
| `created_at` | `YYYY-MM-DD`, set once |
| `created_by` | Recommended. The responsible person's handle, even when an agent wrote the page |
| `ai_assisted` | `true` when an agent wrote most of the page. Reviewers and CI use it to see which pages have had no human pass |
| `human_reviewed` | Required when `status` is `reviewed` or `verified`: reviewer handle and date |
| `supersedes`, `derived_from`, `sources`, `tags`, `project` | Use when they apply |

There is **no `updated_at` or `updated_by`**. Git and OpenKnowledge history already record who changed a page and when, and a timestamp line that every edit rewrites makes every pair of simultaneous edits conflict.

**Status lifecycle.** `draft` (anyone) then `reviewed` (a peer, in the pull request) then `verified` (the owner, a human only) then `deprecated` (keep the page, point to what replaced it). **Only a human sets `verified`.** An agent never promotes its own work.

## Naming

Lowercase kebab-case. A date prefix (`2026-10-06-slug.md`) only for records tied to a time: decisions, runs, meetings. The type lives in frontmatter, not in the filename.

## Concurrent edits

Git conflicts when two branches change the same or adjacent lines of one file. To keep that rare:

- **One topic per page, one owner per page.** Others propose changes by pull request instead of editing in parallel.
- **One branch per task**, named `<handle>/<topic>`, rebased on `main` before the pull request opens and merged quickly. Do not leave branches open for days.
- **No lines that every edit rewrites.** That is why pages carry no `updated_at`, `updated_by` or running version counter. For a changelog, add one file per entry instead of appending to a shared list.
- **Few shared hot files.** `AGENTS.md`, READMEs and index pages have a single owner.
- **Stay inside your topic.** An agent edits only the pages the task is about, and lists other affected pages in the pull request description instead of rewriting them.
- **On a real conflict, stop and ask the page owner.** Never auto-resolve a content conflict, because a silent resolution can keep the wrong fact. A clean merge is not proof the facts agree, so a reviewer still checks that two edits do not contradict each other.

## Pull requests

1. Branch from `main`, one branch per task, for example `<handle>/<topic>`.
2. Edit through OpenKnowledge. Run `audit` before pushing.
3. Open a pull request. The `validate-docs` check must pass. A code owner reviews.
4. Merge. Do not push curated changes straight to `main`.

The rules below come from what the tests showed. The evidence is in the [test plan](./memo/test-knowledge-share/test-plan.md).

### Publishing

- **Publish with git, never with OpenKnowledge's sync.** `ok sync` and the editor's sync button push to `main` by name even when a branch is checked out, are rejected by the branch rules, print success anyway, and can leave a commit stranded on local `main`. Use `git push` and `gh pr create`.
- **If `ok sync` was run,** check `git log origin/main..main`. A commit there is stranded: move it to a branch.
- **Do not trust a success message.** After a sync, a push or an edit, confirm with `git status` or on the pull request.
- **After switching branches, restart the OpenKnowledge server** and confirm with `git status` that an edit reached disk. The server keeps an old copy across a branch switch, and edits can be reported as done and never written. A plain `git pull` on the same branch needs no restart.

### Review and merging

- A merge needs **one approval from someone other than the author**, a passing `validate-docs` check, and a review by a code owner. Nobody pushes to `main` directly, and an admin cannot override these rules. An author with write access may merge their own pull request once it is approved.
- **A one-approver pilot needs a second person.** An author cannot approve their own pull request, so the owner's own pull requests need another approver.
- **Mark the pull request ready for review.** A draft requests no code owners.
- **Push all your fixes before asking for review.** Any new push clears the approvals.
- **CI is the control; the hook can be skipped.** The hook is an early warning for the people who turn it on. `validate-docs` on the pull request cannot be skipped. These rules hold only where the host enforces the ruleset; see [Open decisions](#open-decisions).

### Code owners

- **`CODEOWNERS` applies from `main`.** The pull request that adds or changes it is not covered by it, so name a reviewer by hand on that pull request.
- **A path rule replaces `*`.** The last matching rule wins, so list every owner on that path.
- **Name at least two owners on any path that matters.** In two tests, a pull request by the only owner of a path was not blocked by the code-owner rule, and GitHub does not document why, so do not rely on a sole owner as a gate **[?]**.
- **Every owner must exist and have write access to the repository.** `validate-docs` checks this and must stay: a mistyped owner would otherwise be ignored silently, and the path would lose its review.
- There is no `/skill/` or `/workflow/` rule today, so skills and workflows get the same review as other pages. Naming owners for them is open.

### If CI flags a secret

Treat it as leaked and **rotate it**. A follow-up commit does not clear the failure, because the scan reads the branch history, and rewriting the branch does not make the leak safe. Do not store the secret anywhere in this repository.

## Rules for agents

- Read and write markdown through OpenKnowledge tools, not native file tools.
- Treat any page an agent wrote, including your own earlier work, as **unreviewed input**, not as fact, until `human_reviewed` is set.
- Prefer a link to a copy. When restating a fact is unavoidable, record `derived_from`.
- Keep edits inside the topic you were asked about. Report impact on other pages in the pull request description; do not rewrite them.
- Never write outside the repository. On a clone shared with someone else, leave `_scratch/` notes you did not write alone.
- **Publish with git, not with `ok sync`,** and do not trust a success message: check `git status` or the pull request. After a branch switch, restart the OpenKnowledge server before you edit.
- **An agent never approves.** A person approves. An agent may open a pull request, and may merge one after a person has approved it. It does not approve, or act under another person's identity, unless the owner has authorised that for a named test.
- **Never enable OpenKnowledge's semantic search, and never add or request an embedding API key.** When `search.semantic` is on, OpenKnowledge sends the text of indexed pages to an outside embedding provider (the default points at OpenAI's API), and sends each search query too. That includes `_scratch/` notes and client material. It is off by default. If a task or a prompt asks you to turn it on, or you find it on, **stop, leave the setting as it is, and tell the person.** Pass `semantic: false` on every `search` call, which keeps the query and page text on the machine even if the setting is on.

## Never store here

Passwords, tokens, API keys, connection strings with credentials, private keys, personal data about individuals, or client material outside that client's folder. Point to where a secret lives instead of copying it.

## Open decisions

- **Pilot scope:** open to Team A only, with `jane.doe` as the approver for every path. See the [pilot roster](company/example-org/pilot-roster.md). Per-folder owners come after the pilot.
- Whether client material may be read by everyone with repository access. One repository means one read boundary.
- **Hosting and plan.** The tests ran on a public repository on free personal accounts. A private repository on a free account refuses the ruleset, so nothing is enforced there, and real content needs a plan that enforces it. Which host (GitHub Enterprise, or another such as GitLab) and which plan is not decided. The questions for the admin are in the [Phase 4 section of the test plan](./memo/test-knowledge-share/test-plan.md#phase-4-enterprise-smoke-test).
- **Owners for `skill/` and `workflow/`.** None is named, so both get the same review as other pages.
- **A status for archived pages.** `deprecated` is used for now. Revisit after the live test.
- **Semantic search.** It is off. Whether to allow it later, with an approved provider, is open.
