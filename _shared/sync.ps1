# Sync the authoritative _shared/pipeline-interfaces.md into each pipeline skill's
# references/ folder, so every installed skill is self-contained in both delivery
# modes (copy to ~/.claude/skills and plugin marketplace). Run after any edit to
# _shared/pipeline-interfaces.md; improve-skill's reinstall step runs it automatically.
param(
    [string]$DevRoot = "D:\Project\skills"
)

$source = Join-Path $DevRoot "_shared\pipeline-interfaces.md"
$pipelineSkills = @('split-epics', 'define-change', 'create-issues', 'implement-issue', 'implement-epic')

if (-not (Test-Path $source)) {
    Write-Error "Missing $source — nothing to sync."
    exit 1
}

foreach ($skill in $pipelineSkills) {
    $refDir = Join-Path $DevRoot "$skill\references"
    New-Item -ItemType Directory -Force -Path $refDir | Out-Null
    Copy-Item $source (Join-Path $refDir "pipeline-interfaces.md") -Force
}

Write-Output "Synced pipeline-interfaces.md -> $($pipelineSkills -join ', ')"
exit 0
