---
name: plan
description: Turn a need — three words from a non-technical user or a full brief — into an approved docs/PLAN.md by interviewing the user about what they need, never about technology, then hand straight to build, which runs unattended to the finished product. Use when someone wants something built or changed and no approved plan covers it yet.
---

# Plan

This is the only stage where the user is asked anything. After their "go", `build`
runs to the finished product without them — so this conversation has to surface what
only they know, and the plan has to carry it.

## The interview

Assume the person may never have written code. They know their problem; they do not
know, and should not need to know, how software is made.

- **Look up facts, ask only for what lives in their head.** Read the repo, existing
  docs and whatever they gave you before asking anything. What only they know: who
  uses this, what those people do today, what "it works" looks like to them, hard
  constraints (deadline, budget, where it must run, accounts and data that already
  exist), and what it must never do.
- **Never ask a question they would need you to explain first.** Stack, architecture,
  hosting, data model and tooling are yours to decide. If a technical user volunteers
  a preference, it is a constraint — but do not go fishing for one.
- **Propose, don't quiz.** "I'd have it send you an email each morning with the list —
  does that fit?" gets a better answer than "how should notifications work?". When a
  sensible default exists, state it as your assumption instead of asking.
- **Converse.** A few questions per turn, in their vocabulary, following up on what
  they say. Stop as soon as you could describe the first version back to them and
  they would recognise it. A complete brief earns zero questions.
- **Cut the first version yourself**: the smallest thing that solves their problem end
  to end. Everything else goes under "later", visibly, so nothing they said is lost.

On an existing codebase the same applies, with more to read first: the code tells you
the stack, the conventions and the blast radius of the change. None of that is a
question.

## The plan

Write `docs/PLAN.md` — in English, whatever language the conversation is in, because
later sessions and tools read it. If one already exists, this is a change to a living
plan: extend it with new milestones rather than starting over. Shape is yours; it must
let a fresh session build the right thing without this conversation:

- **Need** — the problem, the users, what they do today.
- **Outcomes** — what a user can do when this is done, each one observable enough to
  be checked by running the product. These are the build's definition of done.
- **Not in this version** — what was parked, and why.
- **Technical decisions** — stack, architecture, data, auth, where it runs; one line of
  why each. Prefer boring and well-supported; on an existing codebase, what is already
  there. Quality rules are not decided here: they are fixed in
  `../build/references/standards.md`, and a project's own documented conventions
  override them.
- **Milestones** — ordered, each one something that runs and can be shown.
- **Needed from the user** — accounts, keys, content, access, payments: everything no
  agent can supply, with how to get each one. Check what you can check now (is the
  tool installed, does the key work) rather than assuming.
- **Assumptions** — the ones that would be expensive to reverse.

## The go

Read the plan back in their language, without jargon: what they will be able to do,
what is left for later, what you need from them, and anything that costs money or
becomes publicly visible. Then ask for the go — once. If they correct something,
adjust and show only what changed.

Collect what you need from them now. A build that stops at milestone three for an API
key has failed at the one thing this stage exists for.

Their go authorises everything the plan describes. Commit the plan, then invoke
`build` in the same turn — do not ask whether to start, and do not come back until the
product is finished or something only they can do stands in the way.

If this skill's own instructions caused a problem during the run, that is for
`feedback` — silently, never as a question to the user.
