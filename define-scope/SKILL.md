---
name: define-scope
description: First of the three planning skills (define-scope → define-specs → define-conventions). Turn a raw project idea — a sentence, a brain-dump, a rant — into a decided, documented scope (docs/planning/SCOPE.md) through a decision ledger the user triages, so the user owns every decision without being interrogated about details. Use whenever the user wants to start planning a project, "define the scope", "scope out this idea", "start a new project plan", "figure out what v1 is", or brings a project idea and asks where to start. Also use to RESUME scoping — if docs/planning/scope/ exists with open decisions, this skill picks up where it left off.
---

# Define Scope

Scope is the "what and why" of a project: the problem, the users, what v1 includes,
what it explicitly does not, and how the work phases into milestones. This skill
produces `docs/planning/SCOPE.md` — the document `split-epics` later cuts into epics —
by walking a decision ledger that the *user* controls.

## Principles (apply throughout — they are the point of this skill)

1. **Facts are looked up, never asked.** If something can be answered by reading the
   repo, the user's input, or existing docs, find it yourself. Only genuine *choices*
   reach the user.
2. **Decisions are the user's, never yours.** You recommend; you never silently decide.
   Every decision carries your recommendation *before* the user sees it, but the verdict
   is theirs — even if their verdict is just "accept your recommendation".
3. **Triage is the dial.** The user controls depth per-decision at triage time, not by
   answering everything one-by-one. One-at-a-time questioning is reserved for intake
   gaps and deep-dives of items the user flagged.
4. **Nothing is finalized until the user confirms.** The deliverable is only written
   from the decided set after explicit confirmation.

## Output format: OKF

`docs/planning/` is an [Open Knowledge Format](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)
(OKF v0.1) bundle. This skill establishes it if absent:

- Bundle root `docs/planning/index.md` (only file allowed `okf_version: "0.1"`
  frontmatter, nothing else; non-root index files get no frontmatter at all).
- Bundle root `docs/planning/log.md` (`## YYYY-MM-DD` headings, newest first).
- Every other `.md` is a concept file: YAML frontmatter with a non-empty `type`.
- Cross-links inside the bundle are bundle-relative with a leading `/`
  (e.g. `[target users](/scope/01-target-users.md)`).

Layout this skill owns:

```
docs/planning/
  index.md            # bundle root listing
  log.md              # bundle history
  SCOPE.md            # the deliverable (written last)
  scope/
    index.md          # decision listing = durable triage view
    01-<slug>.md      # one concept doc per decision
    02-<slug>.md
```

## Step 0: Resume check

If `docs/planning/scope/` already exists, this is a resume, not a fresh start. Read
`scope/index.md` and every decision doc, report the tally (decided / open / n-a), and
jump to the step matching the state: open decisions → Step 3 or 4; all decided but no
`SCOPE.md` → Step 5. Never re-ask a decision that already has a verdict.

## Step 1: Intake

Take whatever the user gives you — free-form text, a file they point at, a half-idea.
Before asking anything:

- Read the repo for context (README, existing code, existing `docs/`) — the project
  may already answer questions the user would otherwise be asked.
- Read `references/checklist.md` (the decision areas this skill guarantees coverage of).

Then, **only for checklist areas the input leaves genuinely blank**, ask orienting
questions — one at a time, waiting for each answer. These are quick fact-gathering
questions ("who is this for?", "is there a deadline?"), not decision-making; keep them
few and stop as soon as you can enumerate sensibly. Do not interrogate: if you can
draft a credible recommendation for an area without asking, don't ask — the triage
pass exists precisely so the user can correct you cheaply.

## Step 2: Enumerate the decision ledger

Build the decision list from two sources:

1. **The checklist** (`references/checklist.md`) — instantiate every area that applies
   to this project. For areas that do not apply, still create a decision doc with
   `status: na` and a one-line reason: an explicit N/A is visible and reversible; a
   silent omission looks identical to a mistake.
2. **Project-specific decisions** — anything this particular project raises that no
   generic checklist anticipates. Add them as first-class decisions.

