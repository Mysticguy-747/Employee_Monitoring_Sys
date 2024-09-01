# Desktop Activity Tracker

This project is a comprehensive desktop activity tracking application developed in Python. It monitors various aspects of user activity and system status, including:

- **Keyboard and Mouse Activity**: Tracks user activity and logs status changes.
- **Network Status**: Monitors and logs internet connection status.
- **Screenshots**: Captures and saves screenshots at regular intervals.
- **Time Zone Changes**: Detects and logs changes in the system's time zone.
- **Active Window Tracking**: Logs active window changes and the duration spent on each window.
- **Drive Sync**: Syncs local files to Google Drive, monitoring changes and updates in real-time.

## Files

- `activity_tracker.py`: Tracks user activity based on keyboard and mouse inputs.
- `network_and_data_monitor.py`: Monitors network connection status and logs it.
- `screenshot.py`: Captures screenshots at regular intervals and manages old screenshots.
- `timezone_change.py`: Monitors and logs changes in the system's time zone.
- `window.py`: Logs changes in the currently active window and the duration spent on each window.
- `drive_sync.py`: Syncs local files with Google Drive, handling uploads, updates, and deletions.
- `stop_listener.py`: Listens for a stop signal to terminate all running scripts.

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/your-repository.git
    cd your-repository
    ```

2. Install the required modules:

    ```sh
    pip install -r requirements.txt
    ```

3. Set up Google Drive API credentials:
    - Place your `credentials.json` file (obtained from Google API Console) in the project directory.

## Usage

1. Start the main application:

    ```sh
    python main.py
    ```

2. To stop all scripts, press `Ctrl + K` while the application is running.

## Requirements

Make sure to install the required Python modules using the provided `requirements.txt` file.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or issues, please contact [Abhishek Yadav](abhishek.yadav_cs.aiml21@gla.ac.in).
