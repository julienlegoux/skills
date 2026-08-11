---
name: split-epics
description: Split a planning document (typically docs/planning/SCOPE.md) into one folder per epic under docs/epics/ — each with an EPIC_N.md, a GitHub milestone, and a tracking issue — ready for create-issues. Use whenever the user wants a plan or scope turned into trackable epics.
---

# Split Epics from a Plan

A planning doc is one big document. This skill turns it into a set of independent,
addressable epics — one folder each, with its own file and its own GitHub issue —
so that each epic can later be handed to the `create-issues` skill without anyone
having to re-read the whole plan.

Read this whole file before starting; the confirmation step (Step 4) is not optional —
creating milestones and issues touches a shared GitHub repo, so the user needs to see
the breakdown before anything is created there.

## Output format: OKF

Every file this skill writes under `docs/epics/` must be a conformant OKF v0.1
bundle, so any OKF-aware tool or agent — not just this skill and `create-issues` —
can read `docs/epics/` as structured knowledge. The epic file schema is defined once
in `../_shared/pipeline-interfaces.md`, and the rules for anything written under
`docs/` — English content, link forms, reserved `index.md`/`log.md` files, and
committing what you write — in `../_shared/bundle-interfaces.md`. Read both before
writing anything. A third governs nothing this skill writes:
`../_shared/feedback-interfaces.md`, the closing reflex for what this run teaches about
*this skill*, read at Step 7.

## Step 1: Find the plan doc

Look in `docs/` for the planning document. Common cases, in order of likelihood:

- The user names the file directly ("split docs/PLAN.md into epics") — use that.
- `docs/planning/SCOPE.md` exists — use it. This is the define-scope skill's
  deliverable and the primary expected input; its `## Milestone N:` headings are
  written to match this skill's boundary detection. Never treat the sibling
  `SPECS.md`/`CONVENTIONS.md` as split candidates — they are context (Step 2b),
  and the decision docs under `docs/planning/*/` aren't plans at all.
- A single obvious candidate exists (`docs/PLAN.md`, `docs/plan.md`, or the only
  markdown file in `docs/` that isn't already under `docs/epics/` or
  `docs/planning/`) — use it.
- Multiple candidates exist — list them with their first heading and ask the user
  which one to split.

Read the whole file into context before moving on. Don't skim — epic boundaries and
cross-epic dependencies are often stated in prose, not just headings.

## Step 2: Detect epic boundaries

Plans don't all use the same structure, so apply these in order and stop at the first
one that fits:

1. **Explicit epic headings** — headings like `## Epic 1: User auth` or `# Epic 2 —
   Billing`. If these exist, they define the epics directly; use the stated numbers
   if present, otherwise number by order of appearance.
2. **Phase/milestone/part structure** — plans (especially ones written by a planning
   skill rather than a human) are often organized as `## Phase 1: ...` or `## Milestone
   2: ...` or `## Part N`. Each top-level grouping like this is an epic candidate.
3. **No grouping at all** — the plan is a flat list of tasks or requirements with no
   natural top-level split. Don't invent a grouping. Instead, summarize the flat
   structure you found and ask the user how they'd like it grouped into epics (or
   whether the whole doc is really just one epic).

Whichever heuristic matched, an "epic" should be a chunk of work that's independently
shippable and meaningfully large — think weeks, not a single afternoon. If a candidate
epic is really just one or two tasks, that's a signal it belongs inside a
neighboring epic rather than standing alone; call this out to the user rather than
silently merging or splitting.

For each epic identified, pull out:

- **Title**
- **Goal / why it matters** (often stated near the top of the section, or inferable
  from the plan's overall goals section)
- **Scope** — what's in and, if the plan says so, explicitly what's out
- **Acceptance criteria / definition of done**, if the plan states any
- **Dependencies** — does this epic block or depend on another epic? Plans often say
  this explicitly ("after Epic 1 ships...") — preserve that ordering, don't reorder
  epics alphabetically or by convenience.

Plans often also state constraints that apply to the whole project rather than one
phase — e.g. an overall "Goals" section saying "no rich text editor, no real-time
collaboration in v1." Don't force these into one epic's "Out of scope" just because
it's the one most likely to touch that area; "Out of scope" is for that epic's own
boundary decisions. Instead, carry a plan-wide constraint into the "Notes" section of
every epic it's actually relevant to, and say plainly that it's project-wide rather
than specific to this epic.

## Step 2b: Gather project-wide context docs

Epic boundaries come solely from the plan doc — but if the planning bundle has
sibling deliverables, every epic should link them rather than anyone re-copying their
content. Check for `docs/planning/SPECS.md` (technical specs from define-specs) and
`docs/planning/CONVENTIONS.md` (repo standards from define-conventions). Whichever
exist go into each epic's `## Context` section (see the Step 3 template) so that
`create-issues` sizes issues against the real stack and `implement-issue` finds the
project's standards — reference, never copy; the planning docs stay the single source
of truth. If neither exists, omit the `## Context` section entirely.

These links cross from the `docs/epics/` bundle into the `docs/planning/` bundle, so
bundle-relative (leading-`/`) links don't apply — use plain relative paths from the
epic file, e.g. `../../planning/SPECS.md`.

## Step 3: Draft epic numbers, slugs, and files

- Number epics by order of appearance in the plan, 1-indexed, unless the plan already
  assigns explicit numbers (preserve those instead — don't renumber a plan that says
  "Epic 3" as epic 1 just because it appears first in the doc).
- Slug: lowercase kebab-case of the title, ASCII only, punctuation stripped, capped
  around 40 characters (e.g. "User Auth & Session Refresh" → `user-auth-session-refresh`).
- Folder: `docs/epics/epic-<n>-<slug>/`
- File: `docs/epics/epic-<n>-<slug>/EPIC_<n>.md`

Write each `EPIC_<n>.md` using the epic file template in
`../_shared/pipeline-interfaces.md` — frontmatter starts at `status: draft` with
`gh_issue`/`milestone` null (filled in Steps 6/7) and no `resource` field yet.
Section content mapping from the plan: Goal = why this epic exists and what it
unlocks; Scope = what's included; Out of scope = what the plan explicitly
excludes; Acceptance criteria as stated or inferable; Dependencies links other
epics bundle-relative or reads "None"; Context = the Step 2b links (omit the
section if none); Notes = anything else worth preserving — open questions, risks,
alternatives considered, plan-wide constraints relevant here.

Carry content over faithfully rather than compressing it — this file, not the original
plan, is what `create-issues` and future readers will treat as the source of truth for
this epic.

## Step 4: Show the breakdown and confirm

Before writing anything, show the user a preview:

- The plan doc you read and the heuristic that matched
- Each epic: number, title, one-line summary, destination path
- What will happen next: local files get written, then one GitHub milestone and one
  tracking issue get created *per epic*

Wait for explicit confirmation. This step exists because Steps 6–7 create real,
repo-visible GitHub state (milestones, issues) — mis-detected epic boundaries are easy
to fix before that point and annoying to fix after.

If the user asks to adjust groupings, re-merge, rename, or renumber epics, do that and
show the updated preview before proceeding — don't just proceed on the first pass.

## Step 5: Write the local files

Create each `docs/epics/epic-<n>-<slug>/` folder and its `EPIC_<n>.md`. Also create or
update `docs/epics/index.md` — the bundle root's OKF directory listing, so a human (or
the create-issues skill, or any other OKF-aware tool) can see all epics at a glance
without opening every file. Per OKF, this file gets no frontmatter except
`okf_version` (only ever set here, only at the bundle root), and its body is a grouped
link list, not a table:

