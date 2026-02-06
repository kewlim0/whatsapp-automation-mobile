@echo off
title Emergency Reset - Kill All Appium and ADB
color 0C
echo ╔════════════════════════════════════════════════════════════════╗
echo ║            EMERGENCY RESET - KILL ALL SERVERS                  ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo This will forcefully stop:
echo   - All Appium servers (node.exe processes)
echo   - All ADB servers
echo   - All Python automation scripts
echo.
echo ⚠️  WARNING: This will terminate ALL running automation!
echo.
pause

echo.
echo ========================================================
echo Step 1/4: Killing all Appium servers...
echo ========================================================
taskkill /IM node.exe /F 2>nul
if %errorlevel% == 0 (
    echo ✅ Appium servers killed
) else (
    echo ℹ️  No Appium servers were running
)

echo.
echo ========================================================
echo Step 2/4: Killing all Python scripts...
echo ========================================================
taskkill /IM python.exe /F 2>nul
if %errorlevel% == 0 (
    echo ✅ Python scripts killed
) else (
    echo ℹ️  No Python scripts were running
)

echo.
echo ========================================================
echo Step 3/4: Restarting ADB server...
echo ========================================================
adb kill-server
timeout /t 2 /nobreak > nul
adb start-server
echo ✅ ADB server restarted

echo.
echo ========================================================
echo Step 4/4: Verifying devices...
echo ========================================================
adb devices -l

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                      RESET COMPLETE                            ║
echo ╠════════════════════════════════════════════════════════════════╣
echo ║  All servers have been stopped and ADB restarted.              ║
echo ║                                                                ║
echo ║  You can now start fresh:                                      ║
echo ║    - Single device: START_HERE.bat                             ║
echo ║    - Multi device:  START_MULTI_DEVICE.bat                     ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
pause
