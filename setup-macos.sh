#!/usr/bin/env zsh
# macOS specific setup helpers

echo "🍎 AI Conversational System - macOS Setup Helper"

# Install Homebrew if needed
if ! command -v brew &> /dev/null; then
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Install Python if needed
if ! command -v python3 &> /dev/null; then
    echo "Installing Python..."
    brew install python@3.11
fi

# Install Node.js if needed
if ! command -v npm &> /dev/null; then
    echo "Installing Node.js..."
    brew install node
fi

# Run the setup script
bash setup.sh
