# Scope decision checklist — brownfield

The floor for `define-scope`'s enumeration when the program runs on a system that is
already built and shipped: every area below either becomes a decision doc
(`status: open` with a recommendation) or an explicit `status: na` with a reason.
Project-specific decisions are added on top — this list is a floor, not a ceiling.

Its sibling `checklist.md` is the greenfield floor. Four of its areas are why this file
exists: problem, users, delivery form and journeys are not *absent* on a shipped
product, they are different questions — what the next phase solves that the shipped
thing doesn't, which existing users it serves and which it disturbs, whether it changes
what the user receives at all, which live flows it touches and what breaks. Asked
greenfield-style they all come back "already decided", and the run writes N/A docs
carrying nothing.

**Which checklist a given run uses is an open question, and this file does not answer
it.** It belongs to the guide skill that knows where a project stands and says what runs
next — the one this repo doesn't have yet. Nothing here or in `define-scope` detects a
brownfield program; today the only route to this file is the user stating that the
project is already shipped.

Areas run in the same typical dependency order as the greenfield sibling, with the
brownfield-only ones inserted where they bind; renumber per project as dependencies
actually fall.

1. **Problem & job-to-be-done for this phase** — What pain remains *after* what already
   shipped, and for what job? Not "why does this product exist" — that shipped, and
   re-deciding it re-opens a question the product's own users already answered.
   Everything downstream traces here exactly as it does on a new project.
2. **Users served, users disturbed** — Which of the existing users this phase is for,
   and which of them it changes things for without asking. Both halves carry weight: an
   existing audience cannot decline a change the way a prospective one declines a
   product, and the disturbed set is who the rollout, migration and phasing decisions
   are actually about.
3. **Delivery form** — Does this change what the user receives at all: a new surface
   (mobile, CLI, API, bot) beside the shipped one, or nothing new? Usually "unchanged",
   and saying so explicitly is what stops specs re-deciding a settled form. A second
   surface is a fork in the product, not a feature — decide it here or pay for it in
   epics.
4. **Existing flows touched, and what breaks** — Which shipped end-to-end flows this
   phase runs through, and what stops working the way users learned it. These seed both
   acceptance criteria and regression coverage. Name flows, not modules: the file-level
   blast radius is `define-change`'s audit, read out of the code rather than asked.
5. **What the shipped system already decides** — Which questions this phase does *not*
   get to reopen: stack, data model, auth, deployment target, the vocabulary already in
   the UI. Recorded as inputs so the ledger stops offering settled things as options.
   Where `SPECS.md` exists (`map-codebase` writes it), it is the source — this area
   records what scope must live within, not a re-derivation of it.
6. **What must not break** — The invariants this phase may not violate: a published
   contract, existing data, an uptime commitment, a customer integration, a compliance
   posture. A scope-level promise with names attached ("the public v1 API stays"), not
   an inventory of call sites — the inventory is `define-change`'s impact audit, and a
   ledger that attempts it asks the user things the code already answers.
7. **The cut for this phase** — What actually ships (greenfield's MVP cut, renamed
   because there is no "M" left). Bias small for the usual reason — each feature becomes
   real issues and PRs — plus one that only exists here: every item lands in a system
   with live users, so a phase too big to finish is also too big to roll back.
8. **Non-goals** — What is explicitly out. The brownfield pull is not the
   tempting-but-deferred feature; it is the adjacent cleanup the code invites now that
   someone is finally in there. Written down it is deferred, unwritten it arrives as an
   unplanned refactor inside someone's issue.
9. **Success criteria** — How you'd know the phase worked, and here a baseline exists:
   criteria can be a delta against measured current behavior instead of an aspiration.
   "No regression in X" is a legitimate criterion when the phase is structural, and
   often the only honest one.
10. **Constraints** — Externally imposed limits: deadline, budget, mandated tech or
    platform, compliance. The same question as greenfield, with one addition — a live
    system has an operating window (release train, freeze period, maintenance slot)
    that a project with no users doesn't.
11. **Existing systems of record & integrations** — Same area, opposite starting point:
    greenfield asks what already holds the truth, brownfield knows, because the shipped
    system is one of them and its integrations have live consumers. What needs deciding
    is which of them this phase keeps feeding unchanged and which it changes the
    contract of.
12. **Migration of existing users & data** — Whether users and their data come across,
    and who pays: automatic and invisible, an opt-in switch, a dual-run period, or a
    deliberate leave-behind. Scoping altitude — *whether, and for whom*; the migration's
    shape, reversibility and row counts are `define-change`'s. No greenfield equivalent,
    because there is nobody to migrate.
13. **Milestones / phasing** — How the work phases into independently shippable chunks
    (weeks-sized). Directly becomes the `## Milestone N:` headings that split-epics cuts
    on. The brownfield constraint greenfield lacks: every chunk ships into a running
    system, so each boundary has to leave the product working for the users already on
    it.
14. **Risks & assumptions** — Unchanged as a question, skewed in its answers: brownfield
    risk concentrates in what the shipped system is *assumed* to do and in users assumed
    to accept the change. Cheap to write down now, expensive to discover in epic 3.
