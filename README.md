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

Everyone can use the skills; only their maintainer's sessions feed them. That keeps the loop a question of quality, not of trust: every report comes from a session the maintainer ran.

| Piece | What it does |
|---|---|
| [`feedback`](skills/feedback/SKILL.md) | When a skill's own instructions cause a problem — a wrong instruction, a gap the user had to fill, a required step that was dead weight — the running session records one occurrence, without asking anyone. It quotes the sentence of the skill at fault; that sentence is the address, so every session that trips on it lands on the same issue and the number of occurrences is the recurrence. It posts only when `gh` is signed in as someone who can push to this repo, and does nothing anywhere else. |
| [`improve-skills`](.claude/skills/improve-skills/SKILL.md) | In a clone of this repo: takes the most reported sentences, reproduces each failure as an eval case, fixes what the eval proves, checks that no other case in [`evals/`](evals) got worse, and proposes one pull request with the scores before and after. It never merges its own work. |

To close the loop, schedule a session on this repo with the prompt `Run the improve-skills skill`, and review the pull requests it opens.

To feed it on purpose, [`exercise-loop.md`](.claude/exercise-loop.md) is a prompt for a loop that takes one tiny project after another through the whole pipeline, plays the user, and reports where a run departs from what the skills say. Start a session in an empty folder and run `/loop Read <repo>/.claude/exercise-loop.md and do one iteration of it`.

Issues other people file are for a person to read: the loop counts only what maintainers posted. Reports say nothing of the project they came from — no names, paths or code — because the tracker is public. `LX_FEEDBACK=off` disables reporting on a machine.

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
├── .claude/exercise-loop.md ← prompt for a loop that exercises the pipeline
├── evals/                   ← behaviour the skills must keep (`claude plugin eval .`)
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
