---
name: pathfinder
description: >-
  Turn a feature or project request into a docs/PLAN.md ready for the
  split-epics skill, through an unhurried, gated planning conversation that
  restates what was understood before designing anything — and bootstrap the
  repo's OKF docs bundle around it if none exists. Use this whenever the user
  wants to plan something new — "let's plan X", "I want to add/build Y", "help
  me think through Z", "we need a plan for this" — and no docs/PLAN.md covers
  the request yet, even if they never say the word "plan". This is the stage
  before split-epics in the pipeline: it produces the plan that split-epics
  splits. Do NOT use for bug fixes or small tweaks that need no plan, and do
  not re-plan a repo whose docs/PLAN.md already covers the request — offer to
  revise it instead.
---

# Pathfinder

A request has arrived — a feature, a project, a change big enough to deserve a
plan. This skill turns it into `docs/PLAN.md` through a conversation, and it is
the entry point of the pipeline:

> request → **pathfinder** → `docs/PLAN.md` → `split-epics` → `create-issues` → `implement-issue`

The one thing to internalize before starting: **the job is not to produce a
plan — it is to produce the *right* plan.** Writing the document is the cheap
part. The expensive part is a misunderstanding that survives planning and
resurfaces three epics later, fossilized in code. So this skill is deliberately
in no hurry to write: it earns the right to plan by first proving it understood.
That said, unhurried is not slow-by-obligation — when the user hands over the
blanks, move fast and fill them (see "Filling the blanks").

Read this whole file before starting. The gates are not optional.

## Ground rules

- **Understanding before design.** Never respond to the initial request with a
  plan, an outline, or "got it". The first substantial thing the user reads
  from you is your restatement of what they meant (see next section).
- **The human answers, never you.** When a question needs the user's answer,
  do not fill it in on their behalf — however obvious the answer feels. The
  only exception is a blank the user has explicitly handed over.
- **One question at a time.** A wall of questions gets shallow answers to all
  of them. Ask, wait, listen, then shape the next question from the answer.
- **Concrete over abstract.** "Should deleted notes go to a trash for 30 days
  or vanish immediately?" beats "what are your data-retention requirements?".
  Offer options with trade-offs when you can see them.
- **Reflect decisions back.** Before recording any decision, restate it in one
  or two lines and let the user correct it. The confirmed restatement is what
  gets written, not your first interpretation.
- **Honest incompleteness.** A plan that pretends completeness is worse than
  one that names its open questions. What can't be answered sharply yet goes
  in "Not yet specified" — visibly, not silently omitted.
- **Out of scope carries its why.** Things consciously ruled out are recorded
  with the reason, so they don't creep back in downstream — and so a future
  reader knows it was a decision, not an oversight.
- **Fluid path, controlled output.** The conversation can take any shape the
  request needs; the files written at the end always have the same shape (see
  "Output").

## The understanding restatement

Here is the failure this exists to prevent: the user means concept A, you
understand concept B, you say "got it" — and both A and B are consistent with
"got it", so the mismatch carries zero signal. B then quietly steers every
design decision and reappears late in implementation, expensive to unwind.

The fix: restate the request **in your own words — different words than the
user used**. A restatement of B produces sentences that a person who meant A
immediately recognizes as wrong, at the moment it costs one sentence to fix.
Paraphrase is the point; echoing the user's own phrasing back defeats it.

Format, as the first substantial message of a planning session:

- **What I understood** — the request re-expressed in your words: what problem
  it solves, for whom, what "done" looks like. Plain language. If you must
  introduce a term of your own, define it in the same breath — a codename the
  user doesn't share is itself an A/B mismatch in the making.
- **What I'm unsure about** — the interpretations you had to choose between,
  stated as questions. Don't bury your uncertainty inside confident prose.

