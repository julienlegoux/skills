---
name: define-conventions
description: Third of the three planning skills (define-scope → define-specs → define-conventions) — instantiate the personal conventions baseline filtered by the stack in SPECS.md, decide only the deviations through a user-triaged ledger, and write docs/planning/CONVENTIONS.md. Use when defining repo standards after define-specs, or resuming open decisions under docs/planning/conventions/.
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

The bundle-wide rules — English content, link forms, reserved files, committing what
you write — are defined once in `../_shared/bundle-interfaces.md`, and the decision
doc schema in `../_shared/ledger-interfaces.md`. Read both before writing anything. A
third governs nothing this skill writes: `../_shared/feedback-interfaces.md`, the
closing reflex for what this run teaches about *this skill* — it decides the promotion
check in Step 4 and the end of the run.

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

Two boundaries on what may enter the ledger at all:

- **Never ledger PR/issue sizing or splitting rules.** Sizing is owned by
  `create-issues` and `split-epics` — a conventions doc that also states line-count
  targets creates a second source of truth that drifts from the skills that
  actually enforce it.
- **Stress-test every recommendation against SCOPE.md and SPECS.md before
  presenting it.** A deviation recommendation that contradicts a decided scope
  constraint or the decided stack wastes a triage round at best and plants a
  contradiction in the bundle at worst; if the tension is real, say so in the
  Question section and let the user arbitrate knowingly.

Decision docs use the template in `../_shared/ledger-interfaces.md`, written to
`docs/planning/conventions/<nn>-<slug>.md` with `tags: [decision, conventions]` and
`phase: conventions`, each with a concrete recommendation. Dependency order rarely
matters here; number by baseline section order. Create `conventions/index.md`.

## Step 3: Triage — the batch pass

The batch pass exactly as `../_shared/ledger-interfaces.md` defines it, over the
deviations ledger. What this phase puts ahead of the list: a one-line note that the
baseline applies by default, with the section titles that made it through the stack
filter — that is the contract's self-excluded list here, the standards this skill
settled without ever opening a decision doc, so what is *not* being asked about stays
visible. The user can pull any of those items into the ledger right there.

## Step 4: Deep-dive the flagged items

The deep-dive pass exactly as `../_shared/ledger-interfaces.md` defines it.

**Promotion check:** when a deviation's rationale is not project-specific ("actually I
always want it this way"), say so and suggest promoting it into `assets/baseline.md`,
so future projects inherit it instead of re-deciding. This stays a local category
because its destination is this skill's own asset rather than an issue; which route
carries the suggestion there is not restated here — `../_shared/feedback-interfaces.md`
decides between `improve-skill` and `send-feedback`. Note the suggestion in the
decision doc's Verdict section, and don't edit the baseline mid-run unless the user
says to.

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
`log.md`, validate if the okf-docs checker is available, then commit and push per
`../_shared/bundle-interfaces.md`.

## Handoff

Planning is complete: `split-epics` can now cut `docs/planning/SCOPE.md`, and it links
CONVENTIONS.md into each epic as context — which is how `implement-issue` and
`code-review`-style checks find the project's standards without this doc being copied
anywhere.

Then close the run per `../_shared/feedback-interfaces.md` — silently, unless this run
turned up something about this skill that clears both its filters. A baseline promotion
is the one category handled in-run, above.

## Revisiting later

Reopen: `status: open`, old verdict kept as history, CONVENTIONS.md regenerated after
the new verdict, `log.md` entry. If the baseline itself has changed since
`baseline_version`, surface the diff and ask whether this project adopts the updates.
