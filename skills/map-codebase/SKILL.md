---
name: map-codebase
description: Reverse-engineer an existing codebase into the docs/planning/ bundle (SPECS.md + CONVENTIONS.md) by reading the code instead of interviewing the user — the brownfield entry point before define-change. Use to map, bootstrap, or refresh the planning bundle for an existing app, or to resume open decisions under docs/planning/mapping/.
---

# Map Codebase

The greenfield planning skills interview the user because the answers don't exist
yet. On an existing codebase they do exist — in the manifests, the folder tree, the
migrations, the git log. This skill reads them out and writes the same two
deliverables `define-specs` and `define-conventions` would have produced:
`docs/planning/SPECS.md` and `docs/planning/CONVENTIONS.md`, in the same format, at
the same paths. Downstream skills must not be able to tell whether the bundle came
from interviews or from code archaeology.

## Principles

1. **Facts are looked up, never asked — and here almost everything is a fact.** The
   stack is whatever `package.json` says; the commit style is whatever `git log`
   shows. The user triages *ambiguities*, not findings. Expect the decision ledger
   to hold zero to a handful of items, not thirty.
2. **Descriptive, not prescriptive.** The mapped CONVENTIONS.md records what the
   code *actually does*, not what anyone wishes it did. If CLAUDE.md or
   CONTRIBUTING.md prescribes something the code contradicts, that conflict is a
   ledger decision for the user — never a silent pick of either side.
3. **Code is ground truth; configs lie.** A `.eslintrc` proves intent, not practice.
   For every area, sample several real source files and believe them over the
   config; where they disagree, that's either a note or a decision.
4. **Unknown beats guessed.** If nothing in the repo answers a question, the
   deliverable says "Unknown — no deployment config found", not a plausible
   invention. A wrong SPECS.md poisons every downstream skill that trusts it.
5. **Nothing is finalized until the user confirms** — even a zero-decision run ends
   with the user sighting a summary before the deliverables are written.

## Output format: OKF

Same `docs/planning/` bundle (OKF v0.1) as the greenfield skills. Establish it if
absent: root `index.md` whose frontmatter holds `okf_version: "0.1"` and nothing
else (its body is the bundle listing), root `log.md`
(`## YYYY-MM-DD` headings, newest first). This skill owns:

```
docs/planning/
  SPECS.md            # deliverable — same sections as define-specs
  CONVENTIONS.md      # deliverable — same shape as define-conventions
  mapping/            # only created if there ARE ambiguities
    index.md          # decision listing (no frontmatter — non-root index)
    01-<slug>.md      # one Decision doc per genuine ambiguity
```

The bundle-wide rules — English content, link forms (bundle-relative with a leading
`/`, e.g. `([decision](/mapping/01-canonical-error-style.md))`), reserved files, and
committing what you write — are defined once in `../_shared/bundle-interfaces.md`,
and the decision doc schema in `../_shared/ledger-interfaces.md`. Read both before
writing anything.

## Step 0: Resume and refresh checks

**Resume:** if `docs/planning/mapping/` exists with open decisions, this is a
resume. Read `mapping/index.md` and every decision doc, report the tally, and jump
to Step 4 (open decisions) or Step 5 (all decided, deliverables missing). Never
re-ask a decided item.

**Refresh:** if `SPECS.md`/`CONVENTIONS.md` already exist with a `mapped_commit`
field, don't re-map blind. Run
`git diff --stat <mapped_commit>..HEAD` and `git log --oneline <mapped_commit>..HEAD`,
summarize what moved (new packages? schema migrations? new CI jobs? just feature
code?), and offer a **refresh**: re-sweep only the areas the diff touches and
regenerate only the affected deliverable sections, bumping `mapped_commit`/
`mapped_at` and appending to `log.md`. Offer a full re-map only if the drift is
sweeping or the user asks. If the deliverables exist but lack `mapped_commit`, they
came from the greenfield skills — say so and ask before overwriting anything;
augmenting a hand-decided bundle is a user call, not a default.

**Greenfield guard:** if the repo has essentially no code (empty or scaffold-only),
this skill has nothing to map — point the user at define-scope/define-specs instead.

## Step 1: Orient

Establish what you're mapping before sweeping:

- Repo root, primary language(s), rough size (`git ls-files | wc -l` scale).
- **Monorepo?** If there are multiple packages/apps (workspaces, `packages/*`,
  `apps/*`, multiple manifests): ask the user which package to map if they didn't
  say. Map that one in depth; record the overall multi-package structure and
  cross-package boundaries in SPECS.md's Architecture section either way, so the
  map doesn't pretend the package lives alone.
- Existing prose: README, CLAUDE.md, AGENTS.md, CONTRIBUTING.md, docs/. Read them
  as *claims to verify*, not facts — Principle 2.
- Record `git rev-parse HEAD` and the current timestamp now; they become
  `mapped_commit` / `mapped_at` in the deliverables.

## Step 2: The sweep

Extract facts area by area. For each area: find the authoritative artifacts, then
**open several real source files and check the code agrees** — every conclusion
should rest on code you actually read, not just a config you found.

SPECS side (feeds SPECS.md):

- **Stack** — manifests and lockfiles (`package.json`, `pyproject.toml`,
  `go.mod`, `Cargo.toml`, …): language, runtime version, framework, key libraries
  with versions.
- **Architecture** — entrypoints, the folder tree, how modules depend on each
  other; monolith vs services; sync vs queued work.
- **Data model & storage** — schema/migration files, ORM models, raw DDL; which
  stores (DB, cache, blob) and what owns what.
