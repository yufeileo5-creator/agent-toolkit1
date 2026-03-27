#!/bin/bash
set -e

echo -e "\033[0;36m🚀 开始初始化 Antigravity Agent Toolkit (V6神装版)...\033[0m"

TARGET_DIR="$HOME/.gemini"
REPO_URL="https://github.com/yufeileo5-creator/agent-toolkit1.git"

if [ -d "$TARGET_DIR" ]; then
    if [ -d "$TARGET_DIR/.git" ]; then
        echo -e "\033[1;33m📦 检测到已有 Toolkit 仓库，正在尝试拉取最新更新...\033[0m"
        cd "$TARGET_DIR"
        git pull origin main
    else
        BACKUP_DIR="${TARGET_DIR}.backup_$(date +%Y%m%d_%H%M%S)"
        echo -e "\033[1;33m⚠️ 检测到非 Git 版的遗留 .gemini 文件夹，正在备份至 $BACKUP_DIR\033[0m"
        mv "$TARGET_DIR" "$BACKUP_DIR"
        echo -e "\033[0;36m📥 正在从远程克隆纯净版战甲...\033[0m"
        git clone "$REPO_URL" "$TARGET_DIR"
    fi
else
    echo -e "\033[0;36m📥 正在从远程克隆纯净版战甲...\033[0m"
    git clone "$REPO_URL" "$TARGET_DIR"
fi

echo -e "\033[0;32m✅ 安装完成！你的电脑现已接管 T0 级最高宪法规则与 93 个技能弹药库！\033[0m"
echo -e "\033[0;32m重启你的 IDE 或命令行 AI 工具即可生效。\033[0m"
