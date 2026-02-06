@echo off
title Appium Server - Device 2 (Port 4724)
color 0D
echo ========================================================
echo      APPIUM SERVER - DEVICE 2 (PORT 4724)
echo ========================================================
echo.

REM Set Android SDK environment
set "ANDROID_HOME=%~dp0android-sdk"
set "ANDROID_SDK_ROOT=%~dp0android-sdk"
set "PATH=%ANDROID_HOME%\platform-tools;%PATH%"

REM Use shared system ADB (don't start own ADB server)
set "APPIUM_ADB_PORT=5037"

echo ✅ Using shared ADB server on port 5037
echo ✅ ANDROID_HOME: %ANDROID_HOME%
echo.

REM Check if shared ADB is running
echo Verifying shared ADB server...
adb devices > nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ⚠️  WARNING: ADB server not running!
    echo Please start the shared ADB server first:
    echo    start_single_adb.bat
    echo.
    pause
    exit
)

echo ✅ Shared ADB server is running
echo.

REM Show connected devices
echo Connected devices:
adb devices
echo.

REM Start Appium on port 4724
echo Starting Appium Server...
echo Port: 4724
echo URL: http://127.0.0.1:4724
echo.
echo ⚠️  Keep this window open!
echo ⚠️  For Device 2 automation
echo.
echo ========================================================

appium server --port 4724 --session-override --log-level info
pause
