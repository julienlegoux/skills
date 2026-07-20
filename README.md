# 🧰 julien-skills

**Claude Code skills for taking a project from raw idea to merged PR** — plus documentation tooling and a self-improvement loop.

This repo is a [Claude Code plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces). One command installs everything:

```
/plugin marketplace add julienlegoux/skills
/plugin install planning-skills@julien-skills
```

---

## 🗺️ The planning-to-PR pipeline

The core of this repo is a chain of skills that carries a project idea all the way to reviewable pull requests. Each skill's output is the next skill's input:

```mermaid
flowchart LR
    A[💡 idea] --> B[define-scope]
    B --> C[define-specs]
    C --> D[define-conventions]
    D --> E[split-epics]
    E --> F[create-issues]
    F --> G[implement-issue]
    G --> H[🚀 PR]
```

| Stage | Skill | What it does |
|---|---|---|
| 1️⃣ Plan | [`define-scope`](define-scope/SKILL.md) | Turn a raw idea into a decided `docs/planning/SCOPE.md` via a decision ledger *you* triage |
| 2️⃣ Plan | [`define-specs`](define-specs/SKILL.md) | Decide the one-way technical doors — stack, architecture, data, auth — into `SPECS.md` |
| 3️⃣ Plan | [`define-conventions`](define-conventions/SKILL.md) | Instantiate your personal conventions baseline; only *deviations* get decided |
| 4️⃣ Break down | [`split-epics`](split-epics/SKILL.md) | Cut the scope into epic folders, each with a GitHub milestone + tracking issue |
| 5️⃣ Break down | [`create-issues`](create-issues/SKILL.md) | Turn one epic into right-sized GitHub sub-issues (~one 500-line PR each) |
| 6️⃣ Build | [`implement-issue`](implement-issue/SKILL.md) | Take one issue from `open` to a focused, test-first PR — bookkeeping included |

### 🔍 Review companions

Audit skills that check the pipeline's output without modifying it:

| Skill | Reviews |
|---|---|
| [`review-epics`](review-epics/SKILL.md) | Plan → epic conversion: epics, milestones, tracking issues vs. the source plan |
| [`review-issues`](review-issues/SKILL.md) | Epic → issue conversion: sizing, coverage, sub-issue wiring |

Both write a prioritized `docs/REPORT_N.md` instead of silently "fixing" things.

## 📚 Knowledge tooling (OKF)

| Skill | What it does |
|---|---|
| [`okf-docs`](okf-docs/SKILL.md) | Write & structurally validate docs in Google's **Open Knowledge Format** — markdown + YAML frontmatter bundles readable by humans and agents alike |
| [`okf-lint`](okf-lint/SKILL.md) | Semantic linter for OKF bundles: contradictions, index drift, duplicate concepts, stale timestamps — everything a mechanical validator can't see |

## 🔁 Meta

| Skill | What it does |
|---|---|
| [`improve-skill`](improve-skill/SKILL.md) | Fold lessons from the current session back into the skill that caused them: diagnose → propose → apply → commit → reinstall |

---

## 📦 Repo layout

```
skills/
├── .claude-plugin/
│   ├── marketplace.json   ← marketplace "julien-skills"
│   └── plugin.json        ← plugin "planning-skills" (bundles every skill below)
├── define-scope/SKILL.md
├── define-specs/SKILL.md
├── ...one folder per skill
```

Every top-level folder holds one skill (`SKILL.md` + supporting files) and is auto-discovered by the plugin.

## 🛠️ Developing

Skills are developed here, then installed. After editing a skill:

```
claude plugin validate .
```

Or let [`improve-skill`](improve-skill/SKILL.md) run the whole loop — it edits, commits, and reinstalls in one pass.

## 📄 License

Personal toolkit — use freely, adapt liberally.
