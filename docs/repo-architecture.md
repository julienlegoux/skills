---
type: Reference
title: "Repo architecture"
description: "How the skills repo is laid out — one folder per skill, shared contracts in _shared/, and a plugin manifest that auto-discovers everything."
tags: [architecture, repo, plugin]
timestamp: 2026-08-13
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
│   │   ├── bundle-interfaces.md  ← rules for anything written under docs/
│   │   ├── ledger-interfaces.md  ← the decision ledger, for ledger-driven skills
│   │   ├── pipeline-interfaces.md ← epic/issue schemas, for epic-to-PR skills
│   │   ├── review-interfaces.md  ← grading and the report, for the planning reviewers
│   │   ├── external-reviewer.md  ← the optional external pass, read only when it is installed
│   │   └── feedback-interfaces.md ← the closing reflex, for every skill but send-feedback
│   ├── define-scope/
│   │   ├── SKILL.md
│   │   └── references/
│   └── ...one folder per skill (18 today)
├── meta/                         ← invisible to the plugin
│   ├── _shared/authoring-interfaces.md
│   ├── create-skill/SKILL.md
│   └── improve-skill/SKILL.md
├── docs/                         ← this bundle
└── README.md
```

`_shared/` sits *among* the skills rather than above them: it has no `SKILL.md`, so
discovery ignores it, and being a sibling keeps every pointer to it a plain
`../_shared/<file>`.

`meta/` holds the two skills that author this repo. They need a clone, git and push
rights, so shipping them to someone who merely installed the plugin would hand over
buttons that can only refuse. Being outside `skills/` is what keeps them out — the
default discovery is not restrictable, and the manifest's `skills` field only ever
*adds* paths.

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

Discovery of `skills/` is unconditional — the manifest's `skills` field cannot narrow
it, only add paths outside it. So the one way to keep something in the repo but out
of the plugin is to put it elsewhere, which is what `meta/` is.

`.claude-plugin/marketplace.json` wraps that plugin as the `lx-engine` marketplace,
which is what makes the repo installable by URL. See
[Installation](/installation.md).

# Families of skills

Everything in the repo is either part of the [idea-to-PR pipeline](/pipeline.md) or
standalone tooling around it:

| Family | Skills |
|---|---|
| Pipeline | `define-concept`, `define-scope`, `define-specs`, `define-conventions`, `split-epics`, `map-codebase`, `define-change`, `create-issues`, `implement-issue`, `implement-epic`, `close-epic` |
| Review companions | `review-epics`, `review-issues`, `review-implementation`, `triage-reports` |
| Knowledge tooling | `okf-docs`, `okf-lint` |
| Feedback | `send-feedback` |
| Meta *(in `meta/`, not shipped)* | `create-skill`, `improve-skill` |

`send-feedback` is the odd one out, and deliberately shipped rather than kept in
`meta/`: it exists for people who installed the plugin and have no clone to fix
anything in. It files an issue on this repo instead — public repo, issues enabled, so
any GitHub account can, with no token bundled and none needed. It is also the one skill
excluded from `feedback-interfaces.md`, the closing reflex every other skill under
`skills/` ends its run with: being the destination, it cannot propose itself as one.

The pipeline skills consume the output contracts in `skills/_shared/`; the meta
skills consume the authoring one in `meta/_shared/`. See
[Shared interfaces](/shared-interfaces.md) for who gets what and why.

# Citations

* `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`
* `README.md`
