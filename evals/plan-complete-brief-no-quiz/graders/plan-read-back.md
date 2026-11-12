---
type: llm
weight: 1
---

A successful response presents a plan for the tool described — what it will do, what is left out, and how the work is ordered — and asks the user whether to go ahead. It respects the stated constraints (Python standard library, no network, no database, no GUI) rather than proposing alternatives to them.

Fail if no plan is shown, or if a stated constraint is overridden.
