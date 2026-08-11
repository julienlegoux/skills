---
name: define-scope
description: First of the three planning skills (define-scope → define-specs → define-conventions) — decide what v1 ships into docs/planning/SCOPE.md through a decision ledger the user triages, taking CONCEPT.md as intake where define-concept produced one. Use when planning a new project, figuring out what v1 is, or resuming a scoping run with open decisions under docs/planning/scope/; if the idea itself is still forming, define-concept comes first.
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
(OKF v0.1) bundle, which this skill establishes unless `define-concept` already did. The rules
every pipeline skill obeys when writing to it — English content, bundle-relative
links, the reserved `index.md`/`log.md` files, and committing what you write — are
defined once in `../_shared/bundle-interfaces.md`; the decision doc schema is in
`../_shared/ledger-interfaces.md`. Read both before writing anything.

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
**restate the project premise** (see the premise gate in Step 1) for a quick
confirmation before continuing — a resume that silently inherits a wrong premise
compounds it across every remaining decision. Then jump to the step matching the
state: open decisions → Step 3 or 4; all decided but no `SCOPE.md` → Step 5. Never
re-ask a decision that already has a verdict.

## Step 1: Intake

Take whatever the user gives you — free-form text, a file they point at, a half-idea.
Before asking anything:

- Read the repo for context (README, existing code, existing `docs/`) — the project
  may already answer questions the user would otherwise be asked.
- Read `docs/planning/CONCEPT.md` and `DOMAIN.md` if they exist. `define-concept` wrote
  them, and everything in them is already validated: the problem, what the product is,
  its positioning, the domain vocabulary. Treat them as settled input, not as a draft to
  re-decide — a scope ledger that re-opens the concept spends the user's attention twice
  on the same question and can end up contradicting the document downstream skills read.
- Read `references/checklist.md` (the decision areas this skill guarantees coverage of).

Then, **only for checklist areas the input leaves genuinely blank**, ask orienting
questions — one at a time, waiting for each answer. These are quick fact-gathering
questions ("who is this for?", "is there a deadline?"), not decision-making; keep them
few and stop as soon as you can enumerate sensibly. Do not interrogate: if you can
draft a credible recommendation for an area without asking, don't ask — the triage
pass exists precisely so the user can correct you cheaply.

**End intake with the premise gate.** Before enumerating anything, state the project
premise in three lines — *what* is being built, *for whom*, and *relative to what*
(greenfield, a rewrite of X, a layer on top of Y) — and get the user's confirmation.
Every recommendation in the ledger silently assumes this framing; a premise
misunderstanding discovered mid-triage invalidates the entire ledger, which is the
most expensive rework this skill can produce.

**Then offer the project home.** Before anything is written to disk, propose a project
folder name derived from the confirmed premise (lowercase kebab-case, e.g.
`recipe-inbox`) and ask whether to create it as a **private** GitHub repo. On accept:

```bash
mkdir <name> && cd <name>
git init -b main
git commit --allow-empty -m "chore: initial commit"
gh repo create <name> --private --source=. --remote=origin --push
git checkout -b develop && git push -u origin develop
```

Run the rest of this skill from inside that folder and leave the user on `develop`, so
`docs/planning/` lands in the project rather than wherever the conversation started, on
the branch the pipeline actually integrates on.

Two defaults worth their why. **Private**: a repo is made public later with one command,
while anything pushed to a public one is already public — never create it public unless
the user says so. **`develop` branched off `main` up front**: `implement-epic` picks its
integration branch by looking for `develop` and falls back to the repo default, so
creating it now is what makes every later PR target one trunk instead of piling onto
`main`. Leave `main` as GitHub's default branch.

This is a one-line offer, not a ledger item: no decision doc, no checklist entry. Skip
it entirely if a git remote already exists — and also if `docs/planning/CONCEPT.md` sits
in a folder with no repo, which means `define-concept` already made this offer and the
user turned it down. If the user declines, drop it and never
raise it again. If `gh` is missing or unauthenticated, do the local half (folder,
`git init`, `develop`), say the remote was skipped, and continue — `split-epics` is what
needs the remote, and not until later.

## Step 2: Enumerate the decision ledger

Build the decision list from two sources:

1. **The checklist** (`references/checklist.md`) — instantiate every area that applies
   to this project. For areas that do not apply, still create a decision doc with
   `status: na` and a one-line reason: an explicit N/A is visible and reversible; a
   silent omission looks identical to a mistake.
2. **Project-specific decisions** — anything this particular project raises that no
   generic checklist anticipates. Add them as first-class decisions.

Number decisions in dependency order (a decision that constrains another comes first)
and record dependencies in `depends_on`. Write one file per decision at
`docs/planning/scope/<nn>-<slug>.md`, using the decision doc template in
`../_shared/ledger-interfaces.md` with `tags: [decision, scope]` and `phase: scope`.

Every `open` decision must have a real recommendation before Step 3 — "it depends" is
not a recommendation. Create `scope/index.md` (no frontmatter) listing every decision
with a **mechanical** line: `* [Title](<nn>-<slug>.md) - <status>`. No recommendation
prose in the index — recommendations live in the decision docs and change as verdicts
land; an index that repeats them needs an edit for every ripple and rots into
disorder. When many statuses change, rewrite the affected index section wholesale
rather than patching line by line.

## Step 3: Triage — the batch pass

The batch pass exactly as `../_shared/ledger-interfaces.md` defines it, over the
ledger Step 2 built, with `scope/index.md` as the index it keeps current. Its rule
that a self-excluded list gets its own confirmation lands here on the checklist areas
Step 2 marked N/A — those areas *are* this skill's coverage guarantee, and an N/A
waved through inside an "accept all" cancels it silently.

## Step 4: Deep-dive the flagged items

The deep-dive pass exactly as `../_shared/ledger-interfaces.md` defines it. Nothing
about it is scope-specific.

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
okf-docs skill's validator is available, run it against `docs/planning/`. Finally
commit and push the bundle per the commit rule in `../_shared/bundle-interfaces.md` —
this is the run's deliverable, and every skill downstream reads it from git.

## Handoff

Tell the user the natural next steps: `define-specs` (reads SCOPE.md, decides the
one-way technical doors) and, when planning is done, `split-epics` on
`docs/planning/SCOPE.md`.

## Revisiting a decision later

If the user reopens a decided item (any session), set it back to `status: open`, note
the reopening in the Verdict section (keep the old verdict visible as history), re-run
the refresh rule on its dependents, and — if `SCOPE.md` already exists — regenerate the
affected sections after the new verdict, with a `log.md` entry.
