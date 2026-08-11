---
name: review-implementation
description: Audit the code an epic actually shipped — review its merged diff against the epic's acceptance criteria, docs/planning/CONVENTIONS.md and the accepted drift, then record a disposition per finding in docs/reviews/<date>-implementation-<subject>.md for triage-reports to convert into work. Use once an epic's PRs are merged and the question is the quality of the implemented code rather than the plan that produced it.
---

# Review an Epic's Implementation

Every PR in the epic was reviewed alone, and passed alone. That is the problem. The
duplication between issue 3 and issue 7, the abstraction four implementers each
re-invented because none could see the others, the convention that eroded a little per
PR — none of it is visible from inside a single PR, and all of it is now merged. This
skill reviews the **accumulated whole**, once, against yardsticks the pipeline already
decided.

Those yardsticks are what separates this from a generic code review: the epic's
acceptance criteria, `docs/planning/CONVENTIONS.md`, and `docs/planning/DRIFT.md`. The
issue schema, `gh_pr`, and the drift register's format live in
`../_shared/pipeline-interfaces.md`; the rules for anything written under `docs/` in
`../_shared/bundle-interfaces.md`. Read both before Step 1. A third governs nothing
under review: `../_shared/feedback-interfaces.md`, the closing reflex for what this run
teaches about *this skill*, read at Step 5.

## Scope boundary

This skill reviews **code**. `close-epic` verifies state — statuses, merges, milestone,
branches — and runs before this one. `review-epics` and `review-issues` audit *planning*
artifacts and run before implementation. Three different questions; don't answer a
neighbour's.

It never patches product code. A finding becomes a follow-up issue or a register entry,
never a fix applied here — a reviewer who fixes what they find has stopped reviewing and
started implementing unreviewed work.

The one place it executes rather than reads is the mutation probe in Step 3, and that
happens in a **disposable worktree**: nothing is committed, nothing pushed, the worktree
is removed afterward. The user's tree is never mutated.

## Step 1: Establish the review surface

The unit of review is the epic's merged diff, attributed per issue.

Read each issue's `gh_pr` from `docs/epics/epic-<n>-<slug>/issues/*.md`, resolve each to
its merge commit, and derive the diff range. **Never take `status: done` as evidence a PR
merged** — resolve the PR. `implement-epic` forbids squash, so every PR is a merge commit
and per-issue attribution is reliable even after `close-epic` deleted the branches.
Recipes, and the fallbacks for a missing `gh_pr` or an unavailable `gh`, are in
`references/diff-recipes.md`.

Note what is *not* in the diff too: an issue with no PR shipped nothing, and its
acceptance criteria are unmet by definition rather than by review.

## Step 2: Load the yardsticks

- The epic's `## Acceptance criteria`, and each issue's `## Acceptance criteria /
  Definition of done`. These are what the code is judged against — not your taste.
- `docs/planning/CONVENTIONS.md` and `SPECS.md`, for the standards the project decided.
- `docs/planning/DRIFT.md`. **Accepted drift is not a finding.** The user already triaged
  it at close; re-reporting it burns their attention on a decision they made, and teaches
  them to skim this report.

Missing DRIFT.md means either no drift or no close — check which, because the second
means the epic isn't ready for this review.

## Step 3: Review through the lenses

Five lenses, each a separate subagent with the full diff and one job. One context trying
to hold all five degrades on a large epic — the exact failure this skill exists to catch.
Spawn them concurrently.

| Lens | Asks |
|---|---|
| **Acceptance honesty** | Does the code actually satisfy each criterion? |
| **Test integrity** | Would we know if it stopped? |
| **Seams** | What does the merged whole show that no single PR could? |
| **Convention erosion** | Where did the decided standards quietly lapse? |
| **Correctness & risk** | Real bugs and unsafe handling in the integrated result. |

The first two are halves of one question and must stay separate: green tests over
unsatisfied criteria, and satisfied criteria over tests that prove nothing, are different
failures with different fixes. Prompts and the substance of each lens are in
`references/review-lenses.md`; test integrity has its own brief and protocol in
`references/test-integrity.md`, because it executes.

Merge the returned findings, dedupe across lenses (one root cause reported four times
reads as four problems), drop anything DRIFT.md already covers, and rank P0–P3 on the
same scale the sibling reviews use:

- **P0** — the epic did not ship what it claims: a criterion unmet, a test suite that
  proves nothing about it.
- **P1** — a real defect, security risk, or a convention breach with teeth.
- **P2** — duplication, erosion, or a seam that will cost the next epic.
- **P3** — naming, wording, local tidiness.

Cite `file:line` and the criterion or convention line each finding violates. A finding
that can't name what it violates is taste, and belongs in the report's notes, not its
findings.

## Step 4: Triage the findings

Present all findings in one batch with a recommended disposition each, and wait. Three
outcomes, and the middle one is the one people forget:

- **fix-now** → recorded as this finding's disposition in the report, and converted into
  work by `triage-reports`, which reads every report in `docs/reviews/` and groups repairs
  across them. Don't create the issues here: one finding fixed alone, while its four siblings from
  the same root cause sit in three other reports, is the duplication this skill exists to
  catch. Hand off to `define-change` instead when a fix is larger than an epic.
- **accept** → the code is right and the *standard* is wrong. That is drift discovered by
  review rather than by implementation, so it becomes a `docs/planning/DRIFT.md` entry in
  the format `../_shared/pipeline-interfaces.md` defines, with this report as its
  evidence link. Accepting also means SPECS/CONVENTIONS should stop contradicting the
  code.
- **won't-fix** → stays in the report, with the reason. Still written down: the next
  reviewer will find it again otherwise.

Dispositions are the user's call, not yours — each one either creates work or rewrites a
standard.

## Step 5: Write the report and hand off

Write `docs/reviews/<YYYY-MM-DD>-implementation-<epic-slug>.md`, in the directory and
under the naming scheme the sibling reviews use — `../_shared/review-interfaces.md`,
"The report", which also owns the same-day `-2` suffix. The name carries the date, the
kind and the epic, so it cannot collide with a report that already exists.

```markdown
# Implementation Review Report

## Scope
- Epic reviewed: <path>
- Diff reviewed: <range>, <n> PRs, <n> files
- Yardsticks: acceptance criteria | CONVENTIONS.md | DRIFT.md (<n> accepted entries excluded)
- Test integrity: <n> criteria read, <n> probed, <n> mutants survived
- Not verified: <what, and why>

## Findings

### P0 - <short finding title>
- Location: <file:line>
- Violates: <criterion, convention line, or "correctness">
- Problem: <what is wrong>
- Evidence: <the surviving mutant, the failing case, the duplicated pair>
- Disposition: fix-now | accepted (drift) | won't-fix - <reason>

## What holds up
- <what the epic got right — a report of only defects misrepresents the work>

## Open questions
```

State the probe budget explicitly. Silence about what wasn't probed reads as coverage,
and this skill's whole value is refusing to imply verification it didn't do.

Commit per `../_shared/bundle-interfaces.md`, then report the P0/P1 findings, the drift
entries written, and that `triage-reports` converts the `fix-now` dispositions — this
report's and every earlier one's — into the remediation epic.

Then close the run per `../_shared/feedback-interfaces.md` — silently, unless this run
turned up something about this skill that clears both its filters. A finding about the
code under review is not that; it is already a disposition.