- **Auth** — middleware, session/token handling, guards/decorators, identity
  provider config.
- **Interfaces & integrations** — route definitions, API schemas; env vars plus
  client libraries reveal third-party services better than docs do.
- **Deployment & operations** — Dockerfiles, CI/CD workflows, IaC, Procfiles,
  platform configs; observability wiring (logging, metrics, error tracking).
- **Testing infrastructure** — test dirs, runners, CI test jobs, coverage config.

CONVENTIONS side (feeds CONVENTIONS.md):

- **Naming and file layout** — read the tree and a spread of files; note the
  dominant casing, module organization, co-location patterns.
- **Lint/format setup** — configs, then confirm the code is actually formatted
  that way.
- **Test patterns** — where tests live, naming, style (unit vs integration mix,
  fixtures, mocking habits) from real test files.
- **Error handling** — sample how errors are raised, wrapped, logged across a few
  modules.
- **Commit and branch style** — `git log --oneline -50` for message conventions;
  merge vs rebase habits; branch naming from `git branch -a` and merged-PR titles.
- **Review/PR ceremony** — PR templates, CODEOWNERS, required checks if visible.

On a large repo, spawn parallel Explore/general-purpose subagents — one per area
above, each returning findings plus the file paths that back them — and reconcile
their reports yourself. On a small repo, sweep directly; subagent overhead isn't
worth it.

Close the sweep with an honest gap list: every area where nothing was found stays
"Unknown" (Principle 4), and every genuine ambiguity goes to Step 3.

## Step 3: Ledger the ambiguities — and only those

Most sweeps produce facts, and facts don't get decision docs. A ledger item exists
only when the repo *cannot answer for itself*:

- **Conflicting conventions** — half the repo does X, half does Y; which is
  canonical for future code?
- **Docs vs code contradictions** — CONTRIBUTING.md prescribes something the code
  ignores; which does CONVENTIONS.md record as the standard?
- **Dead-looking subsystems** — a module nothing references; in scope or legacy to
  ignore?
- **Undocumented intent** — an architectural choice whose "why" matters downstream
  and can't be inferred.

**If the ledger is empty — the common case — skip Steps 3–4 entirely and go
straight to Step 5.** Do not manufacture decisions to look thorough.

Otherwise write one doc per item at `docs/planning/mapping/<nn>-<slug>.md`, using the
template in `../_shared/ledger-interfaces.md` (`tags: [decision, mapping]`,
`phase: mapping`), each with a concrete recommendation grounded in evidence
(e.g. "38 of 51 handlers use pattern X, and all files touched in the last six
months do — recommend X as canonical"). Create `mapping/index.md` (no frontmatter)
listing each with status and one-line recommendation.

## Step 4: Triage, then deep-dive

Both passes from `../_shared/ledger-interfaces.md`, run as a single step rather than
two: what is triaged here is a handful of *ambiguities*, not a checklist of areas, so
the batch list and the walk-through of whatever the user flags fit in one exchange —
and there is rarely an excluded list to confirm, because a finding the code answers
never became a decision at all.

## Step 5: Confirm, then write the deliverables

Summarize the map in a few lines — stack, shape, notable conventions, the Unknowns,
any verdicts — and get the user's confirmation. Then write both deliverables from
findings plus verdicts.

`docs/planning/SPECS.md` — identical section structure to define-specs' output, so
downstream readers can't tell the origin:

```markdown
---
type: Technical Specification
title: "<project> — Technical Specs"
description: "<one-line: the stack and shape of the system>"
tags: [planning, specs]
timestamp: <ISO 8601 — now>
status: final
mapped_commit: <full SHA from Step 1>
mapped_at: <ISO 8601 — sweep time>
---

# <Project> — Technical Specs

## Stack
## Architecture
## Data model & storage
## Auth
## Interfaces & integrations
## Deployment & operations
## Testing infrastructure
## Cross-cutting concerns
```

`docs/planning/CONVENTIONS.md` — same shape as define-conventions' output
(sections: naming & file layout, code style/lint/format, testing, error handling,
commits & branches, review), with the same frontmatter pattern plus
`mapped_commit`/`mapped_at` (no `baseline_version` — there was no baseline).

Rules for both:

- State findings as settled fact in present tense ("Errors are wrapped in
  `AppError` and logged at the boundary"), exactly as a decided spec would read.
- Where a ledger verdict settled a point, link it OKF-style
  (`([decision](/mapping/02-docs-vs-code-commit-style.md))`).
- Keep the honest Unknowns as such — one line each, no padding.
- Shape sections to what the repo actually has; don't force empty headings.

Update root `index.md`, append a `log.md` entry (`* **Creation**: mapped <repo> at
<short-sha>` or `* **Update**: refreshed map ...`), run the okf-docs validator
against `docs/planning/` if available, then commit and push per
`../_shared/bundle-interfaces.md`.

## Handoff

The bundle now looks exactly like a completed greenfield planning run. Natural next
steps: `define-change` to plan the change that motivated the mapping, then
`create-issues` and `implement-epic` — the full brownfield chain is
map-codebase → define-change → create-issues → implement-epic. If the code drifts
later, re-invoking this skill offers the refresh path from Step 0 instead of a
re-map.

## Revisiting later

If the user reopens a mapping decision, set it back to `status: open` (old verdict
kept visible as history), re-decide, regenerate the affected deliverable sections,
and append to `log.md`. If the disagreement is with a *finding* rather than a
decision ("that's not our canonical pattern"), treat the correction as a new ledger
decision — the code said one thing, the user says another, and that conflict
deserves a recorded verdict, not a silent edit.
