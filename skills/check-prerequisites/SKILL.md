---
name: check-prerequisites
description: Probe what the planning bundle depends on — tools, runtimes, services, accounts, secrets — before epics are cut, and write docs/planning/PREREQUISITES.md, which carries the gaps only the user can close and the register implement-epic gates on. Use when planning is complete and before split-epics or create-issues, or to re-probe a stale register.
---

# Check Prerequisites

The planning bundle names things the project does not own: a compiler, a container
runtime, a hosted database, an API key, a paid quota. By the time SPECS.md and
CONVENTIONS.md are final, every one of them is written down as decided — and none of
them has been confirmed to exist.

Implementation is where that bill arrives today. An implementer hits the missing thing
mid-issue, records drift, and the user finds out at the end of a run that the blocker
was theirs to clear all along — one key, one login, one install, discovered one issue
at a time. This skill moves that discovery in front of the epics and does it in one
pass: probe what can be probed, and put what only the user can supply on a single list
before any work is planned around it.

**This is the opposite direction from drift.** Drift travels backwards — discovered
after the fact, against a standard already decided. Prerequisites travel forwards, and
are verifiable before a line of code exists. A prerequisite that reaches implementation
unverified is just drift that hasn't happened yet.

## Principles

1. **A probe is evidence, not an argument.** The command and its actual output, or the
   item is not verified. "It's normally installed" is not a result.
2. **A verification belongs to one machine.** The register records where it was probed;
   on another machine its `ok` entries are claims, not facts.
3. **Presence, never value.** Secrets are checked for existence and never read, echoed,
   or written into a committed file.
4. **A gap is not a stop sign.** It becomes a dated entry against the milestone it
   blocks — the project keeps planning, the user keeps their list.

## Output format: OKF

The deliverable is `docs/planning/PREREQUISITES.md`, part of the same `docs/planning/`
bundle (OKF v0.1) the planning skills fill. Its schema — frontmatter, sections, the
status vocabulary the gate keys on — is in `references/register.md`.

The bundle-wide rules (English content, link forms, reserved files, committing what you
write) are defined once in `../_shared/bundle-interfaces.md`; read it before writing
anything. `../_shared/feedback-interfaces.md` governs nothing this skill writes — it is
the closing reflex for what this run teaches about *this skill*, and it decides the end
of the run.

No decision ledger here. The other planning skills decide one-way doors that deserve a
file each; this one records a machine state that changes on its own. A decision doc
whose verdict a `--version` can invalidate next week would rot in place.

## Step 0: Inputs and re-run check

Read `docs/planning/`: SCOPE.md for the milestone structure, SPECS.md and
CONVENTIONS.md for what the project committed to, DRIFT.md if it exists. If
`docs/epics/` exists, read the epic and issue **frontmatter only** — it is cheap, and
it turns "needed by milestone 2" into "needed by epic 2".

Planning docs missing or thin: don't refuse. Probe against what the user tells you, and
mark in the register what was inferred from the conversation rather than read from a
decided doc — a requirement with no source is the one most likely to be wrong.

**Re-run:** if `PREREQUISITES.md` already exists, this is a refresh. Read it first,
keep every entry's decided disposition, re-probe the rest, and report only what changed.
Never silently flip a `waived` entry back to blocking — the disposition was the user's.

**Machine check:** record the machine you probe on (OS, architecture, shell) in
`probed_on`. If the existing register was probed somewhere else, every `ok` in it is
unverified here — re-probe rather than inherit. This is the whole reason the field
exists: one machine's missing toolchain is a fact about that machine, and treating it
as a fact about the project is how a local constraint becomes a false standard.

## Step 1: Enumerate what the plan depends on

Sweep the categories in `references/checklist.md`. Every requirement is traced to the
line that demands it — a link into SPECS.md, CONVENTIONS.md or SCOPE.md. A requirement
you can't trace is one you invented; drop it. The point is not to inventory the
ecosystem, it is to confirm the decided plan.

