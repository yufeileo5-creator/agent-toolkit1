$targetDir = Join-Path $HOME ".gemini/antigravity"
if (!(Test-Path $targetDir)) {
    New-Item -ItemType Directory -Force -Path $targetDir | Out-Null
}

$scriptPath = $script:MyInvocation.MyCommand.Path
$scriptDir = Split-Path $scriptPath

Write-Host "Installing Antigravity Harness to $targetDir ..." -ForegroundColor Cyan

$folders = @("skills", "workflows", "templates")
foreach ($folder in $folders) {
    $sourceFolder = Join-Path $scriptDir $folder
    if (Test-Path $sourceFolder) {
        Copy-Item -Path $sourceFolder -Destination $targetDir -Recurse -Force
        Write-Host "Copied $folder successfully." -ForegroundColor Green
    }
}

$geminiFile = Join-Path $scriptDir "GEMINI.md"
if (Test-Path $geminiFile) {
    Copy-Item -Path $geminiFile -Destination "$HOME\.gemini\GEMINI.md" -Force
    Write-Host "Copied GEMINI.md successfully." -ForegroundColor Green
}

Write-Host "Installation Complete! Bootstrap ready." -ForegroundColor Green
