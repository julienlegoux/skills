# Sync the authoritative _shared/*-interfaces.md files into each consuming skill's
# references/ folder, so every installed skill is self-contained in both delivery
# modes (copy to ~/.claude/skills and plugin marketplace). Run after any edit to a
# shared interface; improve-skill's reinstall step runs it automatically.
#
# Each interface goes only to the skills it concerns — a skill that never writes an
# epic shouldn't carry the epic schema, and a skill that writes decision docs must
# carry their template. Add a skill to the audience below when it starts obeying the
# interface, not when it merely touches the same bundle.
#
# Path-independent: this script lives in <repo>/_shared/, so the repo root is its
# parent. Never hardcode a machine-specific path here — the repo is cloned anywhere.
param(
    [string]$DevRoot = (Split-Path -Parent $PSScriptRoot)
)

$ledgerSkills   = @('define-scope', 'define-specs', 'define-conventions', 'define-change', 'map-codebase')
$epicSkills     = @('split-epics', 'define-change', 'create-issues', 'implement-issue', 'implement-epic')

# Everything that writes under docs/ obeys the bundle rules (language, links,
# reserved files, committing).
$audiences = [ordered]@{
    'bundle-interfaces.md'   = ($ledgerSkills + $epicSkills | Select-Object -Unique)
    'ledger-interfaces.md'   = $ledgerSkills
    'pipeline-interfaces.md' = $epicSkills
}

foreach ($file in $audiences.Keys) {
    $source = Join-Path $DevRoot "_shared\$file"
    if (-not (Test-Path $source)) {
        Write-Error "Missing $source — nothing to sync."
        exit 1
    }
    foreach ($skill in $audiences[$file]) {
        $refDir = Join-Path $DevRoot "$skill\references"
        New-Item -ItemType Directory -Force -Path $refDir | Out-Null
        Copy-Item $source (Join-Path $refDir $file) -Force
    }
    Write-Output "Synced $file -> $($audiences[$file] -join ', ')"
}

exit 0
