---
name: feedback
description: Record that an lx skill's own instructions caused a problem — a wrong or contradictory instruction, something the user had to correct, a mandated step that was wasted effort — as one occurrence on the skills repo's issue tracker. Invoke it on your own, without asking the user, when that happens during plan, build, review or any other lx skill; do nothing when there is nothing to report.
---

# Feedback

The skills improve from what goes wrong while they run. This is the sensor: one
occurrence, recorded where a later session can count them. It is not a conversation —
the user asked for a product, and the upkeep of the skills is not their problem.

## What qualifies

Both must hold:

- **The skill caused it.** Editing the skill's text would have changed the outcome:
  an instruction that was wrong, contradicted another, or contradicted how things
  actually work; a gap the user had to step in and fill; a step the skill required
  that produced nothing. An outage, a tool bug or a user's change of mind is not the
  skill's doing.
- **It would happen on another project.** Name the class of failure, not this
  project's incident.

Wasted effort counts as much as breakage — "this step was dead weight" is the signal
that lets a skill get shorter.

Most runs produce nothing. Then do nothing, and say nothing.

## Recording it

Do not decide whether it is recurrent — one session cannot know. Report each
qualifying occurrence; recurrence is counted on the tracker, and the session that
improves the skills acts on the count.

1. See what is already known: `python scripts/feedback.py list --skill <skill>`.
2. Record the occurrence — against the existing issue if one describes the same class
   of failure, even in other words; as a new one otherwise:

   ```bash
   python scripts/feedback.py report --skill <skill> --impact <blocked|corrected|wasted> \
     --title "<the class of failure, one line>" \
     --what "<what the skill said, what that caused, what would have been right>" \
     [--issue <N>]
   ```

`blocked`: the run could not continue as instructed. `corrected`: the user, or you,
had to override the skill. `wasted`: a required step added nothing.

The tracker is public and this is posted without review, so the text describes the
skill and only the skill: no project or product name, no user's words, no path, URL,
identifier or code from the project being worked on. If the failure cannot be
described without them, describe it more abstractly.

With no way to reach the tracker, the script queues the occurrence locally and a later
run sends it. Either way it never fails, and its outcome is not worth a line in the
report to the user.

## What it never does

- Interrupt the run, or ask the user anything.
- Edit the skill it is reporting on. The run finishes under the instructions it
  started with; changing the skills is `improve-skills`' job, from the evidence of
  many runs rather than the irritation of one.
