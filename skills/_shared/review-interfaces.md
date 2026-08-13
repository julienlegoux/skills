# Review interfaces

Single source of truth for how the **planning** review skills — `review-epics` and
`review-issues` — grade what they find, verify GitHub, delegate the analysis pass, and
write their report. SKILL.md files point here instead of re-describing these rules.

`review-implementation` is not one of them: it reviews shipped code rather than
planning artifacts and grades against yardsticks of its own. The two audiences share
exactly one thing — the `docs/reviews/` directory and the names written into it —
which is why the naming rule below has to hold across all three, and why `okf-lint`
writes its own reports to the same scheme from outside this contract.

Two sibling files govern the *artifacts* under review rather than the review itself:
`bundle-interfaces.md` (anything written under `docs/` — language, link forms,
reserved files) and `pipeline-interfaces.md` (epic and issue schemas, status
lifecycle, GitHub facts). Both review skills read those too, and judge against them
directly: an epic is only malformed relative to what those files define, so a review
that grades against a remembered copy drifts the moment the contract moves.

This is the one and only copy: both review skills read it at
`../_shared/review-interfaces.md`. Editing it changes behaviour for both at once.

## A review does not repair

Reviewing is read-only. The deliverable is a report; the user decides what to fix.
Never repair epics, issues, milestones, sub-issue links, or indexes during a review
— once a reviewer edits, the user can no longer tell what was wrong from what was
already quietly fixed, and the report stops describing anything that exists. Fixes
happen after, and only when the user asks for them having seen the report.

The one file a review writes is its own report.

## Severity

Grade by what it costs the user, not by how much text the fix takes.

- `P0` — the output cannot be trusted or used at all: reviewed against the wrong
  source, most of the planned work missing, existing tracked state overwritten, or a
  layout broken enough that downstream skills won't run.
- `P1` — a material requirement, acceptance criterion, dependency, or constraint is
  missing, contradicted, or landed in the wrong place. The work would ship wrong.
- `P2` — boundaries, sizing, ordering, schema fields, links, or index entries wrong
  enough to confuse the next skill in the pipeline or the developer implementing it.
- `P3` — naming, wording, formatting, traceability. Real, but nothing breaks.

## What makes a finding

Every finding names **both sides**: the line in the source being honoured, and the
line in the generated artifact that fails to honour it. A finding with only one side
is an opinion, and the user cannot act on it without redoing the comparison.

Cite `file:line` whenever the file has stable line numbers. Then say what is wrong,
why it matters, and the specific fix — not "review this section".

Coverage that is *correct* deserves a mention too, briefly: a report listing only
defects reads as if nothing was checked.

## Verifying GitHub

When the artifacts carry `gh_issue`, `milestone`, or `resource`, and `gh` is
available and authenticated, verify them: the referenced issues and milestones exist,
titles and states match, and the links point back where the local files claim.

If GitHub cannot be checked, never block — mark verification `not verified` with the
reason and review the local metadata for internal consistency instead. The local
files are the artifact under review; GitHub is corroboration, not the subject.

## Delegating the analysis pass to another model

A reviewer that did not write the thing catches what a self-review is blind to. Hand
the analysis pass to a model from another family whenever one is reachable.

Probe once with `command -v external-reviewer`:

- Absent — run the review natively, record `external review: not available` in the
  report's Scope, and say nothing else about it.
- Present — read `external-reviewer.md`, beside this file, and follow it.

The native review runs whenever no external report came back, and is never skipped,
shortened, or made conditional on the external pass having been tried.

What comes back is leads, not findings. The external session has no memory of how these
artifacts were produced and will read a deliberate convention as a defect. Verify each
lead against the files before it enters the report.

## The report

Write the report to `docs/reviews/<YYYY-MM-DD>-<kind>-<subject>.md` in the reviewed
repository, creating the directory if it is not there. `<kind>` is the reviewer that
wrote it — `epics`, `issues`, `implementation`, `lint` — and `<subject>` is what was
reviewed, in the repo's usual slug form:

```
docs/reviews/
  2026-08-09-issues-epic-3.md
  2026-08-11-implementation-epic-3.md
  2026-08-11-issues-epic-4.md
  2026-08-14-issues-epic-4.md
```

A second report of the same kind and subject on the same day takes a `-2` suffix, then
`-3`. That is the only case where a name could collide.

This replaces the flat `docs/REPORT_<n>.md` series, and the replacement has to carry
what the integers were doing:

- The date prefix sorts the directory chronologically for free, which is what the
  numbers actually provided.
- **Never overwrite an existing report** stops being a rule three skills must each
  remember and becomes a property of the name: a distinct date, kind and subject cannot
  collide. The reports are still the history of what the artifacts looked like at each
  point, and an overwritten one still erases the evidence that a problem was already
  raised once — there is simply no longer a way to write one by accident.
- Nothing scans for the next free integer, so three skills stop coordinating on one
  counter. That was the fragile part: two reviews in the same session, or two clones
  both taking number 5, and the series has two report 5s or one that ate the other.
- The name carries the subject, so a directory listing says which epic each report is
  about and whether it graded a plan or the code.

Repositories reviewed before this layout still hold `docs/REPORT_<n>.md` at the root,
and epics link into them (`source: docs/REPORT_1.md#findings`). **Nothing moves** —
that is what keeps those links valid. Only new reports are born in `docs/reviews/`,
and `triage-reports` reads both layouts so a repo mid-transition loses no findings.

`docs/reviews/` is a plain directory, not an OKF bundle: reports carry no frontmatter
and belong to no `index.md`. Where `docs/` is itself a bundle root, add `reviews/` to
its `.okfignore` so the bundle still validates.

```markdown
# <Subject> Review Report

## Scope
- Reviewed: <paths or glob>
- Reviewed against: <path>
- GitHub verification: verified | not verified (<reason>)
- External review: <tier> — <provider/model> [(cut short)] | not available | failed (<reason>)

## Findings

### P1 — <short finding title>
- Location: <file:line>
- Source: <file:line or heading>
- Problem: <what is wrong>
- Impact: <why it matters>
- Recommendation: <specific fix>

## Coverage notes
- <areas that are well covered, or intentionally out of scope>

## Open questions
- <only where the artifacts are genuinely ambiguous — not as a place to park doubt>
```

With no findings, write `No findings.` under `## Findings` and keep every other
section: scope, coverage notes, and any verification gap are what make a clean report
worth reading.

Finish by linking the report and summarising the highest-severity findings in the
response itself. Say plainly when GitHub verification was skipped or the external pass
did not run — a gap the user does not know about is a gap they cannot close.

Then name what turns the findings into work: `triage-reports` reads every report under
`docs/reviews/`, groups the findings by the repair that resolves them, and
converts what the user accepts into the remediation epic. Offer it; don't run it
unasked, and don't repair anything here — the section above is why.
