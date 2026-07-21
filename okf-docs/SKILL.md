---
name: okf-docs
description: Enforce Google's Open Knowledge Format (OKF) — a lightweight markdown + YAML-frontmatter spec for knowledge bundles — on any documentation, notes, runbooks, reference material, or knowledge-base content this session writes to disk. Use this whenever creating or editing a concept doc, an index.md, a log.md, or anything described as a "knowledge bundle" / "knowledge catalog" / "agent-readable docs", and whenever the user mentions OKF or Open Knowledge Format by name. Default to applying it any time a session produces substantive markdown documentation (design notes, playbooks, table/API/metric references, incident write-ups), not just when OKF is named explicitly — skip it only for truly incidental scratch files. Also use to validate an existing directory of markdown docs against the spec.
---

# OKF Docs

Google's Open Knowledge Format (OKF v0.1) is a directory of markdown files with YAML
frontmatter, designed so that both humans and agents can read a corpus of
knowledge without special tooling. This skill makes sure any documentation this
session writes lands in that shape, and keeps the surrounding bundle (its
`index.md` listings and `log.md` history) up to date as you go.

Full spec text (fetched from `GoogleCloudPlatform/knowledge-catalog`) is in
`references/okf-spec.md` — read it when you need an exact rule (e.g. exact
link semantics, versioning). What follows is the operating summary.

## Why this matters

OKF's whole value proposition is that a bundle stays useful precisely because
every file is self-describing and structurally predictable. A single concept
doc missing its `type` field, or a stray unlisted file, silently degrades the
bundle for whatever agent or human consumes it next. So the goal isn't just
"write good docs" — it's "write docs whose structure never has to be
guessed at."

## Core rules (conformance — never skip these)

A bundle is only OKF-conformant if:

1. Every concept `.md` file (i.e. every markdown file that isn't `index.md`
   or `log.md`) opens with a YAML frontmatter block (`---` ... `---`) that
   parses cleanly and contains a non-empty `type` field.
2. `index.md` and `log.md` are reserved — never write concept content into a
   file with either of those names. `index.md` carries **no** frontmatter,
   except a bundle-root `index.md` MAY have `okf_version: "0.1"` and nothing
   else.
3. `log.md` date headings are `## YYYY-MM-DD` (ISO 8601), newest first.

Everything else in the spec — recommended fields, index formatting, citation
numbering — is strong convention, not a hard requirement. Follow it anyway;
it's what makes the bundle pleasant rather than merely valid.

## Ignoring files (`.okfignore`)

A bundle root may contain a `.okfignore`: one gitignore-style pattern per
line, `#` comments allowed. A pattern containing `/` matches from the bundle
root; one without matches any path segment (so `sources` ignores a whole
directory anywhere). No `!` negation. Matched files are **not part of the
bundle**: the validator skips them, they need no frontmatter, and they must
not be listed in any `index.md`. Use it for non-knowledge markdown that has
to live inside the tree — raw source material, generated reports, a repo
README — especially when the bundle root is the project root.

## Workflow

**1. Find or establish the bundle root.**
Look for an existing bundle: a directory containing `index.md`/concept `.md`
files already following this pattern, often named `knowledge/`, `docs/`, or
similar. If one already exists in the project, write into it. If none
exists and you're about to write a knowledge-style doc for the first time in
this project, ask the user once where it should live (a reasonable default is
a top-level `knowledge/` directory) rather than guessing and scattering files.

**2. Write the concept doc.**
Start from `assets/concept-template.md`. Fill in:
- `type` (required) — a short, descriptive noun phrase like `BigQuery Table`,
  `API Endpoint`, `Playbook`, `Metric`, `Reference`. Don't invent a registry —
  pick whatever's self-explanatory for this concept.
- `title`, `description`, `tags`, `timestamp` (recommended) — fill these in
  whenever you know them; they're what make `index.md` generation and search
  previews actually useful. Don't leave them blank out of laziness.
- `resource` — only if the concept describes a concrete addressable asset
  (a table, an endpoint, a dashboard). Omit for abstract concepts (a
  playbook, a metric definition).
- Body — prefer structural markdown (tables, fenced code, headings) over
  prose paragraphs. Use `# Schema`, `# Examples`, `# Citations` headings where
  they apply (see `assets/concept-template.md` for the shape).
- Cross-links — link to other concepts with bundle-relative paths starting
  with `/` (e.g. `[customers](/tables/customers.md)`) rather than deep
  relative paths; they survive the file being moved later. A link to a
  concept that doesn't exist yet is fine — OKF explicitly tolerates that.

**3. Update `index.md` in the same directory.**
Every directory's `index.md` should list what's actually in it. When you add
or rename a concept, add/update its bullet:
`* [Title](file.md) - one-line description` (pull the description straight
from the concept's frontmatter). Use `assets/index-template.md` as the shape.
If a directory doesn't have an `index.md` yet and now has concepts in it,
create one.

**4. Append to `log.md` in the same directory (or the nearest ancestor that
has one).**
Add today's date as a `## YYYY-MM-DD` heading if it isn't already the most
recent one, then a bullet: `* **Update**: ...` / `* **Creation**: ...` /
`* **Deprecation**: ...` describing what changed, linking to the concept.
See `assets/log-template.md`. Don't create a `log.md` speculatively in every
directory — only maintain the ones that already exist, plus the bundle root.

**5. Validate before you finish.**
Run the bundled checker against the bundle root:

```
python scripts/validate_okf.py <bundle-root>
```

It exits non-zero only on real conformance violations (missing/malformed
frontmatter, missing `type`, misused reserved filenames, malformed `log.md`
date headings) and separately reports warnings (missing recommended fields,
broken cross-links) that are worth fixing but don't make the bundle invalid.
Fix errors before considering the doc done; use judgment on warnings.

## Quick reference

**Frontmatter fields**

| Field | Required? | Notes |
|---|---|---|
| `type` | Yes | e.g. `BigQuery Table`, `API Endpoint`, `Playbook`, `Metric` |
| `title` | Recommended | display name; falls back to filename if omitted |
| `description` | Recommended | one sentence, used in index/search previews |
| `resource` | Optional | canonical URI, only for concepts bound to a real asset |
| `tags` | Optional | YAML list |
| `timestamp` | Recommended | ISO 8601, last meaningful change |

**Conventional body headings**: `# Schema`, `# Examples`, `# Citations`.

**Link forms**: `/bundle/relative/path.md` (preferred) or `./relative.md`.

**Reserved filenames**: `index.md`, `log.md` — never use for concept content.

Full details, the two worked examples, and the versioning rules are in
`references/okf-spec.md`.
