# Review interfaces

Single source of truth for how the **planning** review skills — `review-epics` and
`review-issues` — grade what they find, verify GitHub, delegate the analysis pass, and
write their report. SKILL.md files point here instead of re-describing these rules.

`review-implementation` is not one of them: it reviews shipped code rather than
planning artifacts and grades against yardsticks of its own. The two audiences share
exactly one thing — the `docs/REPORT_<n>.md` series — which is why the numbering rule
below has to hold across all three.

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

A review reads better when the reviewer did not write the thing. When the analysis
runs on a model from a different family than the session conducting the review, it is
not re-reading its own reasoning — which is exactly where a self-review is weakest.

This is capability-detected, never required. Probe once with `command -v opencode`.
If it is absent, run the review natively and say nothing about it: most users do not
have it, and a skill that advertises tooling the user never asked for is noise. Record
`external review: not available` in the report's Scope and move on.

When it is present, use it for the analysis pass — no need to ask first:

```
opencode run --dir <repo> --agent plan -m <provider/model> "<the review prompt>"
```

- `--agent plan` is read-only. The external session cannot touch the repo, so this
  skill keeps sole ownership of the report. Never pass `--auto`.
- **Match the model to the weight of the review, not to the largest number
  available.** Three issue files against one epic is a small read; a full plan against
  a dozen epics, or an audit that has to hold many cross-references at once, earns a
  heavier model. `opencode models` lists what is authenticated — pick from a family
  other than the one running this session, since that difference is the entire point.
  Pinning a model id here would rot within months; the judgment does not.
- For a large surface, **batch by area** — one pass for coverage, one for ordering and
  dependencies, one for schema and GitHub metadata — rather than one prompt asking for
  everything. Each pass then keeps the whole surface in view instead of truncating it.
- What comes back are **leads, not findings**. The external session has no memory of
  how these artifacts were produced and will occasionally flag a deliberate convention
  as a defect. Verify each lead against the files before it enters the report; an
  unverified finding costs the user more than a missed one.
- If it errors, hangs, or returns nothing usable, fall back to the native review.
  Never block a review on it.
- Name the model in the report's Scope, so a later reader knows who looked.

## The report

Write a new numbered report under `docs/` in the reviewed repository. Find the next
number by scanning `docs/REPORT_<number>.md` and taking the next integer; start at
`docs/REPORT_1.md`. **Never overwrite an existing report** — the series is a history
of what the artifacts looked like at each point, and an overwritten report erases the
evidence that a problem was already raised once.

```markdown
# <Subject> Review Report <n>

## Scope
- Reviewed: <paths or glob>
- Reviewed against: <path>
- GitHub verification: verified | not verified (<reason>)
- External review: <provider/model> | not available

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

Then name what turns the findings into work: `triage-reports` reads the whole
`docs/REPORT_<n>.md` series, groups the findings by the repair that resolves them, and
converts what the user accepts into the remediation epic. Offer it; don't run it
unasked, and don't repair anything here — the section above is why.
