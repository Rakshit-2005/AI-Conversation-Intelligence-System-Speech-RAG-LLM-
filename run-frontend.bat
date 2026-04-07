@echo off
REM AI Conversational System - Run Frontend (Windows)

cd /d "%~dp0\frontend"

echo.
echo Starting AI Conversation Intelligence Frontend...
echo.
echo Frontend will be available at: http://localhost:3000
echo.

call npm run dev

pause
