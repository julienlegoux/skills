# Reinstall a skill: mirror its dev copy into the installed skills folder,
# excluding dev-only artifacts (evals, git metadata, viewer logs).
param(
    [Parameter(Mandatory = $true)][string]$SkillName,
    [string]$DevRoot = "D:\Project\skills",
    [string]$InstalledRoot = (Join-Path $HOME ".claude\skills")
)

$src = Join-Path $DevRoot $SkillName
$dst = Join-Path $InstalledRoot $SkillName

if (-not (Test-Path (Join-Path $src "SKILL.md"))) {
    Write-Error "No SKILL.md found at $src — is '$SkillName' a skill in $DevRoot ?"
    exit 1
}

# Sync shared pipeline interfaces into pipeline skills' references/ first, so the
# mirror below always ships the current copy of _shared/pipeline-interfaces.md.
$sharedSync = Join-Path $DevRoot "_shared\sync.ps1"
if (Test-Path $sharedSync) {
    & $sharedSync -DevRoot $DevRoot
    if ($LASTEXITCODE -ne 0) {
        Write-Error "_shared/sync.ps1 failed with exit code $LASTEXITCODE"
        exit 1
    }
}

robocopy $src $dst /MIR /XD evals .git /XF viewer.log /NFL /NDL /NJH /NJS | Out-Null

# robocopy exit codes 0-7 mean success (files copied and/or already in sync)
if ($LASTEXITCODE -ge 8) {
    Write-Error "robocopy failed with exit code $LASTEXITCODE"
    exit 1
}

Write-Output "Reinstalled '$SkillName' -> $dst"
exit 0
