---
okf_version: "0.1"
---

# Skills repo — documentation

Reference documentation for this repo: a Claude Code plugin marketplace of skills
that carry a project from raw idea to merged PR, plus documentation tooling and a
self-improvement loop.

* [The idea-to-PR pipeline](pipeline.md) - The chain of skills that carries work from a raw idea (or an existing codebase) to merged pull requests, and what each hand-off passes along.
* [Repo architecture](repo-architecture.md) - How the skills repo is laid out — one folder per skill, shared contracts in _shared/, and a plugin manifest that auto-discovers everything.
* [Shared interfaces](shared-interfaces.md) - The three _shared/ contracts, split by audience, and the sync mechanism that copies each into the references/ of the skills that obey it.
* [Skill lifecycle](skill-lifecycle.md) - How a skill is created, edited, validated, committed and reinstalled — including the improve-skill loop that folds session lessons back into the source.
* [Installation and delivery modes](installation.md) - How the skills reach a Claude Code session — plugin marketplace for users, robocopy mirror for development — and why each skill ships self-contained.
