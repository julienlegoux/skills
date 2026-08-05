# Scope decision checklist

The floor for `define-scope`'s enumeration: every area below either becomes a decision
doc (`status: open` with a recommendation) or an explicit `status: na` with a reason.
Project-specific decisions are added on top — this list is a floor, not a ceiling.

Areas are listed in typical dependency order; renumber per project as dependencies
actually fall.

1. **Problem & job-to-be-done** — What pain does this solve, for what job? Everything
   downstream traces here; if this is fuzzy, every other recommendation is a guess.
2. **Target users** — Who is v1 for, specifically? "Everyone" is not an answer;
   the MVP cut and journeys depend on a concrete first audience.
3. **Delivery form** — What does the user actually receive: web app, CLI, mobile,
   desktop, library, API, bot? (The *form*, not the stack — stack is a specs decision.)
4. **Core user journeys** — The 2–5 flows that must work end-to-end for v1 to mean
   anything. These become acceptance-criteria seeds for epics.
5. **MVP feature cut** — What's in v1. Bias small: each feature here becomes real
   issues and PRs downstream.
6. **Non-goals** — What is explicitly *out* of v1, especially tempting-but-deferred
   features. Written non-goals are what keep scope from creeping back in via issues.
7. **Success criteria** — How you'd know v1 worked: adoption, a workflow replaced,
   a metric, "I use it daily". Must be checkable, not aspirational.
8. **Constraints** — Externally imposed limits: deadline, budget, mandated tech or
   platform, compliance. These bound what specs may later choose.
9. **Existing systems of record & integrations** — What already holds the truth this
   project must respect or connect to: an existing GitHub/issue tracker, a CRM, a
   spreadsheet someone lives in, an API the users already depend on. Surfacing these
   late reworks decisions that silently assumed a blank slate.
10. **Milestones / phasing** — How the work phases into independently shippable chunks
    (weeks-sized). Directly becomes the `## Milestone N:` headings that split-epics
    cuts on — this decision shapes the entire downstream pipeline.
11. **Risks & assumptions** — What could sink the project and what is being assumed
    without proof. Cheap to write down now, expensive to discover in epic 3.
