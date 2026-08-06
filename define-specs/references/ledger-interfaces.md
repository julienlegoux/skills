# Ledger interfaces

Single source of truth for the decision doc — the unit every ledger-driven skill
writes (`define-scope`, `define-specs`, `define-conventions`, `define-change`,
`map-codebase`). The bundle-wide rules those same skills obey (language, links,
reserved files, committing) live in `bundle-interfaces.md`.

Never edit a synced copy — change `_shared/ledger-interfaces.md` and re-run the sync.

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

## Reopening a decision

A decided item the user reopens goes back to `status: open` with the old verdict kept
visible as history in the Verdict section — a ledger that overwrites its own past
can't explain why the project is shaped the way it is. Refresh the dependents
(`depends_on`), regenerate the affected sections of any deliverable already written
from the ledger, and append a `log.md` entry.
