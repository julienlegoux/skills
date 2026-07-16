---
name: pathfinder-v1
description: Turn a loose, foggy idea — one too big or too unclear to plan in a single session — into a shared map of investigation issues (an OKF bundle under docs/pathfinding/ mirrored to a GitHub map issue with native sub-issues), then resolve them one per session until the way forward is clear and a docs/PLAN.md can be written for split-epics. Use this whenever the user arrives with a vague or ambitious idea and no plan yet ("I want to add realtime collab but I'm not sure how", "we should rethink auth", "explore whether we can migrate to X"), asks to "chart a map", "pathfind", "start pathfinding", or wants to "work the map" / "resolve the next issue" on an existing pathfinding effort. Trigger even when the user doesn't say "pathfinder" — a big fuzzy goal with open questions is the signal. Do NOT use when a plan doc already exists (that's split-epics territory) or when the task is small enough to just plan directly.
---

# Pathfinder

A loose idea has arrived — too big for one session, and wrapped in fog: the way
from here to the **destination** isn't visible yet. Pathfinding is about finding
that way, not charging at the destination. This skill charts the way as a shared
**map** — part of the repo's OKF docs bundle, mirrored to a GitHub map issue —
then works its investigation issues one at a time until the route is clear, and
finally synthesizes what was learned into a `docs/PLAN.md` ready for the
`split-epics` skill. It is the stage *before* planning in the pipeline:

> idea → **pathfinder** → `docs/PLAN.md` → `split-epics` → `create-issues` → `implement-issue`

The same word "issue" appears at two pipeline stages, and they are different
things: a **pathfinder issue** resolves a *decision* (it produces knowledge); a
`create-issues` issue delivers a *PR* (it produces code). Both are real GitHub
issues, which is exactly the point — one tracker, one set of conventions,
different labels.

Read this whole file before starting. The confirmation step in charting is not
optional — creating the map touches a shared GitHub repo, and mis-charted maps
are annoying to fix once issues exist.

## Ground rules

These four rules shape everything below; when in doubt, come back to them.

- **Plan, don't do.** Each issue resolves a *decision*, and the map is done when
  nothing is left to decide before someone goes and builds the thing. The pull
  to just start building is usually the signal you've reached the edge of the
  map — time to synthesize the plan and hand off. An effort can override this in
  its map's Notes (carrying execution into the map), but absent that, produce
  decisions, not deliverables.
- **One issue per session.** Resolving an issue consumes context — the reading,
  the conversation, the dead ends. A second issue in the same session starts
  degraded. Chart *or* resolve one issue, then stop.
- **Refer by name.** Every map and issue has a title. In everything the human
  reads — narration, the map's Decisions so far — refer to it by that name,
  never a bare `#42`. The number and URL ride inside the name as a link
  (`[Choose a CRDT library](#43)`), never stand in for it.
- **HITL means the human answers.** Issues are either HITL (human in the loop)
  or AFK (agent works alone). A HITL issue only resolves through live exchange
  with the human — never answer your own questions on their behalf. If the
  human isn't available, the issue stays open.

## Where it lives: the docs bundle

The repo's `docs/` directory is usually already an [Open Knowledge Format](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)
(OKF v0.1) bundle — `docs/index.md` declaring `okf_version: "0.1"` is the tell.
Pathfinder joins that bundle rather than starting a parallel one:

- **`docs/` is already a bundle** → the effort lives at
  `docs/pathfinding/<effort-slug>/` *inside* it. No new `okf_version` anywhere —
  only the existing bundle root declares it. Add the effort's MAP.md to the
  bundle root `docs/index.md` listing (one line, matching its style), and
  cross-link with bundle-relative absolute paths from `docs/`, e.g.
  `[Map](/pathfinding/realtime-collab/MAP.md)`.
