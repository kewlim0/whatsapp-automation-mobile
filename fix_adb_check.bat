@echo off
echo ========================================
echo ADB Device Connection Checker
echo ========================================
echo.

echo [1] Checking ADB devices...
adb devices
echo.

echo [2] Killing ADB server...
adb kill-server
timeout /t 2 /nobreak >nul
echo.

echo [3] Starting ADB server...
adb start-server
timeout /t 3 /nobreak >nul
echo.

echo [4] Checking devices again...
adb devices
echo.

echo [5] If device shows as 'offline', trying to reconnect...
adb reconnect
timeout /t 2 /nobreak >nul
echo.

echo [6] Final device check...
adb devices -l
echo.

echo ========================================
echo If device is still not found:
echo 1. Unplug and replug USB cable
echo 2. Check USB debugging is enabled
echo 3. Accept USB debugging prompt on phone
echo 4. Try different USB cable or port
echo ========================================
pause
