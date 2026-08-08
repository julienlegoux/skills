---
name: review-epics
description: Review split-epics output against the source plan — coverage, boundaries, ordering, OKF structure, GitHub state — and write a prioritized docs/REPORT_N.md. Use when the user asks to audit, QA, or review created epics against the plan or scope.
---

# Review Epics

Audit the epic set that `split-epics` (or `define-change`) produced against the plan
it came from. The question to answer: could someone run `create-issues` across these
epics and end up building what the plan actually asked for?

How a review is graded, verified, delegated to another model, and written down is
defined once in `../_shared/review-interfaces.md` — read it before starting. The
artifacts under review are governed by `../_shared/pipeline-interfaces.md` (epic
schema, status lifecycle, GitHub facts) and `../_shared/bundle-interfaces.md` (link
forms, reserved files, language). Judge against those two files directly; an epic is
only malformed relative to what they define.

## Step 1: Resolve what is under review

The plan comes first, because everything else is graded against it:

- The path the user gave.
- Otherwise `docs/planning/SCOPE.md` — `define-scope`'s deliverable and
  `split-epics`' primary input. Its siblings `SPECS.md` and `CONVENTIONS.md` are
  context, never the document that was split; grading epics against them produces
  findings the epics were never meant to satisfy.
- Then `docs/PLAN.md`, `docs/plan.md`, `plan.md`, then the only plausible planning
  markdown under `docs/` outside `docs/planning/` and `docs/epics/`.
- Several plausible candidates → ask which one before reading further. Reviewing
  against the wrong source is a `P0` finding about your own report.

Then the epics: `docs/epics/index.md` if present, and every
`docs/epics/epic-*/EPIC_*.md` in full, frontmatter included. When an epic's `source`
names a heading or file, compare against that section specifically — it is a claim
the epic makes about its own provenance, and a false one is worth catching.

Read for context when present: the docs each epic's `## Context` links (typically
`docs/planning/SPECS.md` and `docs/planning/CONVENTIONS.md`), plus `CLAUDE.md`,
`AGENTS.md`, `CONTRIBUTING.md`, and `.github/ISSUE_TEMPLATE/`.

## Step 2: What to look for

- **Plan coverage** — every material goal, constraint, acceptance criterion and
  dependency in the plan lands in exactly one epic where it belongs. Constraints are
  the ones most often dropped: they belong to no single feature, so they fall between
  epics rather than into one.
- **No invented scope** — epics add no feature, promise, or constraint the plan does
  not support, unless flagged as an assumption. Invented scope is worse than missing
  scope: it gets built.
- **Epic boundaries** — each epic is independently shippable and actually epic-sized.
  Fragments too small to ship alone should be merged; an epic spanning several phases
  should be split, since `create-issues` will otherwise inherit the sprawl.
- **Ordering and dependencies** — epic numbers preserve plan order unless the plan
  numbers them itself, `depends_on` points at epics that really are prerequisites,
  and no cycle makes the set unstartable.
- **Faithful carry-over** — goal, scope, out-of-scope, acceptance criteria, risks and
  plan-wide constraints survive without over-compression. A summarised acceptance
  criterion stops being testable.
- **Context links** — epics *reference* the planning docs and never copy them, so the
  planning bundle stays the single source of truth. These links cross a bundle
  boundary, which changes their form — `bundle-interfaces.md` specifies which.
- **Schema and GitHub linkage** — frontmatter fields, and the agreement between
  `status`, `gh_issue`, `milestone` and `resource`, are specified in
  `pipeline-interfaces.md`. A deviation is `P2` unless it breaks downstream work.

## Step 3: Write the report

Follow the report contract in `../_shared/review-interfaces.md`. The subject line is
`# Epic Review Report <n>`; Scope names the epic artifacts reviewed, the plan they
were reviewed against, GitHub verification status, and the external model if one ran
the analysis pass.
