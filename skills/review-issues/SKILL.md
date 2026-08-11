---
name: review-issues
description: Review create-issues output against its epic (and the plan when useful) — coverage, sizing, ordering, OKF fields, GitHub linkage — and write a prioritized docs/reviews/<date>-issues-<subject>.md. Use when the user asks to audit, QA, or review generated issues.
---

# Review Issues

Audit the issues `create-issues` produced for one epic. The question to answer: could
a developer work these issues in order, one PR each, and finish the epic without
being blocked or building something the epic never asked for?

How a review is graded, verified, delegated to another model, and written down is
defined once in `../_shared/review-interfaces.md` — read it before starting. The
artifacts under review are governed by `../_shared/pipeline-interfaces.md` (issue
schema, status lifecycle, GitHub facts) and `../_shared/bundle-interfaces.md` (link
forms, reserved files, language). Judge against those two files directly; an issue is
only malformed relative to what they define. A fourth contract judges nothing:
`../_shared/feedback-interfaces.md`, the closing reflex for what this run teaches about
*this skill*, read at Step 3.

## Step 1: Resolve what is under review

The epic comes first, because the issues are graded against it:

- The path, epic number, or title the user gave.
- Otherwise list `docs/epics/epic-*/EPIC_*.md` and ask which epic to review — there
  is no safe default when several epics have issues.

Read that `EPIC_<n>.md` in full, frontmatter and body, then:

- Every issue file under the epic's `issues/`, and its `issues/index.md` if present.
- `docs/epics/index.md`, when cross-epic dependencies matter.
- The docs the epic's `## Context` links — typically `docs/planning/SPECS.md` and
  `docs/planning/CONVENTIONS.md`. Sizing, file paths and required tests are only
  judgeable against the stack and standards decided there.
- The original plan when the epic's `source` points at it, or when the user asks to
  compare all the way back. Otherwise the epic is the contract: an issue is not wrong
  for omitting something the epic itself dropped — that is `review-epics`' finding,
  not this one's.

Read for context when present: `CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`,
`.github/ISSUE_TEMPLATE/`, `.github/PULL_REQUEST_TEMPLATE.md`, and any repo doc
defining labels, tests, or branch conventions.

## Step 2: What to look for

- **Epic coverage** — every goal, scope item, acceptance criterion and dependency in
  the epic appears in at least one issue. Acceptance criteria are the ones that go
  missing: they are easy to summarise away and impossible to verify afterwards.
- **No invented scope** — no endpoint, test, UI or implementation promise the epic
  does not support, unless flagged as an assumption. It will get built.
- **Right-sized PRs** — one issue, one focused, reviewable PR. Split anything heading
  toward ~1000 changed lines; merge anything too small to ship on its own. Sizing is
  the finding developers feel first.
- **Implementation order** — issue numbers and `depends_on` let someone work top to
  bottom without hitting a prerequisite that comes later.
- **Issue body quality** — action-oriented title, and Summary, Scope, Out of scope,
  Acceptance criteria, Relevant files, Dependencies and PR size concrete enough to
  act on. "Implement the backend" is a finding, not an issue.
- **Project conventions** — required tests, linting, labels and templates discovered
  from the repo and from `CONVENTIONS.md` / `SPECS.md` are reflected in the bodies,
  so the implementer is not left to guess them.
- **Schema and GitHub linkage** — issue frontmatter fields, `issues/index.md`, and
  the agreement between `status`, `gh_issue`, `resource`, milestone, labels and
  sub-issue relationships are specified in `pipeline-interfaces.md`. Sub-issue
  linkage in particular is what makes the epic issue's progress bar honest, so a
  break there is `P2` even when every file looks fine.

## Step 3: Write the report

Follow the report contract in `../_shared/review-interfaces.md`: the path is
`docs/reviews/<YYYY-MM-DD>-issues-<subject>.md`, where `<subject>` is the epic whose
issues were reviewed (`epic-4`). The subject line is `# Issue Review Report`; Scope
names the issue artifacts reviewed, the epic (and plan, when read) they were reviewed
against, GitHub verification status, and the external model if one ran the analysis
pass.

Then close the run per `../_shared/feedback-interfaces.md` — silently, unless this run
turned up something about this skill that clears both its filters. A finding about the
artifacts under review is not that; it belongs in the report.
