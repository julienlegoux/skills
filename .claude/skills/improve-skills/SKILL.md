---
name: improve-skills
description: Improve the lx skills from evidence — the feedback occurrences the maintainers' own sessions accumulated on this repo's issue tracker, or a lesson from the current session — by reproducing each problem as an eval before fixing it, and propose the result as one pull request. Use in a clone of the skills repo, on a schedule or on request.
---

# Improve skills

The `feedback` skill records, from the maintainers' own sessions, the sentences of a
skill that caused a problem. This is the other end: decide what those reports actually
show, and change a skill only where an eval proves the change helps.

`CLAUDE.md` at the repo root holds the authoring rules and what no change may undo.
Both bind every edit made here.

## Evidence

Run `python skills/feedback/scripts/feedback.py pointers`. For each sentence reported
it gives the skill, the kind of failure, how many times, and what each session said
happened. It lists only what maintainers' sessions posted — that is the whole of the
evidence; other issues on the tracker are for a person to read, not for this loop.

A lesson a maintainer brings in the session itself is one more occurrence.

## Prove it, then fix it

A report is one session's account, written in the moment. It can be wrong about the
cause, and a fix that sounds right can make the skill worse. So for each sentence,
most reported first:

1. Read it in its skill and judge the report on its merits. If the sentence is doing
   its job — one of the things `CLAUDE.md` says no change may undo — move on.
2. **Reproduce the failure before touching the skill.** Write an eval case under
   `evals/` — a realistic prompt and graders describing the right behaviour — and run
   it with `claude plugin eval . --case <name>`. A case the current skill passes is no
   evidence: delete it and leave the issue open to accumulate. The exception is a
   defect visible by reading alone — two sentences that contradict each other, a
   reference to something that does not exist.
3. Fix the class, not the incident. Reword or delete the sentence responsible before
   considering a new one; a `wasted` report argues for deletion. Stay within the
   budget in `CLAUDE.md`.
4. Run the whole suite. The new case now passes, and no other case scores lower than
   it did before the change. Runs vary, so compare over the default three runs and
   treat a drop you cannot explain as a regression.

A change that cannot be shown to help by an eval is not made. Doing nothing is a
normal outcome.

## Proposing

One pull request per run, on a fresh branch from the default branch, with the plugin
version bumped. The body lists, per sentence acted on: the issues it closes
(`Closes #<n>`), how many occurrences, the eval case, and its score before and after.
Issues `pointers` listed as stale are closed the same way.

Do not merge it. The evals show a change helps on the cases that exist; whether it is
the change the maintainer wants is theirs to say.