Number decisions in dependency order (a decision that constrains another comes first)
and record dependencies in `depends_on`. Write one file per decision,
`docs/planning/scope/<nn>-<slug>.md`:

```markdown
---
type: Decision
title: "<short name>"
description: "<the question, one line>"
tags: [decision, scope]
timestamp: <ISO 8601 — now>
phase: scope
decision: <nn>
slug: <slug>
status: open        # open | decided | na
verdict: null       # the chosen option, once decided
decided_via: null   # triage | discussion | na
depends_on: []      # slugs of decisions this one depends on
---

# Question
<what is being decided, and why it matters for this project>

# Options
<2–4 realistic options, one-line trade-off each>

# Recommendation
<your recommended option and a short why — written now, before triage>

# Verdict
<empty until decided: chosen option, rationale, anything the user added>
```

Every `open` decision must have a real recommendation before Step 3 — "it depends" is
not a recommendation. Create `scope/index.md` (no frontmatter) listing every decision:
`* [Title](<nn>-<slug>.md) - <status>: <recommendation or verdict, one line>`.

## Step 3: Triage — the batch pass

Present the full ledger to the user as one numbered list, dependency-ordered:

- Each open decision: number, title, **recommendation in one line**.
- Then the N/A items with their one-line reasons, so exclusions are visible too.

Ask the user to mark each item **accept** (recommendation becomes the verdict) or
**discuss** (gets a deep-dive in Step 4). Batch replies are the expected use:
"accept all", "accept all except 3 and 7", "discuss 2, 5; accept the rest" are all
fine. So is reclassifying an N/A back to open.

Record the accepts immediately: `status: decided`, `verdict` = the recommended option,
`decided_via: triage`, fill the Verdict section, refresh `timestamp`, update
`scope/index.md`.

## Step 4: Deep-dive the flagged items

Walk the *discuss* items strictly in dependency order, **one at a time, waiting for
each answer**. For each: restate the question, present the options with trade-offs,
give your recommendation, and let the user decide. Record the verdict
(`decided_via: discussion`) with the user's rationale.

**After every verdict, refresh the still-open decisions.** Re-check each open decision
whose `depends_on` includes the one just decided (and any others the verdict plausibly
affects): if its recommendation changes, update the doc and *tell the user what changed
and why* before moving to the next item. A recommendation made before an upstream
verdict is stale the moment that verdict lands.

## Step 5: Confirm, then write the deliverable

When no `open` decisions remain, summarize the decided set in a few lines and ask the
user to confirm. Only after confirmation, write `docs/planning/SCOPE.md` from the
decided entries — decided content only, no open questions, no option-weighing:

```markdown
---
type: Scope
title: "<project> — Scope"
description: "<one-line project summary>"
tags: [planning, scope]
timestamp: <ISO 8601 — now>
status: final
---

# <Project> — Scope

## Problem
## Users
## Goals & success criteria
## Non-goals (out of scope for v1)
## Constraints

## Milestone 1: <name>
<features / outcomes in this milestone>

## Milestone 2: <name>
...

## Risks & assumptions
```

The `## Milestone N:` headings are load-bearing: `split-epics` detects epic boundaries
from exactly this structure. One milestone ≈ one epic — independently shippable,
weeks not an afternoon. Where a section states something decided in the ledger, link
the decision doc OKF-style (e.g. `([decision](/scope/03-mvp-cut.md))`) so the
rationale stays one click away without being copied in.

Then update the bundle: root `index.md` lists `SCOPE.md` and the `scope/` listing;
append a `log.md` entry (`* **Creation**: ...` or `* **Update**: ...`). If the
okf-docs skill's validator is available, run it against `docs/planning/`.

## Handoff

Tell the user the natural next steps: `define-specs` (reads SCOPE.md, decides the
one-way technical doors) and, when planning is done, `split-epics` on
`docs/planning/SCOPE.md`.

## Revisiting a decision later

If the user reopens a decided item (any session), set it back to `status: open`, note
the reopening in the Verdict section (keep the old verdict visible as history), re-run
the refresh rule on its dependents, and — if `SCOPE.md` already exists — regenerate the
affected sections after the new verdict, with a `log.md` entry.
