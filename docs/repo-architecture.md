---
type: Reference
title: "Repo architecture"
description: "How the skills repo is laid out — one folder per skill, shared contracts in _shared/, and a plugin manifest that auto-discovers everything."
tags: [architecture, repo, plugin]
timestamp: 2026-08-06
---

# Repo architecture

The repo is a flat collection of Claude Code skills plus the two things that hold
them together: a plugin manifest that publishes them, and `_shared/` contracts that
keep them agreeing on the same file formats.

# Layout

```
skills/
├── .claude-plugin/
│   ├── marketplace.json          ← marketplace "lx-engine"
│   └── plugin.json               ← plugin "skills"
├── _shared/
│   ├── bundle-interfaces.md      ← rules for anything written under docs/
│   ├── ledger-interfaces.md      ← the decision doc, for ledger-driven skills
│   ├── pipeline-interfaces.md    ← epic/issue schemas, for epic-to-PR skills
│   └── sync.ps1                  ← copies each into its audience's references/
├── define-scope/
│   ├── SKILL.md
│   └── references/
├── ...one folder per skill (14 today)
├── docs/                         ← this bundle
└── README.md
```

# Anatomy of a skill

| Path | Role |
|---|---|
| `<skill>/SKILL.md` | Always loaded when the skill fires. Holds the decision flow and the invariants — not bulk. |
| `<skill>/references/` | Progressive disclosure: templates, schemas, edge cases the skill reads only when it needs them. Also where synced copies of `_shared/*.md` land. |
| `<skill>/assets/` | Files the skill copies or instantiates (e.g. `define-conventions/assets/baseline.md`). |
| `<skill>/scripts/` | Executables the skill runs (e.g. `improve-skill/scripts/reinstall.ps1`, `okf-docs/scripts/validate_okf.py`). |
| `<skill>/agents/` | Subagent definitions, where a skill delegates (`review-epics`, `review-issues`). |

The frontmatter `description` in `SKILL.md` is what decides whether the skill fires
at all — it rides in every session's context, so it stays 1–2 sentences (what + when)
rather than a list of trigger phrases.

# Discovery

`.claude-plugin/plugin.json` declares `"skills": ["./"]`, so **every top-level folder
holding a `SKILL.md` is picked up automatically**. Adding a skill means adding a
folder; there is no registry to update.

`.claude-plugin/marketplace.json` wraps that plugin as the `lx-engine` marketplace,
which is what makes the repo installable by URL. See
[Installation](/installation.md).

# Two families of skills

Everything in the repo is either part of the [idea-to-PR pipeline](/pipeline.md) or
standalone tooling around it:

| Family | Skills |
|---|---|
| Pipeline | `define-scope`, `define-specs`, `define-conventions`, `split-epics`, `map-codebase`, `define-change`, `create-issues`, `implement-issue`, `implement-epic` |
| Review companions | `review-epics`, `review-issues` |
| Knowledge tooling | `okf-docs`, `okf-lint` |
| Meta | `improve-skill` |

Only the pipeline skills consume `_shared/` contracts — see
[Shared interfaces](/shared-interfaces.md) for who gets what and why.

# Citations

* `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`
* `README.md`
