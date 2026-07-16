#!/usr/bin/env python3
"""Check a directory tree for conformance with the Open Knowledge Format (OKF) v0.1 spec.

Usage:
    python validate_okf.py <bundle-root> [--strict]

Exit code is non-zero only when a real conformance violation (spec section 9)
is found. Recommended-field gaps and broken cross-links are reported as
warnings unless --strict is passed, in which case they also fail the run.

No third-party dependencies (works without pyyaml) - frontmatter is parsed
with a small line-based reader that's sufficient for OKF's flat key/value and
list fields.
"""
import argparse
import re
import sys
from pathlib import Path

RESERVED = {"index.md", "log.md"}
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
DATE_HEADING_RE = re.compile(r"^##\s+(.+)$")
ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
RECOMMENDED_FIELDS = ["title", "description", "tags", "timestamp"]


def split_frontmatter(text):
    """Return (frontmatter_lines, body) or (None, text) if no frontmatter block."""
    if not text.startswith("---"):
        return None, text
    lines = text.splitlines()
    if lines[0].strip() != "---":
        return None, text
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return lines[1:i], "\n".join(lines[i + 1:])
    return None, text  # opening --- with no closing --- is not valid frontmatter


def parse_frontmatter_fields(fm_lines):
    """Best-effort flat key/value extraction. Good enough for presence/emptiness checks."""
    fields = {}
    for line in fm_lines:
        if not line.strip() or line.strip().startswith("#"):
            continue
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*)\s*:\s*(.*)$", line)
        if m:
            key, value = m.group(1), m.group(2).strip()
            fields[key] = value
    return fields


def resolve_link(target, bundle_root, current_dir):
    if target.startswith(("http://", "https://", "mailto:", "#")):
        return None  # external or in-page anchor, not a bundle-relative link
    target = target.split("#", 1)[0]
    if not target:
        return None
    if target.startswith("/"):
        return (bundle_root / target.lstrip("/")).resolve()
    return (current_dir / target).resolve()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle_root", type=Path, help="Path to the bundle root directory")
    parser.add_argument("--strict", action="store_true",
                         help="Treat warnings (missing recommended fields, broken links) as errors")
    args = parser.parse_args()

    bundle_root = args.bundle_root.resolve()
    if not bundle_root.is_dir():
        print(f"error: {bundle_root} is not a directory", file=sys.stderr)
        return 2

    errors = []
    warnings = []
    md_files = sorted(bundle_root.rglob("*.md"))

    for path in md_files:
        rel = path.relative_to(bundle_root)
        text = path.read_text(encoding="utf-8")
        fm_lines, body = split_frontmatter(text)

        if path.name == "index.md":
            is_root = rel.parent == Path(".")
            if fm_lines is not None:
                fields = parse_frontmatter_fields(fm_lines)
                if not is_root:
                    errors.append(f"{rel}: index.md must not have frontmatter (only the bundle-root index.md may, for okf_version)")
                elif set(fields.keys()) - {"okf_version"}:
                    errors.append(f"{rel}: bundle-root index.md frontmatter may only contain 'okf_version'")
            _check_links(rel, body, bundle_root, path.parent, warnings)
            continue

        if path.name == "log.md":
            for line in body.splitlines():
                m = DATE_HEADING_RE.match(line)
                if m and not ISO_DATE_RE.match(m.group(1).strip()):
                    errors.append(f"{rel}: log.md date heading '{line.strip()}' must be ISO 8601 (## YYYY-MM-DD)")
            _check_links(rel, body, bundle_root, path.parent, warnings)
            continue

        # Concept document
        if fm_lines is None:
            errors.append(f"{rel}: missing or malformed YAML frontmatter block")
            continue
        fields = parse_frontmatter_fields(fm_lines)
        if not fields.get("type"):
            errors.append(f"{rel}: frontmatter missing required non-empty 'type' field")
        for field in RECOMMENDED_FIELDS:
            if not fields.get(field):
                warnings.append(f"{rel}: missing recommended field '{field}'")
        _check_links(rel, body, bundle_root, path.parent, warnings)

    print(f"Scanned {len(md_files)} markdown file(s) under {bundle_root}\n")

    if errors:
        print(f"ERRORS ({len(errors)}):")
        for e in errors:
            print(f"  - {e}")
        print()
    if warnings:
        print(f"WARNINGS ({len(warnings)}):")
        for w in warnings:
            print(f"  - {w}")
        print()

    if not errors and not warnings:
        print("Bundle is fully conformant with no warnings.")

    fail = bool(errors) or (args.strict and bool(warnings))
    print("RESULT:", "FAIL" if fail else "PASS")
    return 1 if fail else 0


def _check_links(rel, body, bundle_root, current_dir, warnings):
    for target in LINK_RE.findall(body):
        resolved = resolve_link(target, bundle_root, current_dir)
        if resolved is None:
            continue
        if not resolved.exists():
            warnings.append(f"{rel}: broken link -> {target}")


if __name__ == "__main__":
    sys.exit(main())
