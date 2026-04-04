#!/bin/bash
set -e

TARGET_DIR="$HOME/.gemini/antigravity"
mkdir -p "$TARGET_DIR"

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "Installing Antigravity Harness to $TARGET_DIR ..."

for folder in "skills" "workflows" "templates"; do
    if [ -d "$SCRIPT_DIR/$folder" ]; then
        cp -R "$SCRIPT_DIR/$folder" "$TARGET_DIR/"
        echo "Copied $folder successfully."
    fi
done

if [ -f "$SCRIPT_DIR/GEMINI.md" ]; then
    cp "$SCRIPT_DIR/GEMINI.md" "$HOME/.gemini/GEMINI.md"
    echo "Copied GEMINI.md successfully."
fi

echo "Installation Complete! Bootstrap ready."
