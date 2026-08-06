---
name: define-specs
description: Second of the three planning skills (define-scope → define-specs → define-conventions) — decide a project's one-way technical doors (stack, architecture, data model, auth, deployment) through a user-triaged decision ledger, writing docs/planning/SPECS.md. Use when deciding the stack or architecture after define-scope, or resuming open decisions under docs/planning/specs/.
---

# Define Specs

Specs are the "how" of a project at the level that's expensive to change later: the
one-way doors. Everything cheap to reverse (file layout, internal naming, refactors)
is deliberately *not* a spec decision — it gets decided during implementation. This
skill produces `docs/planning/SPECS.md` by walking a decision ledger the *user*
controls, using the same mechanic as `define-scope`.

## Principles (same DNA as define-scope — non-negotiable)

1. **Facts are looked up, never asked** — read SCOPE.md, the repo, and docs before
   asking anything.
2. **Decisions are the user's, never yours** — every decision carries your
   recommendation before the user sees it; the verdict is theirs.
3. **Triage is the dial** — batch triage for control, one-at-a-time only for intake
   gaps and flagged deep-dives.
4. **Nothing is finalized until the user confirms.**

## Step 0: Predecessor and resume checks

**Soft chain:** read `docs/planning/SCOPE.md`. If it's missing (or has open scope
decisions in `docs/planning/scope/`), say so and ask whether to run `define-scope`
first or proceed anyway from what the user tells you verbally — offer, don't refuse.
Scope verdicts (constraints, delivery form, milestones) are inputs that shape nearly
every recommendation below; note in each decision doc which scope decisions it leans on.

**Resume:** if `docs/planning/specs/` exists, read `specs/index.md` and every decision
doc, report the tally (decided / open / n-a), and jump to the matching step. Never
re-ask a decided item.

## Output format: OKF

Same bundle as define-scope — `docs/planning/` (OKF v0.1). This skill owns:

```
docs/planning/
  SPECS.md            # the deliverable (written last)
  specs/
    index.md          # decision listing (no frontmatter — non-root index)
    01-<slug>.md      # one Decision concept doc per decision
```

If the bundle doesn't exist yet (specs running first — allowed by the soft chain),
establish it as define-scope would: root `index.md` with `okf_version: "0.1"` only,
root `log.md`.

The bundle-wide rules — English content, link forms, reserved files, committing what
you write — are defined once in `references/bundle-interfaces.md`, and the decision
doc schema in `references/ledger-interfaces.md`. Read both before writing anything.

## Step 1: Intake

Read `references/checklist.md`. Between SCOPE.md, the repo, and the user's input, most
areas should already be enumerable. Only for areas left genuinely blank, ask orienting
fact-questions — one at a time, few, and stop as soon as you can enumerate. If you can
draft a credible recommendation without asking, don't ask; triage is where the user
corrects you cheaply.

## Step 2: Enumerate the decision ledger

Instantiate every applicable checklist area; give non-applicable areas an explicit
`status: na` doc with a one-line reason; add project-specific decisions the checklist
doesn't anticipate. Number in dependency order (language/runtime almost always first —
most other recommendations hang off it) and record `depends_on`.

One file per decision at `docs/planning/specs/<nn>-<slug>.md`, using the decision doc
template in `references/ledger-interfaces.md` with `tags: [decision, specs]` and
`phase: specs`.

Recommendations here deserve real research: check what the repo already uses, and look
up current library/framework facts rather than recommending from memory — a stale
recommendation wastes the user's triage glance. Every `open` decision has a concrete
recommendation before triage; "it depends" is not one. Create `specs/index.md` listing
every decision with status and one-line recommendation/verdict.

## Step 3: Triage — the batch pass

One numbered list, dependency-ordered: each open decision with its one-line
recommendation, then the N/A items with reasons. The user marks each **accept** or
**discuss** — batch replies expected ("accept all except 4 and 9"). Record accepts
immediately: `status: decided`, `verdict` = recommendation, `decided_via: triage`,
Verdict section filled, index updated.

## Step 4: Deep-dive the flagged items

Strictly in dependency order, one at a time, waiting for each answer: question,
options with trade-offs, recommendation, user decides (`decided_via: discussion`).

**After every verdict, refresh the still-open decisions** — dependents first, then
anything the verdict plausibly affects. If a recommendation changes (choosing a
different runtime routinely flips hosting, testing, and job-queue recommendations),
update the doc and tell the user what changed and why before continuing.

## Step 5: Confirm, then write the deliverable

When nothing is `open`, summarize the decided set and get the user's confirmation.
Then write `docs/planning/SPECS.md` from decided entries only:

```markdown
---
type: Technical Specification
title: "<project> — Technical Specs"
description: "<one-line: the stack and shape of the system>"
tags: [planning, specs]
timestamp: <ISO 8601 — now>
status: final
---

# <Project> — Technical Specs

## Stack
## Architecture
## Data model & storage
## Auth
## Interfaces & integrations
## Deployment & operations
## Testing infrastructure
## Cross-cutting concerns
<error handling, observability, security, config — as decided>
```

Shape the sections to the decisions actually made — don't force empty headings. State
each decision as settled fact and link its decision doc OKF-style
(e.g. `([decision](/specs/02-storage.md))`) instead of restating the rationale.
Update root `index.md`, append to `log.md`, validate if the okf-docs checker is
available, then commit and push per `references/bundle-interfaces.md`.

## Handoff

Next: `define-conventions` (reads SPECS.md to filter its baseline by stack). When
planning is done, `split-epics` cuts `docs/planning/SCOPE.md` and links SPECS.md into
each epic as context — anything decided here reaches implementers through that link,
so it doesn't need copying into epics.

## Revisiting a decision later

Reopen: `status: open`, old verdict kept visible as history in the Verdict section,
dependents refreshed, affected SPECS.md sections regenerated after the new verdict,
`log.md` entry. Spec reversals are exactly the expensive kind — if the user reopens
one after implementation started, point out which epics/issues it touches.