Include what the **pipeline itself** needs, not just what the app needs: a git remote,
`gh` authenticated with the rights to create milestones and merge, a CI provider that
actually runs. `implement-epic` cannot merge a green PR without them, and that failure
looks like a tooling mystery rather than a missing permission.

Split every requirement into one of two classes, because they have different endings:

- **Probeable** — a binary, a flag, a runtime, a local service, a config file. Step 2
  settles it without the user.
- **User-supplied** — an account, an API key, a secret in CI, a quota, a domain, a
  repo permission. No probe creates one of these. The most it can do is report absence,
  and absence is the user's list.

## Step 2: Probe — evidence, not argument

Run the real thing where it is cheap (`gofmt -l .`, the project's test command on an
existing package, `docker run --rm hello-world`). Where it isn't, run the smallest
invocation that proves the tool executes.

**Probe the flag, not just the binary.** A binary answering `--version` proves the
binary and nothing else. `go test -race` needs cgo, which needs a C toolchain that a
machine policy can refuse outright — the compiler answers `--version` happily right up
until the flag aborts the run. Wherever a convention names a command *with options*,
the option is what gets probed.

Record the command and its actual first line of output or error. A requirement you did
not manage to probe is `unknown`, never `ok`.

**Secrets:** check that the variable is set, or that the CLI reports an authenticated
session. Never print the value, never write it into the register, never commit it.

**Local and CI are two different machines.** A key that exists in your shell says
nothing about the CI runner. Where the requirement is needed by CI, probe the CI config
for the secret's declaration; where you can't, it is `user-action`, not `ok`.

**Don't cross into acting.** Installing a toolchain, creating an account, logging in, or
spending money is not a probe — it is a user action, and it is theirs. Report it.

## Step 3: Triage the gaps — one batch

Present everything that isn't `ok` in a single pass, grouped by class, each with a
concrete recommendation. One batch and not one question at a time: the user's attention
is the scarce resource, and a gap list is exactly the kind of thing that reads well
together and terribly in sequence.

Dispositions available per item: install it now, the user supplies it, it runs in CI
only, it is waived and the standard changes, or it is deferred to the milestone that
needs it.

Two boundaries on what this skill does with the answers:

- **It never edits SPECS.md or CONVENTIONS.md.** Those have their own writers, and a
  second one editing a final doc mid-flight is how a bundle stops being trustworthy.
  When a disposition contradicts a decided standard, record it and name the doc that now
  disagrees, so the user can re-decide there.
- **An unresolved gap stays blocking.** Tie it to the milestone (or epic) it blocks and
  move on; nothing here justifies holding the whole plan hostage.

## Step 4: Write the register

Write `docs/planning/PREREQUISITES.md` per `references/register.md`. The user's TODO
list is its **first section** — what only they can provide, in the order the build needs
it, each with what "done" looks like. That list is the reason this skill exists; a
register that opens with a table of things that already work buries it.

Update the planning bundle's `index.md` and append to `log.md`, then commit and push per
`../_shared/bundle-interfaces.md`.

## The gate

`implement-epic` reads the register when it maps an epic and **stops before delegating
any issue** if an entry needed by that epic is neither `ok` nor `waived`. That is the
only enforcement point: it is the last moment before compute gets spent, and it fails in
one place with one message instead of inside an implementer's fifth tool call.
`create-issues` and `implement-issue` read the register for context, the same way they
read `DRIFT.md`, so an issue can carry its own prerequisite in its body.

## Handoff

With the register written, `split-epics` (greenfield) or `create-issues` (brownfield)
proceeds normally. Re-run this skill when the machine changes, when a blocked entry gets
cleared, or when a plan revision names something new — the re-run path in Step 0 keeps
every disposition already decided.

Then close the run per `../_shared/feedback-interfaces.md` — silently, unless this run
turned up something about this skill that clears both its filters.
