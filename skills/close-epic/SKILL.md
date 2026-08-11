---
name: close-epic
description: Close out an epic after its implementation run stops — verify the epic's real state against GitHub and git, promote the drift its implementers recorded into docs/planning/DRIFT.md, close the milestone, and clean up the run's worktrees and merged branches. Use when an epic's implementation has finished or stopped and the repo must be left in a state the next epic can start from.
---

# Close an Epic

`implement-epic` stops when its loop has nothing left to do — but a stopped run is not
a closed epic. The worktrees it spawned are still on disk, the merged branches are
still on the remote, the milestone is still open, and everything its implementers
learned the hard way is sitting in a chat report that dies with the session. This
skill is that seam: leave the repo in a state the next run can start from, and move
this run's discoveries somewhere the next run is guaranteed to read.

The issue schema, the status lifecycle, and the **drift register** (what drift is, its
two artifacts, the register's format) are defined in
`../_shared/pipeline-interfaces.md`; the rules for anything written under `docs/` in
`../_shared/bundle-interfaces.md`. Read both before Step 1. What to do with anything
this run teaches about *this skill* is defined once in
`../_shared/feedback-interfaces.md` — the closing reflex, read at Step 5.

## Scope boundary

This skill verifies **state**: statuses, merges, closed issues, the milestone,
branches, worktrees. It does **not** review the implemented code — not its quality,
not its design, not whether the acceptance criteria were honestly met.

`review-implementation` owns that, and runs after this skill — it needs the register
this one promotes, so that accepted drift isn't re-reported as a finding. When a user
asks for the code to be reviewed, hand off to it rather than doing a shallow version
here under cover of "closing": a closing skill that half-reviews code is how an epic
gets a clean bill of health it never earned.

Within state, this skill writes only bookkeeping and the register. It never touches
product code: a gap it finds becomes a reported fact or a follow-up issue, never a
patch.

## Step 1: Establish the real state

Three sources disagree after a long run, and each is authoritative about something
different. Read all three before concluding anything:

| Source | Authoritative for | How |
|---|---|---|
| the bundle | what the last run *recorded* | frontmatter of `docs/epics/epic-<n>-<slug>/issues/*.md` — fields only, not bodies |
| GitHub | what actually merged and closed | the recorded `gh_pr` per issue, the milestone's open issues, the milestone's own state |
| git | what is still lying around | `git worktree list`, local and remote branches, the integration branch's log |

Recipes in `references/state-and-cleanup.md`.

Resolve the **integration branch** the way `implement-epic` did — the one the user
names, else `develop`, else the repo default — but treat the merged PRs' `baseRefName`
as the ground truth, since that is where the epic's statuses actually live and where
reconcile commits belong.

Then classify every issue: `done` and confirmed merged; recorded `pr-open` but in fact
merged (bookkeeping lag, Step 2 fixes it); PR still open awaiting review; PR closed
unmerged; never started. **Never infer a merge from a status field** — this skill
exists precisely because the previous run's bookkeeping may have stopped mid-flight.

## Step 2: Reconcile the bookkeeping

Apply the lifecycle in `../_shared/pipeline-interfaces.md` to every divergence Step 1
found: a merged PR's issue becomes `status: done` with a refreshed `timestamp`, its
`issues/index.md` bullet updated, a `log.md` entry appended if that file exists, and
its GitHub issue closed with any status label removed.

A PR that is **closed unmerged**, or an issue that was never started, is not yours to
resolve — report it in Step 5 and leave the status telling the truth.

Then close the milestone, once and only once every issue on it is closed. Nothing else
in the pipeline closes it, so an otherwise finished epic keeps showing as open work on
the repo's milestone list. If issues remain open, leave the milestone open and name
them: a closed milestone with open issues is a worse lie than an open one.

**Close the epic itself in the same step**, under the same condition: set
`status: done` on `EPIC_<n>.md` with a refreshed `timestamp`, and update the epic's
bullet in the **epics bundle root** `index.md`. Nothing else in the pipeline writes
either, so an epic whose milestone is closed and whose every issue is `done` otherwise
keeps reading `open` in the one index a later reader scans to see where the project
stands — a mismatch that surfaces only when someone adds the next epic by hand and
notices the neighbouring bullets are wrong.

**Epic 0 is the exception**: it is *retired* rather than closed (Step 4), so it never
takes `status: done`. Leave its frontmatter alone here.

## Step 3: Promote the drift

This is the step the rest of the pipeline depends on. Implementers write one **drift
record** per drifting issue (`docs/epics/epic-<n>-<slug>/drift/<nn>-<slug>.md`) during
the run, concurrently, each blind to the others. Nobody downstream sweeps those folders,
so what they learned dies there. Promotion turns them into the single register every
later run reads — see `../_shared/pipeline-interfaces.md` for what drift is, the
register's format, and who reads it.

1. Collect every drift record in this epic, plus any drift the run's report surfaced
   that never got a record (an implementer that died before committing one, drift the
   supervisor accepted in chat).
2. Fold duplicates: three issues blocked by the same unusable pinned version are **one**
   register entry citing three drift records, not three entries. A register that repeats
   itself stops being read.
3. Draft each entry with a **proposed disposition** — `accepted`, `fix-now`, or
   `deferred` with a concrete revisit trigger. Procedure and the judgment calls are in
   `references/promotion.md`.
4. **The user triages the dispositions.** Present all entries in one batch with your
   recommendation each, and wait. A disposition either rewrites the project's standards
   or creates work — that is the user's call, not yours. Only after the triage: write
   `docs/planning/DRIFT.md`, update the planning bundle's root `index.md`, append to its
   `log.md`.
5. `fix-now` entries become real follow-up issues (or an explicit hand-off to
   `define-change` when the fix is bigger than an issue). A `fix-now` with no issue
   behind it is just a `deferred` that lies about itself.

Never delete or rewrite the drift records. They hold the verified errors and
versions that make the register trustworthy; the register links to them.

## Step 4: Clean the environment

Cleanup is the reason the next epic can start at all — a leftover worktree holds a
branch checked out, and that is what makes branch deletion fail later, with a confusing
error, in the middle of someone else's run.

Order matters: **worktrees, then local branches, then merged remote branches.**
Commands in `references/state-and-cleanup.md`.

Three hard rules, because deleting a remote branch is not reversible from here:

- **Only branches whose PR is MERGED.** Never a branch with an open PR, no PR, or a
  closed-unmerged PR.
- **Never a worktree with uncommitted changes or unpushed commits** — inspect before
  removing. Report it instead; it may be the only copy of an implementer's work.
- **One grouped confirmation.** List exactly what will be removed — every worktree
  path, every branch, local and remote — and get a single explicit go-ahead before
  removing anything. Not a per-item interrogation, and not silent deletion either.

### Retiring epic 0

If this epic is `epic: 0`, cleanup includes the lane itself. Epic 0 is the remediation
lane `triage-reports` opens, and it is a slot rather than an identity — the next triage
cycle produces its own repairs and needs the number back
(`../_shared/pipeline-interfaces.md`). Retirement lands here rather than with the skill
that created it for one reason: `triage-reports` runs when reports pile up, not when an
epic finishes implementing, so it is not loaded at the moment retirement becomes due.
This skill is, and it has already established the exact precondition — every issue
`done`, milestone closed.

Retire it **after** Step 3, which reads the drift records the folder holds, and fold it
into the same grouped confirmation as the worktrees and branches:

1. **Repoint what links into the folder, before removing it.** Both logs are
   append-only, so a link that dies there stays dead. The usual holders are
   `docs/epics/log.md`, `docs/planning/log.md`, and the `Evidence` field of any drift
   entry Step 3 just promoted — that one points straight into `epic-0-<slug>/drift/`.
   Repoint each at what survives on GitHub: the milestone, the tracking issue, the
   issue, or the PR. A promoted drift entry cites `PR #<pr>` instead, which costs
   nothing — its `Because` field already carries the verified blocker inline.
2. **Show what is about to go** — issue count, milestone number, the reports it
   consumed — in the grouped confirmation, and get the go-ahead with the rest.
3. `git rm -r docs/epics/epic-0-<slug>/`, and drop its bullet from
   `docs/epics/index.md`.
4. **Append the retirement notice to `docs/epics/log.md`:**

   ```markdown
   * **Retirement**: Epic 0 (<title>) retired - <n> issues, milestone <m> closed.
     Consumed reports <list>. Fixed: <one line on what it produced>.
   ```

   The folder goes; the memory does not. `triage-reports` reads this notice to know
   which reports have already been converted, so retiring without it is what makes the
   next run ask the user to decide the same hundred findings twice.

Every other epic stays on disk with `status: done`. Only zero is retired.

Finish by confirming the integration branch is checked out, clean, and pushed. That,
not the merge count, is what "the next epic can start" means.

## Step 5: Report

Two shapes, depending on how the run ended.

**The epic is closed** — every issue `done`, the epic and its milestone closed,
environment clean:

- Merged issues with PR links, in merge order.
- Register entries written, with their triaged dispositions and any follow-up issues
  created.
- What was cleaned: worktrees removed, branches deleted.
- Anything left deliberately (an open PR awaiting human review, a human-gate).
- The next epic in `docs/epics/`, and that it is now unblocked.
- That `review-implementation` can now audit what this epic shipped — the register is
  written, so it is the first moment that review can run without re-litigating drift the
  user just triaged. Offer it; don't run it unasked.

**The epic is incomplete** — a stopped or blocked run. Same content, plus the part
that matters more: a **resume snapshot**. What each unfinished issue's real state is,
what blocks it, and the literal next invocation to continue. Cleanup and promotion
still happen — an interrupted run is exactly when its discoveries are most likely to
be lost, and a half-cleaned repo is what makes the resume fail.

Commit everything you wrote per `../_shared/bundle-interfaces.md` before reporting.

Then close the run per `../_shared/feedback-interfaces.md` — silently, unless this run
turned up something about this skill that clears both its filters.
