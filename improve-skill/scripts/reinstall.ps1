# Reinstall a skill: mirror its dev copy into the installed skills folder,
# excluding dev-only artifacts (evals, git metadata, viewer logs).
#
# The dev root is discovered, never hardcoded — this script also ships inside the
# *installed* copy of improve-skill, where deriving the root from its own location
# would point at the install folder and mirror it onto itself. Resolution order:
# -DevRoot, then $env:SKILLS_DEV_ROOT, then this script's grandparent if it looks
# like the repo (i.e. it holds _shared/sync.ps1).
param(
    [Parameter(Mandatory = $true)][string]$SkillName,
    [string]$DevRoot,
    [string]$InstalledRoot = (Join-Path $HOME ".claude\skills")
)

function Test-DevRoot([string]$path) {
    $path -and (Test-Path (Join-Path $path "_shared\sync.ps1"))
}

if (-not $DevRoot) {
    $candidate = $env:SKILLS_DEV_ROOT
    if (-not (Test-DevRoot $candidate)) {
        $candidate = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
    }
    if (-not (Test-DevRoot $candidate)) {
        Write-Error "Can't locate the skills dev repo. Pass -DevRoot <path>, or set SKILLS_DEV_ROOT to your clone of the skills repo."
        exit 1
    }
    $DevRoot = $candidate
}

$DevRoot = (Resolve-Path $DevRoot).Path
$InstalledRoot = if (Test-Path $InstalledRoot) { (Resolve-Path $InstalledRoot).Path } else { $InstalledRoot }

if ($DevRoot -eq $InstalledRoot) {
    Write-Error "DevRoot and InstalledRoot are the same folder ($DevRoot) — refusing to mirror it onto itself."
    exit 1
}

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
