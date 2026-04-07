@echo off
REM Agent Monster Quick Install Script (Windows)

echo Agent Monster - Quick Install
echo ================================

REM Check Python
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo Python 3 is required
    exit /b 1
)

echo Python is installed

REM Check Git
where git >nul 2>&1
if %errorlevel% neq 0 (
    echo Git is required
    exit /b 1
)

echo Git is installed

REM Install dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt

REM Claim starter pet
echo.
echo Claiming your starter pet...
python claim_pet.py

echo.
echo ================================
echo Installation complete!
echo.
echo Usage:
echo    /monster init       - Re-initialize
echo    /monster status     - View pet status
echo    /monster analyze    - Analyze repository
echo    /monster traps      - Scan traps
echo    /monster duel       - Start battle
echo.
echo Hide food cookies:
echo    Add in code: # agent_monster cookie 0x...
echo.
echo Pet egg incubation:
echo    Wait 72 hours for automatic hatching
echo.

pause
