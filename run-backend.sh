#!/bin/bash
# AI Conversational System - Run Backend (macOS/Linux)

cd "$(dirname "$0")"

# Activate virtual environment
source venv/bin/activate

# Start backend
echo ""
echo "Starting AI Conversation Intelligence Backend..."
echo ""
echo "Backend will be available at: http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"
echo ""

python src/api/main.py
