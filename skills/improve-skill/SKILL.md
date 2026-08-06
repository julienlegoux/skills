---
name: improve-skill
description: Fold lessons from the current session back into the skill that caused them — diagnose from the conversation, propose a concrete edit, and after approval apply it to the skills repo and commit. Use whenever the user runs /improve-skill, says a skill misbehaved, or wants a skill updated with what this session taught.
---

# Improve Skill

Fold what just happened in this session back into the skill that caused it. The core loop: identify the skill → diagnose what went wrong → propose a concrete change → get approval → apply and commit.

## Where the skills live

One copy, not two. The repo is loaded **in place** as a plugin, so the file you edit is the file Claude Code runs — there is no install step and no mirrored copy to keep in sync.

```
<repo>/skills/<skill-name>/SKILL.md
<repo>/skills/_shared/*.md          ← the shared contracts, read as ../_shared/<file>
```

Resolve `<repo>` at the start of the run rather than assuming a path — it is cloned wherever its owner puts it. Take the first that holds `skills/_shared/`: a root the user or test harness names, the current working repo, or the target the `~/.claude/skills/*` junction points at. If none does, ask the user where their clone lives instead of guessing.

## Step 1: Identify the target skill

If the user named a skill, use it. Otherwise, scan the current conversation for skills that were invoked this session (Skill tool calls, `<command-name>` blocks, or the user following a skill's workflow). One obvious candidate → state your assumption and proceed ("I'll assume you mean `split-epics`, which we used earlier — stop me if not"). Several candidates or none → ask which skill they mean before doing anything else.

Then verify it lives in this repo: `<repo>/skills/<name>/SKILL.md` must exist. If it doesn't, this skill only manages skills in the repo — tell the user so, name where the skill actually lives (another plugin, a third-party install in `.claude/skills`, etc.), and suggest the skill-creator skill if they want to adopt it into the repo first. Don't edit anything outside `<repo>`.

## Step 2: Diagnose from the session

Before asking the user anything, do your own detective work. Reread the parts of the conversation where the skill was in play and look for:

- Places the user corrected course, repeated themselves, or expressed frustration
- Steps the skill's instructions caused to be skipped, botched, or done in the wrong order
- Things the session had to figure out from scratch that the skill should have anticipated
- What the user's `/improve-skill` arguments say, even if terse

Then read the skill's current SKILL.md (and any bundled files relevant to the problem) and locate which instruction — or missing instruction — produced the behavior. The goal is a specific diagnosis: "the skill says X, which led to Y, but the session needed Z."

If after this you still can't tell what the user wants changed, ask — but ask narrow questions grounded in what you found ("was the problem the milestone step or the labels?"), not "what would you like to improve?".

## Step 3: Propose the change

Present the proposal before touching any file. Show:

1. **Diagnosis** — one or two sentences on what went wrong and why the current wording causes it
2. **The edit** — the affected passage as before/after (or "new section:" for additions), not a vague summary
3. **Rationale** — why this fixes the general case, not just today's incident

Then wait for explicit approval. If the user pushes back or refines, revise the proposal and re-present. Do not edit, commit, or reinstall anything before the user approves.

When drafting the edit, hold to the principles good skills are built on:

- **Generalize.** The session is one sample. Fix the class of failure, not the literal incident — a skill patched with today's file names or one-off details will fail tomorrow. If the fix only makes sense for this session, it belongs in the conversation, not the skill.
- **Explain why, don't just command.** Prefer "do X because Y" over bolded MUSTs. A model that understands the reason applies the instruction to situations the wording didn't anticipate.
- **Keep it lean.** If the diagnosis is that an existing instruction causes wasted work or confusion, the right edit is often a deletion or rewrite, not an addition. Watch total length — a SKILL.md creeping past ~500 lines needs restructuring, not more bullets.
- **Preserve identity.** Never change the `name` field or directory name; the description should only change when the problem is triggering (skill didn't fire when it should have, or fired when it shouldn't).

## How to write skill edits — the structural rules

The skills in this repo follow a deliberate context-engineering shape (single-source interfaces, slim descriptions, progressive disclosure, tiered prescriptiveness). Session-lesson edits must not erode it:

- **A lesson becomes a stated invariant with its why, not another prescriptive step.** Prefer judgment + rationale over new rules. Hard rules are reserved for two cases: irreversible/safety actions, and prompts consumed by smaller models (the implementer templates) — there, prescriptive is deliberate, not debt.
- **Shared formats and rules change in `_shared/` only.** Three interfaces, split by audience: `bundle-interfaces.md` (English content, bundle/link rules, reserved files, committing what you write — every skill that writes under `docs/`), `ledger-interfaces.md` (the decision doc — ledger-driven skills), `pipeline-interfaces.md` (epic/issue schemas, status lifecycle, GitHub facts — epic-to-PR skills). Never re-describe one of those inline in a SKILL.md; point to `../_shared/<file>` instead. There is one file on disk per interface and no generated copies, so an edit there is live for every skill that points at it. When a rule stops fitting its audience, split the interface rather than telling readers to skip sections, and repoint the skills that follow the new file.
- **New templates, recipes, and edge-case handling go to the skill's `references/`**, not the always-loaded SKILL.md body. SKILL.md holds the decision flow and invariants; bulk goes behind a pointer.
- **Frontmatter descriptions stay 1–2 sentences (what + when).** Never grow them back with trigger-phrase lists — the whole listing rides in every session's context, and a bloated description degrades routing for all skills, not just this one.
- **Never soften hard guardrails when rewording around them.** Never-squash, no direct push to the integration branch, and union bookkeeping resolution are irreversible-safety rules; an edit that turns one into "prefer to..." is a regression even if it reads better.

## Step 4: Apply and commit

Once approved:

1. **Apply** the approved edit. The file you edit is the one Claude Code loads — no install step follows.
2. **Commit** with a message that captures the lesson, so history reads as a changelog of what each session taught:
   ```
   git -C <repo> add skills/<skill-name> && git -C <repo> commit -m "improve <skill-name>: <what changed and why>"
   ```
   If the folder isn't a git repo (fresh machine), `git init` it and make an initial commit of everything first.
3. **Tell the user to run `/reload-plugins`** to pick the change up in the current session. It reloads plugins, skills, agents and hooks without a restart. A changed frontmatter `description` affects *triggering* and may need a fresh session instead.

If the edit touched a file under `_shared/`, say which skills obey it — a shared contract changes behaviour well beyond the skill you were asked to fix, and the user deserves to know the blast radius before it surprises them mid-pipeline.

Finish by confirming what changed in one or two sentences.
