# The prerequisite register

`docs/planning/PREREQUISITES.md` — written by `check-prerequisites`, read by
`implement-epic` (which gates on it), `create-issues` and `implement-issue`.

One writer, several readers, which is why this schema lives here rather than in
`skills/_shared/`: the readers need a verdict and a path, not a format. Keep it that
way — a reader that has to parse the layout is a reader that breaks when it changes.

## File

```markdown
---
type: Prerequisites
title: "<project> — Prerequisites"
description: "<one line: N verified, N waiting on the user, N blocking>"
tags: [planning, prerequisites]
timestamp: <ISO 8601 — set on every write>
probed_on: "<os> <arch> — <shell>"      # the machine every `ok` below was verified on
status: blocking | clear                # blocking = at least one unsatisfied entry
---

# Prerequisites

## What only you can provide

- [ ] **<thing>** — <why the plan needs it> ([source](/SPECS.md#stack)) —
      needed by <milestone 2 / epic 2> — done when: <the observable end state>

## Verified

| Requirement | Demanded by | Probe | Result |
|---|---|---|---|
| Go 1.26 toolchain | [Specs](/SPECS.md#stack) | `go version` | `go1.26.3 windows/amd64` |

## Open

### <requirement> — `<status>`

- **Demanded by**: <link to the deciding line>
- **Probe**: `<exact command>` → `<actual output or error, first line>`
- **Disposition**: <the user's verdict from Step 3, or "undecided">
- **Needed by**: <milestone / epic, or "start">
- **Contradicts**: <the planning doc this now disagrees with, if any>
```

## Status vocabulary

| Status | Means | Satisfies the gate |
|---|---|---|
| `ok` | probed on `probed_on`, worked | yes |
| `waived` | the user decided the project proceeds without it | yes |
| `user-action` | only the user can supply it, and they haven't yet | no |
| `blocked` | probed, failed, and no disposition resolves it yet | no |
| `unknown` | not probed — no machine, no access, out of reach | no |

`ok` and `waived` are the only two the gate accepts. `unknown` deliberately does not
pass: an unprobed requirement is the exact state this skill exists to eliminate, and
letting it through would make a silent skip indistinguishable from a verification.

## Field notes

- **`probed_on` is load-bearing.** A register carried to another machine keeps its
  `user-action` and `waived` entries — those are decisions — but its `ok` entries are
  claims about a machine that isn't this one. Re-probe rather than inherit.
- **The TODO section comes first, always**, even when it is empty (write "Nothing —
  every prerequisite is satisfied."). It is the section the user opens the file for.
- **Checkboxes are for the user to tick**, and a later run reads them as a hint, never
  as proof: a ticked box still gets re-probed where a probe exists.
- **Links follow the bundle rules** in `../../_shared/bundle-interfaces.md`: inside
  `docs/planning/` use bundle-relative paths (`/SPECS.md`), and cross into
  `docs/epics/` with a plain relative path (`../epics/epic-2-billing/EPIC_2.md`).
- **Never record a secret's value** — record that it is set, and where it must be set
  (local shell, CI secret store, both).
- **Entries are not deleted when they resolve.** An entry that becomes `ok` keeps its
  history in the Verified table with the probe that settled it; the register is read to
  learn what was already checked, and a file that forgets gets re-derived by hand.

## The gate, stated for its reader

`implement-epic`, at the point it maps an epic: read `docs/planning/PREREQUISITES.md`
if it exists. If any entry whose **Needed by** covers this epic is not `ok` or `waived`,
stop before delegating any issue and report the entries by name. This costs one file
read and saves an implementer discovering it inside a worktree, five tool calls deep,
with a half-written branch to clean up.

Absent register: proceed. The gate reports what exists; it never demands the skill
have been run.
