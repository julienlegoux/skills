---
name: implement-epic
description: Supervise the implementation of ALL remaining issues in an epic by delegating each one to a subagent running the implement-issue skill — pick an adapted model and reasoning effort per issue, wait for CI, merge green PRs into the integration branch (develop) with a merge commit, and loop until the epic is done. Use this whenever the user asks to "finish epic 2", "implement the rest of the issues in epic N", "do the whole epic", "keep merging until the epic is done", "run epic 3 end to end", or wants issues from docs/epics/ implemented with subagents while the main session supervises — even if they phrase it as "implement the remaining issues" or "keep going until everything is green and merged".
---

# Implement an Epic

`create-issues` sized every issue in the epic to be one focused PR, and
`implement-issue` turns one issue into one PR. This skill is the layer above: run
that loop for every remaining issue in an epic — delegate, watch CI, merge, repeat —
until the epic's board shows all `done`.

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

## Step 1: Map the epic

1. Locate the epic folder (`docs/epics/epic-<n>-<slug>/`). Read `issues/index.md`
   and each issue's **frontmatter only** (`issue`, `slug`, `size`, `status`,
   `gh_issue`, `gh_pr`, `depends_on`) — the bodies are for the implementers.
2. Determine the **integration branch**: the one the user named; else `develop` if
   it exists; else the repo's default branch. All PRs in this run target it, and
   every implementer must be told about it explicitly — `implement-issue` defaults
   to the default branch otherwise.
3. **Preflight the permissions this loop depends on**, before spawning anything.
   `gh auth status` must work — the flow is built on `gh`. But auth is not enough:
   restrictive permission modes can deny `gh pr merge` even when `gh` itself works.
   Discovering that after several PRs are green strands the run, and you cannot fix
   it yourself — widening your own permissions is itself blocked. So settle it in
   your opening message: if merging looks gated, ask for it up front. Direct
   `git push` to the integration branch is commonly blocked too; assume it is and
   tell implementers, so they don't each rediscover it and improvise a workaround.
4. Build the board: which issues are `done`, `pr-open` (PR to check on),
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
   so they run concurrently. Cap the frontier at ~4 in-flight implementers; more
   mostly buys merge-conflict churn on a shared integration branch. Give each one
   its own git worktree (`isolation: "worktree"`) — concurrent agents sharing a
   checkout clobber each other's branches and uncommitted work.
3. **As each PR appears**, record its number and the report's essentials, and
   start watching its checks in the background (see CI and merging).
4. **Merge one at a time.** When one or more PRs are green, merge the
   lowest-numbered issue's PR first (dependency order is numbered order within an
   epic). After each merge, every still-open PR is now behind the integration
   branch — any that CI flags as conflicting gets a sync round (see Merge
   conflict below); the rest just merge when their turn comes.
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

## Implementer prompt template

```
Invoke the implement-issue skill and follow it to implement issue <nn> of epic <n>
(<epic folder path>).

Constraints from the supervisor:
- Integration branch is `<branch>`: branch off the LATEST `origin/<branch>` (fetch
  first) and open the PR against `<branch>` — confirm with
  `gh pr view <n> --json baseRefName` after creating it. This overrides
  implement-issue's default-branch assumption.
- Do NOT merge the PR yourself — the supervisor handles merging.
- Do NOT push directly to `<branch>`; if bookkeeping seems to need it, put it on
  your own branch instead.
- Do NOT delete remote branches. Do NOT use `git stash` — `refs/stash` is shared
  across worktrees, so stashing corrupts concurrent agents' work; use a patch file
  or a throwaway commit.
- Bookkeeping: edit only your OWN issue file. Leave `issues/index.md` and the epic
  log to the final reconcile pass.
- Commit and push incrementally, so a transient failure mid-run costs no progress.
- Once your PR is open, report and END your turn. Do NOT watch or poll CI — that's
  the supervisor's job and waiting loops burn your context for nothing.
- <effort steer from the table>
- <traps earlier issues in this epic hit the hard way — a required env var, a
  boundary the test tier can't see. Pass them forward; it saves a red CI round.>

Report back, concisely: PR number and URL, final diff size vs predicted size,
test results (real numbers), any deviation files written, out-of-scope follow-ups
you noted, and anything that blocked you.
```

