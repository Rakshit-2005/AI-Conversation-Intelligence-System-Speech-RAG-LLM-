@echo off
REM AI Conversational System - Run Backend (Windows)

cd /d "%~dp0"

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Set environment variables from .env if they exist
for /f "tokens=*" %%i in ('type .env 2^>nul ^| findstr /v "^REM"') do set %%i

REM Start backend
echo.
echo Starting AI Conversation Intelligence Backend...
echo.
echo Backend will be available at: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.
python src\api\main.py

pause
