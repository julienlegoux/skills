# Promoting drift into the register

Step 3's procedure. The register's format and its readers are defined in
`../../_shared/pipeline-interfaces.md` — this file is only how a drift record becomes
an entry.

## What counts as drift

Drift is the implementation contradicting something **already decided**: a line in
`docs/planning/SPECS.md` or `CONVENTIONS.md`, or the issue's own spec. That is the
whole test.

Not drift, and it clutters the register if promoted:

- **Out-of-scope discoveries** — a bug in neighbouring code, a refactor worth doing.
  Those are follow-up issues.
- **Choices the decided standards never covered.** A gap is not drift; if it should
  have been decided, that is a `define-conventions` or `define-change` input.
- **A tactic the issue simply didn't mention.** Drifting requires something to drift
  from.

## Folding duplicates

Group by **cause, not by issue**. Three issues that each pinned a different version
because one library is unusable in the decided stack are one entry with three evidence
links. Two issues that bypassed the same convention for genuinely different reasons are
two entries — same convention, different causes, different revisit triggers.

The test: would a future reader take one action or two? One action, one entry.

## Drafting an entry

Fill every field from the evidence file, not from memory:

- **Decided** — quote or link the actual SPECS/CONVENTIONS line. If you cannot find the
  decided line, the entry may not be drift at all; check the gap case above.
- **Actual** — what the code does now, in one line.
- **Because** — the *verified* blocker: version numbers, error text, the command that
  failed. "Didn't work" is not a cause, and an entry with a vague cause gets
  re-litigated by every future reader instead of trusted.
- **Evidence** — link every per-issue drift record that fed the entry, plus the PR.

## Proposing a disposition

One per entry, with a recommendation for the user to accept or overrule:

| Disposition | Propose it when | What must also happen |
|---|---|---|
| `accepted` | the drift is the better answer — the decided standard was wrong | recommend the corresponding edit to SPECS.md / CONVENTIONS.md, so the standard stops contradicting the code |
| `fix-now` | the drift is real debt and cheap to undo, and later work will build on it | a follow-up issue exists before the run ends, and the entry links it |
| `deferred` | undoing it needs something not available yet (a release, a migration, a decision) | a **concrete** revisit trigger — a version, an event, a date. Never "later" or "when we have time" |

`accepted` drift that leaves the standard untouched is the worst outcome: the
next planning run reads a standard the code has silently abandoned. Say so when
recommending it.

## Writing the register

A repo from before this vocabulary may hold a `deviations/` folder where the drift
records now go — sweep it too, and promote what it holds; the folder itself stays
where it is, as history.

First promotion into a repo creates `docs/planning/DRIFT.md` and lists it in the
planning bundle's root `index.md`. Later promotions **append** — the file is
append-only across epics, grouped newest-epic-first.

An entry that stops being true is never deleted: its disposition becomes
`resolved (<ISO date>) — <how>`. The history is what makes a future reader trust the
register instead of re-deriving it.

Then append to `docs/planning/log.md`, and commit per
`../../_shared/bundle-interfaces.md`.
