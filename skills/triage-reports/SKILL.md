---
name: triage-reports
description: Turn the findings accumulated across a repo's docs/REPORT_*.md series into one triaged remediation epic — docs/epics/epic-0-<slug>/EPIC_0.md with its milestone and tracking issue — that create-issues consumes unchanged. Use when review reports have piled up and the question is what work they become.
---

# Turn Review Reports into a Remediation Epic

A review never repairs what it reviews — that is what keeps its report trustworthy.
The cost is that findings pile up in `docs/REPORT_<n>.md` with nothing that turns them
into work, and a series of nine reports carrying a hundred findings is not something a
user can act on by hand. This skill is the converter: read the whole series, group the
findings by the repair that fixes them, let the user triage once, and emit a single
epic the rest of the pipeline already knows how to build.

The epic schema, the status lifecycle and the drift register are defined in
`../_shared/pipeline-interfaces.md`; the rules for anything written under `docs/` in
`../_shared/bundle-interfaces.md`; the report's own shape and severity scale in
`../_shared/review-interfaces.md`. Read all three before Step 1 — this skill writes an
epic against schemas it does not own, and reads reports written to a contract it does
not own either.

## What epic 0 means

The remediation epic is always **epic 0**, and the number is not decoration. Every other
epic number is a position in the planned build order. Zero means **before continuing** —
work that jumps the queue because the project cannot honestly proceed until it lands.

That holds in both directions the reports come from. Repairs to the plan land before the
epics they repair get implemented; fixes to shipped code land before the next epic builds
on it. Same lane, same meaning.

It is also **temporary**. Epic 0 is scaffolding that puts the project back on its rails,
not a permanent fixture of the epic bundle — so it is created here and **retired by
`close-epic`**, which is the skill actually running at the moment retirement becomes due.
This one converts findings into work; it does not own the lane's disposal.

## The mode is read, not asked

There is no flag. Each report's `## Scope` says what it reviewed, and that decides what a
fix *is*:

| Reports from | Findings are about | A fix edits |
|---|---|---|
| `review-epics`, `review-issues` | planning artifacts | `docs/epics/**`, sometimes `docs/planning/**` |
| `review-implementation` | shipped code | product code and its tests |

A series holding both yields **one** epic 0, plan repairs first and code fixes after,
wired with `depends_on` — repairing an issue changes the contract the code work will be
judged against, so doing it the other way round means fixing code twice.

## Scope boundary

This skill converts findings into work. It does not review, and it does not repair.

- It never edits an existing report. The series is the evidence of what the artifacts
  looked like when someone looked; a report amended after the fact stops being a record.
- It never applies a fix itself, however small. A one-line link correction applied here
  is an unreviewed edit that no issue tracks and no PR shows.
- It does not re-grade. Severities come from the reports; if a finding is wrong, that is
  a `won't-fix` in the triage, not a re-review.

## Step 1: Own the lane

Before reading anything, look for `docs/epics/epic-0-*/`.

**Nothing there** — the lane is free; continue to Step 2.

**An epic 0 with work still in flight** (any issue not `done`, or its milestone open) —
do not create a second one. New findings join the existing epic 0: extend its `## Scope`
and `## Acceptance criteria`, and let `create-issues` add the new issues to it. Two open
remediation lanes compete for the same "do this first" slot and neither wins.

**An epic 0 with every issue `done` and its milestone closed** — it should not still be
here. `close-epic` retires the lane, folder and all, in the run that closes it. Finding
one means `close-epic` never ran on this epic, so say that and hand off to it rather than
removing the folder yourself.

Two things make the hand-off worth the interruption instead of a quick `git rm -r` here.
`close-epic` writes the retirement notice to `docs/epics/log.md` that Step 2 reads to skip
already-converted reports — delete the folder without it and the next run re-triages
findings that were fixed months ago. And any drift promoted out of that epic still points
its `Evidence` into the folder's `drift/` records until `close-epic` repoints it at the
PRs; removing the folder first leaves the register asserting things it can no longer show.

Once the hand-off is done the lane is free, so continue to Step 2.

## Step 2: Collect the series

Read every `docs/REPORT_<n>.md`. For each, note from its `## Scope` which reviewer wrote
it, what it reviewed, and when — a report's age is what makes its findings suspect later.

Then read `docs/epics/log.md` for creation and retirement notices naming reports already
consumed, and skip those. A run that re-triages last month's reports asks the user to
decide the same hundred findings twice, and they will not do it a second time.

