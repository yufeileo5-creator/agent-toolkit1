#!/bin/bash
set -e

TARGET_DIR="$HOME/.gemini/antigravity"
mkdir -p "$TARGET_DIR"

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "开始向目标路径统一部署 Antigravity 核心环境基座: $TARGET_DIR ..."

for folder in "skills" "workflows" "templates"; do
    if [ -d "$SCRIPT_DIR/$folder" ]; then
        cp -R "$SCRIPT_DIR/$folder" "$TARGET_DIR/"
        echo "已成功同步核心目录: $folder"
    fi
done

if [ -f "$SCRIPT_DIR/GEMINI.md" ]; then
    cp "$SCRIPT_DIR/GEMINI.md" "$HOME/.gemini/GEMINI.md"
    echo "已成功同步全局法则配置: GEMINI.md"
fi

echo "部署进程圆满结束！环境自举已完成，祝您研发愉快。"
