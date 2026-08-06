#!/usr/bin/env python3
"""Consistency digest for an OKF bundle: mechanical *leads* for a semantic
lint pass. Everything printed is a candidate to investigate by reading the
files, not a confirmed finding.

Usage:
    python okf_inventory.py <bundle-root>

Stdlib only (no pyyaml) - frontmatter is parsed with a small reader that
handles OKF's flat key/value fields plus inline and block list values.
"""
import argparse
import re
import sys
from collections import defaultdict
from fnmatch import fnmatch
from datetime import date, datetime
from pathlib import Path

RESERVED = {"index.md", "log.md"}
LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
INDEX_BULLET_RE = re.compile(r"^[*-]\s+\[([^\]]+)\]\(([^)]+)\)\s*[-–—]?\s*(.*)$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
DATE_HEADING_RE = re.compile(r"^##\s+(\d{4}-\d{2}-\d{2})\s*$")
PLACEHOLDER_RE = re.compile(
    r"\bTODO\b|\bTBD\b|\bFIXME\b|\bXXX\b|lorem ipsum|\bfill (?:this |me )?in\b"
    r"|\bplaceholder\b|\?\?\?|<[a-z][a-z0-9 _-]{2,40}>",
    re.IGNORECASE,
)


def split_frontmatter(text):
    if not text.startswith("---"):
        return None, text, 0
    lines = text.splitlines()
    if lines[0].strip() != "---":
        return None, text, 0
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return lines[1:i], "\n".join(lines[i + 1:]), i + 1
    return None, text, 0


def parse_frontmatter(fm_lines):
    """Flat key/value plus list values (inline [a, b] or block '- x' lines)."""
    fields = {}
    key = None
    for line in fm_lines:
        if not line.strip() or line.strip().startswith("#"):
            continue
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*)\s*:\s*(.*)$", line)
        if m:
            key, value = m.group(1), m.group(2).strip()
            if value.startswith("[") and value.endswith("]"):
                fields[key] = [v.strip().strip("'\"") for v in value[1:-1].split(",") if v.strip()]
            else:
                fields[key] = value.strip("'\"")
        elif key and re.match(r"^\s+-\s+", line):
            if not isinstance(fields.get(key), list):
                fields[key] = []
            fields[key].append(re.sub(r"^\s+-\s+", "", line).strip().strip("'\""))
    return fields


def load_ignore(bundle_root):
    """Read .okfignore at the bundle root: one gitignore-lite pattern per line.
    Blank lines and # comments are skipped. No negation support."""
    patterns = []
    f = bundle_root / ".okfignore"
    if f.is_file():
        for line in f.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                patterns.append(line.rstrip("/"))
    return patterns


def is_ignored(rel_posix, patterns):
    """A pattern containing '/' fnmatches the root-relative path or any of its
    directory prefixes; a pattern without '/' matches any single path segment."""
    parts = rel_posix.split("/")
    prefixes = ["/".join(parts[:i]) for i in range(1, len(parts) + 1)]
    for pat in patterns:
        if "/" in pat:
            if any(fnmatch(p, pat) for p in prefixes):
                return True
        elif any(fnmatch(seg, pat) for seg in parts):
            return True
    return False


def resolve_link(target, bundle_root, current_dir):
    if target.startswith(("http://", "https://", "mailto:", "#")):
        return None
    target = target.split("#", 1)[0]
    if not target:
        return None
    if target.startswith("/"):
        return (bundle_root / target.lstrip("/")).resolve()
    return (current_dir / target).resolve()


def strip_code_blocks(body):
    """Blank out fenced code block contents (keep line count) so placeholder
    and link scans don't fire on code examples."""
    out, in_fence = [], False
    for line in body.splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
            out.append("")
        else:
            out.append("" if in_fence else line)
    return "\n".join(out)


def parse_ts(value):
    if not value or isinstance(value, list):
        return None
    v = value.strip().replace("Z", "+00:00")
    for parse in (datetime.fromisoformat, date.fromisoformat):
        try:
            d = parse(v)
            return d.date() if isinstance(d, datetime) else d
        except ValueError:
            continue
    return None


