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
<repo>/
├── .claude-plugin/
│   ├── marketplace.json          ← marketplace "lx-engine"
│   └── plugin.json               ← plugin "lx"
├── skills/                       ← the plugin's default skills directory
│   ├── _shared/
│   │   ├── authoring-interfaces.md ← how a skill here is written, for the meta skills
│   │   ├── bundle-interfaces.md  ← rules for anything written under docs/
│   │   ├── ledger-interfaces.md  ← the decision doc, for ledger-driven skills
│   │   └── pipeline-interfaces.md ← epic/issue schemas, for epic-to-PR skills
│   ├── define-scope/
│   │   ├── SKILL.md
│   │   └── references/
│   └── ...one folder per skill (15 today)
├── docs/                         ← this bundle
└── README.md
```

`_shared/` sits *among* the skills rather than above them: it has no `SKILL.md`, so
discovery ignores it, and being a sibling keeps every pointer to it a plain
`../_shared/<file>`.

# Anatomy of a skill

| Path | Role |
|---|---|
| `<skill>/SKILL.md` | Always loaded when the skill fires. Holds the decision flow and the invariants — not bulk. |
| `<skill>/references/` | Progressive disclosure: templates, schemas, edge cases the skill reads only when it needs them — the ones specific to *this* skill. Shared contracts are read from `../_shared/`, never copied in. |
| `<skill>/assets/` | Files the skill copies or instantiates (e.g. `define-conventions/assets/baseline.md`). |
| `<skill>/scripts/` | Executables the skill runs (e.g. `okf-docs/scripts/validate_okf.py`). |
| `<skill>/agents/` | Subagent definitions, where a skill delegates (`review-epics`, `review-issues`). |

The frontmatter `description` in `SKILL.md` is what decides whether the skill fires
at all — it rides in every session's context, so it stays 1–2 sentences (what + when)
rather than a list of trigger phrases.

# Discovery

`.claude-plugin/plugin.json` declares no component paths, so Claude Code uses the
default location: **every folder under `skills/` holding a `SKILL.md` is picked up
automatically**. Adding a skill means adding a folder; there is no registry to update.
Confirm with `claude plugin details lx@skills-dir`, which lists what was actually
discovered.

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
| Meta | `create-skill`, `improve-skill` |

The pipeline skills consume the three output contracts in `_shared/`; the meta skills
consume the authoring one. See [Shared interfaces](/shared-interfaces.md) for who
gets what and why.

# Citations

* `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`
* `README.md`
