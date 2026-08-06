---
name: improve-skill
description: Fold lessons from the current session back into the skill that caused them — diagnose from the conversation, propose a concrete edit, and after approval apply it to the skills repo and commit. Use whenever the user runs /improve-skill, says a skill misbehaved, or wants a skill updated with what this session taught.
---

# Improve Skill

Fold what just happened in this session back into the skill that caused it. The core loop: identify the skill → diagnose what went wrong → propose a concrete change → get approval → apply and commit.

## Where the skills live

One copy, not two. Everything is junctioned into place, so the file you edit is the file Claude Code runs — there is no install step and no mirrored copy to keep in sync.

```
<repo>/skills/<name>/       ← published in the lx plugin
<repo>/meta/<name>/         ← the authoring tools, installed on their own
```

**Resolve `<repo>` first**, before anything else, rather than assuming a path — it is cloned wherever its owner puts it, and this skill is installed outside it. Take the first that holds `skills/_shared/`: a root the user names, the current working repo, or the target of a `~/.claude/skills/*` junction. If none turns up, say so and stop — without the clone there is nothing to edit and nothing to commit.

Then read `<repo>/meta/_shared/authoring-interfaces.md`, which defines the shape every skill here holds to.

## Step 1: Identify the target skill

If the user named a skill, use it. Otherwise, scan the current conversation for skills that were invoked this session (Skill tool calls, `<command-name>` blocks, or the user following a skill's workflow). One obvious candidate → state your assumption and proceed ("I'll assume you mean `split-epics`, which we used earlier — stop me if not"). Several candidates or none → ask which skill they mean before doing anything else.

Then verify it lives in this repo: `<repo>/skills/<name>/SKILL.md` or `<repo>/meta/<name>/SKILL.md` must exist. If neither does, this skill only manages skills in the repo — tell the user so, name where the skill actually lives (another plugin, a third-party install in `.claude/skills`, etc.), and suggest `create-skill` if they want to adopt it into the repo first. Don't edit anything outside `<repo>`.

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

Then wait for explicit approval. If the user pushes back or refines, revise the proposal and re-present. Do not edit or commit anything before the user approves.

The shape every skill in this repo holds to — the description contract, progressive disclosure, tiered prescriptiveness, the shared-contract rule, identity — is defined in `<repo>/meta/_shared/authoring-interfaces.md`. A session-lesson edit must not erode it, so read it before drafting.

Two things matter on top of that, because an edit is not a blank page:

- **Generalize.** The session is one sample. Fix the class of failure, not the literal incident — a skill patched with today's file names or one-off details will fail tomorrow. If the fix only makes sense for this session, it belongs in the conversation, not the skill.
- **Subtract before adding.** When the diagnosis is that an existing instruction caused wasted work or confusion, the right edit is a deletion or a rewrite. A skill only ever grows if every lesson becomes a new bullet.

## Step 4: Apply and commit

Once approved:

1. **Apply** the approved edit. The file you edit is the one Claude Code loads — no install step follows.
2. **Commit** with a message that captures the lesson, so history reads as a changelog of what each session taught:
   ```
   git -C <repo> add <skills|meta>/<skill-name> && git -C <repo> commit -m "improve <skill-name>: <what changed and why>"
   ```
   If the folder isn't a git repo (fresh machine), `git init` it and make an initial commit of everything first.
3. **Tell the user to run `/reload-plugins`** to pick the change up in the current session. It reloads plugins, skills, agents and hooks without a restart. A changed frontmatter `description` affects *triggering* and may need a fresh session instead.

If the edit touched a file under `_shared/`, say which skills obey it — a shared contract changes behaviour well beyond the skill you were asked to fix, and the user deserves to know the blast radius before it surprises them mid-pipeline.

Finish by confirming what changed in one or two sentences.
