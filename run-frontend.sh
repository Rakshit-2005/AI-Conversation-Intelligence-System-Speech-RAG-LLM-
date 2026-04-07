#!/bin/bash
# AI Conversational System - Run Frontend (macOS/Linux)

cd "$(dirname "$0")/frontend"

echo ""
echo "Starting AI Conversation Intelligence Frontend..."
echo ""
echo "Frontend will be available at: http://localhost:3000"
echo ""

npm run dev
