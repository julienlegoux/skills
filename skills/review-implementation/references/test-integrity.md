# Test integrity

The brief for the test-integrity lens, and the protocol it runs. This lens exists
because of a specific, structural risk in this pipeline: `implement-issue` drives strict
red-green TDD, and the same agent writes both the test and the code that satisfies it.
When that loop goes wrong it produces a **green suite that proves nothing** — and green
is exactly what everyone downstream trusts.

The question is never "do the tests pass". It is: **if the implementation broke, would
this suite go red?**

## The six shapes

Roughly ordered by how hard they are to see.

| # | Shape | What it looks like | Found by |
|---|---|---|---|
| 1 | **Tautological** | The expected value was pasted from a failing run's *actual* output. The bug is now the spec. | mutation only |
| 2 | **Vacuous** | `toBeDefined()`, `not.toThrow()`, `length >= 0`, empty body, no assertion at all. | reading |
| 3 | **Never executes** | `it.skip`/`xit`, a stray `.only` hiding the rest of the file, an un-awaited async body (the assertion throws after the test already resolved), a file the runner never globs. | reading + run manifest |
| 4 | **Mocked to death** | Every collaborator stubbed; the test asserts the mock's wiring, not the code's behaviour. | reading |
| 5 | **Implementation-coupled** | `expect(spy).toHaveBeenCalled()` where the criterion names an observable outcome. Green, refactor-fragile, requirement-blind. | reading |
| 6 | **Wrong oracle** | Well-formed, executes, asserts a real thing — asserts the *wrong* thing. | criterion comparison + mutation |

Shapes 2–5 are reading work. **1 and 6 are invisible to reading** — they look like good
tests, which is the point. Only execution settles them.

## Three tiers, cheapest first

Run in this order, and note the inversion in tier 3: you probe the tests that look
**fine**, because the bad-looking ones were already caught in tier 1. Probing a test you
already know is vacuous wastes a suite run to confirm what you wrote down.

### Tier 1 — Read the tests against the criteria

For each acceptance criterion, find the tests claiming to cover it and check for shapes
2–5. Also check the criterion is covered *as stated*: a criterion about behaviour under
concurrent writes is not covered by a test of the happy path.

Cheap signal, free, and specific to this pipeline: **red-green provenance.** Merges are
never squashed, so per-commit history survives on the integration branch. If a test and
the implementation that satisfies it landed in the **same commit**, the red phase
probably never happened — and a test written after the code is a test written to fit the
code. Same-commit tests are the priority queue for tier 3.

```bash
# per-file commit history within the epic's range
git log --oneline --name-status <base>..<head> -- <test-path> <impl-path>
```

### Tier 2 — Coverage, if the project already has it

Coverage answers one question well — **which criteria have no executing test at all** —
and answers nothing else. Covered-and-unasserted is precisely the failure mode here, so a
high number is not evidence and must never be reported as reassurance. Use it to narrow
where to probe, then move on. If the project has no coverage tooling, skip the tier; do
not add tooling to the repo.

### Tier 3 — Mutation probe

The decisive tier. Break the implementation on purpose; see if the suite notices.

For each criterion that survived tiers 1 and 2 (prioritising same-commit provenance):

1. Locate the implementation line(s) that satisfy the criterion.
2. Inject **one** mutation (catalogue below).
3. Run only the tests claiming to cover that criterion.
4. Record **red** (the test has teeth) or **green** (the mutant survived — the criterion
   is unverified).
5. Revert before the next mutation. Never stack two.

A surviving mutant is a **P0**: the epic cannot show that it shipped that criterion. Report
the mutation verbatim, so the finding is reproducible rather than an assertion of taste.

## Mutation catalogue

Prefer mutations that are semantically real and locally invisible — a change that any
correct test must catch, but that reads as plausible code.

| Mutation | Example |
|---|---|
| Invert a condition | `if (x > 0)` → `if (x >= 0)` |
| Negate a guard | `if (!user) return` → `if (user) return` |
| Return a constant | replace the computed return with `0` / `""` / `null` / `true` |
| Shift a boundary | `slice(0, n)` → `slice(0, n - 1)`; `<=` → `<` |
| Drop a side effect | remove the write, the emit, the commit |
| Swap an operator | `+` → `-`, `&&` → `\|\|` |
| Skip validation | delete the schema check or the auth guard |

Deleting a whole function body is a poor mutation: it usually fails loudly for reasons
unrelated to the criterion (imports, types), so it proves less than it appears to.

## Protocol: the disposable worktree

All probing happens off a throwaway worktree. The user's tree is never mutated, and no
mutation can survive a crash.

```bash
git worktree add <scratch>/probe-epic-<n> <integration-branch>
cd <scratch>/probe-epic-<n>
<install deps>                       # per the project's own setup
<run the full suite once>            # baseline: it MUST be green before probing
```

Hard rules — these are safety, not preference:

- **Baseline first.** A suite that is already red or flaky makes every probe result
  meaningless. If the baseline isn't green, stop and report that instead; it is itself a
  P0 finding.
- **Never commit, never push, from the probe worktree.** Not even to "save" a mutant.
- **One mutation at a time**, reverted (`git checkout -- <file>`) before the next.
- **Remove the worktree when done** (`git worktree remove --force`), and confirm
  `git worktree list` is clean. A leftover worktree holds a branch checked out, which is
  what makes someone else's branch deletion fail later with a confusing error.
- **Never run a probe against the user's working tree** as a shortcut when the worktree
  setup is awkward. Report the obstacle instead.

If the project can't be built or tested in a fresh worktree at all (undocumented
environment, missing secrets), say so, mark tier 3 `not run`, and give the reason. An
unrun probe reported honestly is worth more than a probe faked from reading.

## Subagent prompt

Spawn with the epic's diff range, the criteria list, the test file paths, and:

> You audit whether this epic's tests would catch a regression. Green tests are not
> evidence; your job is to find tests that pass regardless of whether the code is
> correct.
>
> Work the three tiers in `references/test-integrity.md` in order. Tier 1: read every
> test claiming to cover a criterion against the six shapes, and flag same-commit
> test/implementation provenance. Tier 2: use existing coverage only to find criteria
> with no executing test. Tier 3: mutation-probe the criteria that **survived** tiers 1
> and 2, in a disposable worktree, obeying the protocol's hard rules exactly.
>
> Report per criterion: covered yes/no, shapes found, whether it was probed, the exact
> mutation used, and red or green. A surviving mutant is P0 — quote the mutation so it
> can be reproduced. State explicitly which criteria you did **not** probe and why;
> never let silence imply verification. Do not fix any test or any implementation code.
