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

## Changing things

Bump `version` in `.claude-plugin/plugin.json` when a skill's behaviour changes.
Before committing:

```
claude plugin validate .
python skills/okf-docs/scripts/validate_okf.py --help   # scripts still import
python skills/feedback/scripts/feedback.py --help
```

Changes to the skills arrive by pull request; `improve-skills` never merges its own.
