$targetDir = Join-Path $HOME ".gemini/antigravity"
if (!(Test-Path $targetDir)) {
    New-Item -ItemType Directory -Force -Path $targetDir | Out-Null
}

$scriptPath = $script:MyInvocation.MyCommand.Path
$scriptDir = Split-Path $scriptPath

Write-Host "正在向目标路径安装部署 Antigravity 全局脚手架: $targetDir ..." -ForegroundColor Cyan

$folders = @("skills", "workflows", "templates")
foreach ($folder in $folders) {
    $sourceFolder = Join-Path $scriptDir $folder
    if (Test-Path $sourceFolder) {
        Copy-Item -Path $sourceFolder -Destination $targetDir -Recurse -Force
        Write-Host "成功复制并覆盖目录: $folder" -ForegroundColor Green
    }
}

$geminiFile = Join-Path $scriptDir "GEMINI.md"
if (Test-Path $geminiFile) {
    Copy-Item -Path $geminiFile -Destination "$HOME\.gemini\GEMINI.md" -Force
    Write-Host "成功复制并覆盖全局底层规则: GEMINI.md" -ForegroundColor Green
}

Write-Host "安装与部署彻底完成！所有的底层技能与工作流已就绪激活。" -ForegroundColor Green
