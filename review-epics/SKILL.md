---
name: review-epics
description: Review the output of the split-epics skill against the source plan document. Use when the user asks to audit, check, verify, QA, or review created epics, docs/epics/, EPIC_N.md files, GitHub epic issues, milestones, or plan-to-epic conversion against docs/planning/SCOPE.md (the define-scope deliverable), a legacy plan.md / docs/PLAN.md, or another planning document. Writes a numbered docs/REPORT_N.md review report with prioritized findings.
---

# Review Epics

Review the epics produced from a plan. Treat this as a code-review style audit:
find correctness problems first, then write a durable report in `docs/REPORT_<n>.md`.

This skill is read-only for the epic artifacts. Do not repair epics, milestones, issues,
or indexes unless the user explicitly asks for fixes after seeing the report. The only
file this skill should create or update during review is the new report file.

## Step 1: Locate Inputs

Resolve the source plan first:

- Use the path the user provided.
- Otherwise prefer `docs/planning/SCOPE.md` — the define-scope skill's deliverable and
  split-epics' primary input. Never treat its siblings `SPECS.md`/`CONVENTIONS.md` or
  the decision docs under `docs/planning/*/` as the plan — they are context, not the
  document that was split.
- Then fall back to `docs/PLAN.md`, `docs/plan.md`, `plan.md`, then the only plausible
  planning markdown file under `docs/` outside `docs/planning/` and `docs/epics/`.
- If multiple plausible plans exist, ask which one to use.

Resolve the generated epics:

- Read `docs/epics/index.md` if present.
- Read every `docs/epics/epic-*/EPIC_*.md` in full, including frontmatter.
- If an epic frontmatter `source` points to a heading or file, compare it to the
  matching plan section when possible.

Also read relevant workflow context if present: `docs/planning/SPECS.md` and
`docs/planning/CONVENTIONS.md` (the planning-bundle context split-epics links into
each epic's `## Context` section), `CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`,
`.github/ISSUE_TEMPLATE/`, and any repo docs that define planning or issue
conventions.

## Step 2: Verify GitHub State When Available

If epic files contain `gh_issue`, `milestone`, or `resource`, verify them with `gh`
when the CLI is available and authenticated:

- Confirm each referenced issue exists, has the expected title, and is open unless the
  local status says otherwise.
- Confirm each milestone exists and matches the epic title convention used by
  `split-epics`.
- Confirm each epic issue links back to the local `EPIC_<n>.md` file.

If GitHub cannot be checked, do not block the review. Mark GitHub verification as
`not verified` in the report and review the local metadata for internal consistency.

## Step 3: Review Criteria

Prioritize findings by user impact:

- `P0` - The generated epic set cannot be trusted or used: wrong plan, missing most
  planned work, overwritten existing tracked state, or broken artifact layout.
- `P1` - A material plan requirement, acceptance criterion, dependency, or constraint
  is missing, assigned to the wrong epic, or contradicted by an epic.
- `P2` - Epic boundaries, ordering, GitHub metadata, OKF fields, links, or index
  entries are wrong enough to confuse downstream `create-issues` work.
- `P3` - Minor naming, wording, formatting, or traceability problems.

Check at least these areas:

- **Plan coverage** - Every material goal, constraint, acceptance criterion, and
  dependency in the plan is represented in exactly the right epic context.
- **No invented scope** - Epics do not add features, promises, or constraints that are
  not in the plan unless clearly marked as an assumption or note.
- **Epic boundaries** - Each epic is independently shippable and large enough to be an
  epic. Tiny fragments should be merged; sprawling multi-phase epics should be split.
- **Ordering and dependencies** - Epic numbers preserve the plan order unless the plan
  explicitly numbers them. Dependencies point to the right epics and do not create
  impossible cycles.
- **Faithful carry-over** - Goal, scope, out-of-scope, acceptance criteria, risks,
  notes, and plan-wide constraints are preserved without over-compression.
- **OKF structure** - `docs/epics/index.md` is the bundle root index, each `EPIC_<n>.md`
  has required frontmatter, cross-links are bundle-relative absolute paths, and
  `resource` is present only when a backing GitHub issue exists.
- **Context links** - When `docs/planning/SPECS.md` / `docs/planning/CONVENTIONS.md`
  exist, each epic's `## Context` section links each one that exists via a plain
  relative path (e.g. `../../planning/SPECS.md` — these cross bundle boundaries, so
  bundle-relative leading-`/` links are wrong here), and the section is omitted
  entirely when neither exists. Epics reference these docs, never copy their content
  — the planning docs stay the single source of truth.
- **GitHub linkage** - `status`, `gh_issue`, `milestone`, and `resource` agree with
  each other and with GitHub when verified.

For each finding, cite exact files and line numbers whenever possible. Include the
plan line or section and the generated epic line or section that demonstrates the
problem.

## Step 4: Write `docs/REPORT_<n>.md`

Always write a new numbered report under `docs/` in the reviewed repository.

Find the next report number by scanning existing files named `docs/REPORT_<number>.md`
and choosing the next integer. If no reports exist, write `docs/REPORT_1.md`. Never
overwrite an existing report.

Use this structure:

```markdown
# Epic Review Report <n>

## Scope
- Plan reviewed: <path>
- Epic artifacts reviewed: <paths or glob>
- GitHub verification: verified | not verified (<reason>)

## Findings

### P1 - <short finding title>
- Location: <file:line>
- Plan source: <file:line or heading>
- Problem: <what is wrong>
- Impact: <why it matters>
- Recommendation: <specific fix>

## Coverage Notes
- <brief notes on plan areas that are well covered or intentionally out of scope>

## Open Questions
- <questions only when the plan or generated epics are genuinely ambiguous>
```

If there are no findings, write `No findings.` under `## Findings`, then still include
scope, coverage notes, and any residual verification gaps.

## Step 5: Report Back

In the final response, link the created report path and summarize the highest-severity
findings. If GitHub verification was skipped or failed, say so plainly.
