---
type: Playbook
title: "Skill lifecycle"
description: "How a skill is created, edited, validated, committed and reinstalled — including the improve-skill loop that folds session lessons back into the source."
tags: [playbook, development, improve-skill, workflow]
timestamp: 2026-08-06
---

# Skill lifecycle

Skills are **developed in the dev repo and installed from it**. Two roots, and only
one of them is ever edited:

| Root | Path | Role |
|---|---|---|
| Dev | `D:\Project\skills\<skill>\` | Source of truth. All edits go here. |
| Installed | `%USERPROFILE%\.claude\skills\<skill>\` | What Claude Code actually loads. Overwritten on every reinstall. |

Editing the installed copy is the one mistake that loses work silently: the next
reinstall mirrors over it. `improve-skill` checks for that drift before touching
anything.

# The loop

```
edit dev copy → sync _shared → validate → commit → reinstall
```

1. **Edit** `<skill>/SKILL.md` (and its `references/`, `assets/`, `scripts/`).
2. **Sync** if a shared contract changed:
   ```powershell
   pwsh _shared/sync.ps1
   ```
3. **Validate** the plugin manifest:
   ```
   claude plugin validate .
   ```
4. **Commit** — history reads as a changelog of what each session taught.
5. **Reinstall**:
   ```powershell
   pwsh improve-skill/scripts/reinstall.ps1 -SkillName <skill>
   ```
   It runs `_shared/sync.ps1` first, then mirrors dev → installed with
   `robocopy /MIR`, excluding dev-only artifacts (`evals/`, `.git`, `viewer.log`).

If the edit touched a shared interface, **reinstall every skill in that file's
audience**, not just the one being improved — each installed copy embeds its own
snapshot. Read the audience map in [Shared interfaces](/shared-interfaces.md).

New instructions take effect the next time the skill is invoked. A changed
frontmatter **`description`** affects triggering and may need a fresh session to be
picked up.

# improve-skill: the whole loop in one pass

`improve-skill` exists so that a lesson learned mid-session doesn't evaporate at the
end of it. Its steps:

| Step | What happens |
|---|---|
| 1. Identify | Which skill caused the behavior — from the user, or by scanning the session |
| 2. Diagnose | Reread where the skill was in play; locate the instruction (or missing instruction) that produced it. Goal: "the skill says X, which led to Y, but the session needed Z" |
| 3. Propose | Diagnosis + the edit as before/after + rationale. **Wait for explicit approval** — nothing is written first |
| 4. Apply | Edit dev copy → commit → reinstall. All three, or the change is a silent no-op |

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

* `improve-skill/SKILL.md`
* `improve-skill/scripts/reinstall.ps1`
* `_shared/sync.ps1`
