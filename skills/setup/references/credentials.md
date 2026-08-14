# Credentials

`external-reviewer` resolves no credential of its own. Everything below is
[`kern-link`](https://github.com/julienlegoux/kern-link), the library it calls through,
and applies identically to any other tool built on it.

## Resolution order

Per request, highest first:

1. A key passed by the calling program — not a path this skill uses.
2. **A stored credential** for that provider, from `~/.pi/agent/auth.json`: an OAuth
   credential (refreshed under lock when expired) or a stored API key.
3. **Ambient sources** — environment variables, the AWS credential chain, Google ADC.

A stored credential **owns** its provider: there is no silent fallback to the
environment behind it. A provider that reads as broken while its environment variable is
plainly set is a provider with a stale entry in the store.

## The store

`~/.pi/agent/auth.json`, written `0600` inside a `0700` directory, locked across
processes through an `auth.json.lock` sidecar. Unknown providers round-trip untouched.

There is no `logout`: removing a credential means deleting that provider's entry from the
file. Do that only at the user's request, and never print the file's contents.

## Logging in

```
go run github.com/julienlegoux/kern-link/cmd/pi-ai@v0.1.1 login            # interactive picker
go run github.com/julienlegoux/kern-link/cmd/pi-ai@v0.1.1 login openai-codex
go run github.com/julienlegoux/kern-link/cmd/pi-ai@v0.1.1 list             # providers and models
```

`v0.1.1` is the version `external-reviewer@v0.1.0-beta.1` links; the two share the store,
so keeping them on one version keeps the format they agree on out of the question.

Three providers support OAuth:

| Provider | Flow | What the user does |
|---|---|---|
| `openai-codex` (ChatGPT Plus/Pro) | browser PKCE on port 1455, or device code | Pick a method; the device flow prints a code for `https://auth.openai.com/codex/device` |
| `anthropic` (Claude Pro/Max) | PKCE, local callback on port 53692 | Approve the printed URL, or paste the code back |
| `github-copilot` | device code | Open the verification URI and type the shown code |

`openai-codex` has no API-key path at all — OAuth is the only way in.

## Environment variables

One per provider, read only when nothing is stored:

| Provider | Variable |
|---|---|
| `openai` | `OPENAI_API_KEY` |
| `google` | `GEMINI_API_KEY` |
| `mistral` | `MISTRAL_API_KEY` |
| `groq` | `GROQ_API_KEY` |
| `xai` | `XAI_API_KEY` |
| `deepseek` | `DEEPSEEK_API_KEY` |
| `openrouter` | `OPENROUTER_API_KEY` |
| `together` | `TOGETHER_API_KEY` |
| `fireworks` | `FIREWORKS_API_KEY` |
| `cerebras` | `CEREBRAS_API_KEY` |
| `nvidia` | `NVIDIA_API_KEY` |
| `huggingface` | `HF_TOKEN` |
| `github-copilot` | `COPILOT_GITHUB_TOKEN` |
| `anthropic` | `ANTHROPIC_OAUTH_TOKEN`, then `ANTHROPIC_API_KEY` |

`amazon-bedrock`, `google-vertex`, the Azure and Cloudflare providers each need several
variables together; `kern-link`'s `docs/auth.md` is the current list. For any provider not
above, check there rather than guessing a name — a wrong variable is indistinguishable
from an absent credential.

Check presence, never value: `[ -n "$OPENAI_API_KEY" ]`, not an echo.

## Two credential modes, two different risks

Which one the user is on is decided by how they authenticated, not by which model they
call.

- **An API key** from the provider's console bills per token under a developer agreement
  that exists so that programs can call the API. No terms-of-service question.
- **A subscription OAuth login** (Claude Pro/Max, ChatGPT Plus/Pro, GitHub Copilot) is
  not an API key. It is the credential a first-party client uses, and the library presents
  itself as that client so the request is accepted. Driving one's own subscription from
  one's own machine is what the flows are for; using it at scale, or shipping it to
  others, means directing subscriptions at programmatic access their consumer terms do
  not cover, and providers do revoke accounts for it.

Say this once if the user is heading for OAuth on a shared or automated machine. Do not
repeat it on every run.

## Family rules that make a credential useless

The reviewer refuses whole families before it ever reaches a credential, so these two
look like broken setups and are not:

- `--exclude-family` defaults to `anthropic`. A model in that family never reviews —
  which is the point of handing the pass to a second model in the first place.
- A model whose id carries no vendor segment the classifier reads is `unknown`, and an
  unknown family never reviews either. Every `github-copilot` model was in that state as
  of 2026-08.
