#!/bin/bash
echo "🚀 Bootstrapping Harness Engineering Environment (Mac/Linux)..."

# 获取当前脚本所在目录
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
TARGET_DIR="$HOME/.gemini/antigravity"

# 创建目标外层目录
mkdir -p "$TARGET_DIR"

echo "Copying Skills..."
cp -r "$DIR/skills" "$TARGET_DIR/" || echo "Warning: failed to copy skills"

echo "Copying Workflows..."
cp -r "$DIR/workflows" "$TARGET_DIR/" || echo "Warning: failed to copy workflows"

echo "Copying Templates..."
cp -r "$DIR/templates" "$TARGET_DIR/" || echo "Warning: failed to copy templates"

echo "✅ Bootstrap Complete! Your Agent is fully armed with the global Harness tools."
