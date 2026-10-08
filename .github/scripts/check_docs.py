#!/usr/bin/env python3
"""Check frontmatter and relative links for curated markdown.

Curated folders: concept, company, workflow, memo, generated_output (README only).
skill/<name>/SKILL.md is checked separately: name must equal the folder, description required.
_scratch/ is never checked. README.md files need only title and description.
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


def main():
    errors = []
    files = [p for d in CURATED for p in (ROOT / d).rglob("*.md")
             if ".ok" not in p.parts]
    for path in sorted(files):
        rel = path.relative_to(ROOT)
        text = path.read_text(encoding="utf-8")
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
    for e in errors:
        print(e)
    print(f"checked {len(files)} files and {len(skills)} skills, {len(errors)} problems")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
