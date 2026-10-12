---
title: Company
description: One folder per company or client, one subfolder per project. Curated by pull request.
---
# Company

## Purpose

Content about one company or client, kept in one folder per organisation and one subfolder per project. Material about a client stays inside that client's folder. Our own organisation is one of the organisations, so an internal project goes in `company/<our-organisation>/<project>/`.

## What goes here

| Goes here | Does not go here (put it in) |
| --- | --- |
| Reports, specs, decisions and notes about one organisation's project | Reusable reference that applies to everyone: [concept](../concept/README.md) |
| | Unsettled shared notes: [memo](../memo/README.md) |
| | Credentials, personal data, or another client's material |

## Layout and naming

`company/<name>/<project>/`. Keep a project's pages together so that a code owner can be assigned to the folder. Lowercase kebab-case. Use a date prefix (`2026-10-06-slug.md`) only for a record tied to a time. Avoid loose files directly under `company/<name>/` once a project has more than a few pages.

## Frontmatter for this folder

The usual `type` is `report`, `spec`, `decision` or `note`. Set `project` when it applies. The full table is in [AGENTS.md](../AGENTS.md#frontmatter).

## Review and ownership

A change needs a pull request, a passing `validate-docs` check, and one approval from someone other than the author, including a code owner. Code owners are set in `.github/CODEOWNERS`. Today the owners of `*` cover every folder, so a project folder has no stricter review. A path rule such as `/company/<name>/<project>/` could give a project its own owner. A draft pull request requests no code owners, so mark it ready for review.

## How to add a page

1. Draft in `_scratch/`.
2. Branch `<handle>/<topic>`.
3. Move the page into the project folder and fill the frontmatter.
4. Open a pull request and mark it ready for review.

The commands are in [INSTRUCTIONS.md](../INSTRUCTIONS.md).

## Rules for this folder

- Everyone with repository access can read every folder here. See the open decision in [AGENTS.md](../AGENTS.md) before adding sensitive client material.
- No client material outside that client's folder.

## Related

[memo](../memo/README.md), [concept](../concept/README.md), [generated_output](../generated_output/README.md), [AGENTS.md](../AGENTS.md)