## CI and merging

**Watch checks** without babysitting them in the foreground:

```bash
gh pr checks <pr> --watch --fail-fast
```

Run it in the background — but do not treat its exit code as proof of a pass.
`gh pr checks` reports success when the required job is *absent*, and a push
occasionally produces no workflow run at all (a dropped event). That combination is
a convincing false green on a PR nothing ever tested. Confirm a run exists for the
current head before calling anything green:

```bash
gh api "repos/<owner>/<repo>/actions/runs?head_sha=$(gh pr view <pr> --json headRefOid -q .headRefOid)" -q .total_count
```

Zero → nothing was tested; have the implementer push again (an empty commit
suffices) and re-check. Also confirm the required job appears by name in the
`gh pr checks` output, not merely that the command exited 0.

If the repo has **no checks configured**, there's nothing to wait on: rely on the
implementer's reported test results, note the absence of CI once in the final
report, and merge.

**Green → verify the target, then merge with a merge commit, always:**

An implementer can open its PR against the repo default instead of the integration
branch. Unwinding a merge into the wrong branch costs far more than the check does:

```bash
gh pr view <pr> --json baseRefName -q .baseRefName   # must be the integration branch
gh pr merge <pr> --merge --delete-branch
```

Never `--squash` or `--rebase` in this flow: the merge commit preserves each
issue's own commit history (including its red-green TDD trail) and keeps the
integration branch's first-parent line reading as one merge per issue. If the
repo's settings forbid merge commits, stop and tell the user — don't silently
squash to get past it.

**Red → fix round.** Pull only the failure headline (`gh pr checks <pr>` plus
`gh run view --log-failed` if needed — skim for the failing job name and error,
don't study logs at length). Then message the **same implementer agent** (its
context already holds the whole implementation) with the failure summary and ask
it to fix and push. Two failed fix rounds → escalate per the model table. Still
red after escalation → stop and report; don't thrash CI all afternoon.

**Merge conflict** (integration branch moved since the PR branched): have the
implementer merge the integration branch into its feature branch, resolve, and
push — merge, not rebase, consistent with the merge-commit policy.

**An implementer that dies mid-run** (transient API 500/529, context exhaustion)
has not necessarily lost its work. Check whether its PR and pushed commits already
exist before assuming anything, and prefer resuming it by message — its context is
intact — over spawning a replacement that has to rediscover everything.

## Bookkeeping

You never edit bundle files yourself. `implement-issue`'s own reconcile step flips
merged PRs' issues to `done` at the start of the *next* run — so intermediate
statuses self-heal as the loop turns. That leaves exactly one gap: after the
**final** merge there is no next implementer. Close it by spawning one small
(`haiku`) subagent: "Invoke the implement-issue skill and run ONLY its Step 1
reconcile pass, then stop and report what it updated."

**Concurrency makes bookkeeping the main source of merge conflicts.** Every
implementer writes status into the same shared files, so each merge leaves every
other open PR conflicting on lines unrelated to its own work. Unchecked this
dominates the run — a wave of four PRs can cost more sync rounds than the
implementation did. Two things keep it small: implementers touch only their own
issue file (which conflicts with nobody), and when a shared-file conflict does
happen the resolution is always a union — every issue keeps its line, and merged
ones read `done`. Say that in the sync request, so nobody clobbers a sibling's
status while resolving.

## Stopping conditions

Stop the loop and report — rather than pushing through — when:

- **All issues are `done`.** The good ending.
- **Nothing is unblocked** but open issues remain (e.g. waiting on a PR a human
  opened, or a dependency outside this epic). Show the dependency picture.
- **An issue stays red after escalation.** Leave its branch and PR intact, state
  exactly where it stands and what fails.
- **The user needs to decide something** an implementer surfaced — a spec
  contradiction, a forbidden merge-commit setting, a closed-unmerged PR.

## Final report

- **Merged**: each issue with its PR link, in merge order.
- **Models used**: which tier ran each issue (and any escalations) — the user is
  paying for this judgment, show it.
- **Test/CI summary**: per-issue results as reported, plus any repos-has-no-CI note.
- **Deviations**: every deviation file implementers reported, aggregated.
- **Follow-ups**: out-of-scope discoveries collected from all reports.
- **Left over**: anything not `done` and precisely why.
