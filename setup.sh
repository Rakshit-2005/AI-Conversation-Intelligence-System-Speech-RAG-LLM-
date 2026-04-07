#!/bin/bash
# AI Conversational System - Quick Start Script (macOS/Linux)
# This script sets up and runs the entire project

clear

echo ""
echo "========================================"
echo "  AI Conversation Intelligence System"
echo "========================================"
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cat > .env << EOF
OPENAI_API_KEY=your_openai_api_key_here
EMBEDDING_MODEL=all-MiniLM-L6-v2
CHUNK_SIZE=512
CHUNK_OVERLAP=50
LLM_MODEL=gpt-3.5-turbo
EOF
    echo "✓ .env file created - Please add your OPENAI_API_KEY"
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "✗ Python not found! Please install Python 3.10+"
    exit 1
fi
echo "✓ Python found"

# Check Node.js
if ! command -v npm &> /dev/null; then
    echo "✗ Node.js not found! Please install Node.js"
    exit 1
fi
echo "✓ Node.js found"

# Setup Backend
echo ""
echo "--- Setting up Backend ---"
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi
source venv/bin/activate

echo "Installing Python dependencies..."
pip install -q -r requirements.txt
if [ $? -ne 0 ]; then
    echo "✗ Failed to install Python dependencies"
    exit 1
fi
echo "✓ Python dependencies installed"

# Setup Frontend
echo ""
echo "--- Setting up Frontend ---"
cd frontend
echo "Installing Node dependencies..."
npm install -q
if [ $? -ne 0 ]; then
    echo "✗ Failed to install npm dependencies"
    cd ..
    exit 1
fi
echo "✓ Node dependencies installed"
cd ..

echo ""
echo "========================================"
echo "  ✓ Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Open two terminals"
echo ""
echo "Terminal 1 - Backend:"
echo "   source venv/bin/activate"
echo "   python src/api/main.py"
echo ""
echo "Terminal 2 - Frontend:"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "Then open: http://localhost:3000"
echo ""
