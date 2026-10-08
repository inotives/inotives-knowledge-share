---
title: Knowledge Share
description: A public test bed for a team knowledge base built on OpenKnowledge and GitHub. It uses dummy content only, and exists to find out how the workflow behaves before it is used for real.
---
# inotives-knowledge-share

A **public test bed** for a team knowledge base where people and their AI agents write together. The stack is deliberately small:

- **[OpenKnowledge](https://github.com/inkeep/open-knowledge)** is the editor and the AI control panel (markdown files plus MCP tools for agents).
- **GitHub** is the only host. Review, history and access control all come from it.

> **Dummy content only.** Nothing in this repository is real company or client material. It exists so the workflow can be tested in the open on free GitHub accounts, before the real knowledge base is set up on GitHub Enterprise.

## What we want to achieve

A team knowledge base is only useful if people trust it. That needs three things at once: anyone can capture knowledge quickly, shared pages are reviewed before they count, and agents can read and write without silently corrupting the record.

This repository tests whether the rules in [AGENTS.md](./AGENTS.md) actually deliver that with GitHub features we can rely on.

```mermaid
flowchart LR
    subgraph People["People and their agents"]
        A["Contributor A<br/>+ agent"]
        B["Contributor B<br/>+ agent"]
    end
    OK["OpenKnowledge<br/>editor and MCP tools"]
    S["_scratch/handle/<br/>local, gitignored,<br/>free writes"]
    BR["Branch<br/>handle/topic"]
    PR["Pull request"]
    CI["CI: frontmatter,<br/>links, secret scan"]
    R["Code owner<br/>review"]
    M[("main<br/>curated knowledge")]

    A --> OK
    B --> OK
    OK --> S
    S -->|"promote:<br/>move into a curated folder"| BR
    BR --> PR
    PR --> CI
    CI --> R
    R -->|"merge"| M
    M -->|"sync and search"| OK
```

## How the repository is organised

Everything outside `_scratch/` is **curated**: it changes by pull request, not by direct push.

```mermaid
flowchart TD
    ROOT["repository root<br/>AGENTS.md = the team contract"]
    ROOT --> SC["_scratch/handle/<br/>personal drafts<br/>NOT in git"]
    ROOT --> ME["memo/<br/>shared notes, not yet settled"]
    ROOT --> CO["concept/<br/>glossary, distilled knowledge"]
    ROOT --> CP["company/name/project/<br/>one folder per org or client"]
    ROOT --> SK["skill/<br/>atomic agent capabilities"]
    ROOT --> WF["workflow/<br/>end-to-end procedures"]
    ROOT --> GO["generated_output/<br/>rendered reports and decks"]

    classDef local fill:#fff4e5,stroke:#c77700,color:#333
    classDef curated fill:#e8f4ee,stroke:#2f7d57,color:#333
    class SC local
    class ME,CO,CP,SK,WF,GO curated
```

| Folder | Status | Purpose |
| --- | --- | --- |
| `_scratch/<handle>/` | Gitignored, local only | Personal notes and agent drafts. No review, no backup |
| `memo/` | Curated | Shared notes that are not yet settled |
| `concept/` | Curated | Glossary and distilled reference |
| `company/<name>/<project>/` | Curated | Content per organisation and project |
| `skill/` | Curated | Skills. Closest review, because skills execute |
| `workflow/` | Curated | Orchestrated procedures that use skills |
| `generated_output/` | Curated | Shareable renderings. Never the place a fact is edited |

## How a page matures

A page carries a `status` in its frontmatter. Agents may write drafts, but **only a human sets `verified`**.

```mermaid
stateDiagram-v2
    [*] --> draft: anyone, including an agent
    draft --> reviewed: a peer, in the pull request
    reviewed --> verified: the owner, a human only
    verified --> deprecated: replaced or no longer true
    reviewed --> deprecated
    draft --> deprecated
    deprecated --> [*]: kept, with a pointer to what replaced it
```

## What we are testing

The contract makes promises that depend on how GitHub and OpenKnowledge behave. The first three are the ones that could change the design.

| # | Question | Why it matters |
| --- | --- | --- |
| 1 | Does OpenKnowledge's timed sync bypass or break a protected `main`? | If the editor pushes straight to `main`, pull-request review does not hold |
| 2 | Can an approver's own pull request be merged (bypass or second approver)? | A one-approver pilot needs a workable answer |
| 3 | Do code owners resolve, by work email and by `@username`? | Required review depends on it |
| 4 | Is `_scratch/` indexed by OpenKnowledge, and can agents write to it, while Git ignores it? | Drafts must be searchable but never pushed |
| 5 | Do the CI checks and the pre-commit hook catch bad frontmatter, broken links and a planted fake secret? | The checks are the only automation |
| 6 | What happens when two contributors edit the same page? | Conflicts must be visible and never auto-resolved |
| 7 | Does it still work on GitHub Enterprise, where org rulesets and SSO apply? | Free accounts cannot show this |

## Test phases

Each phase adds one control, so any change in behaviour can be traced to it. Results are written up as pages in this repository.

```mermaid
flowchart LR
    P0["Phase 0<br/>Baseline<br/>no protection,<br/>no CODEOWNERS"]
    P1["Phase 1<br/>Ruleset on main<br/>PR + 1 approval"]
    P2["Phase 2<br/>CODEOWNERS<br/>code-owner review"]
    P3["Phase 3<br/>Two contributors<br/>collisions, conflicts"]
    P4["Phase 4<br/>Smoke test on<br/>GitHub Enterprise"]

    P0 --> P1 --> P2 --> P3 --> P4

    style P0 fill:#e8f4ee,stroke:#2f7d57
```

**Phase 0 is the current state.** The repository has the contract, the folders and the CI checks, but no ruleset and no `CODEOWNERS`. This shows what OpenKnowledge and GitHub do by default, which is the baseline every later phase is compared with.

## Accounts used in the test

```mermaid
flowchart TB
    OWNER["Owner and approver<br/>personal account<br/>admin on the repo"]
    T1["Contributor<br/>throwaway account 1<br/>write access"]
    T2["Contributor<br/>throwaway account 2<br/>added for Phase 3"]
    REPO[("inotives-knowledge-share")]

    OWNER -->|"owns, sets ruleset"| REPO
    T1 -->|"branch + pull request"| REPO
    T2 -->|"branch + pull request"| REPO
    OWNER -.->|"reviews and approves"| T1
    OWNER -.->|"reviews and approves"| T2
```

Each account has its own SSH key and its own clone, so every action is attributable to one identity.

## Status

- Phase 0 is being set up. No test has been run yet, so this repository makes no claims about how the workflow behaves.
- Findings will be added here as they are confirmed, not before.

## Using this repository

1. Read [AGENTS.md](./AGENTS.md). It is the contract for people and agents.
2. `git config user.email "<verified address>"` and `git config user.name "<name>"`.
3. `git config core.hooksPath .githooks` to enable the local pre-commit check.
4. `ok init` to set up OpenKnowledge and the agent tool config. Generated files are gitignored.
5. Work in `_scratch/<handle>/`, then promote to a curated folder by pull request.

Do not store passwords, tokens, keys or any real company or personal data here. This repository is public.
