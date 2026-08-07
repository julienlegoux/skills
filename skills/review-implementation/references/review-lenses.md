# Review lenses

The four **reading** lenses of Step 3. Test integrity is the fifth and lives in
`test-integrity.md`, because it executes rather than reads.

Each lens is one subagent, spawned concurrently, given the epic's diff range, the
acceptance criteria, `CONVENTIONS.md`, and the accepted entries from `DRIFT.md`. One
context holding all four degrades on a large epic — which is the same failure the skill
was built to catch, so don't reproduce it in the reviewer.

Every lens gets the same three standing rules:

> Cite `file:line` and name the criterion, convention line, or defect class the finding
> violates. A finding that can't name what it violates is taste — put it in notes, not
> findings. Anything already recorded in the supplied DRIFT.md entries is settled; do not
> report it. Never edit product code.

## Acceptance honesty

> For each acceptance criterion in the epic and its issues, find the code that satisfies
> it and judge whether it *actually does*. Report criteria that are: unimplemented;
> implemented for the happy path only where the criterion is broader; implemented
> somewhere other than where the issue said; or satisfied by a stub, a hardcoded value, a
> `TODO`, or a feature flag left off.

The pairing to watch is a criterion whose code is thin *and* whose tests are green — the
test-integrity lens is auditing the other half of that same pair, so a finding from both
lenses on one criterion is the strongest signal this review produces.

## Seams

The lens that justifies reviewing the epic as a whole. Nothing here is visible inside one
PR.

> The implementers of these issues worked concurrently and blind to each other. Find what
> that cost:
> - the same logic implemented two or more times, in different places, differently
> - competing abstractions for one concept (two date helpers, two error shapes, two ways
>   to reach the same table)
> - a helper or module introduced by one issue that a later issue should have used and
>   didn't
> - dead code: superseded by a later issue, or written for a criterion that moved
> - inconsistent boundaries — the same responsibility living in the controller in one
>   issue and the service in another
>
> For each, name the issues involved. Duplication between issue 3 and issue 7 is a
> different fix than duplication inside issue 3.

## Convention erosion

> Judge the diff against `docs/planning/CONVENTIONS.md` and the stack in `SPECS.md`.
> Report only breaches with consequences: naming, structure, error handling, logging,
> dependency choices, test placement, commit conventions.
>
> Erosion matters more than any single breach — the same convention broken once is a
> slip, broken in five of eight PRs means the convention is either unknown to the
> implementers or wrong, and those have opposite fixes. Say which pattern you see, and
> count the instances.

The second case is drift discovered by review, and Step 4's `accept` disposition is where
it goes.

## Correctness & risk

> Find real defects in the integrated result: logic errors, unhandled failure modes, race
> conditions, resource leaks, unsafe input handling, authz gaps, secrets or credentials in
> code or config, injection paths, and dependency additions with known problems.
>
> Prioritise what integration created. A defect that exists only because two issues'
> changes met — a shared cache one writes and the other assumes immutable, a migration
> ordered wrong across PRs — is what this review is for. A latent bug entirely inside one
> PR was already reviewable at PR time; report it, but rank it below the integration
> defects.
>
> Give a concrete failure scenario for each: the input or state, and the wrong result.
> Without one it is a suspicion, not a finding.
