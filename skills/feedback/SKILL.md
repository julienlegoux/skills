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
improves the skills acts on the count. One command, and no reading of the tracker:

```bash
python scripts/feedback.py report --skill <skill> \
  --kind <wrong|contradictory|missing|wasted> \
  --quote "<the sentence or heading of the skill at fault, exactly as written>" \
  --what "<what it caused, and what would have been right>"
```

- `wrong` — the instruction is incorrect, or contradicts how things actually work.
- `contradictory` — two instructions conflict; quote one of them.
- `missing` — a gap you or the user had to fill; quote the heading it belongs under.
- `wasted` — a required step that added nothing.

The quote is the address: every session that trips on the same sentence lands on the
same issue, which is how occurrences add up without anyone comparing descriptions.
The script refuses a quote that is not in the skill.

The tracker is public and this is posted without review, so `--what` describes the
skill and only the skill: no project or product name, no user's words, no path, URL,
identifier or code from the project being worked on. If the failure cannot be
described without them, describe it more abstractly.

Only the skills' maintainers feed this loop: the script posts when the session is
signed in as someone who can push to the skills repo, and does nothing anywhere else.
Either way it never fails, and its outcome is not worth a line in the report to the
user.

## What it never does

- Interrupt the run, or ask the user anything.
- Edit the skill it is reporting on. The run finishes under the instructions it
  started with; changing the skills is `improve-skills`' job, from the evidence of
  many runs rather than the irritation of one.
