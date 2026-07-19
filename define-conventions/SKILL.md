---
name: define-conventions
description: Third of the three planning skills (define-scope → define-specs → define-conventions). Instantiate the user's personal conventions baseline for a project — filtered by the stack in docs/planning/SPECS.md — and decide only the DEVIATIONS through a user-triaged decision ledger, writing docs/planning/CONVENTIONS.md. Use whenever the user wants to "define conventions", "set up coding standards", "make the conventions doc", "establish repo standards", or continue planning after define-specs. Also use to RESUME if docs/planning/conventions/ has open decisions.
---

# Define Conventions

Conventions are repo standards: how code is written, named, tested, committed, and
reviewed. Unlike scope and specs, most of this is *not* freshly decided per project —
it's a personal baseline that follows the user across projects. So this skill inverts
the enumeration: the baseline applies by default, and the decision ledger contains
only **deviations** — places this project should differ, and gaps the baseline doesn't
cover. On a typical project that's a handful of decisions, not thirty.

The baseline lives in this skill's own `assets/baseline.md`. It is the user's, refined
over time — improving it is a normal improve-skill loop on this skill.

## Principles (same DNA as define-scope / define-specs)

1. **Facts are looked up, never asked** — read SPECS.md, the repo, and the baseline
   before asking anything.
2. **Decisions are the user's, never yours** — recommendations on everything, verdicts
   from the user.
3. **Triage is the dial** — batch triage; one-at-a-time only for deep-dives.
4. **Nothing is finalized until the user confirms.**

## Step 0: Predecessor and resume checks

**Soft chain:** read `docs/planning/SPECS.md` — the stack decided there determines
which baseline sections even apply. If it's missing or has open decisions, say so and
ask whether to run `define-specs` first or proceed on what the user tells you —
offer, don't refuse.

**Resume:** if `docs/planning/conventions/` exists, read its index and decision docs,
report the tally, jump to the matching step. Never re-ask a decided item.

## Output format: OKF

Same `docs/planning/` bundle (OKF v0.1). This skill owns:

```
docs/planning/
  CONVENTIONS.md        # the deliverable
  conventions/
    index.md            # decision listing (no frontmatter — non-root index)
    01-<slug>.md        # Decision docs — deviations and gaps only
```

Establish the bundle root (index.md + log.md) only if running before the other
planning skills ever did.

## Step 1: Instantiate the baseline

Read `assets/baseline.md`. Filter it by the stack in SPECS.md: keep the general
sections, keep the per-stack variants that match, drop the rest. This filtered
baseline is the default outcome — it is what CONVENTIONS.md will say wherever no
deviation is decided.

## Step 2: Enumerate the deviations ledger

The ledger contains only:

1. **Gaps** — things this project needs a standard for that the filtered baseline
   doesn't cover (a new language, an unusual artifact type, a monorepo split).
2. **Proposed deviations** — places where you judge this project should differ from
   the baseline, with the reason (e.g. a solo throwaway doesn't need PR review
   ceremony; a library needs stricter API-doc rules than the app-focused baseline).
3. **User-flagged items** — anything the user already said they want different.

Do **not** re-open baseline items just to confirm them — that would rebuild the
thirty-question interrogation this design exists to kill. If the baseline covers it
and nothing about this project argues otherwise, it's settled by default.

Decision docs use the shared template, `docs/planning/conventions/<nn>-<slug>.md`
(`tags: [decision, conventions]`, `phase: conventions`, same status fields as the
other planning skills), each with a concrete recommendation. Dependency order rarely
matters here; number by baseline section order. Create `conventions/index.md`.

## Step 3: Triage — the batch pass

Show the user:

- A one-line note that the baseline applies by default, with the list of section
  titles that made it through the stack filter (so what's *not* being asked about is
  visible, same spirit as N/A marks elsewhere).
- The numbered deviations ledger, each with a one-line recommendation.

The user marks each **accept** or **discuss**; batch replies expected. They can also
pull any baseline item into the ledger at this point. Record accepts immediately
(`decided_via: triage`).

## Step 4: Deep-dive the flagged items

One at a time, waiting for each answer: question, options, trade-offs,
recommendation, user's verdict (`decided_via: discussion`). Refresh any still-open
items a verdict affects.

**Promotion check:** when a deviation's rationale is not project-specific ("actually I
always want it this way"), say so and suggest promoting it into `assets/baseline.md`
via the improve-skill loop, so future projects inherit it instead of re-deciding.
Note the suggestion in the decision doc's Verdict section; don't edit the baseline
mid-run unless the user says to.

## Step 5: Confirm, then write the deliverable

Summarize (baseline + decided deviations) and get confirmation. Then write
`docs/planning/CONVENTIONS.md`: the filtered baseline with deviations merged in-place
— a reader sees one coherent standard, not a base-plus-patches puzzle. Mark deviated
points with a link to their decision doc (e.g. `([decision](/conventions/02-no-pr-review.md))`).

```markdown
---
type: Conventions
title: "<project> — Conventions"
description: "<one line: baseline + N project deviations>"
tags: [planning, conventions]
timestamp: <ISO 8601 — now>
status: final
baseline_version: <the baseline.md timestamp or a short hash of it>
---
```

Body sections follow the baseline's own structure. Update root `index.md`, append to
`log.md`, validate if the okf-docs checker is available.

## Handoff

Planning is complete: `split-epics` can now cut `docs/planning/SCOPE.md`, and it links
CONVENTIONS.md into each epic as context — which is how `implement-issue` and
`code-review`-style checks find the project's standards without this doc being copied
anywhere.

## Revisiting later

Reopen: `status: open`, old verdict kept as history, CONVENTIONS.md regenerated after
the new verdict, `log.md` entry. If the baseline itself has changed since
`baseline_version`, surface the diff and ask whether this project adopts the updates.
