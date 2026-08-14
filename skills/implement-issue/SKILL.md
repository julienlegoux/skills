---
name: implement-issue
description: Implement a single issue from docs/epics/ (produced by create-issues) as one focused, test-first PR — reconcile merged PRs, branch, strict red-green TDD against the acceptance criteria, open the PR, keep the bundle and GitHub issue in sync. Use whenever the user wants one issue executed ("implement issue 3 of epic 2", "do the next unblocked issue", "keep going on epic 2").
---

# Implement an Issue

`create-issues` sized every issue to become one focused PR. This skill is the execution
half of that contract: take one issue from `status: open` to an open pull request, with
the code, tests, and bookkeeping that lets the next run (and the epic's GitHub progress
bar) know where things stand.

## Status lifecycle

The issue file format, the full status lifecycle (`draft → open → in-progress →
pr-open → done`, who writes each transition, what every status write must also
update), and the GitHub facts about non-default integration branches are defined in
`../_shared/pipeline-interfaces.md` — read it first, alongside
`../_shared/bundle-interfaces.md` for the rules covering anything written under
`docs/` (English content, link forms, committing what you write) and
`../_shared/feedback-interfaces.md` for the closing reflex on what this run teaches
about *this skill*, applied at Step 9. This skill owns the
`open → in-progress → pr-open` transitions and the `pr-open → done` reconcile of
*earlier* runs' issues (merging happens outside this skill).

## Step 1: Reconcile previous PRs

Do this first, before even resolving which issue to work on — the whole point of
`depends_on` is that yesterday's merge is what unblocks today's issue, so stale
statuses give wrong answers about what's workable.

Sweep `docs/epics/*/issues/*.md` for `status: pr-open` and check each recorded PR:

```bash
gh pr view <gh_pr> --json state,mergedAt -q .state
```

- `MERGED` → set `status: done`, refresh `timestamp`, update the epic's
  `issues/index.md` bullet. If `docs/epics/log.md` exists, append a completion entry
  (same date-grouped format `split-epics` uses); never create `log.md` if absent.
  Then close the GitHub issue if it's still open
  (`gh issue close <gh_issue> --comment "Completed by PR #<gh_pr>"`). This is the
  **normal path**, not a fallback: `Closes #N` only auto-closes on merges into the
  repo's *default* branch, so any PR that merged into an integration branch (e.g.
  `develop`) left its issue open by design (see
  `../_shared/pipeline-interfaces.md`). Also remove any status label this flow
  added — a closed issue isn't `pr-open`.
- `CLOSED` without merge → don't guess what happened. Report it to the user and leave
  the status as-is; a human closed that PR for a reason the frontmatter can't know.
- `OPEN` → nothing to do; mention it in the final report so the user remembers it's
  awaiting review.

Commit reconcile updates directly on the branch the epic's statuses live on — the
**integration branch** when one is in play (the branch the merged PRs targeted),
otherwise the default branch. They describe work that *already merged there*;
putting them on the new feature branch would hold finished facts hostage to an
unmerged PR, and putting them on the default branch when the epic lives on
`develop` updates a copy of the bundle nobody downstream reads. If pushing to that
branch is blocked by protection rules, say so and leave the commit local rather
than failing.

If `gh` is unavailable or unauthenticated, skip reconciliation with a clear note —
don't let bookkeeping block implementation.

## Step 2: Resolve the target issue

- **User names it** ("issue 3 of epic 2", a slug, a GitHub `#number`, a path) — use
  that. If they name an epic but not an issue, or say "the next one", auto-pick: the
  lowest-numbered issue with `status: open` whose `depends_on` entries are all `done`
  (this is why reconcile runs first). If several epics are in play and the user didn't
  scope it, prefer the lowest-numbered epic with unblocked work.
