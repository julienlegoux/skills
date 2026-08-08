# CI and merging recipes

Command-level recipes for the supervisor's CI-watch/merge loop. The policy
(merge-commit only, one merge at a time, escalation ladder) lives in SKILL.md;
this file is the how.

## Identify the required checks (once, at Step 1)

Know which job names actually gate merging before the first PR exists:

```bash
gh api "repos/<owner>/<repo>/branches/<integration-branch>/protection/required_status_checks" -q '.contexts' 2>/dev/null
gh api "repos/<owner>/<repo>/rules/branches/<integration-branch>" -q '.[] | select(.type=="required_status_checks")' 2>/dev/null
```

Nothing configured → there are no required checks: rely on implementers' reported
test results, note the absence of CI once in the final report, and merge greens.

Third-party checks that are *not* in the required list (Vercel previews, review
bots, coverage commenters) are surface-to-the-user notes — never merge blockers,
never fix rounds.

## Watching checks

```bash
gh pr checks <pr> --watch --fail-fast
```

Run it in the background. **Do not treat its exit code as proof of a pass**:
`gh pr checks` reports success when the required job is *absent*, and a push
occasionally produces no workflow run at all (a dropped event). That combination
is a convincing false green on a PR nothing ever tested. Before calling anything
green:

1. Confirm the required job(s) appear **by name** in the `gh pr checks` output.
2. Confirm a run exists for the current head:

```bash
gh api "repos/<owner>/<repo>/actions/runs?head_sha=$(gh pr view <pr> --json headRefOid -q .headRefOid)" -q .total_count
```

## Zero CI runs: diagnosis order

```bash
gh pr view <pr> --json mergeable,mergeStateStatus
```

**FIRST**, always. `DIRTY`/`CONFLICTING` → GitHub never builds a conflicting PR
and no number of empty commits will change that — send the sync-round message
(see implementer-prompt.md). Only a MERGEABLE PR with zero runs justifies asking
the implementer to push an empty commit to retrigger, then re-check.

## Merging a green PR

Verify the target first — an implementer can open its PR against the repo default
instead of the integration branch, and unwinding a wrong-branch merge costs far
more than the check:

```bash
gh pr view <pr> --json baseRefName -q .baseRefName   # must be the integration branch
gh pr merge <pr> --merge --delete-branch
```

A local-branch-delete error after the merge is benign under worktrees (the branch
is checked out in an agent's worktree) — the merge itself succeeded; move on.

Right after each merge, close the issue's GitHub issue — `Closes #N` does not
fire on a non-default base (see `pipeline-interfaces.md`):

```bash
gh issue close <gh_issue> --comment "Completed by PR #<pr>"
```

## Red check: pulling the failure headline

```bash
gh pr checks <pr>
gh run view <run-id> --log-failed   # only if the check line isn't enough
```

Skim for the failing job name and the error line — don't study logs at length;
the implementer holding the implementation context does the actual diagnosis.

## End-of-run cleanup

Not this skill's job, and not this file's recipes: worktrees, branches and the
milestone are `close-epic`'s Step 4 (`skills/close-epic/references/state-and-cleanup.md`).
Hand off to it rather than improvising a cleanup here — the ordering rules and the
never-delete-unpushed-work checks live there, in one copy.
