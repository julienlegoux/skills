#!/usr/bin/env python3
"""Check that a change has the shape of an automatic skill improvement.

    guard.py <base> <head>

An automatic improvement rewords prose in a skill and may add eval cases.
Anything else — code, commands, links, manifests, the rules themselves — is a
change a person has to author. This script decides which of the two a diff is,
without reading what it says: it is run by CI from the base branch, on pull
requests whose branch starts with `improve/`, so neither the pull request nor
the session that wrote it can alter the check.

Exit 0: the diff is prose-only and within budget. Exit 1: it is not, with why.
"""

import re
import subprocess
import sys
import unicodedata

SKILL_LINES_MAX = 100     # a SKILL.md after the change
ADDED_LINES_MAX = 40      # prose added under skills/ by one change
EVAL_TOOLS = {"Read", "Glob", "Grep", "Skill"}

SKILL_MD = re.compile(r"^skills/[a-z0-9-]+/SKILL\.md$")
REFERENCE_MD = re.compile(r"^skills/[a-z0-9-]+/references/[\w.-]+\.md$")
EVAL_MD = re.compile(r"^evals/[a-z0-9-]+/(prompt\.md|graders/[\w.-]+\.md)$")
MANIFEST = ".claude-plugin/plugin.json"

LINK = re.compile(
    r"[a-z][a-z0-9+.-]*://|\bwww\.|"
    r"\b[a-z0-9-]+\.(com|net|org|io|dev|sh|ai|co|app|xyz|info|ru|cn|me|to|ly|gg)\b",
    re.IGNORECASE,
)
COMMAND = re.compile(
    r"\b(curl|wget|bash|zsh|sh|powershell|pwsh|iwr|iex|sudo|chmod|chown|nc|ncat|ssh|scp|"
    r"base64|xxd|openssl|pip|npm|npx|pipx|uvx|brew|apt|apt-get|docker|rm -rf)\b"
)
OPAQUE = re.compile(r"[A-Za-z0-9+/=_-]{40,}")


def git(*args):
    return subprocess.run(
        ["git", *args], capture_output=True, text=True, check=True
    ).stdout


def added_lines(base, head, path):
    """Line numbers (in the head version) of lines the diff adds."""
    numbers = []
    for line in git("diff", "-U0", f"{base}...{head}", "--", path).splitlines():
        hunk = re.match(r"^@@ -\S+ \+(\d+)(?:,(\d+))? @@", line)
        if hunk:
            start, count = int(hunk.group(1)), int(hunk.group(2) or 1)
            numbers.extend(range(start, start + count))
    return numbers


def fenced(lines):
    """Line numbers that are a code fence or inside one."""
    inside, numbers = False, set()
    for number, line in enumerate(lines, 1):
        fence = line.lstrip().startswith(("```", "~~~"))
        if inside or fence:
            numbers.add(number)
        if fence:
            inside = not inside
    return numbers


def frontmatter(text):
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return ""
    for end, line in enumerate(lines[1:], 1):
        if line.strip() == "---":
            return "\n".join(lines[: end + 1])
    return text


def hidden(line):
    for char in line:
        category = unicodedata.category(char)
        if category in ("Cf", "Co", "Cs", "Cn") or (category == "Cc" and char != "\t"):
            return f"U+{ord(char):04X}"
    return None


def check_text(path, base, head, problems):
    """Content rules for every line a change adds to a markdown file."""
    lines = git("show", f"{head}:{path}").splitlines()
    in_fence = fenced(lines)
    added = added_lines(base, head, path)
    for number in added:
        line = lines[number - 1]
        where = f"{path}:{number}"
        if number in in_fence:
            problems.append(f"{where} adds or alters a code block")
        if "<!--" in line:
            problems.append(f"{where} adds an HTML comment")
        if LINK.search(line):
            problems.append(f"{where} adds a link or host name")
        if COMMAND.search(line):
            problems.append(f"{where} names a command")
        if OPAQUE.search(line):
            problems.append(f"{where} adds an opaque token")
        char = hidden(line)
        if char:
            problems.append(f"{where} adds an invisible character ({char})")
        tools = re.match(r"\s*allowed_tools\s*:\s*\[(.*)\]", line)
        if tools is not None:
            asked = {tool.strip() for tool in tools.group(1).split(",") if tool.strip()}
            if not asked <= EVAL_TOOLS:
                problems.append(f"{where} grants tools beyond {sorted(EVAL_TOOLS)}")
        elif re.match(r"\s*(allowed_tools|scaffold_script)\s*:", line):
            problems.append(f"{where} sets tools or a scaffold in a form that is not checked")
        grader = re.match(r"\s*type\s*:\s*(\S+)", line)
        if grader is not None and path.startswith("evals/") and grader.group(1) != "llm":
            problems.append(f"{where} adds a grader that is not a judged description")
    return len(added)


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    base, head = sys.argv[1:]
    problems, skill_lines_added = [], 0

    changes = git("diff", "--name-status", "--no-renames", f"{base}...{head}").splitlines()
    for change in changes:
        status, path = change.split("\t", 1)
        if SKILL_MD.match(path) and status == "M":
            skill_lines_added += check_text(path, base, head, problems)
            before = git("show", f"{base}:{path}")
            after = git("show", f"{head}:{path}")
            if frontmatter(before) != frontmatter(after):
                problems.append(f"{path} changes the skill's name or description")
            if len(after.splitlines()) > SKILL_LINES_MAX:
                problems.append(f"{path} exceeds {SKILL_LINES_MAX} lines")
        elif REFERENCE_MD.match(path) and status in ("M", "A"):
            skill_lines_added += check_text(path, base, head, problems)
        elif EVAL_MD.match(path) and status == "A":
            check_text(path, base, head, problems)
        elif path == MANIFEST and status == "M":
            diff = git("diff", "-U0", f"{base}...{head}", "--", path).splitlines()
            touched = [l for l in diff if l[:1] in "+-" and l[:3] not in ("+++", "---")]
            if any(not re.match(r'^[+-]\s*"version":\s*"[0-9.]+",?\s*$', l) for l in touched):
                problems.append(f"{path} changes more than the version")
        elif EVAL_MD.match(path) or path.startswith("evals/"):
            problems.append(f"{path}: an existing eval may not be changed or removed, "
                            "and only prompt.md and graders/*.md may be added")
        else:
            problems.append(f"{path}: outside what an automatic change may touch")

    if skill_lines_added > ADDED_LINES_MAX:
        problems.append(
            f"{skill_lines_added} lines added under skills/ (limit {ADDED_LINES_MAX})"
        )

    if problems:
        print("Not an automatic improvement — a person has to author or review this:\n")
        print("\n".join(f"  - {p}" for p in problems))
        sys.exit(1)
    print(f"OK: {len(changes)} file(s), prose only, within budget.")


if __name__ == "__main__":
    main()
