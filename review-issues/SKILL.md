---
name: review-issues
description: Review the output of the create-issues skill against an epic and, when useful, the original plan. Use when the user asks to audit, check, verify, QA, or review generated issue files, docs/epics/*/issues/, GitHub issues, sub-issues, milestones, or epic-to-issue conversion after running create-issues. Writes a numbered docs/REPORT_N.md review report with prioritized findings.
---

# Review Issues

Review the issues produced for an epic. Treat this as a code-review style audit:
find correctness and workflow risks first, then write a durable report in
`docs/REPORT_<n>.md`.

This skill is read-only for epic and issue artifacts. Do not repair local issue files,
GitHub issues, sub-issue links, or indexes unless the user explicitly asks for fixes
after seeing the report. The only file this skill should create or update during review
is the new report file.

## Step 1: Locate Inputs

Resolve the target epic:

- Use the path, epic number, or epic title the user provided.
- Otherwise list `docs/epics/epic-*/EPIC_*.md` and ask which epic to review.

Read the target `EPIC_<n>.md` in full, including frontmatter and body. Then read:

- Every markdown issue file under that epic's `issues/` folder.
- The epic's `issues/index.md`, if present.
- `docs/epics/index.md`, if useful for cross-epic dependencies.
- The original plan when the epic frontmatter `source` points to it, or when the user
  explicitly asks to compare all the way back to `plan.md` / `docs/PLAN.md`.

Also read relevant workflow context if present: `CLAUDE.md`, `AGENTS.md`,
`CONTRIBUTING.md`, `.github/ISSUE_TEMPLATE/`, `.github/PULL_REQUEST_TEMPLATE.md`, and
repo docs that define labels, tests, branch conventions, or review expectations.

## Step 2: Verify GitHub State When Available

If issue files contain `gh_issue`, `resource`, `milestone`, or dependency metadata,
verify them with `gh` when the CLI is available and authenticated:

- Confirm every referenced issue exists and has the expected title, state, milestone,
  labels, and URL.
- Confirm issue bodies preserve the local issue's scope and definition of done.
- Confirm each issue is attached to the epic's milestone.
- Confirm native sub-issue linkage to the epic issue when the API or CLI available in
  the environment can expose it. If not, mark sub-issue verification as not verified.

If GitHub cannot be checked, do not block the review. Mark GitHub verification as
`not verified` in the report and review local metadata for internal consistency.

## Step 3: Review Criteria

Prioritize findings by user impact:

- `P0` - The generated issues cannot be trusted or used: wrong epic, missing most of
  the epic scope, duplicate live issue creation, or broken artifact layout.
- `P1` - A material epic requirement, acceptance criterion, dependency, or constraint
  is missing, contradicted, assigned to the wrong issue, or impossible to implement in
  the given order.
- `P2` - Issue size, boundaries, ordering, GitHub metadata, OKF fields, links, or index
  entries are wrong enough to confuse implementation work.
- `P3` - Minor naming, wording, formatting, or traceability problems.

Check at least these areas:

- **Epic coverage** - Every material goal, scope item, acceptance criterion, dependency,
  and relevant note from the epic appears in one or more issues.
- **No invented scope** - Issues do not add features, tests, endpoints, UI, or
  implementation promises that the epic does not support unless clearly marked as an
  assumption.
- **Right-sized PRs** - Each issue should map to one focused PR. Split issues that look
  likely to approach 1000 changed lines. Merge issues that are too tiny to review or
  ship independently.
- **Implementation order** - Issue numbers and `depends_on` metadata allow a developer
  to work in order without being blocked by later work.
- **Issue body quality** - Titles are action-oriented; Summary, Scope, Out of scope,
  Acceptance criteria / Definition of done, Relevant files / areas, Dependencies, and
  PR size note are concrete and project-aware.
- **Project conventions** - Required tests, linting, issue templates, labels, and repo
  standards discovered from project docs are reflected in the issue bodies.
- **OKF structure** - Issue frontmatter includes required OKF and extension fields,
  cross-links are valid, `resource` appears only when a GitHub issue exists, and
  `issues/index.md` has no frontmatter.
- **GitHub linkage** - `status`, `gh_issue`, `resource`, milestone, labels, and
  sub-issue relationships agree with local files and GitHub when verified.

For each finding, cite exact files and line numbers whenever possible. Include the
epic line or section and the generated issue line or section that demonstrates the
problem.

## Step 4: Write `docs/REPORT_<n>.md`

Always write a new numbered report under `docs/` in the reviewed repository.

Find the next report number by scanning existing files named `docs/REPORT_<number>.md`
and choosing the next integer. If no reports exist, write `docs/REPORT_1.md`. Never
overwrite an existing report.

Use this structure:

```markdown
# Issue Review Report <n>

## Scope
- Epic reviewed: <path>
- Issue artifacts reviewed: <paths or glob>
- Plan reviewed: <path or "not reviewed">
- GitHub verification: verified | not verified (<reason>)

## Findings

### P1 - <short finding title>
- Location: <file:line>
- Epic source: <file:line or heading>
- Problem: <what is wrong>
- Impact: <why it matters>
- Recommendation: <specific fix>

## Coverage Notes
- <brief notes on epic areas that are well covered or intentionally out of scope>

## Open Questions
- <questions only when the epic or generated issues are genuinely ambiguous>
```

If there are no findings, write `No findings.` under `## Findings`, then still include
scope, coverage notes, and any residual verification gaps.

## Step 5: Report Back

In the final response, link the created report path and summarize the highest-severity
findings. If GitHub verification was skipped or failed, say so plainly.
