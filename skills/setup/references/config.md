# The tier assignment file

One hand-written TOML that says which model answers for each weight. The binary reads it
and never writes it — there is no `init` and no wizard, which is why this skill exists.

## Where it lives

| Platform | Path |
|---|---|
| Windows | `%AppData%\external-reviewer\config.toml` |
| everything else | `$XDG_CONFIG_HOME/external-reviewer/config.toml`, else `$HOME/.config/external-reviewer/config.toml` |

`EXTERNAL_REVIEWER_CONFIG` overrides that with an absolute path to the file itself. When
it is set, that is the file — writing the platform path instead produces a config nothing
reads.

`external-reviewer tiers` prints the path it looked at on its first line, whether or not
anything is there. Prefer that answer to deriving one.

## Precedence

Highest first, per invocation:

1. `--model <provider>/<id>` on the command line — bypasses tiers entirely, and the
   review contract forbids it.
2. `EXTERNAL_REVIEWER_TIER_LIGHT` / `_STANDARD` / `_HEAVY`, each holding `provider/id`.
   Overrides that one tier and leaves the others alone — the way to try a model without
   editing anything.
3. `EXTERNAL_REVIEWER_CONFIG` — where the file is.
4. Platform discovery.

## What goes in it

```toml
# Reviewed by openai-codex; anthropic is excluded by the reviewer's own default.
[tiers.light]
provider = "openai-codex"
model = "gpt-5.5-mini"

[tiers.standard]
provider = "openai-codex"
model = "gpt-5.5"

[tiers.heavy]
provider = "openai-codex"
model = "gpt-5.5"
```

- `light`, `standard`, `heavy` — the whole vocabulary. Any other table name is reported
  and ignored; the set cannot be extended from the file.
- `provider` and `model` are `kern-link`'s own ids, verbatim, exactly as
  `external-reviewer models` printed them. There is no aliasing layer to be forgiving.
- Both keys or neither: a table with one of them assigns nothing.
- A tier may be left out. It then reads `unassigned`, and a review asking for it exits 1.

The models above are an illustration of the shape, not a recommendation — read the
machine's own `models` output.

## Reading `external-reviewer tiers`

```
config  /home/user/.config/external-reviewer/config.toml

tier      model                    source                        status
light     openai-codex/gpt-5.5-mini  config                      reachable (auth=OAuth)
standard  openai-codex/gpt-5.5     EXTERNAL_REVIEWER_TIER_STANDARD  reachable (auth=OAuth)
heavy     -                        -                             unassigned
```

`source` names which knob produced the row — `config`, or the variable that overrode it.
A row that ignores an edit is a row whose source is an environment variable.

| Status | What it means | Fix |
|---|---|---|
| `reachable (auth=…)` | assigned, in the catalog, family-allowed, credential resolves | none |
| `unassigned` | nothing names a model for this weight | assign it, or leave it and use another tier |
| `not in the catalog` | the id is not a model this build knows | re-read `models`; a retired or mistyped id lands here |
| `excluded by family: anthropic` | the default exclusion, working as intended | pick a model from another family |
| `excluded by family: unknown` | the classifier cannot read a vendor from the id | pick another provider — no configuration fixes this |
| `provider unconfigured` | no credential resolves for that provider | `references/credentials.md` |
| `credential broken` | a credential exists and the provider refused it | log in again; an expired OAuth entry that failed to refresh is the usual cause |

Exit 0 covers every one of those rows, including "no tier resolves": the query was
answered. Exit 2 means the query could not be — malformed TOML, an assignment that is not
`provider/id`, or a credential store that cannot be located — and the `error:` line on
stderr says which.
