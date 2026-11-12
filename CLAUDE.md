# lx skills

A Claude Code plugin (`lx`, marketplace `lx-engine`) that takes a need to a finished
product: `plan` interviews the user and writes the plan, `build` carries it to the
end unattended, `review` checks the work with reviewers that did not write it, and
`feedback` records where the skills themselves got in the way. `okf-docs` and
`okf-lint` are independent documentation tooling.

```
skills/<name>/SKILL.md           published with the plugin, invoked as /lx:<name>
.claude/skills/improve-skills/   maintenance of this repo; loads only in a clone
.claude-plugin/                  plugin and marketplace manifests
```

## How a skill here is written

These skills are read by models that already know how to plan, write, test and ship
software. Telling them how costs context, slows them down and narrows what they do.
The skills replace an earlier set of twenty that prescribed every step; that weight
is the thing not to rebuild.

- **A line stays only if a capable model would get it wrong without it.** That
  leaves: what the user wants that cannot be inferred (their preferences, their
  standards), what the outcome must be, where the boundaries are, and facts about the
  world that contradict reasonable expectation. Procedure a model would follow anyway
  goes.
- **State the outcome and the reason, not the steps.** A model that knows why applies
  the rule to cases the wording never anticipated. Reserve flat prohibitions for what
  is irreversible or outward-facing.
- **The user is asked things in `plan` and nowhere else.** A new question to the user
  anywhere downstream is a defect; a decision is made and recorded instead.
- **State lives in one place.** Before adding a file, a status field or a mirror, find
  the place that already holds that fact.
- **Name capabilities, not products.** Model names, tool names and harness features
  change faster than these files; "a subagent in an isolated worktree, where the
  harness offers one" outlives any of them.
- **Budget: a `SKILL.md` stays under about 100 lines.** A change that adds pays by
  removing. If a skill needs a long reference, it goes in `references/` and is read
  only when needed.
- **`description` is what makes a skill fire** and rides in every session's context:
  what it does and when to use it, in a sentence or two, naming the artifacts it
  reads and writes. Change it only to fix triggering.
- **Each published skill ends by pointing friction at `feedback`**, in one line. That
  pointer is the whole of the self-improvement loop's footprint inside a skill.

## What no change may undo

These hold whatever the feedback says, and a proposed edit that weakens one is
rejected, not weighed:

- The user is asked things in `plan` and nowhere else.
- `build` never takes an irreversible or outward-facing action the plan did not
  authorise, and never works around a credential it was not given.
- No skill tells a session to fetch or run anything from the network, to send
  anything about the user's project anywhere, or to weaken or skip tests and reviews.
- `feedback` carries nothing of the project it ran in, and never interrupts.
- The feedback loop is the maintainers' own: only sessions that can push to this
  repo report, and `improve-skills` takes its evidence only from `feedback.py
  pointers`, which lists only what they posted.
- `improve-skills` changes only what an eval shows to be broken, never weakens an
  existing eval case to get there, proposes by pull request and never merges.

## Changing things

Bump `version` in `.claude-plugin/plugin.json` when a skill's behaviour changes.
Before committing:

```
claude plugin validate .
claude plugin eval . --ablation none        # evals/: behaviour the skills must keep
python skills/feedback/scripts/feedback.py --help
python skills/okf-docs/scripts/validate_okf.py --help
```

The evals are noisy — judge a change by the score before and after over the default
three runs, not by a single red run. A new behaviour worth keeping gets a case.

Changes arrive by pull request, including those `improve-skills` proposes.