Then wait. The user's corrections are the most valuable text in the whole
session — record them (they go in the understanding doc's "Corrections along
the way"; see Output), because each one is a divergence that would otherwise
have shipped.

Restating is not only an opening move. Whenever a concept shifts mid-session —
the user introduces a new idea, or an answer reveals your model was off —
restate the changed part before building on it.

## The gates

The session advances through four gates, in order. A gate opens only on the
user's explicit sign-off — never on your own judgment that things seem clear,
and never because the conversation feels "ready". If the user goes quiet at a
gate, the session pauses there; it does not coast through.

1. **Understanding.** Deliver the understanding restatement; iterate until the
   user confirms it. Interview lightly before it only if the request is too
   thin to restate at all.
2. **Scope.** Interview breadth-first across the whole space: goals, what's
   in, what's consciously out (and why), what can't be specified yet. Resist
   tunneling into any single topic — depth comes per-decision, later. Close
   the gate by reflecting the scope back as a short list and getting a yes.
3. **Draft.** Show the plan in conversation before writing any file: the
   epic-shaped chunks (or the flat shape, for small work), the level of detail
   chosen and why, the open questions that will remain in the plan, the
   companion notes you intend to write. Adjust and re-show until confirmed.
4. **Write.** Only now touch the filesystem (see "Output"). Then report.

**Skipping gates is the user's move, not yours.** "Just write it", "fill the
blanks", "I trust you, go" collapses the remaining gates into autonomous mode —
but even then, gate 1 is never skipped silently: if the user demands speed
before you've restated, restate *briefly* inside the same message and proceed.
A one-paragraph restatement costs seconds; a wrong plan costs the pipeline.

## Filling the blanks

When the user hands over blanks — globally ("fill in the rest") or scoped
("your call on the storage layer") — switch from asking to deciding, for
exactly the territory handed over:

- Make the reasonable, boring choice; prefer the option that is easiest to
  reverse later.
- **Record every autonomous decision as an assumption**, in the understanding
  doc's "Assumptions made on the user's behalf" section — one line each, with
  the why. The user must be able to scan, in one place, everything decided
  without them.
- Questions outside the handed-over territory still belong to the human. "Fill
  in the rest of the plan" does not license inventing the product's purpose.

## Scaling the level of detail

The plan's depth follows the request, not a fixed template:

- **A feature** gets a lean plan — possibly a single epic, a page or two. Do
  not inflate it with ceremony; a small plan that ships beats a thorough one
  that exhausts the user before building starts.
- **A project** gets a deep plan — multiple epics, dependencies between them,
  more companion notes.

Whatever the depth, the floor is fixed by the pipeline: **each epic-shaped
chunk must be self-sufficient.** `split-epics` will carve it out into its own
file, and `create-issues` will work from that file without re-reading the
plan. So every epic section carries its own goal, scope, and acceptance
criteria where known — never "see above".

Structure the work sections as `## Epic <n>: <title>` headings when the work
naturally splits (this is the boundary signal `split-epics` detects most
reliably). If the whole request is genuinely one epic, one `## Epic 1: ...`
section is fine — don't manufacture a split.

## Output: the plan in an OKF bundle

Everything written lands in the repo's `docs/` [Open Knowledge Format](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)
(OKF v0.1) bundle. This skill runs first in the pipeline, so it is the one
that **bootstraps the bundle** when none exists:

- **`docs/index.md` missing or lacking `okf_version`** → create/complete it:
  frontmatter is exactly `okf_version: "0.1"` (nothing else), body is a link
  list of the bundle's concept files. If `docs/` has pre-existing markdown,
  list it too — join the docs, don't bulldoze them.
- **`docs/` is already a bundle** → add this session's files to the existing
  `index.md` listing, matching its style. Never add `okf_version` anywhere
  but the bundle root.
- **`log.md`**: if the bundle has one (OKF's optional reserved log — flat,
  date-grouped, newest first), append an entry for the plan's creation. If
  there is no `log.md`, don't create one — same policy as the rest of the
  pipeline.

The OKF rules that matter: every concept file needs YAML frontmatter with a
non-empty `type`; OKF's recommended fields (`title`, `description`, `tags`,
`timestamp`) come first and this skill's tracking fields ride alongside as
extension fields; cross-links between concept files use bundle-relative
absolute paths (leading `/`, relative to `docs/`).

**No GitHub.** Planning is entirely local. The pipeline's GitHub state begins
at `split-epics`.

### Files written

```
docs/
├── index.md                    # bundle root — created if missing
├── PLAN.md                     # the plan (split-epics finds it by this name)
└── notes/
    ├── understanding.md        # the confirmed understanding
    └── <slug>.md               # companion notes, as needed
```

### `docs/PLAN.md`

```markdown
---
type: Plan
title: "<title>"
description: "<one-sentence gist of the goal>"
tags: [plan]
timestamp: <ISO 8601, set to now>
status: ready
understanding: /notes/understanding.md
---

# Plan: <title>

## Goal

<why this exists, what it unlocks — grounded in the confirmed understanding>

## Understanding

<two- or three-line gist of what was confirmed, then:>
Full detail: [Understanding](/notes/understanding.md).

## Approach

<the shape of the solution and the key decisions, with links to any
companion notes holding their detail>

## Epic 1: <title>

<goal of this epic — self-sufficient, no "see above">

### Scope
### Out of scope        <- only if this epic has its own exclusions
### Acceptance criteria
### Dependencies        <- other epics this needs, or "None"

## Epic 2: <title>
...

## Out of scope

<project-wide exclusions, each with its why>

## Not yet specified

<open questions the plan honestly carries — sharp enough to name, not yet
answerable. Empty section omitted, not faked.>
```

### `docs/notes/understanding.md`

```markdown
---
type: Understanding
title: "Understanding: <request title>"
description: "What was understood and confirmed before planning <x>"
tags: [plan, understanding]
timestamp: <ISO 8601, set to now>
plan: /PLAN.md
---

# Understanding: <request title>

## What was asked

<the request as it arrived — a faithful gist of the user's words>

## What it means

<the confirmed restatement — the version that survived the user's
corrections. This, not the raw request, is what downstream work builds on.>

## Corrections along the way

<one line per A→B fix the user made during the session: what you first
understood, what they actually meant. These are the misunderstandings that
would have shipped — keep them; they teach the next session this user's
vocabulary.>

## Assumptions made on the user's behalf

<one line per blank filled autonomously, with the why. "None" if the user
answered everything.>
```

### Companion notes

When a decision, comparison, or piece of research is too big to inline in the
plan without bloating it, write it as its own concept file under
`docs/notes/<slug>.md` (`type` by nature — `Decision`, `Research`, `Guide`),
link it from the plan where the decision surfaces, and list it in `index.md`.
The plan stays a map; the notes hold the terrain. Don't manufacture notes for
small plans — a feature plan often needs none.

## If a plan already exists

Never clobber `docs/PLAN.md` silently. If one exists, read it first:

- **It covers the same request** → offer to revise it. Revision still passes
  the gates — restate your understanding of what should *change*, confirm,
  then edit. Refresh `timestamp`; append to `log.md` if it exists.
- **It's a different, still-live effort** → say so and ask how to proceed; a
  second concurrent plan is a decision for the user, not the skill.
- **It's stale** (already split into epics, or abandoned) → point that out and
  ask before replacing.

## Final report

Close the session by telling the user: the files written (with paths), the
open questions the plan still carries, any assumptions made on their behalf
(gist them here even though they're in the understanding doc — don't make the
user open a file to learn what was decided for them), and that the pipeline
continues with `split-epics` on `docs/PLAN.md`.
