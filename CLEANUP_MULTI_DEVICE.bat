@echo off
title Cleanup Multi-Device Files
color 0E
echo ╔════════════════════════════════════════════════════════════════╗
echo ║              CLEANUP MULTI-DEVICE FILES                        ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo This will remove all multi-device batch files and documentation.
echo Your simple single-device setup will remain.
echo.
echo Files to be REMOVED:
echo   - START_MULTI_DEVICE.bat
echo   - start_single_adb.bat
echo   - start_appium_device1.bat
echo   - start_appium_device2.bat
echo   - start_appium_port4723.bat
echo   - MULTI_DEVICE_SETUP_GUIDE.md
echo   - FIX_ADB_OFFLINE_MULTI_DEVICE.md
echo   - adb_keepalive_helper.py
echo.
echo Files to KEEP:
echo   ✅ START_HERE.bat (single device)
echo   ✅ start_appium.bat
echo   ✅ start_appium_with_env.bat
echo   ✅ whatsapp.py
echo   ✅ All other single-device files
echo.
pause

echo.
echo Removing multi-device files...

del "START_MULTI_DEVICE.bat" 2>nul
del "start_single_adb.bat" 2>nul
del "start_appium_device1.bat" 2>nul
del "start_appium_device2.bat" 2>nul
del "start_appium_port4723.bat" 2>nul
del "MULTI_DEVICE_SETUP_GUIDE.md" 2>nul
del "FIX_ADB_OFFLINE_MULTI_DEVICE.md" 2>nul
del "adb_keepalive_helper.py" 2>nul

echo.
echo ✅ Cleanup complete!
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                  BACK TO SIMPLE SETUP                          ║
echo ╠════════════════════════════════════════════════════════════════╣
echo ║  To start your automation (single device):                    ║
echo ║                                                                ║
echo ║  Option 1 (Easiest):                                           ║
echo ║    START_HERE.bat                                              ║
echo ║                                                                ║
echo ║  Option 2 (Manual):                                            ║
echo ║    Terminal 1: start_appium_with_env.bat                       ║
echo ║    Terminal 2: python whatsapp.py                              ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
pause
