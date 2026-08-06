---
name: implement-epic
description: Supervise the implementation of all remaining issues in an epic by delegating each one to an implement-issue subagent, watching CI, and merging green PRs into the integration branch until every issue is done. Use whenever the user wants an entire epic from docs/epics/ (or its remaining issues) implemented end to end.
---

# Implement an Epic

`create-issues` sized every issue in the epic to be one focused PR, and
`implement-issue` turns one issue into one PR. This skill is the layer above: run
that loop for every remaining issue in an epic — delegate, watch CI, merge, repeat —
until the epic's board shows all `done`.

Shared formats, the issue status lifecycle, and the GitHub facts this flow leans on
live in `../_shared/pipeline-interfaces.md` — read it before Step 1, with
`../_shared/bundle-interfaces.md` for the bundle-wide rules (English content, link
forms, committing what you write). The two facts
that bite hardest: on a non-default integration branch **`Closes #N` never
auto-closes** the issue, and **a CONFLICTING PR gets zero CI runs**.

## You are a supervisor — protect your context

This loop can span many issues, many CI waits, and hours of wall-clock time. Your
context is the scarcest resource in the room: every source file you read, every
diff you inspect, every log you study rides along in every later decision, and a
bloated supervisor starts making sloppy calls exactly when the last issues land.
So the division of labor is absolute:

- **Never implement anything yourself.** No code edits, no running tests, no
  reading source files, no reviewing diffs. If a task needs doing — implementing,
  fixing CI, resolving a merge conflict, even bookkeeping — spawn a subagent.
- **What you may hold:** the epic's issue list (frontmatter fields only), subagent
  final reports, PR numbers and check states, and short `gh` JSON answers to
  questions you asked.
- **When a subagent's report is long,** keep its conclusions (PR number, test
  results, deviations, follow-ups) and let the rest go — don't re-derive its work.

The temptation to "just quickly fix" a one-line CI failure yourself is exactly how
supervisors drown. A subagent fixes it just as fast, and you stay clear-headed.
This rule holds even when subagents are failing for environmental reasons (outages,
permission stalls) — idle waiting is cheaper than context bloat.

## Step 1: Map the epic

1. Locate the epic folder (`docs/epics/epic-<n>-<slug>/`). Read `issues/index.md`
   and each issue's **frontmatter only** (the fields in
   `../_shared/pipeline-interfaces.md`) — the bodies are for the implementers.
   Then read `docs/planning/DEVIATIONS.md` if it exists — the register of standards
   earlier epics proved unworkable (`../_shared/pipeline-interfaces.md`). It is cheap,
   it is the one place that carries what previous runs learned the hard way, and any
   entry touching this epic goes into the affected implementers' prompts. Without it
   each implementer rediscovers the same wall on its own CI round.
2. Determine the **integration branch**: the one the user named; else `develop` if
   it exists; else the repo's default branch. All PRs in this run target it, and
   every implementer must be told about it explicitly — `implement-issue` defaults
   to the default branch otherwise.
3. **Ask the user to pre-approve merging in your opening message — always.**
   `gh auth status` must work (the flow is built on `gh`), but a clean auth check
   proves nothing about permission gating: restrictive permission modes can deny
   `gh pr merge` even when every other `gh` call works, and there is no preflight
   command that detects it. Discovering the gate after several PRs are green
   strands the run, and you cannot widen your own permissions. So the opening
   message always asks the user to pre-approve merging (e.g. `/permissions` allow
   `Bash(gh pr merge:*)`). Assume direct `git push` to the integration branch is
   blocked too, and tell implementers so — otherwise each one rediscovers it and
   improvises a workaround.
4. **Identify the required CI check(s)** for the integration branch now (recipe in
   `references/ci-and-merging.md`), so green means the right jobs passed. Failing
   third-party checks that aren't required (preview deploys, review bots) are
   notes to surface to the user — never merge blockers, never fix rounds.
5. **Scan for human-gates.** Read the issues' scope/acceptance-criteria lines in
   `index.md` for actions no agent can perform — DNS changes, third-party
   dashboards, real-device testing, e-mail inboxes. List them in the opening
   message and track them as explicit user-gates on the board; surfacing them
   mid-run stalls the loop at its least convenient moment.
