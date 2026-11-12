**Claude Code skills that take a need to a finished product** — the user says what they want, answers a few questions, says go, and comes back to something that works.

This repo is a [Claude Code plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces):

```
/plugin marketplace add julienlegoux/skills
/plugin install lx@lx-engine
```

Skills are then namespaced: `/lx:plan`, `/lx:build`.

## The pipeline

```
need ──▶ plan ──"go"──▶ build ──▶ finished product
          │               ▲ │
     the only stage       │ └─▶ review ─┐
     that asks the user   └── fixes ◀───┘
```

| Skill | What it does |
|---|---|
| [`plan`](skills/plan/SKILL.md) | Interviews the user about the need — never about technology — and writes `docs/PLAN.md`: outcomes, technical decisions, milestones, and what only the user can supply. Ends on a single go. |
| [`build`](skills/build/SKILL.md) | Carries the approved plan to the product: slices the work, implements, integrates, reviews, fixes, and verifies by using the result. Makes and records its own decisions in `docs/PROGRESS.md`; stops only for what a human alone can supply. |
| [`review`](skills/review/SKILL.md) | Reviews a body of changes with fresh-context reviewers that did not write the code, verifies what they report, and returns ranked findings. `build` runs it at every milestone; it also runs on request. |

`plan` hands off to `build` on its own. `/lx:build` resumes a build that was interrupted.

Quality rules are not negotiated per project: they are fixed in [`standards.md`](skills/build/references/standards.md), and a project's own documented conventions override them. Edit that file to change how everything gets built.

## The skills improve themselves

| Piece | What it does |
|---|---|
| [`feedback`](skills/feedback/SKILL.md) | When a skill's own instructions cause a problem — a wrong instruction, a gap the user had to fill, a required step that was dead weight — the running session records one occurrence, without asking anyone. The occurrence quotes the sentence of the skill at fault; that sentence is the address, so every session that trips on it lands on the same issue and the number of occurrences is the recurrence. No `gh`? It queues locally and a later run sends it. |
| [`improve-skills`](.claude/skills/improve-skills/SKILL.md) | In a clone of this repo: takes the most reported sentences, reproduces each failure as an eval, fixes what the eval proves, and proposes one pull request. It never merges its own work. |

To close the loop, schedule a session on this repo with the prompt `Run the improve-skills skill`, and review the pull requests it opens.

### Anyone can report; no report is believed

The tracker is public, so it will receive mistaken reports, inflated counts and text written to manipulate whatever reads it. The loop does not filter who may speak — it limits what a report can do:

| Layer | What it guarantees |
|---|---|
| **Pointers, not prose** | `improve-skills` never reads an issue. `feedback.py pointers` parses titles against a fixed pattern and prints only a skill, a kind, the sentence *re-read from this repo*, and counts. Text from an issue is shown only when a maintainer of the repo posted it. An injected instruction never reaches a model. |
| **Counts order, evals decide** | Outside accounts count once each, however often they post. A count only sets what gets looked at: a change is made only if an eval case fails on the current skill and passes after — and no other case in [`evals/`](evals) gets worse. |
| **Invariants** | [`CLAUDE.md`](CLAUDE.md) lists what no feedback may undo; an independent reviewer checks every diff against it. |
| **The guard** | [`guard.py`](.github/scripts/guard.py) runs in CI from the base branch on every `improve/…` pull request and accepts prose edits to skills and new eval cases only — no script, command, link, hidden character, manifest, description or rule change, and a size cap. A pull request cannot alter its own check. |
| **The merge** | A person merges. Nothing reaches users before that. |

Three things only you can set, and the last two layers depend on them: protect `main` (pull request required, `guard` as a required check); give the scheduled session an environment with access to this repository and nothing else — no other secrets, no network beyond GitHub; and treat a pull request from the automation that is *not* on an `improve/…` branch as a red flag.

What a session sends is about the skill only — no project names, paths or code — because nothing is reviewed before posting. `LX_FEEDBACK=off` disables it; `LX_FEEDBACK_REPO` and `LX_FEEDBACK_OUTBOX` redirect it, which is how a host application collects occurrences from users who have no GitHub account.

## Documentation tooling (OKF)

Independent of the pipeline.

| Skill | What it does |
|---|---|
| [`okf-docs`](skills/okf-docs/SKILL.md) | Write and structurally validate docs in Google's **Open Knowledge Format** — markdown + YAML frontmatter bundles readable by humans and agents alike |
| [`okf-lint`](skills/okf-lint/SKILL.md) | Semantic linter for OKF bundles: contradictions, index drift, duplicate concepts, stale timestamps |

## Repo layout

```
├── .claude-plugin/          ← marketplace "lx-engine", plugin "lx"
├── skills/                  ← the plugin: one folder per skill, auto-discovered
├── .claude/skills/          ← improve-skills: loads only in a clone of this repo
├── evals/                   ← behaviour the skills must keep (`claude plugin eval .`)
├── .github/                 ← the guard that checks automatic pull requests
├── CLAUDE.md                ← how a skill here is written
└── README.md
```

## Developing

Point your skills directory at the clone and the file you edit is the file Claude Code runs:

```powershell
New-Item -ItemType Junction -Path "$HOME\.claude\skills\lx-engine" -Target "<repo>"
```

After editing, `/reload-plugins` in the session, then `claude plugin validate .`. The authoring rules are in [`CLAUDE.md`](CLAUDE.md) — the short version: a line stays only if a capable model would get it wrong without it.

## License

Personal toolkit — use freely, adapt liberally.
