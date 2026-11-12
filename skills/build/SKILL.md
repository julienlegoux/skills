---
name: build
description: Carry an approved docs/PLAN.md to the finished, verified product without the user — slice the work, implement, integrate, review, fix, verify — keeping state in docs/PROGRESS.md. Use right after a plan is approved, or to resume a build in progress.
---

# Build

The plan is approved. The job is the product it describes: working, verified against
the plan's outcomes, integrated. The user is not part of this stage — they asked for a
product, not for a project to supervise.

## Decide, don't ask

Every question the plan left open is yours to settle: pick the option that best serves
the plan's outcomes and the standards in `references/standards.md` (the project's own
documented conventions win where they exist), and write the decision down. A
recorded decision can be revisited; a build parked on a question cannot finish.

What the plan did settle is not open. Its outcomes and its technical decisions are
what the user approved, and the one you drop may be the one that decides, for them,
whether the product works. Depart from the plan only where it cannot work — a pinned
version that fails, an approach that breaks — never because another path is easier;
then take the nearest path that still delivers what was asked, and record it. Nothing
in the plan is dropped or put off.

Stop for exactly two things:

- **What only a human can supply** — a credential, an account, a payment, a physical
  device.
- **An irreversible or outward-facing action the plan did not authorise** — deploying
  to production, spending money, publishing something public.

Even then, first finish everything that does not depend on the answer, then ask once,
for all of it together.

## State

`docs/PROGRESS.md` is the one place build state lives, and the orchestrating session
is its only writer. Any shape, as long as a fresh session finds three things in it:
where each milestone and work unit stands, every decision and deviation with its
reason, and what is waiting on the user. With git history, it is how a resumed build
knows where it is — never redo finished work, never restart a unit that has a branch.

No second copy of that state: no per-task files, no status mirrored into labels or
boards. When the project lives on a forge, pull requests are how changes merge, not
where progress is tracked.

## The work

Slice a milestone into units when you reach it, not all up front — what milestone one
teaches reshapes milestone two. A unit is one coherent, reviewable change with its own
check that it works.

Independent units can run in parallel, each in an isolated worktree when the harness
offers subagents. Integrate them one at a time. Units that touch the same files are
not independent, whatever the dependency graph says. On a long build, delegating units
also keeps your own context for coordination — but that is a means; on a small plan,
write the units yourself.

Integrate on the branch the user named, else `develop` if the repo has one, else the
default branch. With a remote and CI: one pull request per unit, merged once the
required checks have passed on its head commit. Two things that look like green and
are not:

- A PR with **no** check runs is usually a PR in conflict — the forge does not build
  what it cannot merge. Look at mergeability before retriggering anything.
- A passing summary proves nothing if the required job never ran. Confirm it by name.

## Done means it works

Passing tests show the tests pass. Before calling a milestone done, use the product
the way the plan's outcomes describe: start it, exercise each outcome, and for an
interface, look at it rendered at phone and desktop widths. Do it on data you made
for the purpose — never on the user's own files or accounts, unless the plan says
so — and stop every process you started for it: a server left on a port answers the
next build's requests. Fix what you find.

At the end of each milestone, and once over the whole build at the end, run the
`review` skill — your own rereading is not it, whatever the size of the plan. Fix the
findings that survive its verification, then verify again. Reviews feed the loop;
they do not produce a backlog for the user.

## Finishing

The build is finished when every outcome in the plan is demonstrably true on the
integration branch, `review` has run over the whole of it and its findings are fixed,
and nothing the build started is still running — or when what is left is out of your
hands: waiting on the user, or on a review you have no means to start. Report in
their language, without jargon: what they can now do and how to start using it, where
the result differs from the plan and why, and what is left with what it needs from
them.

If this skill's own instructions caused a problem during the run, that is for
`feedback` — silently, never as a question to the user.
