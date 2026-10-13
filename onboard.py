#!/usr/bin/env python3
"""Check this machine and clone are ready to contribute, and fix what is safe to fix.

Run from anywhere inside the clone:
    uv run onboard.py            check everything, fix the safe local things, report the rest
    uv run onboard.py --check    read-only: change nothing, only report
    python3 onboard.py           the same without uv (Python 3.9 or later)

It never installs system tools (git, gh, Node, ok, claude): it prints the command to run.
It never writes a secret. Safe to run again; a step that already passes is skipped.
Standard library only. The steps match SETUP.md.
"""
import argparse
import os
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OK, FIX, TODO, WARN = "OK   ", "FIXED", "TODO ", "WARN "
SYSTEM = {"Darwin": "macos", "Windows": "windows", "Linux": "linux"}.get(platform.system(), "linux")

# tool -> (binary, minimum, install command per system, required)
INSTALL = {
    "git": {"macos": "xcode-select --install   (or: brew install git)", "windows": "winget install Git.Git",
            "linux": "use your package manager, e.g. sudo apt install git"},
    "gh": {"macos": "brew install gh", "windows": "winget install GitHub.cli",
           "linux": "see https://github.com/cli/cli#installation"},
    "uv": {"macos": "brew install uv", "windows": "winget install astral-sh.uv",
           "linux": "see https://docs.astral.sh/uv/getting-started/installation/"},
    "node": {"macos": "brew install node", "windows": "winget install OpenJS.NodeJS",
             "linux": "use your package manager, Node 24 or later"},
    "ok": {"any": "see https://github.com/inkeep/open-knowledge for the installer"},
    "claude": {"any": "see https://code.claude.com/docs for the installer"},
}

results = []  # (status, step, detail)


def report(status, step, detail=""):
    results.append((status, step, detail))
    print(f"  {status} {step}" + (f": {detail}" if detail else ""))


def run(*cmd, cwd=ROOT):
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=180)
        return p.returncode, (p.stdout + p.stderr).strip()
    except (OSError, subprocess.TimeoutExpired) as e:
        return 127, str(e)


def install_hint(tool):
    options = INSTALL[tool]
    return options.get(SYSTEM) or options.get("any", "")


def version_of(binary):
    code, out = run(binary, "--version")
    m = re.search(r"(\d+)\.(\d+)", out)
    return (int(m.group(1)), int(m.group(2))) if code == 0 and m else None


def check_tools():
    print("Step 1. Tools")
    minimum = {"git": 2, "gh": 2, "node": 24}
    for tool in ("git", "gh"):
        v = version_of(tool) if shutil.which(tool) else None
        if v and v[0] >= minimum[tool]:
            report(OK, tool, f"{v[0]}.{v[1]}")
        else:
            report(TODO, tool, "missing or too old, required. Install: " + install_hint(tool))
    # uv or python3: this script is already running, so one of them works.
    py = f"Python {sys.version_info.major}.{sys.version_info.minor}"
    if sys.version_info < (3, 9):
        report(TODO, "python", f"{py} is too old, need 3.9 or later; use `uv run onboard.py`")
    else:
        report(OK, "python", py + (", uv found" if shutil.which("uv") else ", uv not needed"))
    v = version_of("node") if shutil.which("node") else None
    if v and v[0] >= minimum["node"]:
        report(OK, "node", f"{v[0]}.{v[1]}")
    else:
        report(TODO, "node", "needed for OpenKnowledge unless you use its desktop app. Install: " + install_hint("node"))
    for tool in ("ok", "claude"):
        if shutil.which(tool):
            report(OK, tool)
        else:
            report(TODO, tool, "Install: " + install_hint(tool))


def check_github():
    print("Step 2. GitHub sign-in")
    if not shutil.which("gh"):
        report(TODO, "gh auth", "install gh first")
        return
    code, out = run("gh", "auth", "status")
    if code == 0:
        report(OK, "gh auth", "signed in")
    else:
        report(TODO, "gh auth", "not signed in. Run: gh auth login   (GitHub.com, HTTPS, yes to git credentials)")
    code, out = run("git", "ls-remote", "--exit-code", "--heads", "origin", "main")
    if code == 0:
        report(OK, "repo access", "origin is reachable")
    else:
        report(TODO, "repo access", "cannot reach origin. Check the invitation was accepted and `gh auth status`")


