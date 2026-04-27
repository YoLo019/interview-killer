param(
    [string]$Pack = "",
    [switch]$NoBrowser,
    [int]$Port = 8765
)

$scriptPath = Join-Path $PSScriptRoot "scripts\review_server.py"

if (-not (Test-Path $scriptPath)) {
    Write-Error "review_server.py not found: $scriptPath"
    exit 1
}

$interviewDir = Join-Path $PSScriptRoot ".interview"
$packsDir = Join-Path $PSScriptRoot "interview-packs"

if (-not (Test-Path $interviewDir)) {
    New-Item -ItemType Directory -Path $interviewDir | Out-Null
}

if (-not (Test-Path $packsDir)) {
    New-Item -ItemType Directory -Path $packsDir | Out-Null
}

$arguments = @($scriptPath, "--port", $Port)
if ($Pack) {
    $arguments += @("--pack", $Pack)
}
if ($NoBrowser) {
    $arguments += "--no-browser"
}

python @arguments
