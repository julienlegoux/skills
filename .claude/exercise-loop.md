# Exercise loop

One iteration: take one tiny project through the whole lx pipeline with you playing
the user, watch where the run departs from what the skills say, and report each
departure through the `feedback` skill. Run it from an empty working folder, outside
the skills repo, so the run under observation sees nothing but the plugin.

## Before the run

Read the `plan`, `build`, `review` and `feedback` skills of the lx plugin: they are
the yardstick, and you will have to quote them.

Read `log.md` in the working folder if it exists, then choose a need it has not
covered. Vary it across iterations: the kind of thing (a command-line tool, a static
page, a small local web app, a script, a change to a project an earlier iteration
left behind), the person (someone who has never written code and gives one line;
someone technical who gives a complete brief), and the language they speak.

Keep it small — an hour of building at most — and local: nothing that needs an
account, a key, a payment, a deployment or a remote repository. Nobody is there to
supply them, and nothing outward-facing should happen unattended.

## The run

Start a fresh subagent in a new empty subfolder and give it only the person's opening
message, as if they had typed it, with the instruction to handle it with the lx `plan`
skill. It must not know it is being exercised: nothing about this file, about what you
watch for, or about feedback.

You are the person. Each time the subagent comes back, reply to that same subagent, in
character:

- Answer the way that person would: briefly, in their words, knowing their problem
  and nothing about how software is made — unless the persona is technical.
- Asked something that person could not answer, say so as they would.
- Give the go when what is read back matches what they wanted, and correct it when it
  does not.
- After the go, the person has left. If the subagent returns with anything other than
  the finished product or a need only a human can meet, note it, and answer only
  "decide yourself and carry on".

## What you look for

When the run ends, check it against the skills' own text and against reality: read
`docs/PLAN.md` and `docs/PROGRESS.md`, then use the product yourself and try every
outcome the plan promises.

An irregularity is one of:

- **`ignored`** — a skill says it, and the run did not do it: a technical question put
  to the user, a questionnaire, a question after the go, a build declared finished
  whose outcomes do not hold, no review, a decision made and not recorded.
- **`wrong`, `contradictory`, `missing`** — the run followed the skill, and the skill
  is what led it astray or left it without guidance.
- **`wasted`** — a step the skill required cost real effort and changed nothing.

It is not an irregularity when the model wrote a bug and the pipeline caught and fixed
it — that is the pipeline working — nor when the cause is the harness, a tool or an
outage.

## Reporting

Report each irregularity through the `feedback` skill, quoting the sentence of the
skill it concerns — once per sentence per iteration. Finding nothing is a result: do
not look for something to say.

If the feedback script answers that there is nothing to do here, the session is not
signed in as a maintainer and nothing is being recorded: stop the loop and say so.

Then append one line to `log.md`: the date, the need, the persona, whether the
product works, and what was reported. Leave the project folder in place.
