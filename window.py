import time
from datetime import datetime
import os
import pygetwindow as gw

LOG_FILE = 'details.txt'
CHECK_INTERVAL = 1  # Check every 1 second
stop_file = 'stop_signal.txt'

def log_event(message):
    """Log events with a timestamp to details.txt"""
    with open(LOG_FILE, 'a') as file:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        file.write(f'{timestamp}: {message}\n')

def get_active_window_title():
    """Returns the title of the currently active window."""
    window = gw.getActiveWindow()
    return window.title if window else None

def main():
    last_app = None
    last_switch_time = time.time()

    while True:
        if os.path.exists(stop_file):
            log_event("Stop signal detected. Stopping window tracker.")
            break

        current_app = get_active_window_title()
        
        if current_app != last_app:
            if last_app:
                time_spent = time.time() - last_switch_time
                log_event(f'Switched from "{last_app}" to "{current_app}" after {time_spent:.2f} seconds.')
            last_app = current_app
            last_switch_time = time.time()

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