def handle_from(email):
    return email.split("@")[0].lower()


def check_identity(check_only):
    print("Step 3. Git identity")
    name = run("git", "config", "user.name")[1]
    email = run("git", "config", "user.email")[1]
    bad = (not email or "noreply" in email or "@" not in email)
    if name and not bad:
        report(OK, "identity", f"{name} <{email}>, handle '{handle_from(email)}'")
        return
    if check_only or not sys.stdin.isatty():
        report(TODO, "identity", 'run: git config user.name "Your Name"; git config user.email "you@company.com" '
                                 "(company address, not a noreply one)")
        return
    print("  Your git identity is not set, or is a noreply address.")
    name = name or input("  Your full name: ").strip()
    email = input("  Your company email (verified on GitHub): ").strip()
    if not name or "@" not in email or "noreply" in email:
        report(TODO, "identity", "not set: needs a name and a company email")
        return
    run("git", "config", "user.name", name)
    run("git", "config", "user.email", email)
    report(FIX, "identity", f"set to {name} <{email}> for this clone")


def check_hook(check_only):
    print("Step 4. Pre-commit hook")
    current = run("git", "config", "core.hooksPath")[1]
    if current == ".githooks":
        report(OK, "hook", "core.hooksPath is .githooks")
    elif check_only:
        report(TODO, "hook", "run: git config core.hooksPath .githooks")
    else:
        run("git", "config", "core.hooksPath", ".githooks")
        report(FIX, "hook", "set core.hooksPath to .githooks")
    if not (ROOT / ".githooks" / "pre-commit").exists():
        report(TODO, "hook file", ".githooks/pre-commit is missing; pull main")


def check_scanner(check_only):
    print("Step 5. Secret scanner (gitleaks)")
    pinned = sorted((ROOT / ".bin").glob("gitleaks-*/gitleaks")) if (ROOT / ".bin").is_dir() else []
    if shutil.which("gitleaks"):
        report(OK, "gitleaks", "found on PATH")
    elif pinned:
        report(OK, "gitleaks", f"pinned copy in {pinned[-1].relative_to(ROOT)}")
    elif check_only:
        report(TODO, "gitleaks", "not found. Run without --check to download the pinned, checksum-verified copy")
    elif platform.system() == "Windows":
        report(TODO, "gitleaks", "no pinned download for Windows. Install gitleaks and put it on PATH, "
                                 "or use SKIP_SECRET_SCAN=1 and tell the owner (CI still scans)")
    elif not shutil.which("sh"):
        report(TODO, "gitleaks", "needs `sh` to download the pinned copy; install gitleaks yourself")
    else:
        code, out = run("sh", ".githooks/pre-commit")
        if code == 0:
            report(FIX, "gitleaks", "downloaded the pinned copy, verified its checksum, scan ran clean")
        else:
            report(TODO, "gitleaks", "the hook did not pass: " + (out.splitlines() or ["no output"])[-1])


def semantic_on(path):
    """True if an uncommented `semantic:` block in this yaml file sets `enabled: true`."""
    if not path.exists():
        return False
    in_block, indent = False, 0
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        depth = len(line) - len(line.lstrip())
        if re.match(r"\s*semantic\s*:\s*$", line):
            in_block, indent = True, depth
        elif in_block and depth <= indent:
            in_block = False
        if in_block and re.match(r"\s*enabled\s*:\s*(true|yes|on)\s*$", line, re.I):
            return True
        if re.match(r"\s*semantic\s*:\s*\{.*enabled\s*:\s*true", line, re.I):
            return True
    return False


