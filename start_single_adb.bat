@echo off
title Shared ADB Server (All Devices)
color 0E
echo ========================================================
echo         SHARED ADB SERVER FOR ALL DEVICES
echo ========================================================
echo.
echo This ADB server will be used by ALL Appium instances.
echo Keep this window open while running multiple devices!
echo.

REM Kill any existing ADB servers to start fresh
echo Stopping any existing ADB servers...
adb kill-server
timeout /t 2 /nobreak > nul

REM Start ADB server
echo Starting shared ADB server...
adb start-server
echo.

REM Show connected devices
echo Connected devices:
adb devices -l
echo.

REM Keep monitoring devices
echo ========================================================
echo ADB Server is running on port 5037 (default)
echo All Appium instances will share this server
echo.
echo Monitoring devices every 30 seconds...
echo Press Ctrl+C to stop
echo ========================================================
echo.

:loop
timeout /t 30 /nobreak > nul
echo [%TIME%] Checking devices...
adb devices -l
goto loop
