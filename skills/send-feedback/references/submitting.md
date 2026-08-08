# Submitting without `gh`

Read this only when `gh auth status` failed. The browser path works for anyone with a
GitHub account and no CLI: GitHub does the authenticating, and the issue form applies
its own labels regardless of what the user is allowed to do on the repo.

## The prefilled URL

Base:

```
https://github.com/julienlegoux/skills/issues/new
```

Preferred form — target the issue template and fill its fields by `id`:

| Param | Fills |
|---|---|
| `template=feedback.yml` | selects the form (required for the field params to bind) |
| `title` | the issue title |
| `skill` | which skill the feedback is about |
| `verbatim` | the user's quoted words |
| `context` | the context block, omitted entirely if they dropped it |
| `version` | plugin / environment line |

```
https://github.com/julienlegoux/skills/issues/new?template=feedback.yml&title=…&skill=…&verbatim=…&context=…
```

Field names that don't match an `id` in `.github/ISSUE_TEMPLATE/feedback.yml` are
ignored silently — the form still opens, just empty. If a param stops binding, check
the template's ids before rewriting the URL.

Fallback, bypassing the template (blank issues are enabled, so this always resolves):

```
https://github.com/julienlegoux/skills/issues/new?title=…&body=…
```

## Encoding

Percent-encode every value. The ones that silently truncate or corrupt a body:

| Character | Encoding |
|---|---|
| newline | `%0A` |
| space | `%20` |
| `#` | `%23` |
| `&` | `%26` |
| `+` | `%2B` |
| `/` | `%2F` |
| `?` | `%3F` |

Markdown fences, backticks and `>` quote markers pass through fine — encode them
anyway if you're building the string by hand rather than with a URL encoder.

## Length

Keep the whole encoded URL under ~6000 characters. The hard ceiling is around 8 KB
(browser and server both), and encoding inflates a body with newlines and punctuation
by roughly half, so a body over ~3500 raw characters is already at risk. Failure is
ugly: a truncated body, or a `414` that looks like the link is broken.

When it doesn't fit, in order:

1. Drop the `context` param and keep the verbatim quote — that was always the part
   that had to survive.
2. Still too long: write the full body to a file, open the plain
   `issues/new?title=…` URL with the title only, and tell the user to paste the file's
   contents into the box.

## Handing it over

Print the URL and let the user click it. Don't shell out to `start` / `open` /
`xdg-open` — opening a browser tab is an outward-facing action, and the point of step
4 was that they decide when this becomes public.

Say explicitly that the issue is not filed until they press submit. A prefilled form
looks enough like a posted issue that people close the tab believing they're done.
