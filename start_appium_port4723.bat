@echo off
title Appium Server - Port 4723
echo ===============================================
echo   STARTING APPIUM SERVER - PORT 4723
echo ===============================================
echo.

REM Set Android SDK environment variables for this session
set "ANDROID_HOME=%~dp0android-sdk"
set "ANDROID_SDK_ROOT=%~dp0android-sdk"
set "PATH=%ANDROID_HOME%\platform-tools;%PATH%"

echo ✅ ANDROID_HOME: %ANDROID_HOME%
echo ✅ ANDROID_SDK_ROOT: %ANDROID_SDK_ROOT%
echo ✅ Platform-tools in PATH
echo.

REM Verify ADB is working
echo Testing ADB connection...
"%ANDROID_HOME%\platform-tools\adb.exe" devices
echo.

REM Start Appium server on port 4723 (default Python script port)
echo Starting Appium Server on port 4723...
echo Server URL: http://127.0.0.1:4723
echo.
echo ⚠️  IMPORTANT: Keep this window open while running whatsapp.py
echo Press Ctrl+C to stop the server
echo.

appium server --port 4723 --log-level info
pause
