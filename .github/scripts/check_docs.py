#!/usr/bin/env python3
"""Check frontmatter and relative links for curated markdown.

Curated folders: concept, company, workflow, memo, generated_output (README only).
skill/<name>/SKILL.md is checked separately: name must equal the folder, description required.
_scratch/ is never checked. README.md files need only title and description.
Every folder under a curated folder needs a README.md, except inside a skill or a workflow.
A page must not contain a personal local path such as /Users/<name>/ or /home/<name>/;
write ~/ or a repo-relative path instead. Fenced code blocks are checked too.
Standard library only.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CURATED = ["concept", "company", "workflow", "memo", "generated_output"]
REQUIRED = ["title", "description", "type", "status", "owner", "created_at"]
LIGHT = ["title", "description"]
TYPES = {"note", "research", "decision", "spec", "runbook", "playbook", "skill",
         "reference", "glossary", "report"}
STATUSES = {"draft", "reviewed", "verified", "deprecated"}
HANDLE = re.compile(r"^[a-z0-9][a-z0-9._-]*$")
NOT_PEOPLE = {"claude", "agent", "ai", "bot"}
LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)\)")
LOCAL_PATH = re.compile(r"(?:/Users/|/home/|[A-Za-z]:\\Users\\)[A-Za-z0-9._-]+")
FENCE = re.compile(r"^(```|~~~).*?^\1", re.S | re.M)


def frontmatter(text):
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    fields = {}
    for line in text[4:end].splitlines():
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if m:
            fields[m.group(1)] = m.group(2).strip().strip("\"'")
    return fields


def folders_without_readme():
    """Every folder under a curated folder (and skill/) needs a README.md.

    Hidden folders such as .ok are skipped. A folder inside a skill or a workflow
    is described by its SKILL.md or workflow.md, so it needs no README.
    """
    problems = []
    for top in CURATED + ["skill"]:
        base = ROOT / top
        if not base.is_dir():
            continue
        for folder in [base] + sorted(p for p in base.rglob("*") if p.is_dir()):
            rel = folder.relative_to(ROOT)
            if any(part.startswith(".") for part in rel.parts):
                continue
            inside_skill_or_workflow = False
            probe = folder
            while probe != ROOT:
                if (probe / "SKILL.md").exists() or (probe / "workflow.md").exists():
                    inside_skill_or_workflow = True
                    break
                probe = probe.parent
            if not inside_skill_or_workflow and not (folder / "README.md").exists():
                problems.append(
                    f"{rel}: folder has no README.md; create it from the folder-readme "
                    "template (see workflow/new-folder/workflow.md)")
    return problems


def main():
    errors = []
    files = [p for d in CURATED for p in (ROOT / d).rglob("*.md")
             if ".ok" not in p.parts]
    for path in sorted(files):
        rel = path.relative_to(ROOT)
        text = path.read_text(encoding="utf-8")
        for n, line in enumerate(text.splitlines(), 1):
            m = LOCAL_PATH.search(line)
            if m:
                errors.append(f"{rel}:{n}: local path '{m.group(0)}', write ~/ or a relative path")
        fm = frontmatter(text)
        if fm is None:
            errors.append(f"{rel}: missing frontmatter")
            continue
        need = LIGHT if path.name == "README.md" else REQUIRED
        for key in need:
            if not fm.get(key):
                errors.append(f"{rel}: missing '{key}'")
        if path.name != "README.md":
            if fm.get("type") and fm["type"] not in TYPES:
                errors.append(f"{rel}: type '{fm['type']}' not in {sorted(TYPES)}")
            if fm.get("status") and fm["status"] not in STATUSES:
                errors.append(f"{rel}: status '{fm['status']}' not in {sorted(STATUSES)}")
            for key in ("created_by", "owner"):
                value = fm.get(key, "")
                if value and (value.startswith("agent:") or value.lower() in NOT_PEOPLE
                              or "@" in value):
                    errors.append(f"{rel}: '{key}' must be a person's handle, not '{value}'")
            if fm.get("status") in {"reviewed", "verified"} and not fm.get("human_reviewed"):
                errors.append(f"{rel}: status '{fm['status']}' needs 'human_reviewed'")
        body = FENCE.sub("", text)
        for target in LINK.findall(body):
            if re.match(r"^(https?:|mailto:|#)", target):
                continue
            target = target.split("#")[0]
            if target and not (path.parent / target).resolve().exists():
                errors.append(f"{rel}: broken link '{target}'")
    skills = [p for p in (ROOT / "skill").glob("*/") if p.is_dir()]
    for folder in sorted(skills):
        rel = folder.relative_to(ROOT)
        skill_md = folder / "SKILL.md"
        if not skill_md.exists():
            errors.append(f"{rel}: missing SKILL.md")
            continue
        fm = frontmatter(skill_md.read_text(encoding="utf-8")) or {}
        if fm.get("name") != folder.name:
            errors.append(f"{rel}/SKILL.md: 'name' must equal folder name '{folder.name}'")
        if not fm.get("description"):
            errors.append(f"{rel}/SKILL.md: missing 'description'")
    errors.extend(folders_without_readme())
    for e in errors:
        print(e)
    print(f"checked {len(files)} files and {len(skills)} skills, {len(errors)} problems")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
