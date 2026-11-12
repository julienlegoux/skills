---
name: review
description: Review a body of changes — a milestone, a branch, a whole build — against docs/PLAN.md and the standards, with reviewers that did not write the code, and return verified findings ranked by severity. Use when build finishes a milestone, or when the user asks for a review of work that was done.
---

# Review

A review is worth what the reviewer's independence is worth. The session that wrote
the code already believes it is right, and will read its own reasoning back as
confirmation.

## Reviewers that did not write it

Hand each lens to a fresh subagent that receives the change range, `docs/PLAN.md`, the
standards (`../build/references/standards.md`, or the project's own) and the recorded
deviations from `docs/PROGRESS.md` — and nothing of the author's conversation. Where
the harness lets you choose, use a different model from the one that wrote the code.

Reviewers are Claude models for now, so independence comes from the fresh context, not
from another vendor. If a reviewer from another model family becomes reachable, it
joins here as one more reviewer; nothing else changes.

Without subagents, review in the current session and say plainly that the review was
not independent.

## Lenses

Run them concurrently, one reviewer each. A reviewer holding every lens over a large
change degrades in exactly the way the review exists to catch; on a small change,
one reviewer holding all four is enough.

- **Does it do what the plan says?** For each outcome in the plan, find the code that
  delivers it and judge whether it really does: missing, happy-path only, stubbed,
  hard-coded, behind a flag left off.
- **Is it correct and safe?** Logic errors, unhandled failures, races, leaks, unsafe
  input handling, authorisation gaps, secrets in code or config. Each finding comes
  with a concrete failure: the input or state, and the wrong result.
- **Does it hold together?** What no single unit's review can see: the same logic
  written twice, competing abstractions for one concept, a helper a later unit should
  have used, dead code, a standard broken a little more in each change. Say whether a
  breach is a slip or a pattern.
- **Would the tests go red?** The question is never whether the suite passes but
  whether it would fail if the implementation broke: assertions that cannot fail,
  expected values copied from actual output, tests that never execute, collaborators
  mocked until only the wiring is tested. Where reading cannot settle it, break the
  implementation on purpose and watch.

A recorded deviation is settled, not a finding.

## Leads, then findings

What a reviewer returns is a lead. It has no memory of why things were built this way
and will read a deliberate choice as a defect. Check every lead against the code —
reproduce it where that is possible — and drop what does not survive.

Rank what does by what it costs: **blocking** (an outcome is not delivered, data can
be lost or exposed), **should fix** (wrong in a case that will occur, or a pattern that
will spread), **minor**. Each finding names the location, what is wrong, and the
failure it causes.

## What happens to them

Called by `build`: return the verified findings; `build` fixes them and verifies
again. Called by the user: report them ranked, and change nothing unless asked.

No report files and no remediation backlog — a finding is fixed, or it is consciously
left and recorded as a decision in `docs/PROGRESS.md`.

If this skill's own instructions caused a problem during the run, that is for
`feedback` — silently, never as a question to the user.
