#!/usr/bin/env python3
"""
ADB Keepalive Helper - Functions to prevent ADB from going offline
Add these functions to your whatsapp.py script
"""

import subprocess
import time

def check_adb_connection(device_udid=None):
    """Check if ADB device is still online"""
    try:
        result = subprocess.run(['adb', 'devices'],
                              capture_output=True,
                              text=True,
                              check=True,
                              timeout=5)

        lines = result.stdout.strip().split('\n')
        for line in lines[1:]:
            if device_udid:
                if device_udid in line and '\tdevice' in line:
                    return True
            else:
                if '\tdevice' in line:
                    return True
        return False
    except Exception as e:
        print(f"[ADB_CHECK] Error checking ADB: {e}")
        return False

def restart_adb_server():
    """Restart ADB server to recover connection"""
    try:
        print("[ADB_RESTART] Killing ADB server...")
        subprocess.run(['adb', 'kill-server'],
                      capture_output=True,
                      timeout=10)
        time.sleep(2)

        print("[ADB_RESTART] Starting ADB server...")
        subprocess.run(['adb', 'start-server'],
                      capture_output=True,
                      timeout=10)
        time.sleep(3)

        print("[ADB_RESTART] ADB server restarted")
        return True
    except Exception as e:
        print(f"[ADB_RESTART] Failed to restart ADB: {e}")
        return False

def reconnect_device(device_udid):
    """Try to reconnect to a specific device"""
    try:
        print(f"[ADB_RECONNECT] Reconnecting to device {device_udid}...")

        # Try reconnect command
        subprocess.run(['adb', '-s', device_udid, 'reconnect'],
                      capture_output=True,
                      timeout=10)
        time.sleep(2)

        # Verify connection
        if check_adb_connection(device_udid):
            print(f"[ADB_RECONNECT] Successfully reconnected to {device_udid}")
            return True
        else:
            print(f"[ADB_RECONNECT] Reconnect failed, trying server restart...")
            return restart_adb_server()

    except Exception as e:
        print(f"[ADB_RECONNECT] Error reconnecting: {e}")
        return restart_adb_server()

def keep_device_awake_via_adb(device_udid=None):
    """Send periodic commands to keep device awake via ADB"""
    try:
        cmd = ['adb']
        if device_udid:
            cmd.extend(['-s', device_udid])

        # Keep screen on
        cmd.extend(['shell', 'input', 'keyevent', 'KEYCODE_WAKEUP'])
        subprocess.run(cmd, capture_output=True, timeout=5)

        # Disable auto-sleep while plugged in
        cmd = ['adb']
        if device_udid:
            cmd.extend(['-s', device_udid])
        cmd.extend(['shell', 'svc', 'power', 'stayon', 'true'])
        subprocess.run(cmd, capture_output=True, timeout=5)

        return True
    except Exception as e:
        print(f"[KEEP_AWAKE] Error: {e}")
        return False

def maintain_adb_connection(device_udid, driver):
    """
    Comprehensive ADB connection maintenance
    Call this periodically during your automation (e.g., every 5 chats)
    """
    print("[ADB_MAINTAIN] Checking ADB connection health...")

    # Check if device is still online
    if not check_adb_connection(device_udid):
        print(f"[ADB_MAINTAIN] Device {device_udid} is OFFLINE! Attempting recovery...")

        # Try to reconnect
        if reconnect_device(device_udid):
            print("[ADB_MAINTAIN] Device reconnected successfully")
        else:
            print("[ADB_MAINTAIN] Failed to reconnect device")
            return False
    else:
        print(f"[ADB_MAINTAIN] Device {device_udid} is online and healthy")

    # Keep device awake
    keep_device_awake_via_adb(device_udid)

    # Verify Appium driver is still alive
    try:
        driver.get_window_size()
        print("[ADB_MAINTAIN] Appium driver is responsive")
    except Exception as e:
        print(f"[ADB_MAINTAIN] Appium driver is unresponsive: {e}")
        return False

    return True

# Example usage in your main loop:
# Call maintain_adb_connection every N chats to prevent offline issues
"""
# In your process_target_chats function, add this every 5 chats:

    if (i + 1) % 5 == 0:  # Every 5 chats
        maintain_adb_connection(SELECTED_ADB_DEVICE, driver)
"""