def check_openknowledge(check_only):
    print("Step 6. OpenKnowledge")
    if not shutil.which("ok"):
        report(TODO, "ok init", "install ok first")
    else:
        # `ok init` is run by hand: it writes per-machine editor wiring and its output is interactive.
        wired = any((ROOT / p).exists() for p in (".mcp.json", ".claude", ".codex", ".cursor", ".opencode"))
        if wired:
            report(OK, "ok init", "editor wiring is present")
        else:
            report(WARN, "ok init", "no editor wiring found in this clone. If your agent cannot see the OpenKnowledge tools, run: ok init --scope project --no-skills")
    on = [str(p) for p in (Path.home() / ".ok" / "global.yml", ROOT / ".ok" / "config.yml") if semantic_on(p)]
    if on:
        report(TODO, "semantic search", "is ON in " + ", ".join(on) + ". Turn it off: it sends page text to an "
                                        "outside provider. Set semantic.enabled to false")
    else:
        report(OK, "semantic search", "off (not enabled in your OpenKnowledge settings)")
    tracked = run("git", "status", "--porcelain", "--untracked-files=no")[1]
    if tracked:
        report(WARN, "working tree", "tracked files are changed; the wizard changes none, check `git status`")
    else:
        report(OK, "working tree", "no tracked file changed")


def check_proof(check_only):
    print("Step 7. Proof: the checks catch a bad page")
    code, out = run(sys.executable, "-I", ".github/scripts/check_docs.py")
    last = (out.splitlines() or [""])[-1]
    if code == 0:
        report(OK, "docs check", last)
    else:
        report(TODO, "docs check", "reports problems on this clone: " + last + ". Run it to see them, or pull main")
    # Proof that the hook refuses: stage a bad page in a throwaway index, never touch the real one.
    hook = ROOT / ".githooks" / "pre-commit"
    if run("git", "config", "core.hooksPath")[1] != ".githooks" or not hook.exists():
        report(TODO, "hook refuses bad page", "turn the hook on first (step 4)")
        return
    if check_only:
        report(WARN, "hook refuses bad page", "not run in --check mode (it needs a temporary file)")
        return
    probe = ROOT / "memo" / "zz-onboard-probe.md"
    if probe.exists():
        report(TODO, "hook refuses bad page", "memo/zz-onboard-probe.md already exists; delete it and rerun")
        return
    try:
        probe.write_text("# no frontmatter\n", encoding="utf-8")
        run("git", "add", "--intent-to-add", "--", str(probe.relative_to(ROOT)))
        code, out = run("sh", ".githooks/pre-commit")
    finally:
        run("git", "rm", "--cached", "-q", "--ignore-unmatch", "--", "memo/zz-onboard-probe.md")
        if probe.exists():
            probe.unlink()
    if code != 0 and "missing frontmatter" in out:
        report(OK, "hook refuses bad page", "refused a page with no frontmatter, then cleaned up")
    else:
        report(TODO, "hook refuses bad page", "the hook did not refuse a bad page. Tell the owner")


def summary(check_only):
    print()
    todo = [r for r in results if r[0] == TODO]
    fixed = [r for r in results if r[0] == FIX]
    print(f"Summary: {sum(r[0] == OK for r in results)} ok, {len(fixed)} fixed, "
          f"{len(todo)} to do, {sum(r[0] == WARN for r in results)} warnings"
          + (" (read-only run)" if check_only else ""))
    if todo:
        print("\nStill to do (fix, then run this again):")
        for _, step, detail in todo:
            print(f"  - {step}: {detail}")
        return 1
    print("\nReady. Next: start OpenKnowledge and your agent (INSTRUCTIONS.md, Part 3), then Part 4.")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true", help="read-only: change nothing, only report")
    args = ap.parse_args()
    if not (ROOT / ".git").exists():
        print("This file must sit at the top of the clone (next to .git).")
        return 2
    print(f"Onboarding check for {ROOT.name} on {platform.system()} {platform.machine()}"
          + (" (read-only)" if args.check else ""))
    check_tools()
    check_github()
    check_identity(args.check)
    check_hook(args.check)
    check_scanner(args.check)
    check_openknowledge(args.check)
    check_proof(args.check)
    return summary(args.check)


if __name__ == "__main__":
    sys.exit(main())
