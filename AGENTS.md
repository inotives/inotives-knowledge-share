# Example Team Knowledge Base -- Team Contract

One shared repository for what the team knows and decides, written by people and their AI agents together. Stack: **OpenKnowledge** as the editor and AI control panel, **GitHub** as the only host. This file is the operating contract for both people and agents.

## Using this repository as durable memory

When an agent is started from this folder, this repository is its long-term memory. It is an OpenKnowledge project, not a code project.

**Start of a session**

- Before re-deriving context, search the knowledge base with the `open-knowledge` MCP tools (`search`, `exec`). Check `company/` for the project you are working on.
- Read and write markdown only through the `open-knowledge` MCP tools, never native file tools. Load the `open-knowledge` skill if it is not already in context.

**Saving what you learn**

- Capture new durable knowledge as a draft in `_scratch/<handle>/` first. See [Identity](#identity) for your handle.
- `_scratch/` is gitignored and unbacked. When something should last, promote it (see below).

**Precedence.** For work done from this folder, this repository is the durable memory and this file is the contract. Ignore user-level instructions that point at a different knowledge vault or that default new notes to `memo/`.

## One-time setup per clone

1. `git config user.email "<you>@example.com"` and `git config user.name "<Your Name>"` (see [Identity](#identity)).
2. `git config core.hooksPath .githooks` to turn on the local pre-commit check. It runs the same frontmatter, link and skill checks as CI, and scans staged changes for secrets with gitleaks (directly, or through Docker).
3. `ok init` to set up OpenKnowledge and the agent tool config. Those generated files are gitignored.

The pre-commit hook protects only the people who enable it. The pull-request checks on GitHub are the ones that cannot be skipped.

## Identity

Every person has one **handle**: the part of their company email address before the `@` (for `jane.doe@example.com`, the handle is `jane.doe`). It is the same email used for their GitHub account.

- **Source:** `git config user.email`. Each person sets it once to their company email, so commits, GitHub and this repository agree.
- **Used for:** `created_by`, `owner`, `human_reviewed`, `_scratch/<handle>/` and branch names (`<handle>/<topic>`).
- **An agent uses the handle of the person it is working for**, never `claude` or `agent`. The person is accountable for what the agent writes.
- **If `git config user.email` is empty, or is not a company address** (for example a GitHub `noreply` address), the agent stops and asks. It never invents a handle.

## Folders

| Folder | Status | What goes here |
| --- | --- | --- |
| `_scratch/<handle>/` | **Gitignored, local only.** The folder exists in git; its contents never do | Your own working notes and agent drafts. Free writes, no review, no backup |
| `memo/` | Curated | Shared notes, research and decisions that are not yet settled enough for `concept/` or `company/` |
| `concept/` | Curated | Glossary, terminology, technical reference and distilled knowledge |
| `company/<name>/<project>/` | Curated | One folder per company or client, one subfolder per project. No loose files directly under `company/<name>/` once a project has more than a few pages |
| `skill/` | Curated | Skills: atomic capabilities that define how to perform one specific task. One folder per skill with a `SKILL.md`. Skills execute, so changes here get the closest review |
| `workflow/` | Curated | Workflows: orchestrated sequences of decisions and actions that achieve a broader, end-to-end objective, and usually invoke several skills |
| `generated_output/` | Curated | Generated, shareable deliverables: HTML reports, PDFs, slide decks. Rendered from markdown sources; never the place a fact is edited |

Everything outside `_scratch/` is **curated**: it changes by pull request, not by direct push.

## Working in _scratch

- Work in `_scratch/<your-handle>/`. Let agents draft there.
- **Nothing in `_scratch/` is saved to GitHub.** If it matters, promote it.
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

## Rules for agents

- Read and write markdown through OpenKnowledge tools, not native file tools.
- Treat any page an agent wrote, including your own earlier work, as **unreviewed input**, not as fact, until `human_reviewed` is set.
- Prefer a link to a copy. When restating a fact is unavoidable, record `derived_from`.
- Keep edits inside the topic you were asked about. Report impact on other pages in the pull request description; do not rewrite them.
- Never write outside the repository or into another person's `_scratch/` folder.

## Never store here

Passwords, tokens, API keys, connection strings with credentials, private keys, personal data about individuals, or client material outside that client's folder. Point to where a secret lives instead of copying it.

## Open decisions

- **Pilot scope:** open to Team A only, with `jane.doe` as the approver for every path. See the [pilot roster](company/example-org/pilot-roster.md). Per-folder owners come after the pilot.
- Whether client material may be read by everyone with repository access. One repository means one read boundary.
- Branch protection on `main` and how OpenKnowledge sync behaves against it.
