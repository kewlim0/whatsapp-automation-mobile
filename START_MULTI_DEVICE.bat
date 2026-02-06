@echo off
title Multi-Device WhatsApp Automation - Master Control
color 0A
echo ╔════════════════════════════════════════════════════════════════╗
echo ║       MULTI-DEVICE WHATSAPP AUTOMATION - MASTER STARTUP        ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Check how many devices are connected
echo Checking connected devices...
adb devices > temp_devices.txt
findstr /R "device$" temp_devices.txt > temp_device_count.txt
for /f %%i in ('find /c /v "" ^< temp_device_count.txt') do set device_count=%%i
del temp_devices.txt temp_device_count.txt

echo.
echo Found %device_count% connected device(s)
echo.

if %device_count% LSS 1 (
    echo ❌ ERROR: No devices connected!
    echo.
    echo Please:
    echo   1. Connect your Android device(s) via USB
    echo   2. Enable USB debugging
    echo   3. Run: adb devices
    echo.
    pause
    exit
)

echo ========================================================
echo Step 1/4: Starting Shared ADB Server
echo ========================================================
echo.
start "Shared ADB Server" cmd /k "%~dp0start_single_adb.bat"
echo ✅ Shared ADB server started in new window
echo.
timeout /t 5 /nobreak

echo ========================================================
echo Step 2/4: Starting Appium Servers
echo ========================================================
echo.

if %device_count% GEQ 1 (
    echo Starting Appium for Device 1 (Port 4723)...
    start "Appium - Device 1 - Port 4723" cmd /k "%~dp0start_appium_device1.bat"
    echo ✅ Appium Device 1 started
    timeout /t 5 /nobreak
)

if %device_count% GEQ 2 (
    echo.
    echo Starting Appium for Device 2 (Port 4724)...
    start "Appium - Device 2 - Port 4724" cmd /k "%~dp0start_appium_device2.bat"
    echo ✅ Appium Device 2 started
    timeout /t 5 /nobreak
)

echo.
echo ========================================================
echo Step 3/4: Verifying Setup
echo ========================================================
echo.

echo Checking ADB server...
adb devices
echo.

echo Checking Appium servers...
netstat -ano | findstr :4723
if %device_count% GEQ 2 (
    netstat -ano | findstr :4724
)
echo.

echo ========================================================
echo Step 4/4: Ready to Run Automation
echo ========================================================
echo.
echo All servers are running! You can now:
echo.

if %device_count% GEQ 1 (
    echo   Device 1: python whatsapp.py --port 4723
)

if %device_count% GEQ 2 (
    echo   Device 2: python whatsapp.py --port 4724
)

echo.
echo ========================================================
echo Do you want to start automation now?
echo ========================================================
echo.
echo 1. Device 1 only
if %device_count% GEQ 2 (
    echo 2. Device 2 only
    echo 3. Both devices in parallel
)
echo 0. Exit (manual control)
echo.
set /p choice=Enter your choice:

if "%choice%"=="1" (
    echo.
    echo Starting automation on Device 1...
    start "Automation - Device 1" cmd /k python whatsapp.py --port 4723
    goto :end
)

if "%choice%"=="2" (
    if %device_count% GEQ 2 (
        echo.
        echo Starting automation on Device 2...
        start "Automation - Device 2" cmd /k python whatsapp.py --port 4724
        goto :end
    ) else (
        echo Only 1 device connected!
    )
)

if "%choice%"=="3" (
    if %device_count% GEQ 2 (
        echo.
        echo Starting automation on BOTH devices...
        start "Automation - Device 1" cmd /k python whatsapp.py --port 4723
        timeout /t 2 /nobreak
        start "Automation - Device 2" cmd /k python whatsapp.py --port 4724
        goto :end
    ) else (
        echo Only 1 device connected!
    )
)

:end
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                    SERVERS ARE RUNNING                         ║
echo ╠════════════════════════════════════════════════════════════════╣
echo ║  Keep all windows open while automation runs!                  ║
echo ║                                                                ║
echo ║  To stop everything:                                           ║
echo ║  - Press Ctrl+C in each window                                 ║
echo ║  - Or run: taskkill /IM node.exe /F                            ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
pause
