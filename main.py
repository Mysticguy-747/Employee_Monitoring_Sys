import multiprocessing
import subprocess
import os
from stop_listener import stop_listener

# Define the scripts to run
scripts = [
    'activity_tracker.py',
    'network_and_data_monitor.py',
    'screenshot.py',
    'timezone_change.py',
    'window.py',
    'drive_sync.py'  # Add drive_sync.py here
]

# Global variable to stop processes
stop_file = 'stop_signal.txt'

def run_script(script):
    """Run a Python script as a subprocess."""
    while not os.path.exists(stop_file):
        subprocess.run(['python', script])

def main():
    # Get the current working directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Full paths to each script
    scripts_full_path = [os.path.join(current_dir, script) for script in scripts]

    # Create a process for each script
    processes = []
    for script in scripts_full_path:
        process = multiprocessing.Process(target=run_script, args=(script,))
        processes.append(process)

    # Start all processes
    for process in processes:
        process.start()

    # Start the stop listener in a separate process
    listener_process = multiprocessing.Process(target=stop_listener)
    listener_process.start()

    # Wait for the listener to signal shutdown
    listener_process.join()

    # Terminate all processes when stop_signal.txt is detected
    for process in processes:
        process.terminate()
        process.join()

if __name__ == '__main__':
    main()
