# Authoring interfaces

How a skill **in this repo** is shaped. The interfaces under `skills/_shared/` govern
what the published skills do — what they write into a *user's* project, and how they
close a run; this one defines how the skills themselves are written. Its audience is
the two meta-skills, `create-skill` and `improve-skill`.

Because those two are installed on their own rather than shipped with the plugin,
they reach this file through the repo they resolve first — `<repo>/meta/_shared/` —
not through a path relative to their own folder.

## Two homes

| Home | What lives there | How it reaches a session |
|---|---|---|
| `<repo>/skills/<name>/` | the published skills | the `lx` plugin, namespaced `/lx:<name>` |
| `<repo>/meta/<name>/` | the authoring tools | installed by hand, junctioned into `~/.claude/skills/<name>`, invoked `/<name>` |

Every folder under `skills/` holding a `SKILL.md` is discovered automatically — there
is no registry to update, and a folder outside `skills/` is invisible to the plugin
unless listed explicitly. `_shared/` folders have no `SKILL.md`, so discovery skips
them.

A new skill belongs in `skills/` unless it authors this repo, in which case it joins
`meta/`. The test is whether someone who installed the plugin could use it: a skill
that needs a clone and a push cannot ship.

Both homes are junctioned rather than copied, so the file you edit is the file that
runs — there is no install step and nothing to keep in sync.

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

Anything more than one skill agrees on lives in `_shared/` — once. Never restate its
content inline, and never copy it into a skill's `references/`. Editing a shared file
is live for every skill pointing at it, so name the blast radius when you touch one.

How a skill points at one depends on how it travels. A published skill ships beside
its contracts and uses `../_shared/<file>`. A skill installed on its own can't — its
`..` is the install folder — so it resolves the repo first and reads
`<repo>/meta/_shared/<file>`.

When a rule stops fitting part of an interface's audience, **split the interface**
rather than writing "skip this section if…". Splitting keeps every skill's context
free of instructions it must reason past.

One of them is not optional: **every new skill under `skills/` points at
`feedback-interfaces.md`**, the closing reflex that decides whether a run taught
something about the skill itself worth carrying out of the session, and where it goes.
Add the pointer when the skill is written — a reflex that depends on someone
remembering it per skill is one that quietly stops existing. `send-feedback` is the
single exclusion, because it is the destination: a `send-feedback` run ending by
proposing feedback about `send-feedback` is a loop with no floor. Skills under `meta/`
are outside it for a structural reason rather than a judgment call — they do not
resolve `skills/_shared/` at all, and the contract's routing half has a constant answer
here anyway, since a clone and push rights are a meta-skill's entry condition.

## Identity

A skill's `name` and folder never change once it exists — renaming breaks every
reference to it. The `description` changes only when the problem is *triggering*: it
fired when it shouldn't have, or didn't when it should.

## Ship it

For a skill under `skills/`:

```
claude plugin validate .              # manifests parse
claude plugin details lx@skills-dir   # the skill is actually discovered
```

The second command is the real test. A manifest can validate while discovering
nothing, so read the inventory rather than trusting the green check.

For a skill under `meta/`, the equivalent is its junction — created once, at
creation time:

```powershell
New-Item -ItemType Junction -Path "$HOME\.claude\skills\<name>" -Target "<repo>\meta\<name>"
```

Then commit — history reads as a changelog of what each session taught — and tell the
user to run `/reload-plugins`. A changed `description` affects triggering and may need
a fresh session instead.
