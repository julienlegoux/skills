#!/usr/bin/env python3
"""Record, and read back, occurrences of friction caused by an lx skill.

    feedback.py report --skill NAME --kind wrong|contradictory|missing|wasted \
                       --quote "<verbatim sentence or heading of the skill>" \
                       --what "<what it caused>"
    feedback.py pointers

The loop is the maintainers' own. `report` posts only when `gh` is signed in as
someone who can push to the skills repo, and does nothing anywhere else;
`pointers` counts only what maintainers posted. Everybody can use the skills;
only their maintainers' sessions feed them.

An occurrence points at a sentence of a skill. The issue title is derived from
that sentence, so two sessions hitting the same sentence land on the same issue:
one issue per (skill, kind, sentence), one comment per further occurrence.

Environment: LX_FEEDBACK_REPO (default julienlegoux/skills), LX_FEEDBACK=off to
disable, GH_TOKEN or GITHUB_TOKEN for `pointers` without gh.

`report` never fails the run that calls it: it always exits 0.
"""

import argparse
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

REPO = os.environ.get("LX_FEEDBACK_REPO", "julienlegoux/skills")
ROOT = Path(__file__).resolve().parents[3]
KINDS = ("wrong", "contradictory", "missing", "wasted")
TITLE = re.compile(r"^\[lx:([a-z0-9-]+)\] (%s): (.+)$" % "|".join(KINDS))
MAINTAINERS = {"OWNER", "MEMBER", "COLLABORATOR"}
PREFIX_LEN = 60
NOTE_LEN = 600


# --- the skills on disk -----------------------------------------------------

def normalise(text):
    return " ".join(re.sub(r"[*`]", "", text).split())


def skill_files(skill):
    folder = ROOT / "skills" / skill
    return sorted(folder.rglob("*.md")) if re.fullmatch(r"[a-z0-9-]+", skill) else []


def locate(skill, fragment):
    """Find normalised `fragment` in the skill. Returns (path:line, sentence) or None."""
    needle = normalise(fragment)
    if not needle:
        return None
    for path in skill_files(skill):
        line_no, block = 1, []
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines() + [""], 1):
            if line.strip():
                if not block:
                    line_no = number
                block.append(line)
                continue
            text = normalise(" ".join(block))
            block = []
            at = text.find(needle)
            if at < 0:
                continue
            end = text.find(". ", at + len(needle))
            sentence = text[at:end + 1] if end >= 0 else text[at:]
            return f"{path.relative_to(ROOT).as_posix()}:{line_no}", sentence[:300]
    return None


def plugin_version():
    try:
        manifest = ROOT / ".claude-plugin" / "plugin.json"
        return json.loads(manifest.read_text(encoding="utf-8"))["version"]
    except (OSError, ValueError, KeyError):
        return "unknown"


# --- the tracker ------------------------------------------------------------

