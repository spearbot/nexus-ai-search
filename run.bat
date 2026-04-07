@echo off
echo.
echo   NEXUS Research Cortex
echo   ----------------------

python --version >nul 2>&1
if errorlevel 1 (
    echo   ERROR: Python not found. Install from https://python.org
    pause & exit /b 1
)

if not exist .env (
    copy .env.example .env >nul
    echo   Created .env from template.
    echo   Open .env, fill in your 3 API keys, then re-run this script.
    start notepad .env
    pause & exit /b 0
)

echo   Installing dependencies...
pip install -r requirements.txt -q

echo   Launching Nexus...
streamlit run app.py
pause
