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

A review reads better when the reviewer did not write the thing. When the analysis
runs on a model from a different family than the session conducting the review, it is
not re-reading its own reasoning — which is exactly where a self-review is weakest.

This is capability-detected, never required. Probe once with
`command -v external-reviewer`. If it is absent, run the review natively and say
nothing about it: most users do not have it, and a skill that advertises tooling the
user never asked for is noise. Record `external review: not available` in the report's
Scope and move on.

**The native review is the unconditional path.** It runs whenever no external report
came back — the binary absent, no reviewer configured on this machine, a run that
failed — and it is never skipped, shortened, or made conditional on the external pass
having been tried. Everything below only ever *adds* a second opinion to a review that
already stands on its own.

When the binary is present, use it for the analysis pass — no need to ask first.

### The invocation

```bash
external-reviewer review \
  --allow docs/planning \
  --allow docs/epics \
  --tier standard \
  /path/to/repo < request.json
```

`request.json` is the whole of what the reviewer is told:

```json
{"system": "…the reviewer's instructions, from the block below…", "task": "…what to review, this time…"}
```

- Both fields are **required and non-empty, and they are the only two accepted**. The
  object is decoded strictly: a mistyped key (`"systm"`) is an error rather than a
  silently missing prompt, and nothing after the object is read. The binary carries no
  default system prompt and substitutes none — that text is this file's job, which is
  why it is written out below rather than assumed.
- Write `request.json` to a temp directory, **not** into the repository under review —
  the reviewed tree stays untouched by the review, and a stray file in it is a
  diff the user did not ask for. Both prompts are multi-line text inside JSON strings,
  so build the object and let the writer escape it; hand-typing `\n` is where a
  request object stops parsing.
- Pipe it rather than typing it: `--system <text> --prompt <text>` exist as a by-hand
  shorthand for the same two values, but they are a **pair** (giving one without the
  other is a usage error), giving them means stdin is not read at all, and a
  multi-kilobyte prompt through shell quoting is exactly where an invocation breaks on
  Windows. Skills use the request object.
- **stdout is the reviewer's markdown report and nothing else**; every diagnostic —
  the resolved model, warnings, errors, the closing `done` line — is on stderr. Keep
  stderr. Never `2>/dev/null`: on a run that produced no report it is the only place
  that says why, and on one that succeeded it is where the resolved model's name comes
  from.

### Choosing the tier, not the model

`--tier light|standard|heavy` asks for a **weight**, and never for a vendor. Which
model a weight resolves to is the user's machine-local assignment, so "pick a model
from a family other than this session's" stops being a judgment this skill re-makes
every run. It defaults to `standard` when omitted.

- `light` — a small read: three issue files against one epic.
- `standard` — an ordinary full pass; the default, and the right answer most of the time.
- `heavy` — a full plan against a dozen epics, or an audit that has to hold many
  cross-references at once.

`--model <provider>/<id>` also exists, bypasses tiers entirely, and cannot be combined
with `--tier`. Skills do not use it: a vendor named in a shared contract is a pin that
rots, which is the whole reason tiers exist.

Nothing here names a family either. `--exclude-family` already defaults to `anthropic`,
so the reviewer comes from a different family than the session running this skill
without anyone asking for it — the entire point of delegating. Pass the flag only when
the user asked for something specific, and pass a real family name: an unrecognised one
is a usage error **by design**, because a typo that quietly disabled the exclusion would
hand the review straight back to the family it was meant to exclude.

### What the reviewer may read

`--allow <path>` is repo-relative, repeatable, and **required** — a run with none is a
usage error. It is the reach of the run: nothing outside the granted subtrees is
readable through any of the reviewer's tools, so the exposure of a review is visible in
the command line that produced it. `--allow .` grants the whole repository; prefer the
subtrees the task actually needs.

The `task` is the reviewer's only orientation — the binary injects no file listing, no
README, no repository path. Name the artifacts in it, repo-relative and spelled as the
grant spells them.

