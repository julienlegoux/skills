---
name: create-skill
description: Add a new skill to this repo — prove the need actually repeats, place it against the skills that already exist, draft it to the repo's authoring contract, then validate, commit and reload. Use when the user wants a new skill, or wants a recurring prompt or workflow turned into one.
---

# Create Skill

A skill exists because something **repeats**. Everything below serves that one test: most requests for a new skill are better served by a prompt, a `CLAUDE.md` line, or an edit to a skill that already exists — and adding one that shouldn't exist costs every future session, since its description rides in all of them.

## Before anything: find the clone

New skills are written into a clone of this repo, committed, and pushed — and this skill is installed outside it, so resolve `<repo>` first. Take the first that holds `skills/_shared/`: a root the user names, the current working repo, or the target of a `~/.claude/skills/*` junction. If none turns up, say so and stop — there is nothing to write into.

Then read `<repo>/meta/_shared/authoring-interfaces.md`: anatomy, the description contract, progressive disclosure, tiered prescriptiveness, and the choice of home below.

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

- **Which home.** `skills/` ships in the `lx` plugin and reaches anyone who installs it. `meta/` stays out of the plugin and is junctioned in by hand. The test: could someone who installed the plugin — no clone, no push rights — actually use it? If it authors this repo, it can't, and it belongs in `meta/`. Everything else goes to `skills/`.
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

Create `<repo>/<home>/<name>/SKILL.md` and only the subfolders it genuinely uses.

Write the first version **small**. A skill earns its length from real failures, and `improve-skill` exists to add what sessions actually teach. Guessing at edge cases up front produces instructions no one needed and everyone must read past.

Never restate a shared contract inline, and never copy one into `references/`. A skill under `skills/` points at `../_shared/<file>`; one under `meta/` is installed away from the repo, so it resolves `<repo>` first and reads `<repo>/meta/_shared/<file>` — see the authoring interface for why.

## Step 6: Install, commit, reload

A skill in `skills/` is discovered by the plugin. Confirm it, because a manifest that validates proves nothing about what was found:

```
claude plugin validate .
claude plugin details lx@skills-dir     # the new name must appear
```

A skill in `meta/` isn't in the plugin, so give it its junction now — it is the only thing that makes it invocable:

```powershell
New-Item -ItemType Junction -Path "$HOME\.claude\skills\<name>" -Target "<repo>\meta\<name>"
```

Then commit, and tell the user to run `/reload-plugins`. A brand-new skill's description may need a fresh session before it starts triggering.

Finish by naming the first real occasion to use it — the next time the thing it was built for repeats.