def gh(*args):
    """Run gh; return stdout, or None on any failure."""
    try:
        done = subprocess.run(
            ["gh", *args], capture_output=True, text=True, timeout=60, check=False
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return done.stdout if done.returncode == 0 else None


def gh_usable():
    return shutil.which("gh") is not None and gh("auth", "status") is not None


def is_maintainer():
    """True when gh is signed in as someone who can push to the skills repo."""
    if shutil.which("gh") is None:
        return False
    raw = gh("api", f"repos/{REPO}")
    try:
        return bool(raw) and json.loads(raw).get("permissions", {}).get("push") is True
    except ValueError:
        return False


def api_get(path, use_gh):
    """GET every page of a REST list endpoint. Returns a list, or None if unreachable."""
    items, page = [], 1
    while True:
        query = f"{path}{'&' if '?' in path else '?'}per_page=100&page={page}"
        if use_gh:
            raw = gh("api", query)
        else:
            request = urllib.request.Request(
                f"https://api.github.com/{query}",
                headers={"Accept": "application/vnd.github+json", "User-Agent": "lx-feedback"},
            )
            token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
            if token:
                request.add_header("Authorization", f"Bearer {token}")
            try:
                with urllib.request.urlopen(request, timeout=60) as response:
                    raw = response.read().decode("utf-8")
            except (urllib.error.URLError, OSError):
                raw = None
        if raw is None:
            return None
        batch = json.loads(raw)
        items.extend(batch)
        if len(batch) < 100:
            return items
        page += 1


def open_issues(use_gh):
    issues = api_get(f"repos/{REPO}/issues?state=open", use_gh)
    if issues is None:
        return None
    return [i for i in issues if "pull_request" not in i]


# --- report -----------------------------------------------------------------

def scrub(text):
    """Mechanical net under the skill's own rule: no local paths leave the machine."""
    for path, placeholder in ((Path.cwd(), "<project>"), (Path.home(), "~")):
        if len(path.parts) > 1:
            text = text.replace(str(path), placeholder)
    return text


def body_of(rec):
    return (
        f"**Skill**: {rec['skill']} · **Kind**: {rec['kind']} · "
        f"**Plugin**: lx {rec['plugin']} · {rec['date']}\n\n"
        f"> {rec['sentence']}\n\n{rec['what']}\n\n"
        "<sub>lx-feedback occurrence, filed automatically</sub>\n"
    )


def send(rec):
    """Post one occurrence. Returns a description of what was done, or None."""
    with tempfile.NamedTemporaryFile(
        "w", suffix=".md", delete=False, encoding="utf-8"
    ) as handle:
        handle.write(body_of(rec))
        body_file = handle.name
    try:
        issues = open_issues(use_gh=True)
        if issues is None:
            return None
        for issue in issues:
            if issue["title"].strip() == rec["title"]:
                number = str(issue["number"])
                ok = gh("issue", "comment", number, "--repo", REPO, "--body-file", body_file)
                return f"occurrence added to #{number}" if ok is not None else None
        create = ["issue", "create", "--repo", REPO, "--title", rec["title"],
                  "--body-file", body_file]
        # Only collaborators can label; the title is what routes the issue.
        url = gh(*create, "--label", "feedback") or gh(*create)
        return f"opened {url.strip()}" if url else None
    finally:
        os.unlink(body_file)


def cmd_report(args):
    if not is_maintainer():
        print("Feedback is the maintainers' loop; nothing to do here.")
        return
    found = locate(args.skill, args.quote)
    if found is None:
        print(f"Not recorded: that quote is not in the {args.skill} skill. "
              "Give a sentence or heading exactly as the skill has it.")
        return
    sentence = found[1]
    done = send({
        "date": datetime.date.today().isoformat(),
        "skill": args.skill,
        "kind": args.kind,
        "plugin": plugin_version(),
        "title": f"[lx:{args.skill}] {args.kind}: {sentence[:PREFIX_LEN].strip()}",
        "sentence": sentence,
        "what": scrub(args.what),
    })
    print(f"Feedback sent: {done}." if done else "Feedback not sent (tracker unreachable).")


# --- pointers ---------------------------------------------------------------

def note_of(body):
    """The free-text part of an occurrence this script filed."""
    parts = [p.strip() for p in (body or "").split("\n\n")]
    parts = [p for p in parts if p and not p.startswith(("**Skill**", ">", "<sub>"))]
    return " ".join(" ".join(parts).split())[:NOTE_LEN]


def cmd_pointers(_args):
    use_gh = gh_usable()
    issues = open_issues(use_gh)
    if issues is None:
        print("Tracker unreachable.")
        sys.exit(1)

    classes, stale = {}, []
    for issue in issues:
        match = TITLE.match(issue["title"])
        if not match or issue.get("author_association") not in MAINTAINERS:
            continue
        skill, kind, prefix = match.groups()
        found = locate(skill, prefix)
        if found is None:
            stale.append(issue["number"])
            continue
        entry = classes.setdefault((skill, kind, found), {"issues": [], "notes": []})
        entry["issues"].append(issue["number"])
        posts = [issue]
        if issue.get("comments"):
            posts += api_get(f"repos/{REPO}/issues/{issue['number']}/comments", use_gh) or []
        for post in posts:
            if post.get("author_association") in MAINTAINERS:
                entry["notes"].append(note_of(post.get("body")))

    for (skill, kind, (where, sentence)), entry in sorted(
        classes.items(), key=lambda item: -len(item[1]["notes"])
    ):
        numbers = " ".join(f"#{n}" for n in entry["issues"])
        print(f"{skill} · {kind} · x{len(entry['notes'])} · {numbers}")
        print(f"  {where}")
        print(f"  > {sentence}")
        for note in entry["notes"]:
            if note:
                print(f"  - {note}")
        print()
    if stale:
        print("Stale — the text they point at is no longer in the skill: "
              + " ".join(f"#{n}" for n in stale))
    if not classes and not stale:
        print("No open occurrences.")


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)

    report = sub.add_parser("report", help="record one occurrence")
    report.add_argument("--skill", required=True)
    report.add_argument("--kind", required=True, choices=KINDS)
    report.add_argument("--quote", required=True,
                        help="the sentence or heading of the skill at fault, verbatim")
    report.add_argument("--what", required=True, help="what it caused, in general terms")
    report.set_defaults(run=cmd_report)

    sub.add_parser("pointers", help="what the tracker points at, as counts").set_defaults(
        run=cmd_pointers)

    args = parser.parse_args()
    if args.command == "pointers":
        args.run(args)
        return
    if os.environ.get("LX_FEEDBACK", "").lower() == "off":
        print("Feedback disabled (LX_FEEDBACK=off).")
        return
    try:
        args.run(args)
    except Exception as error:  # never fail the run that reports
        print(f"Feedback not recorded ({error.__class__.__name__}: {error}).")


if __name__ == "__main__":
    main()
