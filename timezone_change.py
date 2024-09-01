import time
from datetime import datetime
import pytz
import os
import platform

# File to store the time zone change details
log_file = 'details.txt'
stop_file = 'stop_signal.txt'

def log_timezone_change(old_tz, new_tz):
    """Logs the time zone change with a timestamp to details.txt"""
    with open(log_file, 'a') as file:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        file.write(f'{timestamp}: Time zone changed from {old_tz} to {new_tz}\n')

def get_current_timezone():
    """Returns the current system time zone"""
    if platform.system() == 'Windows':
        # Windows-specific time zone detection
        import winreg
        try:
            reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SYSTEM\CurrentControlSet\Control\TimeZoneInformation')
            time_zone = winreg.QueryValueEx(reg_key, 'TimeZoneKeyName')[0]
            return time_zone
        except Exception as e:
            print(f"Error reading time zone from Windows registry: {e}")
            return 'Unknown'
    else:
        # Unix-like systems
        try:
            return time.tzname[time.daylight]
        except Exception as e:
            print(f"Error getting time zone on Unix-like system: {e}")
            return 'Unknown'

def monitor_timezone_changes():
    """Monitors and detects time zone changes"""
    current_tz = get_current_timezone()
    print(f'Initial Time Zone: {current_tz}')

    while True:
        if os.path.exists(stop_file):
            print("\nStop signal detected. Stopping time zone monitor.")
            break

        time.sleep(1)  # Check every second for faster detection
        new_tz = get_current_timezone()
        if new_tz != current_tz:
            print(f'\033[91mTime zone changed from {current_tz} to {new_tz}\033[0m')
            log_timezone_change(current_tz, new_tz)
            current_tz = new_tz

if __name__ == '__main__':
    monitor_timezone_changes()
