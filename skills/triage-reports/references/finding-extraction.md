# Finding extraction, grouping, and staleness

Mechanics for Steps 2–4. The judgment stays in `SKILL.md`; what follows is how to get
a hundred findings out of a report series and down to a set of repairs without losing
any or inventing some.

## Where the reports are

Two layouts, both live at once:

```
docs/reviews/2026-08-11-issues-epic-4.md    # current: date, kind, subject
docs/REPORT_2.md                            # legacy: the flat integer series
```

The legacy files were never migrated, because the epics that link into them
(`source: docs/REPORT_1.md#findings`) stay valid exactly as long as nothing moves. So
read both, and treat them as one set: a repo whose reviews straddle the change has some
of its findings in each, and a pass that globs only one drops the rest without saying
so.

`<kind>` in the current names is the reviewer — `epics`, `issues`, `implementation`,
`lint`. The `lint` ones are `okf-lint`'s and are **not** part of this set: they carry no
`## Scope`, grade High/Medium/Low, and report on a knowledge bundle rather than on the
plan or the code. Skip them, and say in the final report that you did.

## Telling the reports apart

Every report opens with `## Scope`, and its `Reviewed:` line names what was read. That
is the only thing that decides which flavour it is — never the report's date, its
number, or its position in the directory.

| `Reviewed:` points at | Written by | A fix edits |
|---|---|---|
| `docs/epics/*/EPIC_*.md`, milestones, tracking issues | `review-epics` | the epic files and their GitHub state |
| `docs/epics/*/issues/*.md`, `issues/index.md` | `review-issues` | the issue files and their GitHub state |
| a merged diff, PR ranges, product source paths | `review-implementation` | product code and its tests |

`Reviewed against:` matters too: it names the contract the finding is measured by, and
that contract is what the repair has to satisfy. A finding whose source is an epic's
acceptance criterion is fixed either by changing the issue *or* by amending the
criterion — the report says which side it thinks is wrong, and the triage confirms it.

## The two finding layouts

Both use `### P<n> <title>` headings, so both layouts extract with one pass — the
missing glob in a repo that only ever had one of them is what `2>/dev/null` is for:

```bash
grep -nE '^### P[0-3]' docs/reviews/*.md docs/REPORT_*.md 2>/dev/null
```

Lint reports match nothing here, since their headings are `### High` / `### Medium` /
`### Low` — but check the file list the grep covered rather than trusting that, because
a lint report with zero matches and a review report you forgot to read look identical
from the output.

The separator after the severity is an em dash in some reports and a hyphen in others;
match on `P[0-3]` and treat the rest of the line as the title.

Planning reviewers (`review-interfaces.md`'s template) write:

```
- Location:        the artifact line that is wrong
- Source:          the line it fails to honour
- Problem: / Impact: / Recommendation:
```

`review-implementation` writes:

```
- Location: / Violates: / Problem: / Evidence:
- Disposition:     fix-now (#N) | accepted (drift) | won't-fix - <reason>
```

**That last field is authoritative.** It was decided by the user at review time, so a
finding carrying one is not re-triaged: `accepted` and `won't-fix` drop out with a note,
and `fix-now` with a live issue number is already tracked work. A `fix-now` whose issue
does not exist (or was closed unmerged) is the exception — that one comes back into the
triage, since the work it names was never done.

Carry into the working set, per finding: severity, title, location, the contract line it
violates, the recommendation, and the report it came from. The last one is not
bookkeeping — it is how a group proves it spans the series rather than repeating one
reviewer's hobby-horse.

## Grouping by repair

Group on **the edit that resolves them**, not on subject matter. Two findings belong
together when one person, in one sitting, fixing one thing, resolves both.

Reliable groupings:

- **One defect replicated across artifacts** — the same wrong link form in nine
  `issues/index.md` files, the same boilerplate section contradicting its own frontmatter
  in fifty issue files. One convention, one sweep, one verification command.
- **One missing convention** — branch naming, a required header, a status-commit rule
  absent from every body written by the same generator.
- **One orphaned area** — scope named in an epic that no issue owns. The repair is
  "give it an owner", whether that means a new issue in an existing epic or an amended
  boundary.
- **One contract, several symptoms** — a type that does not exist, wired by three issues.
  Fixing the contract fixes all three; fixing them one at a time fixes none.

Do **not** group:

- findings that merely share a severity, an epic, or a file
- findings whose repairs must land in a specific order — that is `depends_on`, not one
  issue
- a repair that would blow past `L` in the size bands (`../_shared/pipeline-interfaces.md`).
  Split it by artifact or by area, and wire the order
- findings whose resolution is a **decision** ("the epic says X, the issue says Y"). Until
  the user answers, there is no edit to size; these go to the triage as questions

Test each group before it goes to the triage: name the single verification that proves it
done. A group with no such command or check is a theme, and themes do not close.

## Staleness checks

Run these per group, cheapest first, and stop at the first that settles it.

```bash
# 1. Does the cited line still say what the finding quotes?
sed -n '<line>p' <file>          # or: git show <ref>:<file>

# 2. Has this area moved since the report was written?
git log --since=<report timestamp> --oneline -- <path>

# 3. Is it already tracked?
gh issue list --state all --search "<distinctive phrase>"

# 4. Was it already accepted as drift?
grep -A6 '<the standard>' docs/planning/DRIFT.md
```

Then the series' own memory: `docs/epics/log.md` retirement notices say what a previous
epic 0 already fixed. A finding whose repair is named there is done, whatever the report
still claims.

Where `gh` is unavailable, check the local artifacts and say in the report which checks
did not run — an unverified drop is worse than a stale finding, because the user never
sees it again.

## Reporting the arithmetic

Findings extracted, findings dropped as stale (with the reason class), groups formed, and
findings absorbed per group. The numbers have to reconcile: every extracted finding is
either in a group, dropped with a reason, or standing as an open question. One that is
none of those was lost, and a converter that loses findings quietly is worse than no
converter at all.
