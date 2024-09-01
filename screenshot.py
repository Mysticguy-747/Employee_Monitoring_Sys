import pyautogui
import time
from datetime import datetime, timedelta
import os

# Directory to save screenshots
screenshot_dir = 'screenshots'
os.makedirs(screenshot_dir, exist_ok=True)

# Time interval (in seconds) between screenshots
interval = 60  # 1 minute

# File to stop the program
stop_file = 'stop_signal.txt'

# Time threshold for deleting old screenshots (7 days)
delete_threshold = timedelta(days=7)

# Function to log screenshot details
def log_screenshot_details(filename):
    with open('details.txt', 'a') as file:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        file.write(f'{timestamp}: Screenshot saved as {filename}\n')

# Function to delete screenshots older than the specified threshold
def delete_old_screenshots():
    current_time = datetime.now()
    for filename in os.listdir(screenshot_dir):
        file_path = os.path.join(screenshot_dir, filename)
        if os.path.isfile(file_path):
            file_creation_time = datetime.fromtimestamp(os.path.getctime(file_path))
            if current_time - file_creation_time > delete_threshold:
                os.remove(file_path)
                print(f"Deleted old screenshot: {filename}")

# Main loop to capture screenshots at regular intervals
try:
    while True:
        if os.path.exists(stop_file):
            print("Stop signal detected. Stopping screenshot capture.")
            break

        # Capture screenshot
        screenshot = pyautogui.screenshot()

        # Create a filename with timestamp
        filename = datetime.now().strftime('%Y%m%d_%H%M%S') + '.png'
        filepath = os.path.join(screenshot_dir, filename)

        # Save the screenshot
        screenshot.save(filepath)

        # Log the details
        log_screenshot_details(filepath)

        # Delete old screenshots
        delete_old_screenshots()

        # Wait for the next interval
        time.sleep(interval)

except KeyboardInterrupt:
    print("Screenshot capturing stopped.")
