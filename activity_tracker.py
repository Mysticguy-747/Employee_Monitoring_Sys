import time
from datetime import datetime
from pynput import mouse, keyboard
import os

# Time (in seconds) before the user is considered inactive
inactive_time_limit = 30

# Initialize the last active time to the current time
last_active_time = time.time()

# File to store the activity details
log_file = 'details.txt'
stop_file = 'stop_signal.txt'

def log_activity_status(status):
    """Logs the activity status with a timestamp to details.txt"""
    with open(log_file, 'a') as file:  # 'a' mode to append to the file
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        file.write(f'{timestamp}: User is {status}\n')

def update_activity_status():
    """Updates the terminal and log file with the current activity status"""
    global last_active_time
    last_status = None

    while True:
        if os.path.exists(stop_file):
            print("\nStop signal detected. Stopping activity tracker.")
            break

        current_time = time.time()
        if current_time - last_active_time > inactive_time_limit:
            status = 'inactive'
        else:
            status = 'active'

        # Log status if it has changed
        if status != last_status:
            print(f'\rUser is {status}', end='', flush=True)
            log_activity_status(status)
            last_status = status

        # Sleep briefly to avoid excessive CPU usage
        time.sleep(1)

def on_activity():
    """Updates the last active time when there is keyboard or mouse activity"""
    global last_active_time
    last_active_time = time.time()

def on_press(key):
    """Callback function for keyboard activity"""
    on_activity()

def on_click(x, y, button, pressed):
    """Callback function for mouse activity"""
    on_activity()

if __name__ == '__main__':
    # Start listening to mouse and keyboard events
    keyboard_listener = keyboard.Listener(on_press=on_press)
    mouse_listener = mouse.Listener(on_click=on_click)

    keyboard_listener.start()
    mouse_listener.start()

    try:
        update_activity_status()
    except KeyboardInterrupt:
        print("\nProgram stopped.")
    finally:
        keyboard_listener.stop()
        mouse_listener.stop()
