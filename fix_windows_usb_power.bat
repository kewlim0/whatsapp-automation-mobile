@echo off
echo ================================================
echo Fix Windows USB Power Management for ADB
echo ================================================
echo.
echo This script will disable USB power management to prevent
echo your Android device from going offline during automation.
echo.
echo IMPORTANT: Run this as Administrator!
echo.
pause

echo.
echo [1/3] Disabling USB Selective Suspend...
powercfg /setacvaluesetting scheme_current 2a737441-1930-4402-8d77-b2bebba308a3 48e6b7a6-50f5-4782-a5d4-53bb8f07e226 0
powercfg /setdcvaluesetting scheme_current 2a737441-1930-4402-8d77-b2bebba308a3 48e6b7a6-50f5-4782-a5d4-53bb8f07e226 0
echo USB Selective Suspend disabled ✓
echo.

echo [2/3] Setting power plan to High Performance...
powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c
echo Power plan set to High Performance ✓
echo.

echo [3/3] Opening Device Manager...
echo Please manually disable power management for:
echo   - All USB Hub/Root Hub devices
echo   - Your Android device (under Portable Devices)
echo.
echo Steps:
echo   1. Right-click each USB device
echo   2. Properties → Power Management tab
echo   3. UNCHECK "Allow computer to turn off this device to save power"
echo   4. Click OK
echo.
start devmgmt.msc
echo.

echo ================================================
echo Configuration Complete!
echo ================================================
echo.
echo Next steps:
echo   1. Complete Device Manager steps above
echo   2. Restart your computer
echo   3. Enable "Stay Awake" in Android Developer Options
echo   4. Run your automation script
echo.
pause
