---
type: Contract
title: "Shared interfaces"
description: "The three _shared/ contracts, split by audience, and the sync mechanism that copies each into the references/ of the skills that obey it."
tags: [contracts, shared, sync, architecture]
timestamp: 2026-08-06
---

# Shared interfaces

Anything more than one skill has to agree on lives in `_shared/` — **once**. A
`SKILL.md` points at its synced copy instead of restating the rule, so a format can
never drift between the skill that writes it and the skill that reads it.

The contracts are split by **audience**, not by topic, so no skill carries rules that
don't apply to it. A skill that never writes an epic shouldn't ship the epic schema.

# Schema

| Interface | Defines | Audience |
|---|---|---|
| [`bundle-interfaces.md`](../_shared/bundle-interfaces.md) | English-only content, the two bundles (`docs/planning/`, `docs/epics/`) and their link forms, reserved `index.md`/`log.md`, committing what you write | every skill that writes under `docs/` |
| [`ledger-interfaces.md`](../_shared/ledger-interfaces.md) | the decision doc schema and the reopening rule | the ledger-driven planning skills |
| [`pipeline-interfaces.md`](../_shared/pipeline-interfaces.md) | epic & issue schemas, the issue status lifecycle, GitHub facts about non-default integration branches | the epic-to-PR skills |

The audience map is not documentation — it is executable, at the top of
`_shared/sync.ps1`:

```powershell
$ledgerSkills = @('define-scope','define-specs','define-conventions','define-change','map-codebase')
$epicSkills   = @('split-epics','define-change','create-issues','implement-issue','implement-epic')

$audiences = [ordered]@{
    'bundle-interfaces.md'   = ($ledgerSkills + $epicSkills | Select-Object -Unique)
    'ledger-interfaces.md'   = $ledgerSkills
    'pipeline-interfaces.md' = $epicSkills
}
```

Add a skill to an audience when it starts **obeying** the interface — not when it
merely touches the same bundle.

# The sync rule

```
_shared/<file>.md   →   <skill>/references/<file>.md
```

Each consuming skill ships a copy under its `references/` so it stays self-contained
in both delivery modes (plugin install, and a plain folder copy into
`~/.claude/skills`). That redundancy is the point — and it is also the trap:

> **Never edit a synced copy.** Edit the file in `_shared/`, then run
> `pwsh _shared/sync.ps1`. A copy edited in place is silently overwritten on the next
> sync, and until then the pipeline holds two contradicting contracts.

Synced copies are committed to git, so a stale one shows up as an unexpected diff
after any sync — that diff is the tell that someone edited the wrong file.

# When a rule stops fitting

If a rule applies to only part of an interface's audience, **split the interface**
rather than adding "skip this section if…". Splitting keeps every skill's context
free of instructions it must reason past. That is exactly how the single original
`pipeline-interfaces.md` became the three files above.

Splitting means: create the new `_shared/` file, update the audience map in
`sync.ps1`, repoint the affected `SKILL.md` files, re-sync, and reinstall every skill
in the changed audiences — see [Skill lifecycle](/skill-lifecycle.md).

# Citations

* `_shared/sync.ps1`
* `_shared/bundle-interfaces.md`, `_shared/ledger-interfaces.md`, `_shared/pipeline-interfaces.md`
* `improve-skill/SKILL.md` — "How to write skill edits — the structural rules"