- **Nothing is unblocked** — don't grab a blocked issue silently. Show what's open,
  what each is waiting on, and where those blockers stand (e.g. "02 waits on 01,
  whose PR #14 is open awaiting review").
- **The named issue has unmet dependencies** — stop and show which. The user can
  explicitly override ("do it anyway"); dependency order is a default, not a cage.
- **Already `in-progress`** — a previous run started it. Look for its branch and offer
  to resume there rather than starting over.
- **Already `pr-open` or `done`** — point at the existing PR and refuse to duplicate
  the work unless the user explicitly asks for a redo.

## Step 3: Read the full spec

The issue's `.md` file is canonical, but it was written before any code existed, and
humans comment on GitHub, not in the repo:

1. Read the issue file in full — Summary, Scope, **Out of scope** (binding, see
   Step 5), Acceptance criteria, Relevant files, Dependencies.
2. Fetch the live issue: `gh issue view <gh_issue> --comments`. Fold in anything new —
   clarifications, scope changes, "actually use library X" comments. If a comment
   *contradicts* the file on something material, surface the conflict and ask which
   wins instead of silently picking one.
3. Read the epic's `EPIC_<n>.md` for the surrounding goal, and skim the `depends_on`
   issues' files to know what the codebase should already contain by now.

## Step 4: Learn how this repo builds and ships

The issue file recorded conventions as of creation time; verify against the repo now:

- The epic's `## Context` links — typically `docs/planning/CONVENTIONS.md` (the
  repo's decided standards) and `docs/planning/SPECS.md` (the decided stack) — these
  are the project's authoritative standards when they exist.
- `docs/planning/DRIFT.md` if it exists — where earlier work already proved one of
  those standards unworkable, with the verified blocker and the disposition
  (`../_shared/pipeline-interfaces.md`). Read it *with* the standards, not instead of
  them: a decided standard plus its live drift is what the code actually looks like,
  and it is the difference between following a convention and rediscovering why the
  last three issues couldn't.
- `docs/planning/PREREQUISITES.md` if it exists — what the plan depends on, and which
  entries were verified rather than assumed (`check-prerequisites` writes it). When this
  issue needs something the register lists as unsatisfied, say so and stop rather than
  improvising around it: the register already names who has to clear it.
- `CLAUDE.md` / `AGENTS.md` / `CONTRIBUTING.md` — test requirements, commit style,
  anything that belongs in the Definition of Done.
- How tests actually run here (test runner, lint, typecheck, build) — find the real
  commands, don't assume.
- Branch naming: check existing branches / merged PR head names for a convention. If
  none is visible, use `issue-<gh_issue>-<slug>` (the GitHub number is unique across
  epics; the local `<nn>` isn't).
- `.github/PULL_REQUEST_TEMPLATE.md` — if it exists, the PR body must follow it.

## Step 5: Branch and mark in-progress

From the up-to-date default branch (or the integration branch, when a supervisor
or the user named one — fetch first, branch from `origin/<branch>`), create the
feature branch. First commit on it:
the issue file's frontmatter flipped to `status: in-progress` (plus `timestamp` and
the `issues/index.md` bullet). The status change travels with the PR — anyone reading
the branch sees a self-consistent bundle, and `main` keeps saying `open` until the
work actually lands, which is true.

Mirror the same transition on GitHub, where teammates actually watch progress:

```bash
gh issue comment <gh_issue> --body "Started work on branch \`<branch-name>\`."
```

Then mark the issue itself as in progress — a comment shows in the timeline, but
only a label is visible from the issue list. GitHub issues have no native status
field, so labels carry it: if Step 4 showed the repo already has status labels
(e.g. `in progress`, `status: wip`), use those; otherwise create a minimal pair
once (`gh label create "status: in-progress"` and `"status: pr-open"`) and apply
the in-progress one (`gh issue edit <gh_issue> --add-label "status: in-progress"`).
Skip silently if `gh` is unavailable — same rule as reconciliation, bookkeeping
never blocks implementation.

Labels cover the issue list, but a GitHub Projects board is a third, separate
surface: its Status field ignores labels entirely, and the only built-in
automation is closed→Done — nothing ever moves an item to "In Progress", so a
board-tracked repo shows stale status for the whole life of the branch unless
this flow sets it. Check `gh issue view <gh_issue> --json projectItems`; if the
issue sits on a project whose Status has an in-progress-like option, set it:

```bash
gh project item-list <number> --owner <owner> --format json   # item id (match content.url)
gh project field-list <number> --owner <owner> --format json  # Status field id + option ids
gh project item-edit --project-id <id> --id <item-id> --field-id <field-id> \
  --single-select-option-id <option-id>
```

Editing projects needs the `project` auth scope; if `gh` refuses on scopes,
mention `gh auth refresh -s project` in the report and move on — bookkeeping
never blocks implementation.

## Step 6: Implement, test-first

Work strictly test-driven, one acceptance criterion at a time:

1. **Red** — write the test that expresses the criterion, run it, and *watch it fail*.
   A test you've never seen fail proves nothing: it might pass vacuously, test the
   wrong thing, or not run at all. The observed failure is the evidence that the test
   is actually connected to the behavior it claims to check.
2. **Green** — write the minimum implementation that makes it pass, and run it again.
3. **Refactor** — clean up with the test as your safety net, then move to the next
   criterion.

No implementation code before its failing test exists — the temptation to "just write
it and backfill tests" is exactly how acceptance criteria end up demonstrably untested
in the PR. If a criterion genuinely can't be expressed as an automated test (e.g. a
docs-only change), say so explicitly in the PR body rather than skipping quietly.

If the repo has no test infrastructure at all, set up the minimal conventional runner
for its stack (nothing fancy — the smallest thing that lets tests run in CI and
locally) and flag that addition prominently in the PR; it's a scope addition the
reviewer should consciously accept.

Two boundaries the issue already drew:

- **Acceptance criteria are the definition of done.** Treat them as a literal
  checklist; each one ends up demonstrably true, with the test written in step Red
  proving it.
