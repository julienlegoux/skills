#!/usr/bin/env python3
"""Record an occurrence of friction caused by an lx skill.

    feedback.py list [--skill NAME]
    feedback.py report --skill NAME --impact blocked|corrected|wasted \
                       --title "..." --what "..." [--issue N]
    feedback.py flush

One issue per class of failure on the skills repo; every further occurrence is a
comment on it, so the comment count is the recurrence count. Without a usable `gh`
the occurrence is appended to a local outbox and sent by a later run.

Environment: LX_FEEDBACK_REPO (default julienlegoux/skills), LX_FEEDBACK_OUTBOX
(default ~/.lx/feedback-outbox.jsonl), LX_FEEDBACK=off to disable.

Reporting never fails the run that calls it: every path exits 0.
"""

import argparse
import datetime
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = os.environ.get("LX_FEEDBACK_REPO", "julienlegoux/skills")
OUTBOX = Path(
    os.environ.get("LX_FEEDBACK_OUTBOX") or Path.home() / ".lx" / "feedback-outbox.jsonl"
)
IMPACTS = ("blocked", "corrected", "wasted")
PLUGIN_JSON = Path(__file__).resolve().parents[3] / ".claude-plugin" / "plugin.json"


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


def plugin_version():
    try:
        return json.loads(PLUGIN_JSON.read_text(encoding="utf-8"))["version"]
    except (OSError, ValueError, KeyError):
        return "unknown"


def scrub(text):
    """Mechanical net under the skill's own rule: no local paths leave the machine."""
    for path, placeholder in ((Path.cwd(), "<project>"), (Path.home(), "~")):
        if len(path.parts) > 1:
            text = text.replace(str(path), placeholder)
    return text


def open_issues():
    """Open feedback issues as [{number, title, count}], or None if unreachable."""
    out = gh(
        "issue", "list", "--repo", REPO, "--state", "open", "--limit", "200",
        "--json", "number,title,comments",
    )
    if out is None:
        return None
    return [
        {"number": i["number"], "title": i["title"], "count": 1 + len(i["comments"])}
        for i in json.loads(out)
        if i["title"].startswith("[lx:")
    ]


def body_of(rec):
    return (
        f"**Skill**: {rec['skill']} · **Impact**: {rec['impact']} · "
        f"**Plugin**: lx {rec['plugin']} · {rec['date']}\n\n{rec['what']}\n\n"
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
        issue = rec.get("issue")
        if issue is None:
            # Same title already open: count it there rather than open a twin.
            for existing in open_issues() or []:
                if existing["title"] == rec["title"]:
                    issue = existing["number"]
                    break
        if issue is not None:
            ok = gh("issue", "comment", str(issue), "--repo", REPO, "--body-file", body_file)
            return f"occurrence added to #{issue}" if ok is not None else None
        create = ["issue", "create", "--repo", REPO, "--title", rec["title"],
                  "--body-file", body_file]
        # Only collaborators can label; the title prefix is what routes the issue.
        url = gh(*create, "--label", "feedback") or gh(*create)
        return f"opened {url.strip()}" if url else None
    finally:
        os.unlink(body_file)


def read_outbox():
    if not OUTBOX.exists():
        return []
    lines = OUTBOX.read_text(encoding="utf-8").splitlines()
    return [json.loads(line) for line in lines if line.strip()]


def write_outbox(records):
    if not records:
        OUTBOX.unlink(missing_ok=True)
        return
    OUTBOX.parent.mkdir(parents=True, exist_ok=True)
    OUTBOX.write_text(
        "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records),
        encoding="utf-8",
    )


def flush():
    """Send what earlier runs could not. Returns how many went out."""
    pending = read_outbox()
    if not pending:
        return 0
    kept = [rec for rec in pending if send(rec) is None]
    write_outbox(kept)
    return len(pending) - len(kept)


def cmd_list(args):
    issues = open_issues() if gh_usable() else None
    if issues is None:
        print("Tracker unreachable — report without --issue; it will be queued locally.")
        return
    if args.skill:
        issues = [i for i in issues if i["title"].startswith(f"[lx:{args.skill}]")]
    if not issues:
        print("No open feedback issues" + (f" for {args.skill}." if args.skill else "."))
    for i in sorted(issues, key=lambda i: -i["count"]):
        print(f"#{i['number']}  x{i['count']}  {i['title']}")


def cmd_report(args):
    rec = {
        "date": datetime.date.today().isoformat(),
        "skill": args.skill,
        "impact": args.impact,
        "plugin": plugin_version(),
        "title": scrub(f"[lx:{args.skill}] {args.title}"),
        "what": scrub(args.what),
        "issue": args.issue,
    }
    if gh_usable():
        flush()
        done = send(rec)
        if done:
            print(f"Feedback sent: {done}.")
            return
    write_outbox(read_outbox() + [rec])
    print(f"Feedback queued in {OUTBOX} — a later run sends it.")


def cmd_flush(_args):
    if not gh_usable():
        print(f"Tracker unreachable — {len(read_outbox())} occurrence(s) still queued.")
        return
    print(f"Sent {flush()} queued occurrence(s); {len(read_outbox())} left.")


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)

    listing = sub.add_parser("list", help="open feedback issues, most recurrent first")
    listing.add_argument("--skill")
    listing.set_defaults(run=cmd_list)

    report = sub.add_parser("report", help="record one occurrence")
    report.add_argument("--skill", required=True)
    report.add_argument("--impact", required=True, choices=IMPACTS)
    report.add_argument("--title", required=True, help="the class of failure, one line")
    report.add_argument("--what", required=True, help="what the skill said and what it caused")
    report.add_argument("--issue", type=int, help="existing issue this is one more occurrence of")
    report.set_defaults(run=cmd_report)

    sub.add_parser("flush", help="send queued occurrences").set_defaults(run=cmd_flush)

    args = parser.parse_args()
    if os.environ.get("LX_FEEDBACK", "").lower() == "off":
        print("Feedback disabled (LX_FEEDBACK=off).")
        return
    try:
        args.run(args)
    except Exception as error:  # never fail the run that reports
        print(f"Feedback not recorded ({error.__class__.__name__}: {error}).")


if __name__ == "__main__":
    main()
    sys.exit(0)
