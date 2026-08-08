---
name: define-concept
description: Shape a raw idea into a validated product concept through open discussion, recording only what the user validates into docs/planning/CONCEPT.md — the optional stage upstream of define-scope. Use when the idea itself is still forming and the user wants to think it out loud rather than answer a decision ledger.
---

# Define Concept

Before a project can be scoped it has to *be* something. This skill covers the phase
that produces that: an open conversation about an idea, out of which a validated
concept gets written down.

It is deliberately the least structured skill in the pipeline, and it has no numbered
steps. The phase it covers is thinking, and thinking marched through a checklist stops
being thinking — the user came to work the idea out loud, not to fill a form. Your job
is to be a good interlocutor and to keep an honest record of what survived the
conversation.

**It is optional.** A project whose idea is already clear goes straight to
`define-scope`.

## The boundary with define-scope

CONCEPT answers **"is this the right thing to build?"**. SCOPE answers **"what is its
first version?"**. Reversed, a concept decision leaves you with a different product; a
scope decision leaves you with the same product shipped differently.

| `CONCEPT.md` holds | `SCOPE.md` holds |
|---|---|
| the problem, and who actually has it | which users v1 serves |
| what the product *is* — its shape, its promise, its behaviour | what v1 *ships* |
| why this, why now, and what people do today instead | milestones and phasing |
| business-model direction, positioning | success criteria, non-goals |
| constraints that are facts about the domain | how v1 responds to them |

So `CONCEPT.md` carries no MVP / post-MVP markers, no feature cut and no milestones.
Naming those here forces `define-scope` to re-litigate them from a document that has no
authority to have decided them — which is exactly what happened the last time this
phase ran without a skill.

## Three modes, no order

The user moves between these freely, many times, across many sessions. Follow; never
announce a transition or propose a plan of phases.

- **Explore** — the idea gets told, questioned, stretched, contradicted.
- **Challenge** — on request, you attack what is on the table: conflicts, gaps, cases
  nobody thought of, someone already doing it.
- **Record** — a piece the user has validated gets written down.

## How the conversation runs

Each of these fixes a real failure from the run that produced this skill.

1. **Ask in prose, one question at a time.** Never `AskUserQuestion`, never a menu of
   lettered options. A half-formed idea flattens into whichever option is nearest, and
   the long, wandering answer — the one that actually carries the idea — never gets
   written.
2. **Never lose the user's question to a tool call.** If they asked you something,
   answer it before you go research anything. Coming back from a search with findings
   and no answer reads as dodging, and it happens twice before anyone forgives it.
3. **Their thread has priority.** "We'll talk about X later" is binding: park X, raise
   it again when the current thread closes, and don't drop it.
4. **Let tangents run.** This phase has no clock and no agenda to protect. An hour
   spent somewhere adjacent is not drift to correct — the user knows what they came
   for, and half-formed ideas rarely arrive by the shortest route.
5. **Push back.** A concept that survived nothing but agreement has been tested by
   nobody. Name the conflict, the missing case, the competitor who already ships it.
   This is most of the value you add.
6. **Don't invent a constraint and present it as a finding.** A number you made up
   ("about three interventions per meeting") reads to the user as analysis. Say what is
   yours to propose, and mark it as a proposal.

## What lands on disk, and when

The conversation is loose; the record is not.

**Nothing is written until the user validates it.** They say when — "write that up",
"add it to the concept". Everything else stays in the chat, however promising it
sounded. A concept doc holding unvalidated speculation is worse than no doc: every
later reader, human or agent, treats it as decided.

`docs/planning/` is an [Open Knowledge Format](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)
(OKF v0.1) bundle — the same one `define-scope`, `define-specs` and `define-conventions`
write into, and this skill is usually the one that establishes it. The rules it obeys
(English on disk whatever language the conversation is in, bundle-relative links, the
reserved `index.md` / `log.md`, committing what you write) are in
`../_shared/bundle-interfaces.md`. Read it before writing anything. Note in passing:
`docs/` itself is never a bundle root — OKF v0.1 has no nested bundles, so a root there
stops the tree validating the moment `docs/planning/` claims its own.

```
docs/planning/
  index.md          # bundle root listing
  log.md            # bundle history — and this phase's ledger
  CONCEPT.md        # the deliverable, grown across the conversation
  DOMAIN.md         # optional; only if the user asks for it
```

**`log.md` is this phase's ledger.** There are no decision docs here — the phase is not
decision-shaped, and a ledger would impose the very structure this skill exists to
avoid. Instead every validated change appends a `log.md` entry saying what was settled
and *why it changed*, which is what a later reader needs and what a diff can't tell
them. It is also how a reopened question stays honest: the old entry stands, a new one
records the reversal.

**`CONCEPT.md`'s structure is emergent.** Open with the problem and with what the
product is; after that, the headings are whatever this particular idea turned out to
need — a capture model, a command surface, an attribution problem. Do not reach for a
template, and do not add an empty section because a generic product doc would have one.

**The project home.** This skill is usually the first thing to write to disk, so if the
conversation isn't already inside a repo, offer — once, before the first write — a
project folder named after the idea plus a **private** GitHub repo:

```bash
mkdir <name> && cd <name>
git init -b main
git commit --allow-empty -m "chore: initial commit"
gh repo create <name> --private --source=. --remote=origin --push
git checkout -b develop && git push -u origin develop
```

Private because a repo goes public later with one command and never comes back;
`develop` because that is the branch the rest of the pipeline integrates on. If the
user declines, drop it and never raise it again — write where you are, say once that
there is no repo, and never block the record on it. `define-scope` makes the same offer
when this skill was skipped, and skips it when a remote already exists.

## The critique pass

When the user asks what's wrong with the concept — and it is worth offering once the
doc has real substance — read it whole and hunt for contradictions, unaddressed cases,
concepts that collide, and claims the market already answers. Research is welcome here;
so is going and reading what competitors actually do.

Hold the results as a **disposable** list in a scratch file outside the bundle, and walk
it one question at a time. It never becomes a bundle artifact, and it has no authority:
when a question turns out to be uninteresting, or an answer three questions in makes the
next five moot, drop them and say so. The list serves the conversation, not the reverse.

## The conceptual domain model

Only if the user asks. `DOMAIN.md` names the entities, their relationships and their
lifecycles **in the language of the domain** — no tables, no storage, no framework.
Build it one domain at a time, validating each before starting the next; the value is in
the vocabulary being agreed, not in the diagram existing.

It is worth having for a reason that only shows up much later: the implementers
downstream are separate agents that never attended this conversation, and a fixed
vocabulary is what keeps them from each inventing their own. Say explicitly what is
deliberately *not* modelled — an entity nobody wants is cheaper to refuse once here than
in four PRs.

The physical model — tables, keys, storage engine — belongs to `define-specs`. If the
conversation starts choosing a database, that is the boundary, and it is `SPECS.md`'s.

## When it's done

The concept is done when the user says it is. Before agreeing, read `CONCEPT.md` as a
stranger would and say — in a line or two, not a checklist — what a reader still
couldn't answer: what it is, who has the problem, why anyone would pick it over what
exists. Something deliberately unresolved is a fine answer; leave it named in the doc so
`define-scope` inherits it as a known question rather than rediscovering it as a gap.

Then hand off: `define-scope` reads `CONCEPT.md` as intake and decides what v1 ships.