- **Out of scope means out.** Adjacent problems you notice (refactors, bugs in
  neighboring code, "while I'm here" improvements) get *noted in the final report* as
  candidate follow-up issues — they don't get done. Scope creep here is precisely what
  breaks the one-issue-one-reviewable-PR sizing that the whole pipeline exists for.

One discovery that must NOT stay informal: implementation sometimes proves a decided
standard wrong (a pinned version the ecosystem can't satisfy, a mandated library that
breaks the build). When you depart from SPECS/CONVENTIONS or the issue spec to make
acceptance criteria pass, that is **drift**, and it gets a **drift record** — path,
fields and role in `../_shared/pipeline-interfaces.md`. State what was decided, what
blocked it (verified versions and error text, not vibes), the alternatives you tried,
and the concrete trigger for revisiting; keep that folder's `index.md` listing it, and
commit it on the issue branch so it lands with the PR.

That record is the only durable trace: `close-epic` promotes it into
`docs/planning/DRIFT.md`, which every later run reads. Drift that lives only
in a PR body or in your final report is invisible to the next issue that trips over the
same wall — so also name it in the report (Step 9), because a supervisor that never
hears about it cannot get it promoted.

Finish by running the *full* test suite and lint — not just your new tests — and fix
what breaks, including pre-existing tests your change disturbed.

## Step 7: Size check

Compare against the default branch: `git diff --stat <default-branch>...HEAD`. The
issue targeted ~500 changed lines (its `size` field predicted S/M/L). If the real diff
blew past ~1000: **open the PR anyway, but flag it loudly** — a prominent warning at
the top of the PR body (actual line count vs. the issue's predicted size, and where
the growth came from), and the same in your report to the user. Include a sentence on
how the issue *could* have been split — that feeds back into sizing the next epic's
issues better. Don't silently ship an oversize PR as if it were normal.

## Step 8: Open the PR and write back

1. Commit and push the branch. Write the PR body to a temp file (safer than `--body`
   for multi-paragraph text) and create the PR:

   ```bash
   gh pr create --title "<issue title>" --body-file <tmpfile> \
     --milestone "<the issue's milestone title>"
   ```

   The body must contain `Closes #<gh_issue>` (it links the PR to the issue in
   GitHub's UI — but note it only auto-closes on default-branch merges; on an
   integration branch the reconcile step closes the issue, see
   `../_shared/pipeline-interfaces.md`), a summary of what changed and why, the acceptance
   criteria as a checked checklist, how it was tested (real commands, real output
   summary), a link to the issue's `.md` file in the bundle, and the oversize warning
   from Step 7 if applicable — all shaped to the repo's PR template when one exists.

2. Capture the new PR number, then update the issue file once more: `status: pr-open`,
   `gh_pr: <number>`, refreshed `timestamp`; update `issues/index.md`; append a
   `log.md` entry if that file exists. Commit and push — the open PR picks up the
   bookkeeping commit automatically.

3. Update the GitHub issue to match: comment with the PR link
   (`gh issue comment <gh_issue> --body "PR opened: <pr-url> — will close this issue
   on merge."`) and swap the status label (`gh issue edit <gh_issue>
   --remove-label "status: in-progress" --add-label "status: pr-open"` — the
   labels Step 5 ensured exist), and if Step 5 found a Projects board, move its
   Status likewise (an in-review/pr-open-like option if one exists, else leave it
   at in progress — Done arrives via the board's own closed→Done automation at
   merge). The `Closes #N` keyword links the PR in GitHub's UI, but the
   explicit comment makes the state change visible in the issue's timeline and in
   notifications — the local `.md` and the GitHub issue should tell the same story at
   every transition.

**If pushing or `gh pr create` fails** (no remote, no auth, protected setup): stop
gracefully. Leave the branch intact and the status at `in-progress` (it's the truth —
no PR exists), and tell the user exactly what's ready locally and which command failed,
so they can push themselves and re-run the skill to finish the write-back.

## Step 9: Report

If a permission-classifier outage or repeated transient failures block one final
command (a push, the `gh pr create`, a label edit), don't retry in a loop and
don't report the run as failed: state the **single remaining command** verbatim,
note that everything else is done, and end the turn. A supervisor (or the user)
treats such a report as retryable — the work is intact and one approved retry
finishes it.

End with a summary the user can act on:

- **Reconciled**: which issues moved to `done` (with PR links); any closed-unmerged
  PRs or still-open PRs worth chasing.
- **Implemented**: the issue, the branch, the PR link, final diff size vs. predicted
  size, test results (actual numbers, not "tests pass"), and any drift records
  written.
- **Follow-ups**: out-of-scope discoveries worth turning into new issues.
- **Next up**: which issue becomes unblocked once this PR merges — the natural next
  invocation of this skill.

Then close the run per `../_shared/feedback-interfaces.md` — silently, unless this run
turned up something about this skill that clears both its filters; delegated by a
supervisor, that goes in this report rather than to a user who isn't there. Drift is
not it: that is the *project's* standard proving wrong, and it already has a record and
a register.
