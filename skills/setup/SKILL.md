---
name: setup
description: Set up this machine for the lx skills — today the `external-reviewer` CLI the review skills hand their analysis pass to, by installing the binary, putting a provider credential in place through kern-link's `pi-ai login`, and assigning the light/standard/heavy tiers in the machine-local `external-reviewer/config.toml`. Use to install or re-point the external reviewer, or when a review reported the external pass unavailable, or `external-reviewer tiers` leaves a tier unassigned or unreachable.
---

# Setup

What the lx skills need from the **machine**, as opposed to from a project. The
deliverable never lands in a repository: it is a binary on the `PATH`, a credential in
the user's own store, and one config file under their profile.

One subject today — the external reviewer. Anything else the pipeline comes to expect of
a machine joins it as its own section, under the same principles.

## Principles

1. **The machine, never the repo.** Nothing here is written, committed or pushed inside
   a project. A tool that configures itself into the repo under review has changed the
   thing being reviewed.
2. **Secrets are never read, echoed, or written.** Not into a config file, not into a
   transcript, not into a commit. The binary being configured reads none either — that
   is `kern-link`'s store, and it stays its business.
3. **Interactive logins and money are the user's.** An OAuth flow opens a browser and a
   review costs real tokens on their account. Hand over the command, name the cost, and
   let them run it.
4. **Verified means the tool said so.** `external-reviewer tiers` and `models` are the
   proof; "it should work now" is not a result.
5. **Never name a model the tool did not print.** A remembered id resolves to `not in
   the catalog` and looks like a broken install.

## Step 0: Where this machine stands

`command -v external-reviewer`, then `external-reviewer tiers` if it answers. That one
pair says which of the steps below still has work in it — a re-run to swap a model or
clear an expired credential is the common case, and the whole of it may be step 3.

Read the config path `tiers` prints. It is the file this machine actually uses, and it
beats re-deriving one from the platform rules.

## Step 1: Install the binary

Needs Go 1.26 or newer (`go version`) and `git` on the `PATH` for the reviewer's
`git_read` tool. There are no prebuilt binaries — `go install` is the whole distribution
story, so a machine without Go stops here, and that is the finding.

```
go install github.com/julienlegoux/external-reviewer@v0.1.0-beta.1
```

Pin the version `../_shared/external-reviewer.md` is written against rather than
`@latest`: the contract calls specific flags and reads specific exit codes, and a tag
that moves the CLI out from under it breaks every reviewer at once. `@latest` resolves to
this same beta today.

Then confirm `command -v external-reviewer` answers. That probe is the *only* thing the
review skills consult, so a binary in `$(go env GOPATH)/bin` with that directory off the
`PATH` is, to every one of them, a binary that does not exist. The fix belongs in the
user's shell profile — name the directory and the line, and let them add it.

## Step 2: A credential kern-link can find

The binary has no `login`, reads no credential and stores none. Two ways in: a
provider's environment variable, or an OAuth credential in `~/.pi/agent/auth.json` put
there by `pi-ai login`. Resolution order, variable names and the three OAuth flows are in
`references/credentials.md`.

Recommend `openai-codex` unless the user has a reason of their own: it is the only
provider v0.1 is validated against, and everything else is wired and reachable rather
than tested. Two dead ends are worth naming *before* the user spends time on them —
`anthropic`, excluded by default and for the reason the external pass exists at all, and
`github-copilot`, whose model ids carry no vendor segment the family classifier can read,
so a tier assigned there resolves to nothing however correctly it is written.

The login is interactive and browser-driven, so it is the user's to run — offer it as a
line they type:

```
! go run github.com/julienlegoux/kern-link/cmd/pi-ai@v0.1.1 login openai-codex
```

An API key in the environment needs no login at all, and carries none of the
subscription-OAuth caveat in `references/credentials.md`. Where the user already has one,
that is the shorter path.

## Step 3: Choose one model per tier

```
external-reviewer models
```

Every row is a model this machine can actually reach — the listing is already filtered by
credential and by the family rule — with its price per million tokens and its context
window. Empty output means step 2 is unfinished, not that there is nothing to pick.
`--refresh` fetches the catalogs that are fetched rather than embedded; `--all` shows
what the filters dropped and why.

What each tier is *for* is defined in `../_shared/external-reviewer.md`; read it rather
than assuming, then match each choice to the load it will carry:

- **heavy** holds a whole plan or a dozen epics at once, so choose on context window
  first. Measured runs peaked near 99k tokens of context; a window under ~200k is a real
  ceiling, not a margin.
- **light** is the one that runs often. Choose on price.
- **standard** is what every caller gets when it says nothing, so it is where a
  half-considered choice is felt most often.

A measured review costs $0.35 to $1.50. Multiply by how often this user reviews before
recommending the expensive row, and present the choice with that number attached — it
is their account.

Propose one model per tier with the reason, and let the user settle it. Assigning only
`standard` is a legitimate place to stop: it is the default every caller falls back to,
and the other two can wait until a review is actually too large or too small for it.

## Step 4: Write the assignments

Write the `[tiers.*]` tables into the config file — the path `tiers` printed, or, on a
machine where the binary is fresh, the platform path in `references/config.md`. Create
the directory if it is missing.

Preserve what is already in the file: other tiers' assignments, and any comment the user
wrote. TOML was chosen for those comments; a rewrite that drops them costs the user
something the format was picked to give them.

Never write this file inside a repository, and never commit it. It names what the user
pays for and belongs to their profile.

To try a model before committing to it, an environment override beats an edit:
`EXTERNAL_REVIEWER_TIER_HEAVY=<provider>/<id>` for one shell, one run.

## Step 5: Prove it

```
external-reviewer tiers
```

Every assigned tier should read `reachable (auth=…)`. `references/config.md` maps each
other status to its cause and its fix.

`reachable` proves the credential resolves, not that a review completes. The end-to-end
proof is a real review — minutes of wall clock and money — so offer it, name the cost,
and run it only on a yes: the `light` tier, against a small `--allow` subtree of a
repository the user picks, invoked exactly as `../_shared/external-reviewer.md` specifies.

## Handoff

Nothing in any project changes, and no skill needs telling. The next review probes
`command -v external-reviewer`, finds it, and delegates.

Come back when a credential expires, when a status turns `not in the catalog` because a
model was retired, or when a tier's weight stops matching what the user asks of it.

Then close the run per `../_shared/feedback-interfaces.md` — silently, unless this run
taught something about this skill that clears both its filters.
