# Bundle interfaces

Single source of truth for the rules every skill in the pipeline obeys when it writes
to `docs/` — the ledger skills that fill `docs/planning/` (`define-scope`,
`define-specs`, `define-conventions`, `map-codebase`), the ones that write epics and
issues (`split-epics`, `define-change`, `create-issues`), and the ones that implement
them (`implement-issue`, `implement-epic`). SKILL.md files point here instead of
re-describing these rules.

Two sibling files carry the parts that only concern some skills:
`ledger-interfaces.md` (the decision doc, for ledger-driven skills) and
`pipeline-interfaces.md` (epic/issue schemas, status lifecycle, GitHub facts).

This is the one and only copy: every skill that obeys these rules reads this file at
`../_shared/bundle-interfaces.md`. Editing it changes behaviour for all of them at
once.

## Language rule

All pipeline artifacts — epics, issues, decision docs, indexes, logs, drift
records — are written in **English**, regardless of the language of the conversation
that produced them. Bundles outlive their conversation and are read by later
sessions, agents, and tools; a mixed-language bundle forces every future reader to
translate. The conversation itself stays in the user's language — only what lands
on disk is English.

## The two bundles and their link rules

`docs/planning/` and `docs/epics/` are two **separate** OKF v0.1 bundles. That
split drives the link rules:

| Link | Form | Example |
|---|---|---|
| Within a bundle | bundle-relative absolute path (leading `/`, relative to the bundle root) | `[Epic 1](/epic-1-core-crud/EPIC_1.md)` |
| Across bundles (e.g. epic → planning doc) | plain relative path | `[Specs](../../planning/SPECS.md)` |

Reserved files, as the pipeline uses them:

- The **bundle root** `index.md` carries `okf_version: "0.1"` as its only
  frontmatter. **Non-root** `index.md` files (e.g. an epic's `issues/index.md`, a
  ledger's `index.md`) carry no frontmatter at all.
- `log.md` uses `## YYYY-MM-DD` headings, newest first. Append to a `log.md` that
  exists; never create one that doesn't — with one exception: the skill that
  *establishes* a bundle creates `log.md` alongside the root `index.md`. Both
  establishers of `docs/epics/` (`split-epics`, `define-change`) do, so a later
  skill's "append if it exists" reliably appends instead of silently dropping the
  bundle's history.
- Index bullets are **mechanical**: `* [Title](file.md) - <status or one-line
  description>`, tracking the target file's frontmatter — no recommendation prose,
  no commentary. When statuses change, update the bullet; when repeated edits have
  left a section disordered, rewrite the section wholesale instead of patching
  line by line.

## Committing what you write

Every skill commits the files it writes before it reports back — the bundle is a
deliverable, not a scratch pad, and a skill that leaves it dirty makes the next one
reconcile edits it didn't make. It matters most where a skill also creates GitHub
state: issue and milestone bodies link back to files like
`docs/epics/epic-1-x/EPIC_1.md`, so until the commit is pushed those links 404 for
everyone but the author.

So don't ask whether to commit, and don't defer it to the user. Stage only what the
run touched, follow the repo's commit conventions (e.g. `docs: add Epic <n> issues`),
and push to the branch doc work lands on — the integration trunk (`develop`) when one
is in play, otherwise the current branch. If the tree isn't a git repo, or has no
remote because the user declined one at scoping, do the half that applies, say so once
in the final report, and never block the deliverable on it.

**Any message longer than one line goes through a file** — write it out, then
`git commit -F <file>`. Never assemble a multi-line message inside the command line.
Heredocs and here-strings are shell-dialect specific, and a dialect that reaches the
wrong shell corrupts the message *without erroring*: a PowerShell here-string
(`git commit -m @'…'@`) executed by bash is read as three adjacent tokens and
concatenated, planting the `@` delimiters as the message's first and last lines. Git
accepts it, the commit pushes, and history is append-only — by the time anyone reads
the log it is upstream. `-F` has no quoting surface at all and behaves identically
under bash, PowerShell and cmd, which is what makes it the mechanism rather than one
option among several.
