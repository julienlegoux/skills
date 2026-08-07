# Diff recipes

Deriving the epic's merged diff, attributed per issue. Step 1's mechanics.

The diff — not the issue files — is the review surface. Bookkeeping records intent; the
merge commits record what shipped.

## Resolve the PRs

Read `gh_pr` from every issue file in the epic:

```bash
grep -H '^gh_pr:' docs/epics/epic-<n>-<slug>/issues/*.md
```

Resolve each to its real state and merge commit. **`status: done` is not evidence** — the
previous run's bookkeeping may have stopped mid-flight, which is why `close-epic` exists:

```bash
gh pr view <pr> --json number,state,mergedAt,mergeCommit,baseRefName,files
```

Classify: MERGED (in the surface), OPEN (not shipped — note it), CLOSED unmerged (not
shipped). The `baseRefName` of the merged PRs is the integration branch the epic actually
landed on; trust it over any branch name the user or a doc supplies.

## Derive the range

`implement-epic` merges with `--merge` and forbids squash, so every PR is a merge commit
and per-issue attribution survives `close-epic`'s branch deletion.

```bash
# oldest merge commit in the epic
git log --format='%H %ct' <merge-commits> | sort -k2 -n | head -1

# the epic's whole surface
git diff <first-merge>^1..<last-merge> --stat
git diff <first-merge>^1..<last-merge>
```

Per issue, from its own merge commit:

```bash
git show <merge-commit> --stat
git diff <merge-commit>^1..<merge-commit>       # only that PR's changes
```

`^1` is the integration branch's side of the merge — the state before that PR landed.

Commits by other people can land between the epic's merges, so `first^1..last` may
include work outside the epic. Check with `git log --merges <first>^1..<last>` and, if
foreign merges appear, review the per-issue diffs and treat their union as the surface
rather than the contiguous range. Say which you used in the report's scope section.

## Fallbacks

| Situation | Do this |
|---|---|
| An issue has no `gh_pr` | Search by branch or title: `gh pr list --search "<issue title>" --state merged`. If nothing, the issue shipped nothing — a finding, not a gap. |
| `gh` unavailable or unauthenticated | Fall back to git: `git log --merges --grep='#<issue>' <integration>`. Mark GitHub state `not verified` in the report. |
| The epic used the milestone but issue files are incomplete | `gh pr list --search 'milestone:"<milestone>"' --state merged --json number,mergeCommit,title` |
| PRs were squashed anyway (a repo overriding the convention) | Per-issue attribution is lost. Review the range as a whole, and record the lost attribution in the report — it also means the red-green provenance check in `test-integrity.md` can't run. |
| Merge commit missing from local history | `git fetch origin <integration-branch>` first; the branch may be behind. |

## Size the review before spawning

```bash
git diff <range> --stat | tail -1
```

Report the file and line counts in the report's scope section. They are what makes a
later reader able to judge how much the review could plausibly have seen.
