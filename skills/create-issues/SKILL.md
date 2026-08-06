---
name: create-issues
description: Break one epic (docs/epics/epic-N-slug/EPIC_N.md) into PR-sized issues — one .md file each plus a real GitHub issue on the epic's milestone, linked as a native sub-issue of the epic's tracking issue. Use whenever the user wants an epic broken into tasks, tickets, or issues.
---

# Create Issues for an Epic

An epic is too big to review as one PR. This skill turns one epic into a set of
issues sized so each becomes a reviewable PR — and wires each one up as a GitHub
sub-issue of the epic, so the epic issue's progress bar tracks completion
automatically.

This skill assumes `split-epics` already ran for this epic (so it has a `gh_issue`
and `milestone` recorded). If it hasn't, say so and offer to stop, or proceed without
milestone/sub-issue linkage if the user explicitly wants standalone issues.

## Output format: OKF

`docs/epics/` is an OKF v0.1 bundle — `split-epics` (or `define-change`)
established it, and every issue file this skill adds must fit the same rules. The
issue file schema and status lifecycle are defined once in
`../_shared/pipeline-interfaces.md`, and the rules for anything written under
`docs/` — English content, link and index forms, reserved files, committing what you
write — in `../_shared/bundle-interfaces.md`. Read both before drafting anything.

## Step 1: Resolve the target epic

The user usually names it ("epic 2", "the billing epic", a path). If ambiguous, list
`docs/epics/*/EPIC_*.md` (or read `docs/epics/index.md` if present) and ask.

Read the epic file in full, including frontmatter (`epic`, `gh_issue`, `milestone`)
and body (Goal, Scope, Out of scope, Acceptance criteria, Dependencies). If `gh_issue`
is `null`, stop and tell the user to run `split-epics` first — everything downstream
(the milestone, the sub-issue link target) depends on that issue existing.

## Step 2: Learn the project's conventions

Before drafting a single issue, check what already exists so the issues you write fit
the repo rather than reading as generic filler:

- The epic's `## Context` links — typically `docs/planning/SPECS.md` (the decided
  stack, so issue sizing and file paths match reality) and
  `docs/planning/CONVENTIONS.md` (repo standards) — read whichever exist in full.
- `docs/planning/DEVIATIONS.md` if it exists — the register of standards earlier epics
  proved wrong in practice (see `../_shared/pipeline-interfaces.md`). An issue written
  against a decided standard the code already abandoned sends its implementer into a
  wall someone else already hit; where a live deviation touches this epic, write the
  issue against reality and cite the entry.
- `CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`, `docs/CONVENTIONS.md` (or similar) —
  coding standards, required testing, commit/branch naming, review expectations.
- `.github/PULL_REQUEST_TEMPLATE.md` and `.github/ISSUE_TEMPLATE/` — if a template
  exists, match its sections instead of inventing your own issue format.
- `gh label list --json name -q '.[].name'` — reuse whatever labeling scheme the repo
  already has (e.g. `area:backend`, `good first issue`) rather than inventing new ones.
