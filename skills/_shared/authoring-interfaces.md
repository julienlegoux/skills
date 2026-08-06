# Authoring interfaces

How a skill **in this repo** is shaped. The three sibling interfaces
(`bundle-`, `ledger-`, `pipeline-`) define what skills write into a *user's*
project; this one defines how the skills themselves are written. Its audience is the
meta-skills — `create-skill` and `improve-skill` — and anything else that adds to or
edits `skills/`.

This is the one and only copy: both read it at `../_shared/authoring-interfaces.md`.

## Where a skill lives

```
<repo>/skills/<name>/SKILL.md
```

Every folder under `skills/` holding a `SKILL.md` is discovered automatically — there
is no registry to update. `skills/_shared/` has no `SKILL.md`, so discovery skips it
while staying readable by its neighbours at `../_shared/<file>`.

The repo is loaded in place as the `lx` plugin, so the file you edit is the file that
runs. Skills are namespaced: `/lx:<name>`.

## Anatomy

| Path | Role |
|---|---|
| `<name>/SKILL.md` | Always loaded once the skill fires. The decision flow and the invariants — not bulk. |
| `<name>/references/` | Progressive disclosure: templates, schemas, edge cases, read only when needed. |
| `<name>/assets/` | Files the skill copies or instantiates into a user's project. |
| `<name>/scripts/` | Executables the skill runs. |
| `<name>/agents/` | Subagent definitions, where the skill delegates. |

Create only the folders the skill actually uses. An empty `references/` is noise.

## The description contract

The frontmatter `description` is the routing surface: it decides whether the skill
fires at all, and **every skill's description rides in every session's context** —
including sessions that will never use it.

- One or two sentences: *what it does* + *when to use it*.
- Never a list of trigger phrases. It bloats the always-on cost and degrades routing
  for every other skill, not just this one.
- Name the artifacts it consumes and produces — that is what a router can match on.

## Progressive disclosure

`SKILL.md` holds the decision flow and the invariants. Templates, recipes, schemas
and edge-case handling go behind a pointer in `references/`. A `SKILL.md` creeping
past ~500 lines needs restructuring, not more bullets.

## Tiered prescriptiveness

Default to judgment plus rationale: *"do X because Y"* beats a bolded MUST, because a
model that understands the reason applies it to cases the wording never anticipated.

Hard, prescriptive rules are reserved for two cases:

1. **Irreversible or safety-critical actions** — never squash, no direct push to the
   integration branch, union resolution of bookkeeping conflicts.
2. **Prompts consumed by smaller models** (the implementer templates). There,
   prescriptive is deliberate, not debt.

Never soften a hard guardrail while rewording around it. Turning one into "prefer
to…" is a regression even when it reads better.

## Shared contracts

Anything more than one skill agrees on lives in `_shared/` — once. Point at
`../_shared/<file>`; never restate its content inline, and never copy it into a
skill's `references/`. Editing a shared file is live for every skill pointing at it,
so name the blast radius when you touch one.

When a rule stops fitting part of an interface's audience, **split the interface**
rather than writing "skip this section if…". Splitting keeps every skill's context
free of instructions it must reason past.

## Identity

A skill's `name` and folder never change once it exists — renaming breaks every
reference to it. The `description` changes only when the problem is *triggering*: it
fired when it shouldn't have, or didn't when it should.

## Ship it

```
claude plugin validate .              # manifests parse
claude plugin details lx@skills-dir   # the skill is actually discovered
```

The second command is the real test. A manifest can validate while discovering
nothing, so read the inventory rather than trusting the green check.

Then commit — history reads as a changelog of what each session taught — and tell the
user to run `/reload-plugins`. A changed `description` affects triggering and may need
a fresh session instead.
