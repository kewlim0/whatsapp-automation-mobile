# Appium Connection Error - Complete Fix Guide

## The Error You're Seeing

```
Error: HTTPConnectionPool(host='localhost', port=4723): Max retries exceeded with url: /session
(Caused by NewConnectionError: Failed to establish a new connection: [WinError 10061]
No connection could be made because the target machine actively refused it')
```

**Translation:** Your Python script is trying to connect to Appium on port 4723, but there's no Appium server running.

## Root Cause

You had a **port mismatch**:
- Your batch files were starting Appium on **port 4724**
- Your Python script was looking for Appium on **port 4723** (default)

**This has now been FIXED** - all batch files now use port 4723.

---

## How to Start Everything (3 Methods)

### Method 1: Use START_HERE.bat (Easiest - Recommended)

Just double-click:
```
START_HERE.bat
```

This will:
1. Check if Appium is running
2. Start Appium if needed (in a separate window)
3. Check ADB devices
4. Optionally run your Python script

**IMPORTANT:** Keep the Appium window open while your script runs!

---

### Method 2: Manual Startup (2 Steps)

**Step 1:** Start Appium server (in one terminal/window)
```batch
# Double-click this file, or run in terminal:
start_appium_with_env.bat
```

You should see:
```
Starting Appium Server on port 4723...
Server URL: http://127.0.0.1:4723
[Appium] Welcome to Appium v2.x.x
[Appium] Appium REST http interface listener started on 0.0.0.0:4723
```

**Step 2:** Run your Python script (in a NEW terminal)
```batch
python whatsapp.py
```

---

### Method 3: Command Line (For Advanced Users)

Terminal 1 - Start Appium:
```batch
appium server --port 4723 --log-level info
```

Terminal 2 - Run Python:
```batch
python whatsapp.py
```

---

## Verification Steps

### 1. Check if Appium is Running
```batch
netstat -ano | findstr :4723
```

**Good output (Appium is running):**
```
TCP    0.0.0.0:4723           0.0.0.0:0              LISTENING       12345
TCP    [::]:4723              [::]:0                 LISTENING       12345
```

**Bad output (Appium NOT running):**
```
(no output or empty)
```

### 2. Check if ADB Detects Your Device
```batch
adb devices
```

**Good output:**
```
List of devices attached
da2a3288        device          <- Shows "device" status
```

**Bad output:**
```
List of devices attached
da2a3288        offline         <- Shows "offline" (USB power issue - see ADB_OFFLINE_FIX_SUMMARY.md)
```

### 3. Test Appium Connection Manually
Open browser and go to:
```
http://localhost:4723/status
```

**Good response (JSON):**
```json
{
  "value": {
    "ready": true,
    "message": "The server is ready to accept new connections"
  }
}
```

**Bad response:**
```
This site can't be reached
```

---

## Common Errors and Fixes

### Error: "appium: command not found"

**Cause:** Appium not installed or not in PATH

**Fix:**
```batch
# Install Appium globally
npm install -g appium

# Verify installation
appium --version

# If still not found, add to PATH:
# C:\Users\YourName\AppData\Roaming\npm
```

### Error: "Port 4723 already in use"

**Cause:** Another Appium instance or process is using port 4723

**Fix:**
```batch
# Find what's using port 4723
netstat -ano | findstr :4723

# Note the PID (last column), then kill it:
taskkill /PID <PID_NUMBER> /F

# Or kill all node processes:
taskkill /IM node.exe /F

# Then restart Appium
```

### Error: "UiAutomator2 driver not installed"

**Cause:** Appium UiAutomator2 driver missing

**Fix:**
```batch
appium driver install uiautomator2
appium driver list
```

### Error: "ANDROID_HOME not set"

**Cause:** Android SDK environment variables not configured

**Fix:** Use `start_appium_with_env.bat` instead of just `start_appium.bat`
- This batch file automatically sets ANDROID_HOME for the session

---

## Workflow: How Everything Works Together

```
1. Start Appium Server (port 4723)
   │
   ├─→ Appium loads UiAutomator2 driver
   ├─→ Appium waits for connections at http://localhost:4723
   │
2. Run Python Script (whatsapp.py)
   │
   ├─→ Python connects to Appium at localhost:4723
   ├─→ Appium receives request to control Android device
   │
3. Appium connects to Android device via ADB
   │
   ├─→ ADB uses USB connection (UDID: da2a3288)
   ├─→ Appium installs UiAutomator2 on device (first time)
   ├─→ Appium sends UI automation commands
   │
4. WhatsApp automation runs
   │
   ├─→ Opens WhatsApp
   ├─→ Sends messages
   └─→ Completes automation tasks
```

---

## Keeping Appium Running

### Problem: Appium window closes accidentally

**Solutions:**

1. **Pin the Appium window** to taskbar
2. **Use `start /min`** to minimize instead of close
3. **Run as Windows Service** (advanced):

Create `appium-service.bat`:
```batch
@echo off
:loop
appium server --port 4723 --log-level info
timeout /t 5
goto loop
```

This will auto-restart Appium if it crashes.

---

## Using Different Ports (Advanced)

If you need to use a different port (e.g., 4724):

**Option 1:** Update Python script
```batch
python whatsapp.py --port 4724
```

**Option 2:** Change default in whatsapp.py
```python
# Line 21 in whatsapp.py
APPIUM_PORT = 4724  # Change from 4723 to 4724
```

---

## Quick Reference Commands

```batch
# Start Appium
appium server --port 4723

# Check Appium version
appium --version

# List installed drivers
appium driver list

# Install UiAutomator2
appium driver install uiautomator2

# Check ADB devices
adb devices

# Restart ADB
adb kill-server
adb start-server

# Check what's on port 4723
netstat -ano | findstr :4723

# Kill all Appium/Node processes
taskkill /IM node.exe /F

# Test Appium in browser
http://localhost:4723/status
```

---

## Success Checklist

Before running your automation, verify:

- [ ] Appium server is running (port 4723)
- [ ] ADB detects device (`adb devices` shows "device")
- [ ] Android device has USB debugging enabled
- [ ] Phone is unlocked and screen is on
- [ ] UiAutomator2 driver is installed
- [ ] Python script can see Appium (no connection errors)

If all checkboxes are ✅, you're ready to run `python whatsapp.py`!

---

## Still Having Issues?

1. **Check Appium logs** in the Appium terminal window - errors are shown there
2. **Check Python error messages** - they usually point to the exact problem
3. **Verify Android settings**:
   - Developer Options enabled
   - USB debugging ON
   - Stay awake ON
   - USB debugging authorization granted
4. **Try a different USB cable/port**
5. **Restart everything**:
   ```batch
   taskkill /IM node.exe /F
   adb kill-server
   adb start-server
   # Unplug/replug phone
   # Start Appium again
   ```

---

## Files Created to Help You

- `START_HERE.bat` - All-in-one startup script
- `start_appium_port4723.bat` - Start Appium on port 4723
- `start_appium.bat` - Updated to use port 4723
- `start_appium_with_env.bat` - Updated to use port 4723 with Android SDK env
- This guide - Complete troubleshooting reference

All batch files now use the correct port (4723) so there's no more confusion!