- Skim the actual codebase structure relevant to this epic (main directories, test
  layout) so the "relevant files" you note per issue are real paths, not guesses. On a
  greenfield repo (or one where this epic's code genuinely doesn't exist yet), there's
  nothing to skim — say so explicitly in each issue's "Relevant files / areas" section
  (e.g. "No existing code for this yet — paths below follow typical <stack>
  conventions, not verified against this repo") rather than presenting a guess as if
  it were a confirmed path.

Fold whatever's relevant directly into each issue body — e.g. if `CONTRIBUTING.md`
requires tests for new endpoints, say so in the issue's Definition of Done instead of
leaving it implicit.

## Step 3: Break the epic into issues

The target is simple: **each issue should become one focused PR** — one cohesive
capability, or a small handful of clearly related tweaks, not a grab-bag. Roughly
500 changed lines is the comfortable size, and anything that looks like it's
approaching 1000 needs to be split further. This is a gut-check, not a precise
estimate — nobody can count lines before the code exists — so don't over-engineer the
math. A few ways to actually split scope, roughly in order of preference:

- **By layer or endpoint**, not by "everything for this feature" — e.g. "add the
  `POST /sessions` endpoint + its handler" is one issue; "add the login UI that calls
  it" is another; don't bundle backend + frontend + migration into one issue just
  because they serve the same feature.
- **By independently testable unit** — if it needs its own test suite, it's probably
  its own issue.
- Watch for issues that are too *small* as well as too big — three one-line config
  tweaks with no independent value are better as one issue than three PRs nobody wants
  to review separately.

For each issue, capture:

- **Title** — specific and action-oriented ("Add POST /sessions endpoint", not
  "Backend work").
- **Rough size** — S (~under 200 lines), M (~200–500), or L (~500–1000, only use this
  when it genuinely can't be split further — flag these to the user explicitly in
  the confirmation step, since L is the ceiling, not the target).
- **Dependencies** — does it block or depend on another issue in this batch? Preserve
  ordering; note it in both directions.

Number issues within the epic by a sensible dependency/build order (issue 1 shouldn't
depend on issue 3), 1-indexed, zero-padded to two digits.

## Step 4: Draft the issue files

Slug the title the same way `split-epics` does (lowercase kebab-case, ASCII, ~40 char
cap). Write each to `docs/epics/epic-<n>-<slug>/issues/<nn>-<slug>.md` using the
issue file template in `../_shared/pipeline-interfaces.md` — `status: draft`,
`gh_issue: null`, no `resource` yet (both arrive in Step 7). Section content
guidance: Summary = what this PR does and why, in the epic's context; Scope = the
specific bounded change; Out of scope = explicitly not this issue, especially
anything a reviewer might expect to see but shouldn't; Acceptance criteria as a
checklist including any testing requirement pulled from CONTRIBUTING.md etc.;
Relevant files / areas = the real paths Step 2 verified (or the explicit
greenfield caveat); Dependencies = blocked by / blocks, or "None"; PR size note =
"Target ~500 changed lines; if this grows past ~1000, split it before opening the
PR."

Prefer acceptance criteria that are executable over prose: a concrete command and
its expected outcome, a named test that must pass, an observable behavior with its
input and output. An implementer (often a smaller model) turns "criterion → failing
test" mechanically when the criterion is testable, and stalls or improvises when
it's vibes. Likewise, carry file-level findings into the issue body as real paths
(`src/x.ts:120`, the named contract that breaks) rather than summarizing them away.

Also write or update `docs/epics/epic-<n>-<slug>/issues/index.md` (no frontmatter —
non-root index) listing every issue in this batch:

```markdown
# Issues — Epic <n>: <title>

* [<title>](./01-<slug>.md) - <size>, draft
```

## Step 5: Show the breakdown and proceed

List all drafted issues for the epic: number, title, size, dependencies. Flag any
sized L prominently and say why it couldn't be split further. Then continue straight
into Step 6 — creation is the default, not something to ask permission for: the user
invoked the skill to get issues, and a bad split is cheap to fix after the fact
(edit the `.md`, `gh issue edit`, close strays).

The exception is when the user asked for review (at invocation or mid-run — "let me
review first", "one by one", "step by step"): then go issue by issue instead —
display each issue in full (frontmatter + body), wait for sign-off or edits, create
it on GitHub, and move to the next.

## Step 6: Create the GitHub issues

You need `owner/repo` (`gh repo view --json nameWithOwner -q .nameWithOwner`) and the
epic's `gh_issue` and `milestone` number from its frontmatter.

For each issue, in dependency order:

```bash
gh issue create \
  --title "<title>" \
  --body-file <tmpfile> \
  --milestone "<epic's milestone title>" \
  --label <whatever convention Step 2 found, or the epic label as a fallback>
```

Capture the new issue's number, then attach it as a sub-issue of the epic. The
sub-issues API needs the child's *numeric id* (not its `#number`); send it with `-F`:

```bash
child_id=$(gh api "repos/<owner>/<repo>/issues/<new_issue_number>" --jq '.id')
gh api -X POST "repos/<owner>/<repo>/issues/<epic_gh_issue_number>/sub_issues" -F sub_issue_id="$child_id"
```

**Idempotency:** if an issue's `.md` already has `gh_issue` set, skip creating it again
— report it as already-created instead. If the user wants to force a recreate, that's
an explicit ask, not the default.

## Step 7: Write results back

Update each issue's frontmatter: `status: open`, `gh_issue: <number>`, plus the OKF
fields that only become known now — `resource: https://github.com/<owner>/<repo>/issues/<number>`
and a refreshed `timestamp`. Update `docs/epics/epic-<n>-<slug>/issues/index.md` so
each bullet reflects the real status (and, if you want, links straight to the GitHub
issue via its `resource` field).

If `docs/epics/log.md` exists, append an entry per issue created (see `split-epics`'
Step 7 for the log format). Don't create it if it doesn't already exist.

Then commit and push per the commit rule in `../_shared/bundle-interfaces.md`,
staging only what this run touched (the epic's `issues/` folder, plus `log.md` if
appended) — e.g. `docs: add Epic <n> issues`.

Report a summary: issues created (with links), their sizes, the commit pushed, and
a reminder that the epic's GitHub issue now shows them as sub-issues/progress.
