@echo off
title WhatsApp Automation - Complete Startup
color 0A
echo ========================================================
echo   WHATSAPP AUTOMATION - COMPLETE STARTUP
echo ========================================================
echo.

REM Check if Appium is already running on port 4723
netstat -ano | findstr :4723 > nul
if %errorlevel% == 0 (
    echo ✅ Appium server is already running on port 4723
    echo.
    goto :run_python
) else (
    echo ⚠️  Appium server is not running
    echo.
)

REM Ask user if they want to start Appium
echo Do you want to start Appium server? (Y/N)
set /p start_appium=Choice:

if /i "%start_appium%"=="Y" (
    echo.
    echo Starting Appium server in a new window...
    echo ⚠️  IMPORTANT: Keep the Appium window open!
    echo.

    REM Start Appium in a new window
    start "Appium Server - Port 4723" cmd /k "%~dp0start_appium_with_env.bat"

    echo Waiting 10 seconds for Appium to start...
    timeout /t 10 /nobreak
    echo.
) else (
    echo.
    echo ❌ Cannot proceed without Appium server!
    echo Please start Appium manually:
    echo    - Run: start_appium_with_env.bat
    echo    - Or run: appium server --port 4723
    echo.
    pause
    exit
)

:run_python
REM Check ADB devices
echo Checking ADB devices...
adb devices
echo.

REM Ask if user wants to run the Python script now
echo Do you want to run the WhatsApp automation script? (Y/N)
set /p run_script=Choice:

if /i "%run_script%"=="Y" (
    echo.
    echo Starting WhatsApp automation...
    echo.
    python whatsapp.py
) else (
    echo.
    echo Appium server is running. You can now run:
    echo    python whatsapp.py
    echo.
)

echo.
echo ========================================================
pause
