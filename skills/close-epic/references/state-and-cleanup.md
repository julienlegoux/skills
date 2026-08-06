# State and cleanup recipes

Command-level recipes for Steps 1 and 4. The policy — what may be deleted, what must
be confirmed — is in SKILL.md; this file is the how.

## Reading the real state

The bundle, frontmatter only:

```bash
# every issue's recorded status and PR, without reading any body
for f in docs/epics/epic-<n>-*/issues/[0-9]*.md; do
  echo "$f: $(sed -n '/^status:/p;/^gh_issue:/p;/^gh_pr:/p' "$f" | tr '\n' ' ')"
done
```

GitHub, per recorded PR — the authoritative answer on merges:

```bash
gh pr view <gh_pr> --json state,mergedAt,baseRefName,headRefName -q \
  '[.state, .mergedAt, .baseRefName, .headRefName] | @tsv'
```

The milestone: what is still open on it, and its own state.

```bash
gh issue list --milestone "<milestone title>" --state open --json number,title
gh api "repos/<owner>/<repo>/milestones" -q '.[] | select(.title=="<title>") | [.number, .state, .open_issues] | @tsv'
```

`--state open` matters: a milestone whose `open_issues` is 0 is the only one safe to
close.

git, what is still lying around:

```bash
git worktree list                              # agent worktrees from the run
git branch --list 'issue-*'                    # local feature branches
git branch -r --merged origin/<integration>    # remote branches already merged in
git log --oneline origin/<integration> -15     # one merge per issue, as expected?
git status --short                             # the integration branch must be clean
```

## Closing the milestone

`gh` has no `milestone close` command — it goes through the API:

```bash
gh api -X PATCH "repos/<owner>/<repo>/milestones/<number>" -f state=closed
```

## Cleanup, in order

Worktrees first. Removing a worktree that still has a branch checked out is what makes
the later branch deletion fail — not the other way around.

```bash
git worktree list                              # identify the run's worktrees
git -C <worktree-path> status --short          # MUST be empty
git -C <worktree-path> log --oneline @{u}..    # MUST be empty (nothing unpushed)
git worktree remove <worktree-path>
git worktree prune                             # clears stale administrative entries
```

If either check is non-empty, stop on that worktree and report it. `git worktree
remove --force` on unpushed work destroys the only copy.

Then local branches, then merged remote branches — each one verified merged first:

```bash
gh pr view <pr> --json state -q .state         # MERGED, or it does not get deleted
git branch -d <branch>                         # -d, never -D: it refuses unmerged work
git push origin --delete <branch>
```

`git branch -d` refusing to delete is a signal, not an obstacle: it means the branch
holds commits that never landed. Investigate; do not reach for `-D`.

## Windows note

Worktree removal fails while any process holds a file in the tree — an editor, a
watcher, a dev server started by an implementer. The error names the path, not the
holder. Report it and let the user close it rather than retrying in a loop.
