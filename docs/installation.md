---
type: Playbook
title: "Installation and delivery modes"
description: "How the skills reach a Claude Code session — marketplace install for users, an in-place skills-directory plugin for development — and why the repo, not the folder, is the unit."
tags: [install, plugin, marketplace, delivery]
timestamp: 2026-08-06
---

# Installation and delivery modes

The repo is **one plugin**, `lx`, holding fourteen skills. Both delivery modes below
load it whole.

| Manifest | Declares |
|---|---|
| `.claude-plugin/marketplace.json` | marketplace `lx-engine`, owning one plugin |
| `.claude-plugin/plugin.json` | plugin `lx` — no component paths, so the default `skills/` layout is discovered |

Every folder under `skills/` holding a `SKILL.md` is picked up automatically, so
publishing a new skill is committing its folder. `skills/_shared/` has no `SKILL.md`
and is ignored by discovery while staying readable by its neighbours.

Plugin skills are namespaced by the plugin name: `/lx:define-scope`, `/lx:okf-docs`.

Validate the manifests before pushing, and check what actually got discovered:

```
claude plugin validate .
claude plugin details lx@skills-dir
```

The inventory is the real test. A manifest can validate while discovering zero
skills — that is exactly what a `"skills": ["./"]` entry does, since `"./"` means
*the plugin root is itself one skill*, not *every folder under the root is a skill*.

# For users — the plugin marketplace

```
/plugin marketplace add julienlegoux/skills
/plugin install lx@lx-engine
```

Zero scripts. A marketplace install **copies** the plugin into Claude Code's plugin
cache, so `/plugin marketplace update` is what refreshes it.

# For development — a skills-directory plugin

Any folder under `~/.claude/skills/` containing a `.claude-plugin/plugin.json` loads
as `<name>@skills-dir` with no marketplace and no install step, and — the part that
matters — *is discovered in place rather than copied into the plugin cache*.

Point that folder at the clone with a junction (or a symlink on Unix), once:

```powershell
New-Item -ItemType Junction -Path "$HOME\.claude\skills\lx-engine" -Target "<repo>"
```

```
~\.claude\skills\lx-engine  ──junction──▶  <repo>
```

From then on the edited file *is* the loaded file. `/reload-plugins` picks changes up
mid-session. There is no mirror step, nothing to reinstall, and no way for an
installed copy to drift from the source.

Alternatively, `claude --plugin-dir <repo>` loads it for one session without touching
`~/.claude/skills`.

# Why the repo is the unit, not the folder

A skill reads its shared contracts at `../_shared/<file>` — a real path to a real
file, resolved because every mode above ships the repo whole. The trade is explicit:
**lifting a single skill folder into some other `.claude/skills/` breaks it.**

The repo used to make the opposite trade, generating a copy of each contract into
every consuming skill's `references/` so that a lone folder stayed self-contained.
That bought a portability nobody used, at the price of a build step and three copies
of every rule. See [Shared interfaces](/shared-interfaces.md).

# Citations

* `README.md`
* `.claude-plugin/marketplace.json`, `.claude-plugin/plugin.json`
* Claude Code docs — *Plugins reference*, "Skills-directory plugins" and "Path resolution"