```markdown
---
okf_version: "0.1"
---

# Epics

* [Epic 1: User auth](/epic-1-user-auth/EPIC_1.md) - draft, no GitHub issue yet
```

Each bullet's description should track that epic's `EPIC_<n>.md` frontmatter
(`description` + `status`) — update it after Step 7 once the GitHub issue exists.

**Idempotency:** if `EPIC_<n>.md` already exists and already has a `gh_issue` set in
its frontmatter, don't recreate it or its GitHub issue — report that it already exists
and skip it. If the plan doc changed since that epic was created, say so and ask
whether to update the local file's body (never silently overwrite; never touch
`gh_issue`/`milestone` once set).

## Step 6: Create a GitHub milestone and epic issue per epic

You need the repo's `owner/repo` first:

```bash
gh repo view --json nameWithOwner -q .nameWithOwner
```

For each epic, in order (respect the dependency ordering from Step 2 — create epic 1's
issue before epic 2's if the plan implies a sequence, since epic 2's issue body may
reasonably reference epic 1's):

1. **Milestone** — one per epic, titled `Epic <n>: <title>`. Use the bundled script,
   which finds-or-creates so re-runs are safe:

   ```bash
   bash scripts/ensure_milestone.sh <owner>/<repo> "Epic <n>: <title>"
   ```

   This prints `{"number": N, "title": "..."}`.

2. **Label** — check for an existing convention before inventing one:

   ```bash
   gh label list --json name -q '.[].name'
   ```

   If a label scheme for epics already exists (e.g. `epic`, `type: epic`), reuse it.
   Otherwise create a plain `epic` label (`gh label create epic --color BFD4F2
   --description "Tracks an epic" 2>/dev/null || true` — tolerate "already exists").

3. **Epic issue** — write the issue body to a temp file (safer than `--body` with
   multi-paragraph text) and create it:

   ```bash
   gh issue create \
     --title "Epic <n>: <title>" \
     --body-file <tmpfile> \
     --milestone "Epic <n>: <title>" \
     --label epic
   ```

   The issue body should summarize the goal/scope/acceptance criteria and link back to
   `docs/epics/epic-<n>-<slug>/EPIC_<n>.md` (a relative link resolves fine on GitHub for
   files in the same repo). Capture the created issue's number from `gh issue create`'s
   output URL.

## Step 7: Write results back

For each epic, update its `EPIC_<n>.md` frontmatter: `status: open`, `gh_issue: <number>`,
`milestone: <number>`, plus the two OKF fields that only become known now —
`resource: https://github.com/<owner>/<repo>/issues/<number>` (the canonical asset this
concept represents) and a refreshed `timestamp`. Update the matching bullet in
`docs/epics/index.md` to link the issue and reflect the new status.

Append an entry per epic created to `docs/epics/log.md` — OKF's reserved log file,
flat, date-grouped, newest first — creating the file when this run established the
bundle:

```markdown
## 2026-07-05
* **Creation**: Established [Epic 1: User auth](/epic-1-user-auth/EPIC_1.md).
```

Creating it is this skill's job precisely because it founds the bundle: every later
skill in the pipeline only ever *appends* to a log that already exists, so a bundle
founded without one never gets a history at all — and the epics that started it would
be the one event nobody recorded.

Then commit and push the bundle per the commit rule in
`../_shared/bundle-interfaces.md`. It matters more here than anywhere: each epic
issue you just created links back to its `EPIC_<n>.md`, and those links 404 for
everyone until the push lands.

Report a final summary to the user: epics created, issue numbers/links, the commit
pushed, and a reminder that `create-issues` can now be run per epic to break each one
into PR-sized issues.

Then close the run per `../_shared/feedback-interfaces.md` — silently, unless this run
turned up something about this skill that clears both its filters.
