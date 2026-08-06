**Claude Code skills for taking a project from raw idea to merged PR** — greenfield or brownfield — plus documentation tooling and a self-improvement loop.

This repo is a [Claude Code plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces). One command installs everything:

```
/plugin marketplace add julienlegoux/skills
/plugin install lx@lx-engine
```

Skills are then namespaced: `/lx:define-scope`, `/lx:okf-docs`.

---

## 🗺️ The planning-to-PR pipeline

The core of this repo is a chain of skills that carries work all the way to reviewable pull requests. Each skill's output is the next skill's input. There are two entry points — a new project, or an existing codebase — and they converge on the same epic → issue → PR machinery:

```mermaid
flowchart LR
    A[💡 idea] --> B[define-scope]
    B --> C[define-specs]
    C --> D[define-conventions]
    D --> E[split-epics]

    A2[📦 existing code] --> M[map-codebase]
    M --> N[define-change]

    E --> F[create-issues]
    N --> F
    F --> G[implement-issue]
    G --> H[🚀 PR]
    F -.-> I[implement-epic]
    I -.-> G
```

### 🌱 Greenfield — plan a new project

| Stage | Skill | What it does |
|---|---|---|
| 1️⃣ | [`define-scope`](skills/define-scope/SKILL.md) | Turn a raw idea into a decided `docs/planning/SCOPE.md` via a decision ledger *you* triage |
| 2️⃣ | [`define-specs`](skills/define-specs/SKILL.md) | Decide the one-way technical doors — stack, architecture, data, auth — into `SPECS.md` |
| 3️⃣ | [`define-conventions`](skills/define-conventions/SKILL.md) | Instantiate your personal conventions baseline; only *deviations* get decided |
| 4️⃣ | [`split-epics`](skills/split-epics/SKILL.md) | Cut the scope into epic folders, each with a GitHub milestone + tracking issue |

### 🏗️ Brownfield — change an existing app

| Stage | Skill | What it does |
|---|---|---|
| 1️⃣ | [`map-codebase`](skills/map-codebase/SKILL.md) | Reverse-engineer `SPECS.md` + `CONVENTIONS.md` by reading the code, not interviewing you |
| 2️⃣ | [`define-change`](skills/define-change/SKILL.md) | Audit one change's blast radius, decide *how it lands*, emit an `EPIC_N.md` `create-issues` consumes unchanged |

### 🔨 Build — both paths

| Skill | What it does |
|---|---|
| [`create-issues`](skills/create-issues/SKILL.md) | Turn one epic into right-sized GitHub sub-issues (~one 500-line PR each) |
| [`implement-issue`](skills/implement-issue/SKILL.md) | Take one issue from `open` to a focused, test-first PR — bookkeeping included |
| [`implement-epic`](skills/implement-epic/SKILL.md) | Supervise a whole epic: delegate each issue to `implement-issue`, watch CI, merge green PRs, repeat |

### 🔍 Review companions

Audit skills that check the pipeline's output without modifying it:

| Skill | Reviews |
|---|---|
| [`review-epics`](skills/review-epics/SKILL.md) | Plan → epic conversion: epics, milestones, tracking issues vs. the source plan |
| [`review-issues`](skills/review-issues/SKILL.md) | Epic → issue conversion: sizing, coverage, sub-issue wiring |

Both write a prioritized `docs/REPORT_N.md` instead of silently "fixing" things.

## 📚 Knowledge tooling (OKF)

| Skill | What it does |
|---|---|
| [`okf-docs`](skills/okf-docs/SKILL.md) | Write & structurally validate docs in Google's **Open Knowledge Format** — markdown + YAML frontmatter bundles readable by humans and agents alike |
| [`okf-lint`](skills/okf-lint/SKILL.md) | Semantic linter for OKF bundles: contradictions, index drift, duplicate concepts, stale timestamps — everything a mechanical validator can't see |

## 🔁 Meta

| Skill | What it does |
|---|---|
| [`improve-skill`](skills/improve-skill/SKILL.md) | Fold lessons from the current session back into the skill that caused them: diagnose → propose → apply → commit |

---

## 📦 Repo layout

```
├── .claude-plugin/
│   ├── marketplace.json          ← marketplace "lx-engine"
│   └── plugin.json               ← plugin "lx" (bundles every skill below)
├── skills/
│   ├── _shared/
│   │   ├── bundle-interfaces.md  ← rules for anything written under docs/
│   │   ├── ledger-interfaces.md  ← the decision doc, for ledger-driven skills
│   │   └── pipeline-interfaces.md ← epic/issue schemas, for epic-to-PR skills
│   ├── define-scope/SKILL.md
│   ├── define-specs/SKILL.md
│   └── ...one folder per skill
├── docs/                         ← documentation bundle
└── README.md
```

Every folder under `skills/` holds one skill (`SKILL.md` + supporting files) and is auto-discovered by the plugin. `_shared/` has no `SKILL.md`, so discovery skips it.

### Shared contracts

What the skills agree on lives in `skills/_shared/`, split by audience so no skill carries rules that don't apply to it:

| Interface | Defines | Audience |
|---|---|---|
| [`bundle-interfaces.md`](skills/_shared/bundle-interfaces.md) | English content, bundle & link rules, reserved `index.md`/`log.md`, committing what you write | every skill that writes under `docs/` |
| [`ledger-interfaces.md`](skills/_shared/ledger-interfaces.md) | the decision doc schema and reopening rule | the ledger-driven planning skills |
| [`pipeline-interfaces.md`](skills/_shared/pipeline-interfaces.md) | epic & issue schemas, status lifecycle, GitHub facts on integration branches | the epic-to-PR skills |

One file per contract, read in place by its audience as `../_shared/<file>` — no generated copies, so an edit is live everywhere at once. The trade: a skill folder is not portable on its own. The repo is the unit.

## 🛠️ Developing

There is no install step. Point your skills directory at the clone once, and the file you edit is the file Claude Code runs:

```powershell
New-Item -ItemType Junction -Path "$HOME\.claude\skills\lx-engine" -Target "<repo>"
```

Then, after editing: `/reload-plugins` in the session, and

```
claude plugin validate .
claude plugin details lx@skills-dir    # confirms what was actually discovered
```

Or let [`improve-skill`](skills/improve-skill/SKILL.md) run the loop — it diagnoses, edits and commits in one pass.

## 📄 License

Personal toolkit — use freely, adapt liberally.
