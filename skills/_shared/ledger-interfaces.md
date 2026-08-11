# Ledger interfaces

Single source of truth for the decision ledger: the decision doc every ledger-driven
skill writes (`define-scope`, `define-specs`, `define-conventions`, `define-change`,
`map-codebase`), and the two passes they all run over it — a batch triage, then a
deep-dive on whatever the user flagged. The bundle-wide rules those same skills obey
(language, links, reserved files, committing) live in `bundle-interfaces.md`.

This is the one and only copy: the skills above read it at
`../_shared/ledger-interfaces.md`. Editing it changes behaviour for all of them at once.

## Decision doc

One file per decision under the phase's folder
(`docs/planning/<phase-dir>/<nn>-<slug>.md`), numbered in dependency order.

```markdown
---
type: Decision
title: "<short name>"
description: "<the question, one line>"
tags: [decision, <phase>]
timestamp: <ISO 8601 — now>
phase: <scope|specs|conventions|change|mapping>
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

`define-change` adds extension fields `change: <N>` and `change_slug: <slug>`.
Every `open` decision carries a real recommendation before triage — "it depends"
is not a recommendation. The phase's `index.md` (non-root — no frontmatter) lists
each decision mechanically: `* [Title](<nn>-<slug>.md) - <status>`.

## Triage — the batch pass

Present the whole ledger at once, dependency-ordered and numbered — prose or a table,
whichever reads better for the set in hand: each open decision with its **one-line
recommendation**, then the items you marked N/A with their one-line reasons, so what
was excluded is as visible as what is being asked. The user marks each item **accept**
(the recommendation becomes the verdict) or **discuss** (it gets a deep-dive).

The answer is free-form text, and batch replies are the expected use: "accept all",
"accept all except 3 and 7", "discuss 2, 5; accept the rest", and reclassifying an N/A
back to open. **Never `AskUserQuestion` at triage.** It cannot express any of those
replies, and it flattens a free-form answer into whichever option sits nearest — here
that produces a verdict the user never gave, recorded as if they had.

**Any list of items you excluded on your own judgment gets its own explicit
confirmation, never folded into a general "accept all."** An exclusion is you deciding
an area doesn't apply, and a wrong one silently deletes a pillar of the user's project
— it has happened: three core pillars auto-N/A'd in a single session. Ask for that list
as its own question before any deep-dive starts, and read "accept all" as covering the
open decisions only.

Record accepts immediately: `status: decided`, `verdict` = the recommendation,
`decided_via: triage`, the Verdict section filled, `timestamp` refreshed, the phase's
`index.md` updated.

## Deep-dive

Walk the *discuss* items strictly in dependency order, **one at a time, waiting for
each answer**. For each: restate the question, give the options with their trade-offs,
give your recommendation, and let the user decide — verdict recorded with
`decided_via: discussion` and their rationale.

Label the options **A / B / C** and record a verdict only on an explicit letter or an
unambiguous restatement of one option. Conversational assent ("yeah that's it",
voice-input fragments) is not a verdict — you can't tell *which* option it blesses.
Re-ask with the letters rather than guessing, and say why you're re-asking so it
doesn't read as a loop.

Keep the presentations terse: one line per option, one short paragraph for the
recommendation. The detail already lives in the decision doc, and a pass that reprints
it for every item exhausts the context window mid-ledger. A user asking to go one-by-one
over a large set (more than ~15 items) still gets the fast accept/discuss pass first —
"one by one" usually means "don't decide without me", not "print every doc", and
walking 40 items at full depth serves nobody.

**After every verdict, refresh the still-open decisions.** Re-check each open decision
whose `depends_on` names the one just decided, then anything else the verdict plausibly
affects: if a recommendation changes, update the doc and *tell the user what changed and
why* before moving on. A recommendation made before an upstream verdict is stale the
moment that verdict lands.

When a verdict names a concept the ledger deferred or hasn't defined yet ("defer auth
to the plugin system"), define that concept in one clause right in the Verdict section
— the next reader, and the next skill, shouldn't have to reverse-engineer what the
deferral meant.

## Reopening a decision

A decided item the user reopens goes back to `status: open` with the old verdict kept
visible as history in the Verdict section — a ledger that overwrites its own past
can't explain why the project is shaped the way it is. Refresh the dependents
(`depends_on`), regenerate the affected sections of any deliverable already written
from the ledger, and append a `log.md` entry.
