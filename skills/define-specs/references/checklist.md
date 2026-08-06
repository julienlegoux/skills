# Specs decision checklist

The floor for `define-specs`'s enumeration: each area becomes a decision doc or an
explicit `status: na` with a reason. This list is one-way doors only — if it's cheap
to reverse during implementation, it doesn't belong here. Typical dependency order;
renumber per project.

1. **Language & runtime** — Nearly everything else hangs off this. Weigh what the
   user already knows and what the repo already contains over novelty.
2. **Framework(s)** — Application framework(s) for the delivery form scope chose.
   "None / stdlib" is a legitimate option and sometimes the right recommendation.
3. **Data model & storage** — What entities exist, where they live (relational,
   document, files, none), and roughly how they relate. The single most expensive
   thing to change post-launch.
4. **Auth & authorization** — Who can do what and how identity works: none, local
   accounts, OAuth provider, magic links. Include the "is auth even in v1?" question.
5. **Interface contracts** — The shape of the system's public surface: REST/GraphQL/
   RPC, CLI argument conventions, library API. Contracts outlive implementations.
6. **External integrations** — Third-party services and APIs the project depends on.
   Each is a dependency risk; each needs a decided fallback posture (hard fail vs
   degrade).
7. **Hosting & deployment** — Where it runs and how it ships: local-only, VPS, PaaS,
   serverless, app store. Includes CI/CD shape at the "what runs on merge" level.
8. **Testing infrastructure** — Frameworks and harness (the *tooling* — test-writing
   style lives in conventions). What implement-issue's TDD loop will actually run.
9. **Error handling & observability** — Logging, error reporting, monitoring: what
   exists in v1 and what's deliberately deferred.
10. **Performance & scale targets** — Honest expected load and any latency budget.
    Usually the right v1 answer is "modest, don't architect for scale" — decide it
    explicitly so nobody gold-plates.
11. **Security & privacy** — What data is sensitive, threat posture, compliance
    constraints carried in from scope. Even "nothing sensitive, public data only"
    deserves an explicit verdict.
12. **Configuration & secrets** — How config and secrets reach the app (env vars,
    files, a manager) across dev and prod.
13. **Background work** — Async jobs, queues, schedulers — or explicitly none.
14. **Data migrations** — How schema/data changes roll out once real data exists —
    or explicitly "pre-launch, drop and recreate".
