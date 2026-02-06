# ADB Device Going Offline - Complete Fix Guide

## What I've Done

### 1. Modified whatsapp.py
Added ADB connection monitoring and automatic recovery:
- `check_adb_connection()` - Monitors if device is online
- `restart_adb_server()` - Restarts ADB when connection drops
- `keep_device_awake_via_adb()` - Prevents device sleep via ADB
- `maintain_adb_connection()` - Comprehensive health check

The script now checks ADB every 3 chats and automatically recovers if offline.

### 2. Created Helper Files
- `fix_windows_usb_power.bat` - Batch file to fix Windows USB settings
- `fix_usb_power_windows.md` - Detailed manual instructions
- `adb_keepalive_helper.py` - Standalone helper functions reference

## Quick Start - Fix the Issue NOW

### Step 1: Fix Windows USB Power (REQUIRED)
1. Right-click `fix_windows_usb_power.bat`
2. Select "Run as Administrator"
3. Follow the on-screen instructions
4. In Device Manager:
   - Expand "Universal Serial Bus controllers"
   - For EACH USB Hub/Root Hub:
     - Right-click → Properties → Power Management
     - UNCHECK "Allow computer to turn off..."
   - Find your Android device
   - Right-click → Properties → Power Management
   - UNCHECK "Allow computer to turn off..."
5. **RESTART YOUR COMPUTER** (important!)

### Step 2: Fix Android Device Settings
On your Android phone:
1. Go to Settings → About Phone
2. Tap "Build Number" 7 times to enable Developer Options
3. Go back → Developer Options
4. Enable these settings:
   - ✓ USB debugging (should already be on)
   - ✓ Stay awake (keeps screen on while charging)
   - ✓ Disable USB debugging authorization timeout (if available)

### Step 3: Use Better USB Setup
- Use USB 2.0 cable (not USB 3.0) - more stable
- Use cable shorter than 1.5 meters
- Connect to USB port on BACK of PC (more power than front)
- Avoid USB hubs - connect directly to motherboard

### Step 4: Test Your Setup
```batch
# Kill and restart ADB
adb kill-server
adb start-server

# Check device connection
adb devices

# Should show:
# List of devices attached
# ABC123456789    device        <- "device" not "offline"

# Keep this running while you test
adb shell "while true; do echo 'alive'; sleep 30; done"
```

Run your automation in another terminal:
```batch
python whatsapp.py
```

## How the Code Fix Works

The modified `whatsapp.py` now:

1. **Monitors ADB** every 3 processed chats
2. **Detects offline** status before it causes crashes
3. **Auto-restarts** ADB server if connection drops
4. **Keeps device awake** using ADB shell commands
5. **Logs status** so you can see what's happening

Example output you'll see:
```
[ADB_MAINTAIN] Checking ADB connection...
[ADB_MAINTAIN] Device online ✓
[KEEP_AWAKE] Keeping device awake via ADB
```

If device goes offline:
```
[ADB_MAINTAIN] Device OFFLINE! Attempting recovery...
[ADB_RESTART] Killing ADB server...
[ADB_RESTART] Starting ADB server...
[ADB_MAINTAIN] Device reconnected
```

## Troubleshooting

### Still going offline after 5+ minutes?
- Check Windows Event Viewer for USB errors
- Try different USB cable
- Try different USB port (use USB 2.0 port, not 3.0)
- Check Windows Update - install latest USB drivers

### Device shows "unauthorized"?
- On phone, tap "Always allow" when USB debugging prompt appears
- Delete `~/.android/adbkey*` and reconnect
- On phone: Developer Options → Revoke USB debugging authorizations, then reconnect

### "adb: command not found" errors in Python?
- Add ADB to Windows PATH:
  - Search "Environment Variables" in Windows
  - Edit System PATH
  - Add: `C:\Users\YourName\AppData\Local\Android\Sdk\platform-tools`
  - Restart terminal

### Device still sleeping?
- On phone: Settings → Display → Screen timeout → 30 minutes
- On phone: Developer Options → Stay awake → ON
- On phone: Battery → Turn off battery optimization for System UI

## Additional Tips

### Monitor ADB Connection in Real-Time
Open separate terminal and run:
```batch
# Watch ADB status live
:loop
adb devices
timeout /t 10
goto loop
```

### Check Device Battery Settings
Some devices aggressively kill USB:
- Disable "Battery Saver" mode
- Disable "Doze" mode for ADB/System UI
- Some brands (Xiaomi, Oppo) have extra battery restrictions

### For Very Long Runs (100+ chats)
Edit line 1860 in whatsapp.py to check MORE frequently:
```python
if (i + 1) % 2 == 0:  # Every 2 chats instead of 3
```

## Success Indicators

You'll know it's working when:
1. No "offline" messages in `adb devices`
2. Script runs for 30+ minutes without errors
3. You see regular "[ADB_MAINTAIN] Device online ✓" messages
4. Phone screen stays on while charging

## Need More Help?

If still having issues:
1. Check `txt/script_log_*.txt` for error patterns
2. Run `adb logcat > adb_log.txt` during automation
3. Check if specific operations trigger offline (photo transfer, etc.)
4. Try with just text messages (no photos) to isolate issue