def section(title):
    print(f"\n## {title}\n")


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle_root", type=Path)
    args = parser.parse_args()
    root = args.bundle_root.resolve()
    if not root.is_dir():
        print(f"error: {root} is not a directory", file=sys.stderr)
        return 2

    ignore = load_ignore(root)
    md_files = sorted(p for p in root.rglob("*.md")
                      if not is_ignored(p.relative_to(root).as_posix(), ignore))
    concepts, indexes, logs = {}, {}, {}
    for path in md_files:
        rel = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8")
        fm_lines, body, body_start = split_frontmatter(text)
        fields = parse_frontmatter(fm_lines) if fm_lines else {}
        entry = {"path": path, "rel": rel, "fields": fields, "body": body,
                 "body_start": body_start, "scan": strip_code_blocks(body)}
        if path.name == "index.md":
            indexes[rel] = entry
        elif path.name == "log.md":
            logs[rel] = entry
        else:
            concepts[rel] = entry

    print(f"# OKF inventory digest — {root}")
    print(f"\n{len(concepts)} concept file(s), {len(indexes)} index.md, {len(logs)} log.md")
    print("\nAll items below are LEADS — verify by reading before reporting.")

    # --- file census ---
    section("File census")
    for rel, c in concepts.items():
        f = c["fields"]
        tags = f.get("tags") if isinstance(f.get("tags"), list) else ([f["tags"]] if f.get("tags") else [])
        print(f"- {rel} | type={f.get('type', '∅')!r} | title={f.get('title', '∅')!r} | "
              f"ts={f.get('timestamp', '∅')} | tags={tags}")
        desc = f.get("description")
        print(f"    desc: {desc if desc else '∅'}")

    # --- index drift ---
    section("Index drift (unlisted files / dangling entries / description mismatches)")
    found = False
    for rel, idx in indexes.items():
        idir = idx["path"].parent
        listed = {}
        for i, line in enumerate(idx["body"].splitlines(), start=idx["body_start"] + 1):
            m = INDEX_BULLET_RE.match(line.strip())
            if m:
                resolved = resolve_link(m.group(2), root, idir)
                if resolved is not None:
                    listed[resolved] = (i, m.group(1), m.group(3).strip())
        siblings = [p for p in idir.iterdir()
                    if ((p.suffix == ".md" and p.name not in RESERVED) or p.is_dir())
                    and not is_ignored(p.relative_to(root).as_posix(), ignore)]
        for p in siblings:
            if p.resolve() not in listed and not (p.is_dir() and not any(p.rglob("*.md"))):
                print(f"- {rel}: does NOT list {p.relative_to(root).as_posix()}")
                found = True
        for resolved, (line_no, title, bullet_desc) in listed.items():
            if not resolved.exists():
                print(f"- {rel}:{line_no}: entry '{title}' -> missing target {resolved.name}")
                found = True
                continue
            try:
                target_rel = resolved.relative_to(root).as_posix()
            except ValueError:
                continue
            c = concepts.get(target_rel)
            if c:
                fm_desc = c["fields"].get("description", "")
                if isinstance(fm_desc, str) and fm_desc and bullet_desc and bullet_desc.rstrip(".") != fm_desc.rstrip("."):
                    print(f"- {rel}:{line_no}: description differs from {target_rel} frontmatter:")
                    print(f"    index:       {bullet_desc}")
                    print(f"    frontmatter: {fm_desc}")
                    found = True
                fm_title = c["fields"].get("title", "")
                if isinstance(fm_title, str) and fm_title and title != fm_title:
                    print(f"- {rel}:{line_no}: entry title {title!r} != frontmatter title {fm_title!r} ({target_rel})")
                    found = True
    if not found:
        print("(none detected)")

    # --- tag / type censuses ---
    for label, getter in (("Tag", lambda f: f.get("tags") if isinstance(f.get("tags"), list)
                           else ([f["tags"]] if f.get("tags") else [])),
                          ("Type", lambda f: [f["type"]] if f.get("type") else [])):
        section(f"{label} census")
        census = defaultdict(list)
        for rel, c in concepts.items():
            for v in getter(c["fields"]):
                census[v].append(rel)
        for v in sorted(census, key=str.lower):
            print(f"- {v!r} ×{len(census[v])}  ({', '.join(census[v][:4])}{'…' if len(census[v]) > 4 else ''})")
        groups = defaultdict(set)
        for v in census:
            groups[v.strip().lower().rstrip("s")].add(v)
        suspects = [g for g in groups.values() if len(g) > 1]
        if suspects:
            print(f"\n  Near-duplicate suspects:")
            for g in suspects:
                print(f"  - {sorted(g)}")

    # --- duplicate resources ---
    section("Duplicate resource URIs")
    by_res = defaultdict(list)
    for rel, c in concepts.items():
        r = c["fields"].get("resource")
        if isinstance(r, str) and r:
            by_res[r].append(rel)
    dupes = {r: rels for r, rels in by_res.items() if len(rels) > 1}
    for r, rels in dupes.items():
        print(f"- {r}\n    claimed by: {', '.join(rels)}")
    if not dupes:
        print("(none)")

    # --- timestamps ---
    section("Timestamp anomalies")
    today = date.today()
    log_mentions = defaultdict(lambda: None)  # concept rel -> latest log date mentioning it
    for rel, lg in logs.items():
        current = None
        for line in lg["body"].splitlines():
            m = DATE_HEADING_RE.match(line.strip())
            if m:
                current = parse_ts(m.group(1))
                continue
            if current:
                for _, target in LINK_RE.findall(line):
                    resolved = resolve_link(target, root, lg["path"].parent)
                    if resolved is None:
                        continue
                    try:
                        t = resolved.relative_to(root).as_posix()
                    except ValueError:
                        continue
                    if log_mentions[t] is None or current > log_mentions[t]:
                        log_mentions[t] = current
    found = False
    for rel, c in concepts.items():
        raw = c["fields"].get("timestamp")
        ts = parse_ts(raw if isinstance(raw, str) else None)
        if raw and ts is None:
            print(f"- {rel}: unparseable timestamp {raw!r}")
            found = True
        elif ts and ts > today:
            print(f"- {rel}: timestamp {ts} is in the future")
            found = True
        if ts and log_mentions.get(rel) and log_mentions[rel] > ts:
            print(f"- {rel}: timestamp {ts} older than latest log mention {log_mentions[rel]} (stale?)")
            found = True
    if not found:
        print("(none detected)")

    # --- log checks ---
    section("Log checks")
    found = False
    for rel, lg in logs.items():
        dates, order_flagged = [], False
        for i, line in enumerate(lg["body"].splitlines(), start=lg["body_start"] + 1):
            m = DATE_HEADING_RE.match(line.strip())
            if m:
                d = parse_ts(m.group(1))
                if dates and d and dates[-1] and d > dates[-1] and not order_flagged:
                    print(f"- {rel}:{i}: dates not newest-first ({d} appears below {dates[-1]})")
                    found = order_flagged = True
                dates.append(d)
            for _, target in LINK_RE.findall(line):
                resolved = resolve_link(target, root, lg["path"].parent)
                if resolved is not None and not resolved.exists():
                    print(f"- {rel}:{i}: links to missing {target}")
                    found = True
    if not found:
        print("(none detected)")

    # --- placeholders ---
    section("Placeholder / template-leftover hits (code blocks excluded)")
    found = False
    for group in (concepts, indexes, logs):
        for rel, c in group.items():
            for i, line in enumerate(c["scan"].splitlines(), start=c["body_start"] + 1):
                if PLACEHOLDER_RE.search(line):
                    print(f"- {rel}:{i}: {line.strip()[:100]}")
                    found = True
    if not found:
        print("(none detected)")

    # --- empty sections ---
    section("Empty sections (heading with no content before the next heading)")
    found = False
    for rel, c in concepts.items():
        lines = c["body"].splitlines()
        for i, line in enumerate(lines):
            if HEADING_RE.match(line):
                j = i + 1
                while j < len(lines) and not lines[j].strip():
                    j += 1
                if j >= len(lines) or HEADING_RE.match(lines[j]):
                    print(f"- {rel}:{c['body_start'] + i + 1}: '{line.strip()}' is empty")
                    found = True
    if not found:
        print("(none detected)")

    # --- inbound links / orphans ---
    section("Orphan candidates (no inbound links from any doc, index, or log)")
    inbound = defaultdict(int)
    for group in (concepts, indexes, logs):
        for rel, c in group.items():
            for _, target in LINK_RE.findall(c["scan"]):
                resolved = resolve_link(target, root, c["path"].parent)
                if resolved is None:
                    continue
                try:
                    inbound[resolved.relative_to(root).as_posix()] += 1
                except ValueError:
                    continue
    orphans = [rel for rel in concepts if inbound[rel] == 0]
    for rel in orphans:
        print(f"- {rel}")
    if not orphans:
        print("(none)")

    print("\n---\nDigest complete. These are leads; read the files before reporting.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
