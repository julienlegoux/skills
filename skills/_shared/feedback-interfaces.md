# Feedback interfaces

Single source of truth for what a skill does with what it learned **about itself**
during a run: the closing check that decides whether this run taught something worth
carrying out of the session, and where that lesson goes. Skills learn things about
themselves constantly — a step that reads wrong, an instruction that sent the run down
a path the user had to correct — and without this reflex the lesson dies with the
session that paid for it.

Its audience is **every skill under `skills/` except `send-feedback`**. Stated as a
rule rather than as a list, because a list goes stale the next time a skill is created
and a rule does not: a new skill joins the audience the day it exists.

`send-feedback` is the exclusion because it *is* the destination. A `send-feedback` run
ending by proposing feedback about `send-feedback` is a loop with no floor — the output
of the reflex would be another instance of the thing that just ran.

This is deliberately its own file rather than a section of `bundle-interfaces.md`: none
of this concerns writing under `docs/`, and the audience is a different, larger set —
`okf-docs` and `okf-lint` obey this contract and not that one.

This is the one and only copy: every skill that obeys these rules reads this file at
`../_shared/feedback-interfaces.md`. Editing it changes behaviour for all of them at
once.

## When it fires

Once, at the end of the run, after the deliverable has been reported. Never mid-run and
never as an interruption: the user invoked the skill to get an epic, a report, a PR —
stopping to discuss the skill's own shortcomings while they wait makes its maintenance
their problem at the moment they care least.

**A skill running as a delegated subagent has no user to route to.** Neither
destination below can be reached from there — one edits a repo the supervisor owns, the
other posts under the user's account — so name what cleared the bar in the final report
instead, in one line, and stop. The supervisor's own closing check is what carries it
the rest of the way.

## The bar — two filters, both must hold

| Filter | Passes | Does not pass |
|---|---|---|
| **Attribution** | caused by the skill, or workaroundable by the skill | the API was down, the user ran the wrong command, a tool bug |
| **Generality** | true on any project | "our monorepo has an odd layout" |

Attribution asks whether editing this skill could have changed the outcome. An outage
or a harness bug is real and worth a complaint, but not to the person who maintains the
skill — a tracker filling with things its owner cannot fix is a tracker nobody reads.
"Workaroundable" is what keeps a genuine external cause in scope when the skill could
have anticipated it: the tool is broken, and the skill could have said so before the
run wasted an hour.

Generality asks whether the fix would help the next project. This session is one
sample, and a skill patched with this repo's layout fails on the next one — the lesson
has to name the *class* of failure, not the incident.

## Silence when the list is empty

Which is most runs, and ending silently is the design rather than a shortcut. **Do not
offer, do not ask, do not mention that there was nothing to report — just end the run.**
A skill that closes every run with "anything to report?" trains the user to answer no
without reading, and the reflex is then worth nothing on the one day it had something
to say. The bar above is only a bar if it is allowed to reject.

## Routing

Two destinations, and the choice is the user's once they can see it:

- **`improve-skill`** — a clone of the skills repo is at hand *and* the fix is
  happening now. The lesson becomes an edit and a commit in the same session that
  learned it.
- **`send-feedback`** — otherwise. The lesson becomes an issue on
  `julienlegoux/skills`, which is what makes it survive a session that has no clone,
  no push rights, or no appetite for a detour.

The discriminator is not "does the user have a clone" alone. A session with a clone can
still legitimately want `send-feedback` — when the lesson needs recording upstream
rather than fixing on the spot, because it deserves discussion, or because the run in
progress is not the moment to edit the skill running it. So name both routes and what
separates them, and let the user pick; swapping one name for the other decides
something that was theirs to decide.

## Never fix the running skill mid-run

Do not edit a skill's own assets, references or shared contracts to apply the lesson
unless the user says to. The run is producing a deliverable under the instructions as
they stand, and changing those instructions underneath it means the output no longer
matches any single version of the skill — nor can the user tell what the run decided
from what it quietly rewrote.

Where the running skill keeps a decision record, note the suggestion there instead
(`define-conventions` does this in the decision doc's Verdict section). That way it
survives the session even when the user takes neither route.
