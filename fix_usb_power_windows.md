# Fix ADB Offline Issue on Windows

## Problem
ADB device goes offline after a few minutes due to Windows USB power management.

## Solution 1: Disable USB Selective Suspend (Recommended)

### Step 1: Power Options
1. Open Control Panel → Power Options
2. Click "Change plan settings" next to your active power plan
3. Click "Change advanced power settings"

### Step 2: Disable USB Suspend
4. Expand "USB settings"
5. Expand "USB selective suspend setting"
6. Set to **Disabled** for both:
   - On battery: Disabled
   - Plugged in: Disabled
7. Click Apply and OK

### Step 3: Disable Device Power Management
1. Open Device Manager (Win + X → Device Manager)
2. Expand "Universal Serial Bus controllers"
3. For EACH USB Hub/Root Hub:
   - Right-click → Properties
   - Go to "Power Management" tab
   - **UNCHECK** "Allow the computer to turn off this device to save power"
   - Click OK
4. Repeat for ALL USB hubs

### Step 4: Disable Android Device Power Management
1. In Device Manager, expand "Portable Devices" or "Android Device"
2. Find your Android device
3. Right-click → Properties → Power Management tab
4. **UNCHECK** "Allow the computer to turn off this device to save power"

## Solution 2: Keep Device Awake on Android

### Enable Developer Options on Phone:
1. Settings → About Phone → Tap "Build Number" 7 times
2. Go back → Developer Options
3. Enable "Stay Awake" (keeps screen on while charging)
4. Keep "USB debugging" enabled

## Solution 3: Use Better USB Cable
- Use USB 2.0 cable (not USB 3.0) - more stable for ADB
- Use cable shorter than 1.5 meters
- Try different USB port (avoid USB hubs)
- Use USB port on back of PC (more power than front)

## Solution 4: Kill and Restart ADB Server Periodically
See the Python code modification in `adb_keepalive.py`

## Verification
After making changes:
1. Restart computer
2. Run `adb devices` - should show "device" not "offline"
3. Run your automation script
