# Implementer prompts

Prompts the supervisor sends to subagents. These stay deliberately prescriptive:
implementers often run on smaller models (haiku/sonnet) that follow rules better
than principles — do not soften them when editing.

## Implementer prompt template

Spawn each implementer with the Agent tool, `isolation: "worktree"`, and the model
from the SKILL.md table. Fill every `<placeholder>`:

```
Invoke the implement-issue skill and follow it to implement issue <nn> of epic <n>
(<epic folder path>).

Worktree operating manual — you are in a fresh git worktree, and the harness guard
refuses compound git commands:
- Plain single git commands only: no `&&`, no pipes, no `cd <path> && git ...`
  prefix. One git operation per command.
- Your first two commands: `git fetch origin`, then
  `git checkout -b <feature-branch> origin/<integration branch>`. The worktree was
  created from whatever the main checkout had — its HEAD may predate the epic
  bundle — so never trust the initial file state; branch from the latest
  `origin/<integration branch>` before reading anything.
- Every path you read or edit is under YOUR worktree root, never the main
  checkout's path. After any path redirect or file-not-found, Read the file fresh
  before editing — edits aimed at main-checkout paths corrupt concurrent agents'
  work and cascade.

Constraints from the supervisor:
- Integration branch is `<branch>`: open the PR against `<branch>` — confirm with
  `gh pr view <n> --json baseRefName` after creating it. This overrides
  implement-issue's default-branch assumption.
- Do NOT merge the PR yourself — the supervisor handles merging.
- Do NOT push directly to `<branch>`; if bookkeeping seems to need it, put it on
  your own branch instead.
- Do NOT delete remote branches. Do NOT use `git stash` — `refs/stash` is shared
  across worktrees, so stashing corrupts concurrent agents' work; use a patch file
  or a throwaway commit.
- Reconcile scope: in implement-issue's Step 1, settle only the issues in YOUR
  issue's `depends_on` chain; leave the rest of the epic's statuses alone.
  Epic-wide reconciliation happens in a dedicated final pass, and siblings are
  writing those lines concurrently.
- Bookkeeping: keep `issues/index.md` and the epic log updated as implement-issue
  requires — an OKF index that disagrees with its own docs is broken. Expect
  conflicts there, since siblings write the same lines; resolve as a union that
  keeps every issue's line, never by clobbering a sibling's status.
- Commit and push incrementally, so a transient failure mid-run costs no progress.
- Once your PR is open, report and END your turn. Do NOT watch or poll CI — that's
  the supervisor's job and waiting loops burn your context for nothing.
- If an acceptance criterion produces bulky verification evidence (screenshots,
  log dumps), write it to disk under the epic folder and reference the path in
  your report — never paste it into context.
- If a permission classifier outage or repeated 5xx blocks your final command,
  state the single remaining command in your report and end your turn — the
  supervisor treats that as retryable, not failed.
- <effort steer from the model table>
- <traps earlier issues in this epic hit the hard way — a required env var, a
  boundary the test tier can't see. Pass them forward; it saves a red CI round.>

Report back, concisely: PR number and URL, final diff size vs predicted size,
test results (real numbers), any deviation files written, out-of-scope follow-ups
you noted, and anything that blocked you.
```

## Fix-round message (same agent, red CI)

Message the **same implementer** — its context already holds the whole
implementation:

```
CI failed on PR #<pr>. Failing job: <job name>. Error headline:
<one-to-three lines from the failed log>

Fix it and push to your branch. Same constraints as before: single git commands
only, no stash, don't merge, don't watch CI — push and end your turn.
```

## Sync-round message (same agent, merge conflict)

```
PR #<pr> is conflicting with `<integration branch>` (it moved since you branched).
Merge `origin/<integration branch>` INTO your feature branch — merge, not rebase —
resolve, and push. For `issues/index.md` and the epic log, resolve as a UNION:
every issue keeps its own line, merged issues read `done`, never clobber a
sibling's status. Then end your turn.
```

## Final-reconcile agent prompt

After the last merge there is no next implementer to self-heal the statuses. Spawn
one small (`haiku`) agent — with the same base-branch constraints as implementers,
because a reconcile PR merged into the wrong branch is still a wrong-branch merge:

```
Invoke the implement-issue skill and run ONLY its Step 1 reconcile pass for epic
<n> (<epic folder path>), then stop and report what it updated.

Constraints from the supervisor:
- Integration branch is `<branch>`. Commit the reconcile updates on a fresh branch
  off the LATEST `origin/<branch>` (fetch first) and open a PR against `<branch>`
  — never against the repo default. If direct push to `<branch>` is permitted in
  this repo, commit directly on it instead and skip the PR.
- Close every GitHub issue whose PR merged and is still open
  (`gh issue close <N> --comment "Completed by PR #<pr>"`), and remove stale
  status labels.
- Do NOT merge any PR yourself; report the PR number if you opened one.
```
