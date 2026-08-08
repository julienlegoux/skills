---
name: send-feedback
description: Send feedback on the lx skills upstream as a GitHub issue on julienlegoux/skills — capture the user's own words verbatim, offer the technical context around them, redact anything private, and file it through gh or a prefilled browser URL. Use when a skill misbehaved, is missing something, or sparked an idea, and the user has no clone of the skills repo to fix it in.
---

# Send Feedback

These skills ship through a marketplace to people who have no clone of the repo they
came from. When one of them misfires, the lesson dies in the session where it
happened — the person who could fix it never hears about it. This skill is the return
path: turn what just went wrong into an issue on `julienlegoux/skills`.

It needs no token, no clone and no write access. The repo is public with issues
enabled, so **any GitHub account can file one** — and where there is no account at
all, the draft still leaves the session in a form the user can paste.

`improve-skill` is the other half of the same reflex, for the maintainer: a clone, an
edit, a commit. Reach for this one when the fix isn't the user's to make, or isn't
happening now — the point is that the observation survives the session.

## What gets filed

Target repo: `julienlegoux/skills`, always. Title: `[<skill-name>] <short summary>`,
or `[lx]` when no single skill owns it. The skill name rides in the title rather than
a label because **a non-collaborator cannot apply labels** — see step 5.

Body: the user's quoted words, then the optional context block. Nothing else.

## Step 1 — The user's words, verbatim

The quoted block is theirs, not yours. Copy what they wrote, unedited — trim nothing,
smooth nothing, translate nothing.

This is the one rule here with no judgment in it, because paraphrase destroys exactly
the feedback worth having. An obvious bug survives being restated; a subtlety or a
half-formed idea does not — a reformulation lands on whatever the model already
understood, which is precisely the part that was never the problem.

If the user has only gestured at it ("this skill is useless", "meh"), ask for the
sentence they'd want the maintainer to read. Waiting for their words beats inventing
them.

## Step 2 — Offer the context, don't assume it

Draft the surrounding context and show it as a **separate block the user can accept,
trim, or drop entirely**. The quote on its own is a valid issue.

Offer only what you actually observed in this session:

- which skill fired, and the step where it went wrong
- expected versus what happened
- the shortest reproduction
- environment: plugin version (`claude plugin list`, read the `lx@…` entry), OS,
  Claude Code version

Lean toward a full block for a bug and a thin one for an idea — repro steps on a
suggestion are noise. Ask once and take the answer; don't negotiate field by field.

## Step 3 — Redact before showing

The issue is public and permanent — indexed, mirrored, cached even after deletion. So
sweep the draft *before* it is displayed, not after: absolute paths and usernames,
project, client or employer names, internal URLs and hostnames, anything key-shaped.
Replace with a placeholder and say what you replaced, so the user can put back
whatever was harmless.

Redact your context block; leave the user's quote alone. If their own words carry
something private, tell them and let *them* rewrite the sentence.

## Step 4 — Approve

Show the exact title and the exact body, as they will be posted. **Post nothing before
an explicit yes.**

That one is hard, not advisory: publishing to a public tracker under the user's own
account is outward-facing and cannot be taken back. Having asked for the skill is not
approval of the text.

## Step 5 — Submit

Try in order, stop at the first that works.

**`gh`, if `gh auth status` succeeds:**

```bash
gh issue create --repo julienlegoux/skills --title "<title>" --body-file <file> --label feedback
```

Write the body to a temp file rather than passing it inline — multi-line bodies
through a shell argument are a quoting minefield on every platform.

If it fails on the label (a non-collaborator gets `422` / "not have permission"),
retry the identical command **without** `--label`. That is the expected path for most
users, not an error worth reporting: the title carries the routing.

**Otherwise, the browser.** Build a prefilled URL against the issue form and hand it
to the user — GitHub authenticates them, and the form's own `labels:` apply whatever
their permissions. Read `references/submitting.md` for the URL shape, encoding, and
what to do when the body is too long for one.

**Otherwise, leave it on disk.** No GitHub account: write the final body to a file,
give the path plus `https://github.com/julienlegoux/skills/issues/new`, and stop.

## Step 6 — Report

Give the issue URL. If it went out through the browser path, say plainly that nothing
is filed until they press submit — that URL only opens a prefilled form.