6. Build the board: which issues are `done`, `pr-open` (PR to check on),
   `in-progress` (a previous run started it — resume it, don't restart), `open`
   and unblocked, or blocked and on what.

## Step 2: The loop

The dependency graph, not a queue, drives scheduling: **run every unblocked issue
concurrently; serialize only the merges.** Implementation is the slow part and
independent issues don't need to wait on each other — but PRs land into the
integration branch one at a time, in a deliberate order.

Repeat until no issue in the epic remains short of `done`:

1. **Settle inherited state first.** Any `pr-open` issue from this epic: check its
   PR — merged → fine (statuses self-heal, see Bookkeeping); open → adopt it into
   the CI-watch/merge flow below; closed unmerged → surface to the user, don't
   guess.
2. **Spawn the whole frontier.** Every `open` issue whose `depends_on` are all
   `done` (or already merged this run) gets an implementer subagent now — choose
   each one's model and effort (next section), then launch them **in one batch**
   so they run concurrently, each with `isolation: "worktree"` (concurrent agents
   sharing a checkout clobber each other's branches and uncommitted work). The
   prompt template — including the worktree operating manual implementers need to
   survive their isolation — is in `references/implementer-prompt.md`; use it.
   Cap the frontier at ~4 in-flight implementers; more mostly buys merge-conflict
   churn on a shared integration branch.
3. **As each PR appears**, record its number and the report's essentials, and
   start watching its checks in the background (see CI and merging).
4. **Merge one at a time.** When one or more PRs are green, merge the
   lowest-numbered issue's PR first (dependency order is numbered order within an
   epic). Right after each merge, close that issue's GitHub issue — `Closes #N`
   never fires on a non-default base. After each merge, every still-open PR is now
   behind the integration branch — any that CI flags as conflicting gets a sync
   round; the rest just merge when their turn comes.
5. **Each merge may unblock new issues** — go back to step 2 and spawn them
   without waiting for the rest of the current wave.

One caveat worth judgment: two independent issues that obviously stomp the same
files (the index said so, or the epic's scope makes it plain) are better run
back-to-back than concurrently — the second one's rework costs more than the
overlap saves. Dependency-unrelated ≠ file-disjoint; use the scope lines in
`index.md` to spot this.

## Choosing model and effort per issue

This is the supervisor's real judgment call, and it's why the issue frontmatter
carries `size`. Match the horsepower to the work — a frontier model on a
rename-and-wire-up issue burns money for nothing, and a small model on a
migration-with-concurrency issue burns a CI round instead:

| Issue profile | Model | Effort steer in the prompt |
|---|---|---|
| S and mechanical — docs, config, boilerplate, CRUD copying an existing pattern, renames | `haiku` | "This is a small, well-specified task. Implement it directly without over-engineering; the acceptance criteria are the whole job." |
| M, or S with real logic — a typical feature slice with tests | `sonnet` | Normal prompt, no special steer. |
| L, or any size touching architecture, data model/migrations, auth/security, concurrency, public API shape, or cross-cutting refactors | `opus` (or the session's model if stronger) | "Think hard about design before writing tests; this issue has structural consequences." |

Judge from the **title, size, and one-line scope in `index.md`** — not the full
body. Two overrides:

- **When unsure, go one tier up.** A red CI round costs more than the model
  savings, in both tokens and wall-clock.
- **Escalate after failure.** If an issue's CI is still red after two fix rounds,
  or an implementer reports it couldn't finish, retry with the next tier up and
  higher effort, as a fresh agent with the failure summary in its prompt.

Mechanism: set the Agent tool's `model` parameter. If the harness also exposes an
effort/thinking parameter, set it to match the tier; otherwise the effort steer
lives in the prompt as above.

## Mid-run permission denials

When a command you or a subagent needs gets denied mid-run, there are exactly two
moves you never make: **never edit permission settings yourself** (widening your
own permissions is both blocked and not yours to decide), and **never hand the
user a command to run themselves** (it fractures the run's state across two
actors). The protocol: state plainly what's blocked and what it's blocking, ask
for the go-ahead, then retry the **identical** command — in auto modes a denial
clears on explicit user approval, so the retry succeeds without any settings
change.

## CI and merging

Command recipes — watching checks, the false-green verification, zero-CI-runs
diagnosis, failure-headline extraction — are in `references/ci-and-merging.md`.
The policy:

**Green means verified green.** A passing `gh pr checks` exit code is not proof:
confirm the required job ran by name and that a workflow run exists for the
current head. Zero runs → diagnose with `mergeable` FIRST — a conflicting PR gets
no CI, and no empty commit fixes that.

**Merge with a merge commit, always** — after verifying the PR's base is the
integration branch:

```bash
gh pr view <pr> --json baseRefName -q .baseRefName   # must be the integration branch
gh pr merge <pr> --merge --delete-branch
```

Never `--squash` or `--rebase` in this flow: the merge commit preserves each
issue's own commit history (including its red-green TDD trail) and keeps the
integration branch's first-parent line reading as one merge per issue. If the
repo's settings forbid merge commits, stop and tell the user — don't silently
squash to get past it.

**Red → fix round.** Pull only the failure headline, then message the **same
implementer agent** (its context already holds the whole implementation) with the
fix-round message from `references/implementer-prompt.md`. Two failed fix rounds →
escalate per the model table. Still red after escalation → stop and report; don't
thrash CI all afternoon.

**Merge conflict** (integration branch moved since the PR branched): send the
implementer the sync-round message — merge the integration branch into the feature
branch (merge, not rebase, consistent with the merge-commit policy), union
resolution on bookkeeping files, push.

**An implementer that dies mid-run** has not necessarily lost its work. Check
whether its PR and pushed commits already exist before assuming anything. For a
transient death (API 500/529, context exhaustion), prefer resuming it by message —
its context is intact — over spawning a replacement that has to rediscover
everything. For a death by **session or usage limit**, the limit applies to
replacements too: verify what was pushed, snapshot the board in a short report,
and stop cleanly until the limit resets — don't spawn fresh agents into the same
wall.

## Bookkeeping

You never edit bundle files yourself. `implement-issue`'s own reconcile step flips
merged PRs' issues to `done` at the start of the *next* run — so intermediate
statuses self-heal as the loop turns. Two scoping rules keep that sane under
concurrency:

- **Implementers settle only their own `depends_on` chain** (their prompt says so)
  — epic-wide reconciliation while siblings run would have every agent rewriting
  every line.
- **After the final merge there is no next implementer.** Close the gap with the
  final-reconcile agent (prompt in `references/implementer-prompt.md`) — it
  carries the same integration-branch constraints as implementers, because a
  reconcile PR merged into the wrong branch is still a wrong-branch merge.

**Concurrency makes bookkeeping the main source of merge conflicts — a cost to
manage, not to avoid.** `implement-issue` updates `issues/index.md` and the epic
log on every status write, because an OKF index that disagrees with its own docs
is broken and a stale index is worse than a conflicted one. So do not tell
implementers to skip it. The consequence is structural: each merge leaves the
other open PRs conflicting on index lines unrelated to their work. Keep that
cheap:

- **Always state the resolution rule** in the sync request: it is a **union** —
  every issue keeps its own line, merged issues read `done`, nobody clobbers a
  sibling's status. Left to guess, implementers resolve by overwriting and
  silently revert each other's bookkeeping.
- **Merge promptly once green.** Conflict cost scales with how long PRs sit open
  alongside each other, not with the epic's size.
- **On a bookkeeping-heavy epic** — many small issues all touching one index — a
  narrower frontier can finish sooner than a wide one. Sync rounds are real
  wall-clock and they serialize on you.

## UI epics: verify the rendered app

Green CI proves the tests pass, not that the UI works — a whole epic can close on
green checks while the deployed app breaks on a phone. On an epic that changes
user-facing UI, before writing the final report: verify the deployed or preview
build in a browser at both mobile and desktop widths (delegate to a subagent with
browser tools if available; otherwise say plainly that no rendered-app
verification happened). The final report then includes the preview URL and a
short check-on-device list for the user. Every deviation found gets its own
disposition — fix now, accept, or defer with a named trigger — not a line in an
aggregate list.

## Stopping conditions

Stop the loop and report — rather than pushing through — when:

- **All issues are `done`.** The good ending.
- **Nothing is unblocked** but open issues remain (a human-gate from Step 1, a PR
  a human opened, a dependency outside this epic). Show the dependency picture.
- **An issue stays red after escalation.** Leave its branch and PR intact, state
  exactly where it stands and what fails.
- **The user needs to decide something** an implementer surfaced — a spec
  contradiction, a forbidden merge-commit setting, a closed-unmerged PR.
- **The toolchain itself is down** — permission-classifier outage, repeated 5xx
  from the API or GitHub. After two or three spaced retries, stop cleanly: report
  the repo state (branches, open PRs, board), list the literal commands that
  remain, and tell the user to clear any goal/Stop hook that would keep relaunching
  you into the outage. An implementer report that ends with "one command left,
  blocked by outage" is retryable later, not failed — record it as such.

## Final report

- **Merged**: each issue with its PR link, in merge order.
- **Models used**: which tier ran each issue (and any escalations) — the user is
  paying for this judgment, show it.
- **Test/CI summary**: per-issue results as reported, plus any repo-has-no-CI note.
- **UI verification** (UI epics): preview URL, widths checked, deviations with
  their dispositions.
- **Deviations**: every deviation file implementers reported, aggregated — `close-epic`
  promotes them, so name each one's epic/issue and evidence path, not just the gist.
- **Follow-ups**: out-of-scope discoveries collected from all reports.
- **Left over**: anything not `done` and precisely why — including human-gates
  still waiting on the user.

## Hand off to close-epic

Your loop stopping is not the epic being closed, and the two are not the same job. The
worktrees you spawned still hold branches checked out, the merged remote branches are
still there, the milestone is still open, and the deviations above exist only in this
report — which dies with the session. That state is what stops the *next* epic from
starting, and sorting it out is not tail work for a supervisor's context at its most
depleted: it needs a fresh one.

So end the run by handing over to `close-epic` — it verifies the epic's real state
against GitHub and git, promotes the deviations into `docs/planning/DEVIATIONS.md`,
closes the milestone, and cleans up. Offer to run it now (or spawn a subagent to, with
this report as its input); if the user declines, say plainly that worktrees, branches
and the milestone are left as-is and the deviations are unpromoted.

This applies just as much when the run stopped early — an interrupted run is when its
discoveries are most likely to be lost and a half-cleaned repo is what makes the resume
fail.
