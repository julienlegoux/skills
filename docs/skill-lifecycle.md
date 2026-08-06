---
type: Playbook
title: "Skill lifecycle"
description: "How a skill is created, edited, validated and committed — one copy loaded in place, plus the improve-skill loop that folds session lessons back into the source."
tags: [playbook, development, improve-skill, workflow]
timestamp: 2026-08-06
---

# Skill lifecycle

There is **one copy of every skill**: `<repo>/skills/<skill>/`. Claude Code loads the
repo in place as a plugin — see [Installation and delivery
modes](/installation.md) — so the file you edit is the file that runs. No install
step, no mirror, no drift to check for.

`<repo>` is wherever the clone lives; nothing hardcodes a path.

# The loop

```
edit → validate → commit → /reload-plugins
```

1. **Edit** `skills/<skill>/SKILL.md` (and its `references/`, `assets/`, `scripts/`).
   Shared contracts change in `skills/_shared/` — one file, live for every skill that
   points at it.
2. **Validate** the plugin manifest:
   ```
   claude plugin validate .
   ```
   Then confirm the skill is still discovered — the inventory catches a folder that
   moved or a manifest that stopped matching:
   ```
   claude plugin details lx@skills-dir
   ```
3. **Commit** — history reads as a changelog of what each session taught.
4. **`/reload-plugins`** to pick the change up in the running session.

A changed frontmatter **`description`** affects triggering and may need a fresh
session to be picked up.

Editing a `_shared/` contract changes behaviour for every skill pointing at it, all
at once. That is the point of the design, and the reason to say out loud which skills
an interface edit reaches.

# improve-skill: the whole loop in one pass

`improve-skill` exists so that a lesson learned mid-session doesn't evaporate at the
end of it. Its steps:

| Step | What happens |
|---|---|
| 1. Identify | Which skill caused the behavior — from the user, or by scanning the session |
| 2. Diagnose | Reread where the skill was in play; locate the instruction (or missing instruction) that produced it. Goal: "the skill says X, which led to Y, but the session needed Z" |
| 3. Propose | Diagnosis + the edit as before/after + rationale. **Wait for explicit approval** — nothing is written first |
| 4. Apply | Edit → commit → tell the user to `/reload-plugins` |

# Editing principles

These are what keep a fourteen-skill repo from rotting into fourteen divergent ones:

* **Generalize.** One session is one sample. Fix the class of failure, not the literal
  incident. If a fix only makes sense for today, it belongs in the conversation.
* **Explain why, don't just command.** "Do X because Y" beats a bolded MUST — a model
  that understands the reason applies it to cases the wording never anticipated.
* **Keep it lean.** Often the right edit is a deletion. A `SKILL.md` creeping past
  ~500 lines needs restructuring, not more bullets.
* **Bulk goes to `references/`.** `SKILL.md` holds the decision flow and the
  invariants; templates, recipes and edge cases sit behind a pointer.
* **Descriptions stay 1–2 sentences.** They ride in every session's context; bloating
  one degrades routing for *all* skills.
* **Preserve identity.** Never change a skill's `name` or directory. Change the
  `description` only when the problem is triggering.
* **Never soften a hard guardrail.** Never-squash, no direct push to the integration
  branch, and union resolution of bookkeeping conflicts are safety rules. Rewording
  one into "prefer to…" is a regression even when it reads better.

Hard, prescriptive rules are reserved for two cases: irreversible or safety-critical
actions, and prompts consumed by smaller models (the implementer templates). Elsewhere,
judgment plus rationale.

# Citations

* `skills/improve-skill/SKILL.md`
* `.claude-plugin/plugin.json`
