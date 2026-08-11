---
name: okf-lint
description: Semantic linter for OKF knowledge bundles — finds what a mechanical validator can't see (contradictions, index/log drift, duplicate concepts, taxonomy inconsistencies, stale content) and writes a severity-ranked report without modifying the bundle. Use whenever the user wants a knowledge bundle or docs directory audited, linted, or sanity-checked.
---

# OKF Lint

Reviews an existing OKF knowledge bundle for *semantic* problems: docs that
contradict each other, indexes that drifted from reality, concepts that
duplicate each other, taxonomy chaos, and content weirdness. It is the
companion to `okf-docs`: that skill writes and structurally validates
bundles; this one reads them with a critical eye.

Structural conformance (frontmatter parses, `type` present, reserved
filenames, log date format) is `okf-docs`' job via its `validate_okf.py`.
Don't re-litigate those rules here — but if the bundle is so structurally
broken that semantic review is pointless, say so in the report and stop.

**This skill never edits the bundle.** The deliverable is a report; the user
decides what to fix.

## Why a model-driven linter

The valuable findings — two docs disagreeing about a join key, a "Playbook"
that contains no steps, two concepts that are really the same table — cannot
be detected by pattern matching. They require actually reading the corpus
and holding it in mind. The bundled script exists only to make the
mechanical part cheap and deterministic; the reading is the job.

## Workflow

**1. Locate the bundle root.** Usually a `knowledge/` or `docs/` directory
whose files carry OKF frontmatter. If the user pointed at a specific
directory, use it. If several candidates exist, ask once. Check for a
`.okfignore` at the root; ignored files are out of scope for the lint pass
(the inventory script already skips them) — don't report findings on them,
though you may still read them as evidence.

**2. Run the inventory script:**

```
python scripts/okf_inventory.py <bundle-root>
```

It prints a digest: file census with frontmatter, index-vs-directory drift,
tag/type censuses with near-duplicate suspects, duplicate resource URIs,
timestamp anomalies, log-order and log-target problems, placeholder hits,
empty sections, and orphan candidates. **Everything it prints is a lead, not
a finding.** Leads must be verified by reading before they enter the report;
a `TODO` inside a fenced code example is not a placeholder leftover.

**3. Read the bundle.** This is the heart of the pass. Read every concept
doc (for large bundles see "Big bundles" below), building a mental model of
the domain as you go, and look for:

- **Contradictions** — the same fact stated differently in two places: join
  keys, column types, SLAs, rate limits, owners, definitions of a metric,
  whether something is included or excluded. Cross-check schema tables that
  describe the same asset. This is the highest-value finding class.
- **Overlap / duplication** — two concepts that describe the same thing
  (same `resource`, near-identical titles, or bodies covering the same
  ground). Bundles rot fastest through parallel docs that then diverge.
- **Drift** — index bullet descriptions that no longer match the concept's
  frontmatter or content; `log.md` claiming changes the files don't show
  (or silent about files that clearly changed); `timestamp` older than the
  doc's latest log mention; future timestamps.
- **Taxonomy hygiene** — tags and `type` values that are near-duplicates
  (`sales`/`Sales`, `Playbook`/`playbook`/`Runbook`), or so inconsistent
  that filtering by them would fail.
- **Content weirdness** — template leftovers and placeholders, empty
  sections, descriptions that merely restate the title, bodies that don't
  match their `type` (a Playbook with no steps, a Table with no schema),
  suspiciously thin or duplicated passages.
- **Relationship claims** — prose in doc A asserting something about doc B
  ("joined on X", "part of dataset Y") that doc B doesn't support.

**4. Write the report** to `LINT_REPORT_<N>.md` **next to the bundle root,
never inside it** (a report inside the bundle would itself be a
non-conformant concept). Exception: when the bundle root *is* the project
root there is no "next to" — put the report in the root and make sure
`LINT_REPORT_*.md` is covered by `.okfignore`, adding the pattern if missing
(this is the one write to the bundle tree the skill is allowed). `<N>` is
one more than the highest existing report number, so history is kept.

**5. Close the run** per `../_shared/feedback-interfaces.md` — the reflex for what
this run taught about *this skill*, as opposed to about the bundle. Read it; it is
silent unless something clears both its filters, which most runs is nothing.

## Report structure

Use this template:

```markdown
# OKF Lint Report <N> — <bundle path>

Date: <YYYY-MM-DD> · Files read: <n>/<total> · Verdict: <one line>

## Summary
<2-4 sentences: overall health, the one or two things most worth fixing.>

## Findings

### High — contradictions & misleading content
#### H1. <short title>
- **Where:** `file.md:line` ↔ `other.md:line`
- **Evidence:** quoted lines from each side
- **Why it matters:** <one sentence>
- **Suggested fix:** <one sentence>

### Medium — drift & duplication
#### M1. ...

### Low — hygiene
#### L1. ...

## Checked and clean
<Bullet list of check categories that came back clean, so a clean area
isn't mistaken for an unchecked one.>
```

Severity guide: **High** = a reader following the docs would be actively
misled (contradictions, wrong relationships, duplicate concepts that have
diverged). **Medium** = the bundle's self-description is out of sync (index
drift, stale timestamps/log, non-diverged duplication, taxonomy splits that
break filtering). **Low** = cosmetic hygiene (placeholders, empty sections,
weak descriptions).

## False-positive discipline

Every finding must carry quoted evidence — for contradictions, quotes from
*both* sides. If you can't quote it, don't report it. Domain docs often
contain apparent tensions that are actually correct (a raw table and a
filtered view legitimately report different row semantics); read enough
context to rule that out before flagging.

A clean bundle gets a short, confident report. Finding count is not a
quality metric — do not pad Low findings to look thorough, and do not
promote hygiene nits to Medium to make the report feel weighty.

## Big bundles

Above roughly 40 concept files, full reading may not be practical. Read
fully: everything the inventory digest flagged, plus every directory
involved in cross-links between flagged files. Sample the rest (at least
one doc per directory, preferring the largest). State explicitly in the
report header which parts were read fully vs sampled — an unread area must
never silently pass as clean.
