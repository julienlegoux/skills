---
name: improve-skill
description: Improve an existing skill based on how it performed during the current session. Use whenever the user runs /improve-skill, complains that a skill misbehaved or underperformed, says things like "the X skill should have done Y", "update the skill so it...", "that skill missed a step, fix it", or wants to fold lessons learned this session back into a skill — even if they don't name a specific skill. Diagnoses the problem from the conversation, proposes a concrete edit, and after approval updates the dev copy in D:\Project\skills, commits it, and reinstalls to ~/.claude/skills.
---

# Improve Skill

Fold what just happened in this session back into the skill that caused it. The core loop: identify the skill → diagnose what went wrong → propose a concrete change → get approval → apply, commit, reinstall.

## Paths

- **Dev root** (source of truth): `D:\Project\skills\<skill-name>\`
- **Installed root** (what Claude Code actually loads): `%USERPROFILE%\.claude\skills\<skill-name>\`

Never edit the installed copy directly — it gets overwritten on reinstall. All edits go to the dev copy. If the user or a test harness specifies different roots, use those instead.

## Step 1: Identify the target skill

If the user named a skill, use it. Otherwise, scan the current conversation for skills that were invoked this session (Skill tool calls, `<command-name>` blocks, or the user following a skill's workflow). One obvious candidate → state your assumption and proceed ("I'll assume you mean `split-epics`, which we used earlier — stop me if not"). Several candidates or none → ask which skill they mean before doing anything else.

Then verify the skill has a dev copy: `D:\Project\skills\<name>\SKILL.md` must exist. If it doesn't, this skill only manages skills developed in the dev folder — tell the user so, name where the skill actually lives (a plugin, a third-party install in `.claude\skills`, etc.), and suggest the skill-creator skill if they want to adopt it into the dev folder first. Don't edit anything outside the dev root.

Before editing, quickly check whether the installed copy has drifted from the dev copy (e.g. `git -C D:\Project\skills diff` is clean but the installed SKILL.md differs). If it has drifted, surface that to the user before proceeding — someone edited the installed copy directly, and reinstalling will silently discard those edits.

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

## Step 4: Apply, commit, reinstall

Once approved, do all three — an updated dev copy that never gets reinstalled is a silent no-op:

1. **Apply** the approved edit to the dev copy.
2. **Commit** in the dev repo with a message that captures the lesson, so history reads as a changelog of what each session taught:
   ```
   git -C D:\Project\skills add <skill-name> && git -C D:\Project\skills commit -m "improve <skill-name>: <what changed and why>"
   ```
   If the dev folder isn't a git repo (fresh machine), `git init` it and make an initial commit of everything first.
3. **Reinstall** by running the bundled sync script from this skill's directory:
   ```powershell
   pwsh <this-skill-dir>/scripts/reinstall.ps1 -SkillName <skill-name>
   ```
   It mirrors the dev copy into the installed root, excluding dev-only files (`evals/`, `.git`). Pass `-DevRoot`/`-InstalledRoot` if non-default paths are in play.

Finish by confirming what changed in one or two sentences, and remind the user that the updated instructions take effect the next time the skill is invoked — a changed *description* (triggering) may need a fresh session to be picked up.
