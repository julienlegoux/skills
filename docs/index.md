---
okf_version: "0.1"
---

# Skills repo — documentation

Reference documentation for this repo: a Claude Code plugin marketplace of skills
that carry a project from raw idea to merged PR, plus documentation tooling and a
self-improvement loop.

* [The idea-to-PR pipeline](pipeline.md) - The chain of skills that carries work from a raw idea (or an existing codebase) to merged pull requests, and what each hand-off passes along.
* [Repo architecture](repo-architecture.md) - How the skills repo is laid out — one folder per skill, shared contracts in _shared/, and a plugin manifest that auto-discovers everything.
* [Shared interfaces](shared-interfaces.md) - The four _shared/ contracts, split by audience, read in place by the skills that obey them.
* [Skill lifecycle](skill-lifecycle.md) - How a skill is created, edited, validated and committed — one copy loaded in place, plus the improve-skill loop that folds session lessons back into the source.
* [Installation and delivery modes](installation.md) - How the skills reach a Claude Code session — marketplace install for users, an in-place skills-directory plugin for development — and why the repo, not the folder, is the unit.
