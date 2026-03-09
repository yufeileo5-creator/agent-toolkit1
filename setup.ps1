<#
.SYNOPSIS
  一键安装 Antigravity Agent 全局规则 + DSP 图谱初始化。

.EXAMPLE
  .\.agents\setup.ps1
#>

$ErrorActionPreference = "Stop"

# 自动定位：脚本在 .agents/ 下，项目根目录是上一级
$AgentsDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $AgentsDir

$SourceFile = Join-Path $AgentsDir "GEMINI.md"
$TargetDir = Join-Path $env:USERPROFILE ".gemini"
$TargetFile = Join-Path $TargetDir "GEMINI.md"
$DspDir = Join-Path $ProjectRoot ".dsp"
$DspCli = Join-Path $AgentsDir "skills\data-structure-protocol\scripts\dsp-cli.py"

Write-Host ""
Write-Host "=================================" -ForegroundColor Cyan
Write-Host " Antigravity Agent 环境安装脚本" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# ── 步骤 1：安装全局规则 ──
if (!(Test-Path $SourceFile)) {
    Write-Host "[错误] 找不到 $SourceFile" -ForegroundColor Red
    exit 1
}

if (!(Test-Path $TargetDir)) {
    New-Item -ItemType Directory -Path $TargetDir -Force | Out-Null
    Write-Host "[创建] 目录 $TargetDir" -ForegroundColor Yellow
}

if (Test-Path $TargetFile) {
    Write-Host "[发现] 已存在 $TargetFile" -ForegroundColor Yellow
    $confirm = Read-Host "是否覆盖？(y/N)"
    if ($confirm -ne "y" -and $confirm -ne "Y") {
        Write-Host "[跳过] 保留现有的 GEMINI.md" -ForegroundColor Gray
    }
    else {
        Copy-Item -Path $SourceFile -Destination $TargetFile -Force
        Write-Host "[安装] GEMINI.md -> $TargetFile" -ForegroundColor Green
    }
}
else {
    Copy-Item -Path $SourceFile -Destination $TargetFile -Force
    Write-Host "[安装] GEMINI.md -> $TargetFile" -ForegroundColor Green
}

# ── 步骤 2：初始化 DSP 图谱 ──
if (Test-Path $DspDir) {
    Write-Host "[跳过] .dsp/ 已存在，无需重新初始化" -ForegroundColor Gray
}
elseif (Test-Path $DspCli) {
    Write-Host "[初始化] DSP 图谱 (.dsp/) ..." -ForegroundColor Yellow
    Push-Location $ProjectRoot
    try {
        python $DspCli init 2>&1
        if (Test-Path $DspDir) {
            Write-Host "[完成] DSP 图谱已初始化" -ForegroundColor Green
        }
        else {
            Write-Host "[警告] dsp-cli init 执行完毕但未生成 .dsp/，请手动检查" -ForegroundColor Yellow
        }
    }
    catch {
        Write-Host "[警告] DSP 初始化失败: $_" -ForegroundColor Yellow
        Write-Host "        你可以稍后手动运行: python $DspCli init" -ForegroundColor Gray
    }
    Pop-Location
}
else {
    Write-Host "[跳过] 未找到 dsp-cli.py，跳过 DSP 初始化" -ForegroundColor Gray
}

# ── 汇报结果 ──
Write-Host ""
Write-Host "=================================" -ForegroundColor Green
Write-Host " 安装完成！" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green
Write-Host ""
Write-Host "已安装:" -ForegroundColor White
Write-Host "  [v] 全局规则    -> $TargetFile" -ForegroundColor White
Write-Host "  [v] 18 个 Skills -> .agents/skills/" -ForegroundColor White
Write-Host "  [v] 计划工作流  -> .agents/workflows/plan.md" -ForegroundColor White

if (Test-Path $DspDir) {
    Write-Host "  [v] DSP 图谱    -> .dsp/" -ForegroundColor White
}
else {
    Write-Host "  [ ] DSP 图谱    -> 待初始化 (需要 Python)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "打开 Antigravity 即可使用完整配置。" -ForegroundColor Cyan