### The system prompt

Send this as `"system"`, adapted only where a run genuinely differs:

```
You are reviewing a repository you did not write, for the people who did.

You see it through four read-only tools — list, read_file, search and git_read —
and they are the only way you see it. Nothing has been summarised, excerpted, or
chosen on your behalf, and no file is in front of you until you read it. Read
what you need: the reading is the review.

Report leads, not findings. A lead says what looks wrong, where, and what would
confirm it. Do not assert a defect you have not read in the file — name the file
and the line, say what you suspect, and say what would settle it. Say plainly
when you are uncertain.

Volume is not the goal. A review that confirms the work is sound is a legitimate
outcome, and inventing a defect in order to have something to report costs the
reader more than saying nothing would have.

You cannot edit, commit, or reach GitHub — not as a rule you might break, but as
a property of the tools you have. Do not propose to.

When you have read enough, write a markdown report as your final message: the
leads, each with its location and what would confirm it, and what you checked
that looked right. That final message is the whole deliverable; nothing else you
emit is read.
```

### What comes back, and what to do about it

Read the exit code — it is the branch, and the three cases want different things:

- **Exit 0** — the report is on stdout. What comes back are **leads, not findings**:
  the external session has no memory of how these artifacts were produced and will
  occasionally read a deliberate convention as a defect. Verify each lead against the
  files before it enters the report; an unverified finding costs the user more than a
  missed one. Name the tier and the resolved `provider/model` in the report's Scope, so
  a later reader knows who looked — the pair is on stderr, on the line reading
  `model   <provider>/<id>  auth=<source>`.
  A run that hit its ceiling also exits 0, with `stop=bounds` on the `done` line and
  whatever report it had — occasionally none at all. Use what came back the same way,
  and say in Scope that it was cut short.
- **Exit 1** — no reviewer resolved on this machine: nothing was reached, so there is
  nothing to report about it. Run natively and record `external review: not available`,
  exactly as for an absent binary. This is the silent-fallback case **by design** — a
  machine with no reviewer configured must not put a line about an unrequested
  capability into every report it writes. It is not a silent *run*, though: stderr
  carries one `warn` line naming the tier, the rule that refused it, and the layer that
  assigned the model, and that line is the answer to "why didn't it run?" when the user
  asks. Another reason not to discard stderr.
- **Exit 2** — reached and failed: either a malformed invocation (`stop=usage`) or a
  machine that is wrong while the invocation is right (`stop=failed`), with one
  `error:` line on stderr saying which. Run natively and record
  `external review: failed (<the error: line>)` in the report's Scope — a reviewer that
  broke is a fact the reader needs, unlike one that was never there. Ignore stdout on
  this path even when it is not empty: the one failure that can leave bytes there is a
  partially written report, and stderr says so, with the byte counts.

If it hangs, crashes, or returns nothing usable, that is the native path too. Never
block a review on it.

For a large surface, **batch by area** — one pass for coverage, one for ordering and
dependencies, one for schema and GitHub metadata — rather than one prompt asking for
everything. Each pass then keeps the whole surface in view instead of truncating it.
Each is its own invocation with its own `task`; the system prompt does not change
between them.

### When the user asks how to set it up

`external-reviewer tiers` prints which tiers resolve on this machine right now: the
config file that was read, each tier's assigned model and where the assignment came
from, and — when a tier does not resolve — which rule refused it. That is the command
to point a user at. This skill never writes that config and never prompts for one.

Two statuses are worth recognising when reading it back: `unassigned` means nothing
names a model for that weight, and `excluded by family: unknown` means the provider's
model ids carry no vendor segment the classifier can read. Every `github-copilot` model
is in that second state today, so a tier assigned there resolves to nothing however
correctly it is configured, and every review through it exits 1.

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
- External review: <tier> — <provider/model> | not available | failed (<reason>)

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
