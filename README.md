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

*STEPS TO DO SO*
To get the credentials.json file from the Google API Console, follow these steps:

Go to the Google API Console:

Visit Google API Console.
Create a new project (if you don’t have one already):

Click on the project dropdown on the top left.
Click on "New Project."
Enter a name for your project and click "Create."
Enable the API you need:

Go to the "Library" in the left sidebar.
Search for the API you need (e.g., Google Drive API, Google Sheets API).
Click on the API and then click "Enable."
Create credentials:

Go to the "Credentials" tab in the left sidebar.
Click on "Create Credentials" and select "OAuth 2.0 Client IDs."
If prompted, configure the consent screen by providing the necessary information (app name, user support email, etc.).
Choose "Application type" based on your project (e.g., Desktop app, Web application).
Enter a name for your credentials and click "Create."
Download the credentials:

Once the credentials are created, you'll see a "Download" button. Click on it to download the credentials.json file.
Save this file in your project directory.
Use the credentials:

Place the credentials.json file in the directory where your application can access it.

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
