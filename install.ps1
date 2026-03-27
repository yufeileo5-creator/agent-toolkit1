$ErrorActionPreference = "Stop"

Write-Host "🚀 开始初始化 Antigravity Agent Toolkit (V6神装版)..." -ForegroundColor Cyan

$targetDir = "$env:USERPROFILE\.gemini"
$repoUrl = "https://github.com/yufeileo5-creator/agent-toolkit1.git"

if (Test-Path -Path $targetDir) {
    if (Test-Path -Path "$targetDir\.git") {
        Write-Host "📦 检测到已有 Toolkit 仓库，正在尝试拉取最新更新..." -ForegroundColor Yellow
        Push-Location $targetDir
        git pull origin main
        Pop-Location
    } else {
        $backupDir = "$targetDir.backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
        Write-Host "⚠️ 检测到非 Git 版的遗留 .gemini 文件夹，正在备份至 $backupDir" -ForegroundColor Yellow
        Rename-Item -Path $targetDir -NewName $backupDir
        Write-Host "📥 正在从远程克隆纯净版战甲..." -ForegroundColor Cyan
        git clone $repoUrl $targetDir
    }
} else {
    Write-Host "📥 正在从远程克隆纯净版战甲..." -ForegroundColor Cyan
    git clone $repoUrl $targetDir
}

Write-Host "✅ 安装完成！你的电脑现已接管 T0 级最高宪法规则与 93 个技能弹药库！" -ForegroundColor Green
Write-Host "重启你的 IDE 或命令行 AI 工具即可生效。" -ForegroundColor Green
