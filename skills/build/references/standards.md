# Standards

The quality rules every build follows. They are fixed here so that no project has to
decide them and no user has to be asked. A project's own documented conventions
(`CLAUDE.md`, `CONTRIBUTING.md`, an existing codebase's evident practice) override
any line below.

This file is the maintainer's dial: change a line here and every future build follows.

## Code

- A formatter and a linter run in CI with the stack's community-standard settings;
  warnings are errors. Style is never a review topic.
- Follow the language's community naming and layout. No house style.
- Fail fast. Never swallow an error: handle it meaningfully or let it propagate with
  context. Messages say what was being attempted, not only what broke.
- Comments only for what the code cannot show — an invariant, a workaround with its
  link, a non-obvious why.
- No commented-out code, no dead code left behind by a later change.

## Tests

- Test-first wherever correctness is an assertable behaviour: domain logic,
  calculations, data transforms, trust boundaries (APIs, validation, handlers). Write
  the test, watch it fail, make it pass.
- An interface reproduced from a design is not test-first: cover its interactive logic
  with behaviour tests, the user journeys end to end, and check the rendering by eye.
- Test names state the behaviour asserted. Prefer real collaborators over mocks where
  the real thing is cheap; mock only true externals (network, clock, third parties).
- Never weaken, skip or delete a test to get to green.

## Dependencies

- Prefer the standard library. A new dependency earns one line of justification where
  it is added.
- Pin or lock everything the ecosystem can lock.

## Git

- Conventional commits (`feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `test:`),
  imperative mood.
- Merge with a merge commit — never squash or rebase a unit's history away. If the
  repository forbids merge commits, say so rather than squashing around it.
- No force-push to a shared branch.
- A repository created for a new project is private.
- Secrets never enter the repository, its history or its logs.
