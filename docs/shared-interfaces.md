---
type: Contract
title: "Shared interfaces"
description: "The three _shared/ contracts, split by audience, read in place by the skills that obey them."
tags: [contracts, shared, architecture]
timestamp: 2026-08-08
---

# Shared interfaces

Anything more than one skill has to agree on lives in `_shared/` — **once**, as one
file on disk. A `SKILL.md` points at `../_shared/<file>` instead of restating the
rule, so a format can never drift between the skill that writes it and the skill that
reads it.

The contracts are split by **audience**, not by topic, so no skill carries rules that
don't apply to it. A skill that never writes an epic shouldn't ship the epic schema.

# Schema

| Interface | Defines | Audience |
|---|---|---|
| [`bundle-interfaces.md`](../skills/_shared/bundle-interfaces.md) | English-only content, the two bundles (`docs/planning/`, `docs/epics/`) and their link forms, reserved `index.md`/`log.md`, committing what you write | every skill that writes under `docs/` |
| [`ledger-interfaces.md`](../skills/_shared/ledger-interfaces.md) | the decision doc schema and the reopening rule | the ledger-driven planning skills |
| [`pipeline-interfaces.md`](../skills/_shared/pipeline-interfaces.md) | epic & issue schemas, the issue status lifecycle, the drift register (`docs/planning/DRIFT.md` and the per-epic records behind it), GitHub facts about non-default integration branches | the epic-to-PR skills |
| [`authoring-interfaces.md`](../meta/_shared/authoring-interfaces.md) | how a skill in this repo is shaped: anatomy, the description contract, progressive disclosure, tiered prescriptiveness, identity | the meta skills — `create-skill`, `improve-skill` |

The first three live in `skills/_shared/` and govern what skills write into a *user's*
project. The fourth lives in `meta/_shared/`, alongside its only two consumers, and
governs how the skills themselves are written; it exists because `create-skill` and
`improve-skill` need the same answer to "what does a good skill here look like", and
a rule stated twice is a rule that drifts.

There is no audience registry to maintain: a skill joins an audience by pointing at
the file, and leaves it by deleting the pointer. Point at an interface when the skill
starts **obeying** it — not when it merely touches the same bundle.

# How a skill reaches one

A published skill reads the file one level up from its own folder:

```
skills/define-scope/SKILL.md  ──reads──▶  ../_shared/bundle-interfaces.md
```

That resolves because the plugin is always loaded **whole** — see [Installation and
delivery modes](/installation.md). One file on disk, one file in git, no generated
copies, nothing to re-sync after an edit.

The cost is the invariant that pays for it: **a published skill folder is not
portable on its own.** Lifting `define-scope/` into some other `.claude/skills/`
breaks its `../_shared/` pointers. The unit of distribution is the repo, not the
folder.

The two skills in `meta/` are the exception, because they *are* installed on their
own — a junction straight into `~/.claude/skills/`, where `..` is the install folder
and no relative pointer can survive. They pay for it with a step they already take:
locating the clone is their first action, so they read the absolute
`<repo>/meta/_shared/authoring-interfaces.md`.

The rule generalises: **a relative pointer is available to a skill that travels with
its contracts; one that travels alone must resolve the repo first.**

Until 2026-08-06 the opposite trade was made: `_shared/` was copied into each
skill's `references/` by a `sync.ps1` build step, so a lone folder stayed
self-contained. Three generated copies of every contract bought a portability nobody
used.

# When a rule stops fitting

If a rule applies to only part of an interface's audience, **split the interface**
rather than adding "skip this section if…". Splitting keeps every skill's context
free of instructions it must reason past. That is exactly how the single original
`pipeline-interfaces.md` became the three files above.

Splitting means: create the new `_shared/` file and repoint the affected `SKILL.md`
files at it. That is the whole operation — see [Skill lifecycle](/skill-lifecycle.md).

# Citations

* `skills/_shared/bundle-interfaces.md`, `skills/_shared/ledger-interfaces.md`, `skills/_shared/pipeline-interfaces.md`
* `meta/_shared/authoring-interfaces.md`
* `improve-skill/SKILL.md` — "How to write skill edits — the structural rules"
