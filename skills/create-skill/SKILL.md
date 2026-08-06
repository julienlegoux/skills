---
name: create-skill
description: Add a new skill to this repo — prove the need actually repeats, place it against the skills that already exist, draft it to the repo's authoring contract, then validate, commit and reload. Use when the user wants a new skill, or wants a recurring prompt or workflow turned into one.
---

# Create Skill

A skill exists because something **repeats**. Everything below serves that one test: most requests for a new skill are better served by a prompt, a `CLAUDE.md` line, or an edit to a skill that already exists — and adding one that shouldn't exist costs every future session, since its description rides in all of them.

The shape of a skill in this repo — anatomy, the description contract, progressive disclosure, tiered prescriptiveness — is defined once in `../_shared/authoring-interfaces.md`. Read it before drafting anything.

## Before anything: find the clone

New skills are written into a clone of this repo, committed, and pushed. Resolve it the same way `improve-skill` does: a root the user names, the current working repo, or the target of the `~/.claude/skills/*` junction — whichever holds `skills/_shared/`, and never a path under `~/.claude/plugins/`.

If none turns up, this machine installed the plugin rather than cloning it. Say so and stop: a skill written into an installed copy runs until the next marketplace update erases it, leaving nothing in git and nothing upstream.

## Step 1: Prove the need repeats

Ask the user for **two or more concrete past occurrences**. Not hypotheticals — times it actually happened. Then classify what you hear:

| What you find | What it should be |
|---|---|
| Repeats across projects, multi-step, decisions to make | A skill. Continue. |
| Happened once, or is one project's quirk | A prompt, or that project's `CLAUDE.md` |
| Repeats, but is a *rule* rather than a *procedure* ("always use pnpm") | `CLAUDE.md`, or the conventions baseline |
| Repeats, but an existing skill already owns the territory | An edit — hand it to `improve-skill` |

Say which one you landed on and why, in a sentence. If it isn't a skill, name the better home rather than just declining — the underlying need is real either way.

Don't stall on this. If the user has already argued the case, take it and move on.

## Step 2: Place it against what exists

Read the frontmatter descriptions of the skills under `skills/` before designing anything. Two questions:

**Does it overlap?** If an existing skill would plausibly fire for the same request, you have a boundary problem, not a new skill. Either extend the existing one, or carve an explicit boundary into *both* descriptions — a router can't split territory that two descriptions both claim.

**Which contracts does it inherit?** These are not optional once the skill touches the artifacts they govern:

| If the skill… | It must point at |
|---|---|
| writes anything under `docs/` | `../_shared/bundle-interfaces.md` |
| drives decisions through a ledger | `../_shared/ledger-interfaces.md` |
| reads or writes epics and issues | `../_shared/pipeline-interfaces.md` |

A skill that writes bundle files while ignoring the bundle rules produces output the rest of the pipeline can't consume.

## Step 3: Design the shape

Decide these before writing prose:

- **Name** — verb-noun, kebab-case, matching the folder (`create-issues`, `map-codebase`, `improve-skill`). It is permanent; renaming later breaks every reference.
- **The spine** — the decision flow, as steps. If you can't state it as a sequence with branch points, the skill isn't understood well enough to write yet.
- **The invariants** — what must hold however the run goes, each with its *why*.
- **What is bulk** — templates, schemas, long recipes, edge cases. That goes to `references/`, not the body.
- **Whether it delegates** — a subagent under `agents/` when the work needs a fresh context window rather than more instructions.

## Step 4: Propose before writing

Present, and wait for approval:

1. **The frontmatter `description`**, in full. It is the routing surface and the hardest part to get right — settle it before any prose.
2. **The section outline** — the spine as headings.
3. **What lands in `references/`**, and what each file is for.
4. **Which shared contracts it points at**, and the boundary against any neighbouring skill.

If the user pushes back, revise and re-present. Nothing is written before approval.

## Step 5: Write it

Create `skills/<name>/SKILL.md` and only the subfolders it genuinely uses.

Write the first version **small**. A skill earns its length from real failures, and `improve-skill` exists to add what sessions actually teach. Guessing at edge cases up front produces instructions no one needed and everyone must read past.

Point at `../_shared/<file>` for anything shared. Never restate a contract inline, and never copy one into `references/` — see the authoring interface for why.

## Step 6: Validate, commit, reload

```
claude plugin validate .
claude plugin details lx@skills-dir
```

The new name must appear in the inventory. If it doesn't, discovery didn't pick it up — a manifest that validates proves nothing about what was found.

Then commit, and tell the user to run `/reload-plugins`. A brand-new skill's description may need a fresh session before it starts triggering.

Finish by naming the first real occasion to use it — the next time the thing it was built for repeats.