- **`docs/` is not a bundle (or doesn't exist)** → `docs/pathfinding/` becomes
  its own bundle root: its `index.md` declares `okf_version: "0.1"` (its only
  frontmatter) and lists efforts; cross-links are bundle-relative to
  `docs/pathfinding/`.

Either way, the OKF rules that matter:

- Every concept file (`MAP.md`, every issue `.md`) needs YAML frontmatter with a
  non-empty `type` field. OKF's recommended fields (`title`, `description`,
  `tags`, `timestamp`, `resource` once a GitHub issue exists) come first; this
  skill's tracking fields (`effort`, `issue`, `status`, `gh_issue`, etc.) are
  OKF extension fields alongside them.
- Non-root index files (the effort's `issues/index.md`) carry **no frontmatter
  at all**.
- **`log.md`**: if the bundle has one (OKF's optional reserved log — flat,
  date-grouped, newest first), append an entry for each session's bundle
  changes: the effort's creation, each resolution, the way declared clear. If
  there is no `log.md`, don't create one — same policy as `split-epics`; adding
  it unprompted is the user's call, not this skill's.

## Layout

One folder per effort, so a repo can pathfind several ideas at once. The
`issues/` folder mirrors `docs/epics/epic-N-slug/issues/` from the rest of the
pipeline:

```
docs/
├── index.md                          # bundle root (existing docs bundle, or pathfinding/index.md if standalone)
├── log.md                            # appended to if it exists — never created by this skill
└── pathfinding/
    └── <effort-slug>/
        ├── MAP.md                    # destination, notes, decisions, fog, out-of-scope
        └── issues/
            ├── index.md              # non-root index: issues + status at a glance
            ├── 01-<slug>.md
            └── 02-<slug>.md
```

The local files are the **source of truth**; GitHub is the shared, visible
mirror — the map is a GitHub issue labelled `pathfinder:map`, and each
investigation issue is a native **sub-issue** of it, so the map issue's progress
bar tracks resolution automatically and collaborators see the frontier without
cloning the repo.

## Committing and links

GitHub issue bodies link back to the local files by repo-relative path (e.g.
`docs/pathfinding/<effort-slug>/MAP.md`) — these resolve on GitHub only once the
files are committed and pushed to the default branch. So: **commit the bundle
changes at the end of each session** with a plain message (e.g. `docs:
pathfinder — chart realtime-collab` / `... resolve <issue title>`), and never
fabricate absolute `blob/...` URLs for files that haven't landed. Whether to
**push** follows the repo's practice — push if sessions have been pushing docs
directly, otherwise leave the commit local and say so in the session summary,
so the user knows the issue links won't resolve until it lands.

## The map

The map is an **index**, not a store. It lists decisions made and points at the
issues that hold their detail; a decision lives in exactly one place — its
issue — so the map never restates it, only gists it and links. Open issues are
*not* listed in the map body — they live in `issues/` (and as open sub-issues),
found by listing.

`MAP.md` template:

```markdown
---
type: Map
title: "<effort title>"
description: "<one-sentence gist of the destination>"
tags: [pathfinder, map]
timestamp: <ISO 8601, set to now>
effort: <effort-slug>
status: charting
gh_issue: null
---

# Map: <effort title>

## Destination

<what reaching the end of this map looks like — the spec, decision, or change
this effort is finding its way to. One or two lines; every session orients to it
before choosing an issue.>

## Notes

<domain context; skills every session should consult; standing preferences for
this effort — e.g. "prefer boring technology", "the map may carry execution">

## Decisions so far

<!-- one line per resolved issue: enough to judge relevance, then follow the
link for the detail the issue holds -->

- [<resolved issue title>](/pathfinding/<effort-slug>/issues/<file>.md) — <one-line gist of the answer>

## Not yet specified

<!-- fog of war: in-scope questions you can't phrase sharply yet -->

## Out of scope

<!-- work consciously ruled beyond the destination; never graduates -->
```

`status` moves `charting` → `wayfinding` (issues being worked) → `clear` (way
found, plan written). Once `gh_issue` is set, never change it.

## Investigation issues

Each issue is one decision or investigation, sized to a single agent session.
Its body is the **question**; the answer is appended on resolution, never
written in advance.

Issue file template (`issues/<nn>-<slug>.md` — `nn` zero-padded by creation
order; order is identity, not priority):

```markdown
---
type: Issue
title: "<question, phrased as a title>"
description: "<one-line restatement of the question>"
tags: [pathfinder, <issue_type>]
timestamp: <ISO 8601, set to now>
effort: <effort-slug>
issue: <nn>
issue_type: <research | prototype | grilling | task>
mode: <HITL | AFK>
status: open
gh_issue: null
depends_on: []
---

# <question, phrased as a title>

## Question

<the decision or investigation this issue resolves — sharp enough that a
session can pick it up cold>
```

On resolution, append a `## Resolution` section (see Work the map, step 5).

- **Claiming**: on GitHub, assign the issue to yourself *before any work* — the
  assignee *is* the claim, so concurrent sessions skip it. Mirror locally as
  `status: claimed`. An open, unassigned issue is unclaimed.
- **Dependencies**: `depends_on` in frontmatter (a list of issue numbers, same
  field the `create-issues` pipeline uses) is the source of truth. Mirror it as
  a `Depends on: #<gh-issue>` line at the top of the GitHub issue body so the
  ordering is visible in the tracker. An issue is **unblocked** when every
  issue in its `depends_on` is resolved.
- **The frontier**: open, unblocked, unclaimed issues — the edge of the known.
  This is where the next session picks from.

### Issue types

Every investigation issue carries a `pathfinder:<type>` label on GitHub:

- **Research** (AFK): reading documentation, third-party APIs, or local
  resources. Produces a markdown summary saved next to the issue
  (`issues/<nn>-<slug>.notes.md`) and linked from the resolution — not pasted
  into it. Use when knowledge outside the working directory is required.
- **Prototype** (HITL): raise the fidelity of the discussion with a cheap,
  rough, concrete artifact to react to — an outline, a stub, a throwaway UI.
  Build it somewhere disposable (a scratch branch or folder), link it from the
  resolution. Use when "how should it look/behave" is the key question. The
  prototype is a conversation prop, not a deliverable — resist polishing it.
- **Grilling** (HITL): a structured interview with the human — see
  [Interviewing](#interviewing) below. The default type when in doubt.
- **Task** (HITL or AFK): manual work that must happen before a *decision* can
  be made — signing up for a service so its API can be judged, provisioning
  access, moving data so its shape can be seen. The one type that *does* rather
  than decides, and it earns its place by unblocking a decision, not by
  delivering the destination. Drive it alone where possible (AFK); otherwise
  hand the human a precise checklist (HITL). The resolution records what was
  done and any resulting facts (credential locations, URLs, row counts) later
  issues depend on.

## Fog of war

The map is *deliberately* incomplete: don't chart what you can't yet see. Beyond
the live issues lies the fog — decisions you can tell are coming but can't pin
down, because they hang on questions still open. Resolving an issue clears the
fog ahead of it; whatever becomes specifiable graduates into fresh issues.

**Fog or issue?** The test is whether you can state the question precisely
*now* — not whether you can answer it now.

- **Issue** when the question is already sharp — even if it depends on others
  and can't be worked yet.
- **Not yet specified** when you can't phrase it that sharply. Don't pre-slice
  fog into issue-sized pieces — one patch may graduate into several issues, or
  none, once the frontier reaches it.

**Out of scope** is different from fog: fog only gathers *toward* the
destination. Work ruled beyond the destination goes in the map's Out of scope
section — gist plus why — and never graduates. If an existing issue turns out
to sit past the destination, close it (locally `status: out-of-scope`, on
GitHub closed as not-planned) and leave one line in Out of scope linking it. It
stays out of Decisions so far, which records only the route actually walked.

## Interviewing

Several steps below say "interview the user". The technique, inlined so this
skill stands alone:

- **One question at a time.** A wall of questions gets shallow answers to all of
  them. Ask, wait, listen, then ask the next — each question shaped by the last
  answer.
- **Concrete over abstract.** "Should presence indicators show cursor position
  or just who's online?" beats "what are your requirements for presence?".
  Offer options with trade-offs when you can see them.
- **Breadth-first when charting, depth-first when resolving.** Charting a map,
  fan out across the whole space to surface *what the open questions are* —
  resist tunneling into any single one. Resolving a grilling issue, go deep on
  that one question until it's decided.
- **Reflect decisions back.** Before recording a resolution, restate the
  decision in one or two lines and let the user correct it — that restatement
  becomes the resolution gist.

## Mode 1: Chart a map

The user arrives with a loose idea and no map yet.

1. **Name the destination.** Interview the user to pin down what this effort is
   finding its way to — a spec to hand off, a decision to lock, a change made in
   place. The destination fixes the scope, so it's settled first. Write it in
   one or two lines and get explicit agreement on the wording.
2. **Map the frontier.** Interview again, breadth-first: fan out across the
   whole space, surfacing the open decisions and the first steps takeable now.
   **If this surfaces no fog** — the way is already clear, the whole journey
   small enough to plan directly — say so and stop: the user should write (or
   ask for) `docs/PLAN.md` directly and skip the map. A map with nothing to
   discover is overhead.
3. **Draft the effort slug and issues.** Slug: lowercase kebab-case of the
   effort title, ASCII, capped ~40 chars. Draft an issue for every question you
   can state sharply now, each with a type and mode; sketch everything else into
   Not yet specified.
4. **Show the breakdown and confirm.** Before writing anything: the destination,
   each issue (number, title, type, what it depends on), the fog, and what
   happens next (local files, then one GitHub map issue and one sub-issue per
   investigation issue). Wait for explicit confirmation; adjust and re-preview
   if asked. This exists because step 6 creates repo-visible GitHub state.
5. **Write the local files.** Locate the docs bundle first (see "Where it
   lives"). Write `MAP.md` (`status: charting`), each issue file,
   `issues/index.md`, and add the effort to the bundle root's `index.md`
   listing. Append a Creation entry to `log.md` if it exists.
6. **Create the GitHub mirror.** Get the repo (`gh repo view --json
   nameWithOwner -q .nameWithOwner`), then:
   - Ensure labels exist: `pathfinder:map`, plus `pathfinder:<type>` for each
     type used (`gh label create <name> --color 5319E7 --description "..."
     2>/dev/null || true` — tolerate "already exists"; reuse any existing
     scheme first: `gh label list --json name -q '.[].name'`).
   - Create the **map issue**: title `Map: <effort title>`, label
     `pathfinder:map`, body = the map's Destination + Notes + a repo-relative
     link back to `docs/pathfinding/<effort-slug>/MAP.md`. Write bodies to a
     temp file and use `--body-file` (safer than `--body` for multi-paragraph
     text).
   - Create each **investigation issue**: title = the issue title, label
     `pathfinder:<type>`, body = the Question + a repo-relative link back to
     its `.md` file.
   - Link each one as a native sub-issue of the map:
     `bash scripts/link_sub_issue.sh <owner>/<repo> <map#> <issue#>`.
   - **Second pass — wire dependencies**: issues need numbers before they can
     reference each other, so only now edit each dependent issue's GitHub body
     to prepend its `Depends on: #<n>` line(s).
7. **Write results back.** Set `gh_issue` and
   `resource: https://github.com/<owner>/<repo>/issues/<n>` in every
   frontmatter, refresh timestamps, set the map `status: wayfinding`, and
   update both index files. Commit the bundle changes (see "Committing and
   links"). Report a summary: map issue link, issue count, the frontier, and a
   reminder that the next session works one issue.
8. **Stop.** Charting is one session's work — do not also resolve issues.

**Idempotency:** if `docs/pathfinding/<effort-slug>/MAP.md` already exists with
`gh_issue` set, don't re-chart — report it exists and offer Mode 2 instead. If
an issue file has `gh_issue` set, never recreate its GitHub issue.

## Mode 2: Work the map

The user invokes with a map (or there's exactly one effort with `status:
wayfinding`). Naming an issue is optional — without one, you pick.

1. **Load the map** — `MAP.md` plus `issues/index.md`: the low-res view, not
   every issue body. Orient to the Destination before anything else.
2. **Sync with GitHub.** Other sessions may be working concurrently. `gh issue
   list` the map's sub-issues; if a GitHub issue is closed but its local file
   still says `open`, or assigned but locally unclaimed, update the local file
   first — GitHub wins on claim/closed state, local files win on content.
3. **Choose and claim.** If the user named an issue, use it (warn if it's
   blocked or already claimed). Otherwise take the first frontier issue by
   number. Assign yourself the GitHub issue **before any work**, set the local
   `status: claimed`.
4. **Resolve it** per its type (see Issue types). Zoom as needed — read the
   full body of any related resolved issue on demand; consult whatever skills
   the map's Notes name. Honor HITL: if the issue needs the human and they're
   not responsive, leave it claimed and stop rather than inventing answers.
5. **Record the resolution.**
   - Append to the issue file:

     ```markdown
     ## Resolution

     <the answer — the decision made and the key reasoning. Link assets
     (research notes, prototypes); don't paste them in.>
     ```

   - Set `status: resolved`, refresh `timestamp`.
   - Post the same resolution as a comment on the GitHub issue, then close it.
   - Append one line to the map's **Decisions so far** — name-linked gist, per
     the Refer-by-name rule.
   - Update `issues/index.md`, and append a log entry if `log.md` exists.
6. **Advance the frontier.** Graduate any fog the answer has made specifiable
   into new issues (create file + GitHub issue + sub-issue link + dependencies,
   exactly as in charting steps 5–7), clearing each graduated patch from Not
   yet specified so it lives only as its issue. If the answer reveals an issue
   sits beyond the destination, rule it out of scope (see Fog of war). If the
   decision invalidates other open issues, update or close them.
7. **Stop** — one issue per session. Commit the bundle changes. Report: what
   was decided, what graduated, what the frontier looks like now.

## Mode 3: Declare the way clear

When step 6 of a work session leaves **no open issues and no fog**, the map is
done. In that session or the next:

1. Confirm with the user that the way is clear — walk the Decisions so far
   against the Destination and check nothing is left to decide.
2. **Synthesize `docs/PLAN.md`** from the map: the destination becomes the
   plan's goal, the decisions become its approach and constraints, out-of-scope
   items become explicit non-goals. Pull detail from issue resolutions — the
   plan must stand alone; a reader must not need the map to act on it, because
   `split-epics` will treat it as the source of truth. If a `docs/PLAN.md`
   already exists, ask before overwriting — never clobber it silently.
3. **Offer to promote durable knowledge.** Research notes often outlive the
   effort — a provider comparison or an auth-flow write-up is bundle-worthy
   reference material (like a `type: Guide` concept doc), not just a decision
   artifact. Offer to graduate any such notes into proper concept files in the
   docs bundle, listed in the root `index.md`. Offer, don't just do it — what
   belongs in the long-lived bundle is the user's call.
4. Set the map `status: clear`, refresh its timestamp, close the map issue with
   a comment pointing at `docs/PLAN.md` (repo-relative), update the bundle
   indexes, append a log entry if `log.md` exists, and commit.
5. Tell the user the pipeline continues with `split-epics` on the new plan.
