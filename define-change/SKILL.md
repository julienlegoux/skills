---
name: define-change
description: Brownfield planning for ONE feature or serious change to an existing app (the brownfield pipeline is map-codebase → define-change → create-issues → implement-epic). Turn a feature idea, change request, or rant into a decided change plan — grounded in an impact audit of the actual code, decided through a user-triaged decision ledger under docs/planning/changes/, and delivered as a docs/epics/epic-N-slug/EPIC_N.md (with GitHub milestone + tracking issue) that create-issues consumes unchanged. Use whenever the user wants to "add a feature to this app", "plan this change", "I want to build X into the existing app", "make a serious change", "plan a refactor" or "plan a migration", "turn this feature idea into an epic/issues", or continues after map-codebase. Also use to RESUME — if docs/planning/changes/ has a change with open decisions, pick up where it left off. Do NOT use for brand-new projects (that's define-scope) or trivial one-file fixes (just do those directly).
---

# Define Change

A change to an existing app is not a new project: the stack is decided, the
conventions exist, and most "options" are constrained by code that already runs. What
still needs deciding is *how the change lands* — extend or refactor, migrate or
version, flag or big-bang — and those are the user's calls, not yours. This skill
walks them through a decision ledger (same mechanics as `define-scope` — its four
principles apply throughout: facts looked up never asked, decisions the user's never
yours, triage is the dial, nothing finalized until confirmed) and delivers one
`docs/epics/epic-<N>-<slug>/EPIC_<N>.md`, format-identical to `split-epics` output,
so `create-issues` and `implement-epic` work downstream without knowing which
pipeline produced it.

One change = one epic. That's the contract; the size guard in Step 2 protects it.

## Output format: OKF

Both directories this skill touches are [Open Knowledge Format](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)
(OKF v0.1) bundles — and they are *separate* bundles, which matters for links:

- `docs/planning/` — established by the planning skills or `map-codebase`. This skill
  adds `changes/change-<N>-<slug>/` (Decision concept docs + a non-root `index.md`
  with no frontmatter). Links inside this bundle are bundle-relative with a leading
  `/` (e.g. `/changes/change-1-csv-export/03-migration.md`).
- `docs/epics/` — its own bundle root. If absent, establish it: `docs/epics/index.md`
  with `okf_version: "0.1"` as its only frontmatter, and `docs/epics/log.md`
  (`## YYYY-MM-DD` headings, newest first). (`split-epics` historically didn't
  create `log.md` here — a deliberate divergence; if the bundle already exists from
  either origin, append to what's there and create `log.md` only if missing.) Links from an epic file into
  `docs/planning/` cross bundles, so bundle-relative paths don't apply — use plain
  relative paths (`../../planning/SPECS.md`), exactly as `split-epics` does.

Layout this skill owns:

```
docs/planning/changes/
  change-<N>-<slug>/
    index.md          # decision listing = durable triage view (no frontmatter)
    01-<slug>.md      # one Decision concept doc per decision
docs/epics/
  epic-<N>-<slug>/
    EPIC_<N>.md       # the deliverable (written last)
```

The change number and the epic number are assigned independently: each is the next
free number in its own directory (`docs/planning/changes/change-*` and
`docs/epics/epic-*` respectively) — they will often differ, and that's fine; the
epic's frontmatter records the linkage.

## Step 0: Prerequisites and resume

**Resume first:** if any `docs/planning/changes/change-<N>-<slug>/` exists with open
decisions, this is a resume. Read its `index.md` and every decision doc, report the
tally (decided / open / n-a), and jump to the matching step: open decisions → Step 4
or 5; all decided but no EPIC file → Step 6; EPIC written but `gh_issue: null` (a
run where `gh` was skipped or failed) → Step 6.3 to finish only the GitHub objects.
Never re-ask a decided item. If several
changes are in flight, ask which one (or whether this is a new change).

**Prerequisites:** read `docs/planning/SPECS.md` and `docs/planning/CONVENTIONS.md`.

- **Missing (either):** stop and say so. Offer to run the `map-codebase` skill first
  — it reverse-engineers the codebase into exactly these two files. Do *not* inline a
  half-baked audit as a substitute: every recommendation below leans on these docs,
  and a wrong stack assumption poisons the whole ledger. If the user insists on
  proceeding without them, they can — but note it in the ledger docs so downstream
  readers know the ground truth was verbal.
- **Present but stale:** `map-codebase` stamps SPECS.md's frontmatter with a
  `mapped_commit` extension field. Compare it with `git rev-parse HEAD`; if they
  differ, report roughly how far the docs trail the code (`git rev-list --count
  <mapped_commit>..HEAD` commits) and offer a `map-codebase` refresh — but let the
  user proceed on the existing docs if they judge the drift irrelevant to this
  change. No `mapped_commit` field (greenfield-authored docs) → nothing to check.

## Step 1: Intake

Take whatever the user gives — a sentence, a spec fragment, a rant about what the app
can't do. Separate what's *decided* (things the user has clearly already chosen) from
what's *open*. Read SPECS.md, CONVENTIONS.md, and any docs the user points at before
asking anything. Only for genuine blanks that block the audit ("which of these two
apps in the monorepo?", "is there a deadline?") ask orienting fact-questions — one at
a time, few, and stop as soon as you can start the audit. If you can draft a credible
recommendation without asking, don't ask; triage is where the user corrects you
cheaply.

## Step 2: Impact audit — facts, not questions

This is the step `define-scope` doesn't have, and it's why brownfield planning gets
its own skill: before any decision is enumerated, read the *actual code* and
establish the blast radius. Never ask the user what the code does — that is always a
lookup. Establish:

- **Modules and files touched** — where the change lands, what it must modify versus
  merely call.
- **Contract breaks** — public APIs, CLI flags, exported types, events, file formats:
  what existing consumers would break, and who those consumers are.
- **Schema and data migrations** — tables/collections affected, whether existing rows
  need transforming, whether the migration is reversible.
- **Affected tests** — which suites cover the touched modules, which will break by
  design versus by accident.
- **Feature interactions** — existing behavior that overlaps, conflicts, or silently
  assumes the thing being changed.

Record the audit as facts inside the relevant decision docs' Question sections (the
audit is *why* each decision exists) — it doesn't need a standalone document.

**Size guard — apply it here, before the ledger exists.** If the audit reveals the
change is really multi-epic sized — several independently shippable chunks, weeks
each, spanning unrelated subsystems — say so plainly and recommend the
`define-scope` → `split-epics` route instead: that pipeline exists precisely to cut
big scopes into epics, and stretching one EPIC file to hold it would just push the
overload onto `create-issues`. Let the user either shrink the change to one-epic
size or switch pipelines. Don't proceed into the ledger with a change you believe is
oversized without flagging it.

## Step 3: Enumerate the decision ledger

Pick the change's slug (lowercase kebab-case, ASCII, ~40 chars) and number `<N>`
(next free under `docs/planning/changes/`). Build the decision list from the audit
plus the user's input. Typical categories — instantiate the ones this change raises,
skip the rest (unlike define-scope's checklist, there's no fixed coverage guarantee
to mark N/A against, though `status: na` with a one-line reason is still the right
move for a category you considered and ruled out):

1. **Approach** — extend the existing implementation, refactor first, or rewrite the
   affected part. Almost always first; most other recommendations hang off it.
2. **Data migration / backward compatibility** — transform existing data or leave it,
   support old formats/clients or cut them.
3. **Rollout strategy** — feature flag, big bang, phased by user segment.
4. **API/contract versioning** — version the endpoint, evolve in place, deprecation
   window for the breaks the audit found.
5. **Scope boundary** — which adjacent cleanups the audit surfaced are explicitly OUT
   (the brownfield equivalent of non-goals; without this, every change snowballs).
6. **Acceptance criteria** — what "done" observably means for this change.

Add project-specific decisions the audit raises that no list anticipates. Number in
dependency order, record `depends_on`. One file per decision,
`docs/planning/changes/change-<N>-<slug>/<nn>-<slug>.md`, using define-scope's exact
Decision template (Question / Options / Recommendation / Verdict sections; `status`,
`verdict`, `decided_via`, `depends_on` frontmatter) with these fields instead:
`tags: [decision, change]`, `phase: change`, plus extension fields `change: <N>` and
`change_slug: <slug>`. Ground every Question in audit facts (name the files, the
contracts, the row counts) and every Recommendation in SPECS.md/CONVENTIONS.md —
"it depends" is not a recommendation.

Create `change-<N>-<slug>/index.md` (no frontmatter) listing every decision:
`* [Title](<nn>-<slug>.md) - <status>: <recommendation or verdict, one line>`.

## Step 4: Triage — the batch pass

Same as define-scope's Step 3: present the full ledger as one numbered,
dependency-ordered list — each open decision with its one-line recommendation, then
any N/A items with reasons. The user marks each **accept** or **discuss**; batch
replies are the expected use ("accept all except 2"). Record accepts immediately
(`status: decided`, `verdict` = the recommendation, `decided_via: triage`, Verdict
section filled, timestamp refreshed, index updated).

## Step 5: Deep-dive the flagged items

Strictly in dependency order, one at a time, waiting for each answer: restate the
question with its audit facts, options with trade-offs, your recommendation, the
user decides (`decided_via: discussion`). **After every verdict, refresh the
still-open decisions** — dependents first, then anything the verdict plausibly
affects (choosing "rewrite" over "extend" routinely flips the migration and rollout
recommendations). If a recommendation changes, update the doc and tell the user what
changed and why before continuing.

## Step 6: Confirm, then write the epic

When nothing is `open`, summarize the decided set in a few lines and get the user's
explicit confirmation — this step also gates the GitHub writes below, so it does the
job of split-epics' preview step. Only then:

**1. Establish `docs/epics/` if absent** (bundle root `index.md` + `log.md`, per the
OKF section above). Pick the epic number `<N>` — next free across `docs/epics/`
regardless of which skill created the existing epics — and the epic slug (usually
the change slug).

**2. Write `docs/epics/epic-<N>-<slug>/EPIC_<N>.md`** — format-identical to
split-epics output so `create-issues` works unchanged:

```markdown
---
type: Epic
title: "<title>"
description: "<one-sentence summary of the change's goal>"
tags: [epic, change]
timestamp: <ISO 8601 — now>
epic: <N>
slug: <slug>
status: draft
gh_issue: null
milestone: null
source: docs/planning/changes/change-<N'>-<slug>/index.md
---

# Epic <N>: <title>

## Goal
## Scope
## Out of scope
## Acceptance criteria
## Dependencies
## Context
## Notes
```

Fill the body from the decided ledger only — settled fact, no option-weighing. Goal
from the intake + approach verdict; Scope from the approach/migration/rollout
verdicts, concrete enough that the audit's file-level findings survive (this file,
not the ledger, is what `create-issues` treats as the source of truth); Out of scope
straight from the scope-boundary verdict; Acceptance criteria from its decision;
Dependencies is usually "None" (link other epics OKF-style, bundle-relative, if this
change genuinely depends on one). `## Context` links the planning bundle with plain
relative paths — `[Technical specs](../../planning/SPECS.md)`,
`[Conventions](../../planning/CONVENTIONS.md)` — and the change ledger
(`../../planning/changes/change-<N'>-<slug>/index.md`) so implementers are one click
from every rationale. Notes carries surviving risks and audit findings worth
preserving. Don't add `resource` yet — it arrives with the GitHub issue.

**3. Create the GitHub milestone and tracking issue** exactly as split-epics does
(its Steps 6–7). In short: get `owner/repo` (`gh repo view --json nameWithOwner -q
.nameWithOwner`); find-or-create a milestone titled `Epic <N>: <title>` (split-epics
bundles `scripts/ensure_milestone.sh` for this — use it if that skill is installed,
otherwise find via `gh api repos/<owner>/<repo>/milestones` and create only if
missing); reuse the repo's existing epic label or create a plain `epic` one; create
the issue with `gh issue create --title "Epic <N>: <title>" --body-file <tmpfile>
--milestone "Epic <N>: <title>" --label epic`, the body summarizing
goal/scope/acceptance criteria and linking `docs/epics/epic-<N>-<slug>/EPIC_<N>.md`.
Then write back to the EPIC frontmatter: `status: open`, `gh_issue: <number>`,
`milestone: <milestone number>`,
`resource: https://github.com/<owner>/<repo>/issues/<number>`, refreshed timestamp.

**No remote, or `gh` fails?** Degrade gracefully: keep the local files, leave
`gh_issue`/`milestone` as `null` and `status: draft`, and tell the user exactly what
was skipped and how to finish later (fix `gh auth` / add a remote, then re-run —
Step 0's resume path lands back here, and `create-issues` refuses politely until
`gh_issue` is set).

**4. Update both bundles:** add the epic's bullet to `docs/epics/index.md` (tracking
its `description` + `status`); append a `docs/epics/log.md` entry; update
`docs/planning/` root `index.md` to list the change ledger and append a
`docs/planning/log.md` entry. If the okf-docs validator is available, run it against
both bundles.

**Idempotency:** if the EPIC file already exists with `gh_issue` set, don't recreate
either it or its GitHub state — report and stop. If the ledger changed since the
epic was written (a reopened decision), regenerate the affected body sections, never
touch `gh_issue`/`milestone`, and log the update.

## Handoff

Tell the user the next step: `create-issues` on this epic to break it into PR-sized
issues, then `implement-epic` to run them. The change ledger stays put — it's the
durable rationale behind every line of the EPIC file.

## Revisiting a decision later

Same as define-scope: reopen with `status: open`, keep the old verdict visible as
history in the Verdict section, refresh dependents, and — if the EPIC file exists —
regenerate its affected sections after the new verdict, with log entries in both
bundles. If implementation already started (`issues/` exists under the epic), point
out which issues the reversal touches before regenerating anything.
