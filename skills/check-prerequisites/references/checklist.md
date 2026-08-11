# Requirement categories and how to probe them

A sweep list for Step 1, and a probe recipe per category for Step 2. It is a prompt for
recall, not a form to fill: skip whole categories the plan never touches, and add what
the plan names that isn't here. Every entry kept must trace back to a line in SCOPE.md,
SPECS.md or CONVENTIONS.md.

Probes below are illustrative. Prefer the project's own command over a generic one — the
real thing failing is worth more than a synthetic check passing.

## Probeable — settled without the user

| Category | What to confirm | Probe shape |
|---|---|---|
| Language runtime & toolchain | the version the plan pinned, not just "a" version | `<runtime> --version`, then compare against the pinned range |
| Native toolchain | a C/C++ compiler where anything downstream needs one | compile a hello-world, not `cc --version` |
| Package manager | the one the plan names, and that it can resolve the lockfile | the offline/frozen install command |
| Formatter & linter | the binary **and** the ruleset the plan names | run it over the repo in check mode |
| Test runner | the exact command from CONVENTIONS.md, **flags included** | run it on one existing package |
| Build & task runner | make, just, npm scripts, whatever the plan assumes | the no-op or `--dry-run` target |
| Container runtime | the daemon runs, not merely that the CLI exists | `docker run --rm hello-world` |
| Local services | database, cache, queue — reachable at the configured address | the client's ping/`SELECT 1` |
| Migrations & schema tooling | the CLI, and that it can reach the dev database | the status/version subcommand |
| Cloud & provider CLIs | installed **and** authenticated to the right account | the CLI's `whoami`/`account show` |
| Version control & pipeline | git remote, `gh auth status`, the CI provider's config parsing | `gh auth status`, `gh repo view` |
| Editor/agent-side tooling | anything the plan assumes an agent will run | invoke it once |

## User-supplied — a probe reports absence, nothing more

| Category | What the user has to do | What to check |
|---|---|---|
| Accounts & orgs | create it, or invite the project into it | the CLI reports a session on the right account |
| API keys & tokens | issue the key and place it | the variable is **set** — never its value |
| CI secrets | add each secret to the CI store | `gh secret list` (names only), or the provider's equivalent |
| Repo permissions | grant the rights the pipeline uses — milestones, merge | `gh api` a read that requires the scope |
| Paid plans & quotas | upgrade, or accept the free-tier ceiling | nothing automatic; ask, and record the answer |
| Domains, DNS & certs | register, delegate, issue | a resolution check at most; the rest is theirs |
| Third-party app config | OAuth callback URLs, webhook endpoints, app registrations | the provider's console — user-verified, recorded here |
| Hosted infrastructure | the database, bucket, or project actually provisioned | connect with the credentials they supplied |
| Device & OS policy | anything the machine's administrator must relax | re-run the failing probe after they act |

## Traps worth naming

- **The binary is not the capability.** A compiler that answers `--version` can still
  refuse to link; a test runner that runs can still abort on the one flag the standard
  requires. Probe what the plan actually invokes.
- **Local ≠ CI.** They are two machines with two sets of secrets and two toolchains.
  Every requirement is placed on one side, the other, or both — and probed on the side
  it lives on.
- **Authenticated ≠ authorized.** A green `auth status` says a session exists, not that
  it may create a milestone or merge a PR. Where the pipeline needs a right, probe an
  operation that needs it.
- **Absent ≠ blocking.** Something needed by the last milestone is not in the way of the
  first one. `Needed by` is what keeps a long list from reading as a wall.
- **A machine policy is not a project standard.** When a probe fails for something the
  machine forbids, the entry describes *this machine*. Never generalize it into the
  plan — that is how one laptop's constraint becomes every future project's rule.
