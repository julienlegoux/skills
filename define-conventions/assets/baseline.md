---
type: Conventions Baseline
title: "Personal conventions baseline"
description: "Default repo standards applied to every project unless a project decides a deviation"
tags: [conventions, baseline]
timestamp: 2026-07-19T00:00:00Z
---

# Personal conventions baseline

> **STARTER CONTENT** — this is a reasonable generic baseline, not yet Julien's.
> Refine it via the improve-skill loop as real projects decide deviations worth
> promoting. Sections marked *(per-stack)* are filtered by the stack in SPECS.md.

## Code style & formatting

- A formatter is law: run it in CI, never debate style in review.
  *(per-stack)* JS/TS: Prettier defaults. Python: ruff format. Go: gofmt. Rust: rustfmt.
- A linter runs in CI with the stack's community-standard ruleset; warnings are errors.
- No commented-out code in committed files.

## Naming

- Descriptive over short; no abbreviations that aren't industry-standard.
- *(per-stack)* Follow the language's community casing (camelCase JS/TS, snake_case
  Python, PascalCase exported Go/C#) — never invent a house style.
- Files are named after the main thing they export/define.

## Repository layout

- Top level stays small: source, tests, `docs/`, `scripts/`, config.
- Knowledge-style docs (plans, references, runbooks) are OKF bundles under `docs/`;
  `README.md` is for humans landing on the repo, not a knowledge dump.

## Git & PRs

- Conventional commit messages: `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`,
  `test:` — imperative mood, no trailing period in the subject.
- One branch per issue, named `issue-<n>-<slug>`; branches are short-lived.
- PRs target roughly 500 changed lines and never approach 1000 (matches how
  create-issues sizes issues); a PR closes exactly one issue via `Closes #<n>`.
- CI (lint + tests) must be green before merge; no force-pushes to main.

## Testing

- Features and fixes are built test-first (strict red-green, as implement-issue runs
  it): failing test → minimal pass → refactor.
- Tests live beside or mirror the source structure; test names state the behavior
  being asserted, not the method being called.
- Prefer integration-level tests over heavy mocking where the real thing is cheap;
  mock only true externals (network, clock, third-party APIs).

## Error handling

- Fail fast; never swallow an error silently — handle it meaningfully or let it
  propagate with context added.
- Error messages state what was being attempted, not just what broke.
- User-facing errors and log-facing errors are different audiences; write both.

## Dependencies

- Prefer the standard library; a new dependency needs a one-line justification in the
  PR that adds it.
- Pin or lock everything the ecosystem lets you lock.

## Documentation & comments

- Code comments only for constraints the code can't show (invariants, workarounds
  with links, non-obvious "why") — never narration of what the next line does.
- Every substantive doc produced during work lands in the OKF bundle, not in ad-hoc
  scattered markdown.
