# Pipeline interfaces

Single source of truth for the epic and issue schemas, their status lifecycle, and
the GitHub facts the skills that carry an epic to merged PRs depend on
(`split-epics`, `define-change`, `create-issues`, `implement-issue`,
`implement-epic`). SKILL.md files point here instead of re-describing these formats.

The rules that apply to *anything* written under `docs/` — language, bundle and link
rules, reserved files, committing what you write — live in `bundle-interfaces.md`,
and the decision doc `define-change` writes lives in `ledger-interfaces.md`. Read
`bundle-interfaces.md` alongside this file; the schemas below assume its link rules.

This is the one and only copy: every epic-to-PR skill reads it at
`../_shared/pipeline-interfaces.md`. Editing it changes behaviour for all of them at
once.

## Epic file

Path: `docs/epics/epic-<n>-<slug>/EPIC_<n>.md`. Slug: lowercase kebab-case, ASCII,
~40 chars. Written by `split-epics` (greenfield) or `define-change` (brownfield) —
format-identical from either producer, so downstream skills can't tell which one
made it.

```markdown
---
type: Epic
title: "<title>"
description: "<one-sentence summary of the epic's goal>"
tags: [epic]                 # define-change adds: change
timestamp: <ISO 8601 — set on every meaningful write>
epic: <n>
slug: <slug>
status: draft                # draft | open
gh_issue: null               # tracking issue number, once created
milestone: null              # milestone number, once created
source: <plan path#heading, or the change ledger's index.md path>
---

# Epic <n>: <title>

## Goal
## Scope
## Out of scope
## Acceptance criteria
## Dependencies
## Context
## Notes
```

Field notes:

- `status: draft` = local file only; `status: open` = GitHub milestone + tracking
  issue exist, at which point `gh_issue`, `milestone`, and
  `resource: https://github.com/<owner>/<repo>/issues/<number>` are filled and
  `timestamp` refreshed. `resource` never appears before the GitHub issue exists.
- `## Dependencies` links other epics bundle-relative
  (`[Epic 1](/epic-1-core-crud/EPIC_1.md)`), or reads "None".
- `## Context` links `docs/planning/` docs (SPECS.md, CONVENTIONS.md, and for
  brownfield the change ledger) with plain relative paths — they cross bundles.
  Omit the section entirely when none exist. Reference, never copy — the planning
  docs stay the single source of truth.

## Issue file

Path: `docs/epics/epic-<n>-<slug>/issues/<nn>-<slug>.md` — `<nn>` 1-indexed,
zero-padded to two digits, numbered in dependency/build order (issue 1 must not
depend on issue 3). Written by `create-issues`; updated by `implement-issue` and
`implement-epic` as status changes.

```markdown
---
type: Issue
title: "<title>"
description: "<one-sentence summary of what this PR does>"
tags: [epic-<n>]
timestamp: <ISO 8601 — set on every meaningful write>
epic: <n>
issue: <nn>
slug: <slug>
size: S|M|L
status: draft                # draft | open | in-progress | pr-open | done
gh_issue: null
depends_on: []               # other issue numbers in this epic
---

# <title>

## Summary
## Scope
## Out of scope
## Acceptance criteria / Definition of done
## Relevant files / areas
## Dependencies
## PR size note
```

Field notes:

- `size`: S ≈ under 200 changed lines, M ≈ 200–500, L ≈ 500–1000. L is the
  ceiling, not the target.
- `gh_pr: <PR number>` is an extension field **added by implement-issue** when the
  PR opens. No other fields are ever added — conformant OKF consumers tolerate
  extensions, but every new field is one more thing the whole pipeline must agree
  on.
- `resource` appears only once the GitHub issue exists (same rule as epics).

## Issue status lifecycle

`draft → open → in-progress → pr-open → done`

| Transition | Written by | When |
|---|---|---|
| (created) `draft` | create-issues | the `.md` file is written locally |
| `draft → open` | create-issues | the GitHub issue is created (`gh_issue` + `resource` filled) |
| `open → in-progress` | implement-issue | the feature branch is created — the flip is the branch's first commit |
| `in-progress → pr-open` | implement-issue | the PR is opened (`gh_pr` recorded) |
| `pr-open → done` | implement-issue's Step-1 reconcile in a **later** run, or implement-epic's final reconcile agent | the recorded PR is MERGED |

Every status write also refreshes the file's `timestamp`, updates the matching
bullet in that epic's `issues/index.md`, and appends a `docs/epics/log.md` entry if
that file exists. An index that disagrees with its own docs is broken — never skip
the bullet update to avoid a merge conflict; resolve conflicts as a union instead
(every issue keeps its own line, merged issues read `done`, nobody clobbers a
sibling's status).

The GitHub issue mirrors every transition: a timeline comment plus a status label
(`status: in-progress`, `status: pr-open` — reuse the repo's own scheme if one
exists), and the issue is closed at `done`. Bookkeeping never blocks
implementation: if `gh` is unavailable, skip the mirror with a note.

Reconcile commits — the writes that flip merged work to `done` — belong on the
branch the epic's statuses live on: the **integration branch** when one is in play,
otherwise the default branch. They describe work that already merged there;
putting them on a feature branch holds finished facts hostage to an unmerged PR.

## GitHub facts on non-default integration branches

When PRs target an integration branch (e.g. `develop`) rather than the repo
default, two behaviors differ from what most GitHub experience predicts:

- **`Closes #N` never auto-closes the issue.** GitHub fires closing keywords only
  on merges into the *default* branch. Keep the keyword in the PR body (it links
  the PR to the issue in the UI), but plan for explicit closing — at reconcile, or
  by the supervisor right after each merge. That explicit close is the *normal*
  path, not a fallback for a missed keyword.
- **A CONFLICTING PR gets zero CI runs.** GitHub doesn't build a PR whose merge
  would conflict, and pushing an empty commit doesn't change that. Diagnosis order
  for a PR with no checks: `gh pr view <pr> --json mergeable,mergeStateStatus`
  FIRST; `DIRTY`/`CONFLICTING` → resolve the conflict (sync round with the
  integration branch); only MERGEABLE-with-zero-runs justifies an empty commit to
  retrigger CI.

## Decision doc (planning ledger)

Moved: the decision doc schema lives in `ledger-interfaces.md`, synced to every
ledger-driven skill. `define-change` is the only skill here that writes one.
