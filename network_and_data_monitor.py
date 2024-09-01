import time
from datetime import datetime
from threading import Thread, Event
import requests
import os

# Configuration
CHECK_INTERVAL = 10  # Time interval in seconds for checking the connection
LOG_FILE = 'details.txt'  # Use this file for logging network status
stop_file = 'stop_signal.txt'

# Event for graceful shutdown
shutdown_event = Event()

def log_event(message):
    """Log events with a timestamp to details.txt"""
    with open(LOG_FILE, 'a') as file:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        file.write(f'{timestamp}: {message}\n')

def check_internet_connection():
    """Check if the internet connection is available."""
    try:
        # Attempt to make a request to a known URL
        response = requests.get('https://www.google.com', timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

def monitor_network():
    """Monitor network status in real-time."""
    last_status = None
    while not shutdown_event.is_set():
        if os.path.exists(stop_file):
            log_event("Stop signal detected. Stopping network monitor.")
            break
        
        current_status = check_internet_connection()
        status_message = "Internet connection available" if current_status else "No internet connection"
        
        if current_status != last_status:
            log_event(status_message)
            last_status = current_status
        
        time.sleep(CHECK_INTERVAL)

def handle_shutdown(signum, frame):
    """Handle application shutdowns gracefully."""
    log_event("Shutdown signal received. Saving data and exiting...")
    shutdown_event.set()

def main():
    """Main function to run the application."""
    import signal
    signal.signal(signal.SIGINT, handle_shutdown)
    signal.signal(signal.SIGTERM, handle_shutdown)

    # Start network monitoring thread
    network_thread = Thread(target=monitor_network, daemon=True)
    network_thread.start()

    try:
        # Main application loop
        while not shutdown_event.is_set():
            time.sleep(1)  # Keep the main thread alive

    except Exception as e:
        log_event(f"An unexpected error occurred: {e}")
    finally:
        handle_shutdown(None, None)

if __name__ == "__main__":
    main()
