Write-Output "🚀 Bootstrapping Harness Engineering Environment (Windows)..."

$SourceDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$TargetDir = "$env:USERPROFILE\.gemini\antigravity"

if (-not (Test-Path -Path $TargetDir)) {
    New-Item -ItemType Directory -Force -Path $TargetDir
}

Write-Output "Copying Skills..."
if (Test-Path "$SourceDir\skills") {
    Copy-Item -Path "$SourceDir\skills" -Destination "$TargetDir\skills" -Recurse -Force
}

Write-Output "Copying Workflows..."
if (Test-Path "$SourceDir\workflows") {
    Copy-Item -Path "$SourceDir\workflows" -Destination "$TargetDir\workflows" -Recurse -Force
}

Write-Output "Copying Templates..."
if (Test-Path "$SourceDir\templates") {
    Copy-Item -Path "$SourceDir\templates" -Destination "$TargetDir\templates" -Recurse -Force
}

Write-Output "✅ Bootstrap Complete! Your Agent is fully armed with the global Harness tools."
