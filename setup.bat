@echo off
echo ================================
echo Civic Issue Reporter - Setup
echo ================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

echo Python found!
echo.

echo Which AI API do you want to use?
echo 1) Gemini API (recommended - free tier)
echo 2) Claude API (premium)
echo.
set /p choice="Enter choice (1 or 2): "

if "%choice%"=="1" (
    echo.
    echo Installing dependencies for Gemini...
    pip install -r requirements_gemini.txt
    
    echo.
    echo Please enter your Google API Key
    echo Get it from: https://aistudio.google.com/apikey
    set /p api_key="API Key: "
    
    set GOOGLE_API_KEY=%api_key%
    
    echo.
    echo Setup complete!
    echo Starting server with Gemini API...
    python backend_api_gemini.py
    
) else if "%choice%"=="2" (
    echo.
    echo Installing dependencies for Claude...
    pip install -r requirements.txt
    
    echo.
    echo Please enter your Anthropic API Key
    echo Get it from: https://console.anthropic.com/
    set /p api_key="API Key: "
    
    set ANTHROPIC_API_KEY=%api_key%
    
    echo.
    echo Setup complete!
    echo Starting server with Claude API...
    python backend_api.py
    
) else (
    echo Invalid choice. Please run again and select 1 or 2.
    pause
    exit /b 1
)

pause
