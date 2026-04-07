@echo off
REM AI Conversational System - Quick Start Script (Windows)
REM This script sets up and runs the entire project

cls
echo.
echo ========================================
echo  AI Conversation Intelligence System
echo ========================================
echo.

REM Check if .env exists
if not exist ".env" (
    echo Creating .env file...
    (
        echo OPENAI_API_KEY=your_openai_api_key_here
        echo EMBEDDING_MODEL=all-MiniLM-L6-v2
        echo CHUNK_SIZE=512
        echo CHUNK_OVERLAP=50
        echo LLM_MODEL=gpt-3.5-turbo
    ) > .env
    echo ✓ .env file created - Please add your OPENAI_API_KEY
)

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ✗ Python not found! Please install Python 3.10+
    exit /b 1
)
echo ✓ Python found

REM Check Node.js
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ✗ Node.js not found! Please install Node.js
    exit /b 1
)
echo ✓ Node.js found

REM Setup Backend
echo.
echo --- Setting up Backend ---
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
)
call venv\Scripts\activate.bat

echo Installing Python dependencies...
pip install -q -r requirements.txt
if %errorlevel% neq 0 (
    echo ✗ Failed to install Python dependencies
    exit /b 1
)
echo ✓ Python dependencies installed

REM Setup Frontend
echo.
echo --- Setting up Frontend ---
cd frontend
echo Installing Node dependencies...
call npm install -q
if %errorlevel% neq 0 (
    echo ✗ Failed to install npm dependencies
    cd ..
    exit /b 1
)
echo ✓ Node dependencies installed
cd ..

echo.
echo ========================================
echo  ✓ Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Open two terminals
echo.
echo Terminal 1 - Backend:
echo   venv\Scripts\activate
echo   python src\api\main.py
echo.
echo Terminal 2 - Frontend:
echo   cd frontend
echo   npm run dev
echo.
echo Then open: http://localhost:3000
echo.