If the user names specific reports, use those. If the series is entirely consumed, say so
and stop rather than manufacturing an epic out of nothing.

## Step 3: Group by fix, not by finding

This is the step that makes the difference between this skill and doing it by hand.

Extract every finding, then group them by **the repair that resolves them**. The same
defect recurs across reports because the reviewers looked at nine artifacts built the same
way: one link-form mistake in nine `issues/index.md` files is one repair touching nine
files, not nine repairs. A group is one future issue, so it needs one owner, one
verification, and a diff that stays inside the size bands in
`../_shared/pipeline-interfaces.md`.

Extraction, the two report layouts, and the grouping heuristic — including what must
*not* be grouped — are in `references/finding-extraction.md`.

Findings whose resolution is a decision rather than an edit ("the epic says X, the issue
says Y") stay ungrouped. They go to the user as questions in Step 5, and only the answer
becomes a repair.

## Step 4: Kill the stale

A report is a snapshot. In a series, the early ones are the oldest thing in the room, and
an epic half-filled with work already done is how a user learns to skip the triage.

Verify each group against what is true **now**, not against what the report said:

- the cited `file:line` still says what the finding quotes
- no open or merged GitHub issue already covers it
- `docs/planning/DRIFT.md` has not already accepted it — accepted drift is not a finding
- a report already recorded a disposition for it (`review-implementation` writes them),
  in which case honour it rather than re-triaging: `accepted` and `won't-fix` drop out,
  `fix-now` with a live issue is already work

Recipes in `references/finding-extraction.md`. Drop what is settled, and say how many
dropped and why — a triage that silently shrinks looks like findings went missing.

## Step 5: Triage in one batch

Present every surviving group at once — severity, the reports it came from, how many
findings it absorbs, the repair, and a recommended disposition. Then wait.

- **fix** — becomes work in epic 0.
- **drift** — the artifact is right and the *standard* is wrong. That is a
  `docs/planning/DRIFT.md` entry in the format `../_shared/pipeline-interfaces.md`
  defines, citing the report as evidence; the standard gets corrected rather than the
  code.
- **won't-fix** — recorded in the epic with its reason. Written down even so, because the
  next reviewer finds it again otherwise and the user pays for the same decision twice.

Dispositions are the user's call — each one either creates work or rewrites a standard.
Ask the ungrouped questions from Step 3 in the same batch; a batched triage the user runs
through once is the whole point.

## Step 6: Shape epic 0 and confirm

Draft the epic from the accepted groups:

- **Slug** from what the round is actually about (`epic-0-plan-remediation`,
  `epic-0-auth-hardening`) — lowercase kebab-case, ASCII, ~40 chars.
- **Goal** — what proceeding requires, not "fix the review findings".
- **Scope** — the accepted groups, plan repairs before code fixes.
- **Acceptance criteria** — checkable, one per group where the group warrants it. A group
  whose criterion cannot be checked was a theme, not a repair; fold it back.
- **Notes** — the `won't-fix` decisions with their reasons, and the reports consumed.

Then show the user the whole breakdown before anything is written: the reports read, the
findings dropped as stale, the groups accepted, the destination path, and what happens
next — local files, then one GitHub milestone and one tracking issue. Wait for explicit
confirmation. Mis-grouped repairs are cheap to fix before the milestone exists and
tedious after.

## Step 7: Create, write back, hand off

Write `docs/epics/epic-0-<slug>/EPIC_0.md` to the epic template in
`../_shared/pipeline-interfaces.md`: `epic: 0`, `tags: [epic, remediation]`, and `source`
listing the reports consumed. Update `docs/epics/index.md`, and append a creation entry to
`docs/epics/log.md` naming those reports — the same record Step 2 reads next time.

Create the milestone and the tracking issue the way `split-epics` does (`Epic 0: <title>`,
the repo's own epic label, body linking back to `EPIC_0.md`), then write back
`status: open`, `gh_issue`, `milestone`, `resource` and a refreshed `timestamp`.

Write any `drift` dispositions into `docs/planning/DRIFT.md` and correct the SPECS or
CONVENTIONS line each one contradicts — an accepted drift that leaves the standard
standing means the next review reports it again.

Commit and push per `../_shared/bundle-interfaces.md`; the tracking issue links to
`EPIC_0.md` and that link 404s until it lands.

Report: findings read, dropped, and accepted; the epic and its issue link; the drift
entries written; and that `create-issues` can now cut epic 0 into PR-sized issues. Say
plainly what was left undecided — a group the user deferred is still a finding nobody
owns.
