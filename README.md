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
| [`feedback`](skills/feedback/SKILL.md) | When a skill's own instructions cause a problem — a wrong instruction, something the user had to correct, a required step that was dead weight — the running session records one occurrence, without asking anyone. One issue per class of failure on this repo, titled `[lx:<skill>] …`; each further occurrence is a comment, so the comment count is the recurrence. No `gh`? It queues locally and a later run sends it. |
| [`improve-skills`](.claude/skills/improve-skills/SKILL.md) | In a clone of this repo: reads the accumulated occurrences, acts on what recurs or is confirmed by reading the skill, and proposes the edits as one pull request. It never merges its own work. |

To close the loop, schedule a session on this repo with the prompt `Run the improve-skills skill`, and review the pull requests it opens.

What a session sends is about the skill only — no project names, paths or code — because the tracker is public and nothing is reviewed before posting. `LX_FEEDBACK=off` disables it; `LX_FEEDBACK_REPO` and `LX_FEEDBACK_OUTBOX` redirect it, which is how a host application collects occurrences from users who have no GitHub account.

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
