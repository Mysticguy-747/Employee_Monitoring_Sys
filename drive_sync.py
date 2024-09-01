import os
import io
import pickle
import secrets
import threading
from time import sleep
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaIoBaseUpload
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

class DriveSync:
    def __init__(self, local_folder):
        self.local_folder = Path(local_folder).resolve()
        self.creds = None
        self.service = None
        self.folder_id = None
        self.files_mapping = {}  # Maps local paths to Drive file IDs
        self.load_credentials()
        self.init_drive_folder()
        self.build_files_mapping()
        self.start_watchdog()

    def load_credentials(self):
        """Load or create credentials."""
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)
        # If there are no valid creds, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:

                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)
        self.service = build('drive', 'v3', credentials=self.creds)

    def init_drive_folder(self):
        """Initialize main folder on Drive."""
        folder_name = self.local_folder.name
        results = self.service.files().list(
            q=f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false",
            spaces='drive',
            fields='files(id, name)').execute()
        files = results.get('files', [])
        if files:
            self.folder_id = files[0]['id']
        else:
            file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            file = self.service.files().create(body=file_metadata, fields='id').execute()
            self.folder_id = file.get('id')

    def build_files_mapping(self):
        """Build mapping of local files to Drive file IDs."""
        for root, dirs, files in os.walk(self.local_folder):
            for name in files:
                local_path = Path(root) / name
                relative_path = local_path.relative_to(self.local_folder)
                drive_file_id = self.search_drive_file(relative_path)
                if not drive_file_id:
                    drive_file_id = self.upload_file(local_path)
                self.files_mapping[str(relative_path)] = drive_file_id

    def search_drive_file(self, relative_path):
        """Search for a file in Drive."""
        file_name = relative_path.name
        parent_folder_id = self.folder_id
        if relative_path.parent != Path('.'):
            parent_folder_id = self.create_drive_folders(relative_path.parent)
        query = f"name='{file_name}' and '{parent_folder_id}' in parents and trashed=false"
        results = self.service.files().list(
            q=query,
            spaces='drive',
            fields='files(id, name)').execute()
        files = results.get('files', [])
        if files:
            return files[0]['id']
        return None

    def create_drive_folders(self, relative_path):
        """Create nested folders on Drive."""
        folders = relative_path.parts
        parent_id = self.folder_id
        for folder in folders:
            query = f"name='{folder}' and '{parent_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
            results = self.service.files().list(
                q=query,
                spaces='drive',
                fields='files(id, name)').execute()
            files = results.get('files', [])
            if files:
                parent_id = files[0]['id']
            else:
                file_metadata = {
                    'name': folder,
                    'mimeType': 'application/vnd.google-apps.folder',
                    'parents': [parent_id]
                }
                file = self.service.files().create(body=file_metadata, fields='id').execute()
                parent_id = file.get('id')
        return parent_id

    def upload_file(self, local_path):
        """Upload a file to Drive."""
        relative_path = local_path.relative_to(self.local_folder)
        parent_folder_id = self.folder_id
        if relative_path.parent != Path('.'):
            parent_folder_id = self.create_drive_folders(relative_path.parent)
        file_metadata = {
            'name': local_path.name,
            'parents': [parent_folder_id]
        }
        media = MediaIoBaseUpload(
            io.FileIO(str(local_path), 'rb'),
            mimetype='application/octet-stream'
        )
        file = self.service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id').execute()
        return file.get('id')

    def update_file(self, local_path, file_id):
        """Update an existing file on Drive."""
        media = MediaIoBaseUpload(
            io.FileIO(str(local_path), 'rb'),
            mimetype='application/octet-stream'
        )
        file = self.service.files().update(
            fileId=file_id,
            media_body=media).execute()
        relative_path = local_path.relative_to(self.local_folder)


    def delete_file(self, file_id):
        """Delete a file from Drive."""
        self.service.files().delete(fileId=file_id).execute()


    def start_watchdog(self):
        """Start watchdog observer to monitor file changes."""
        event_handler = LocalFolderEventHandler(self)
        observer = Observer()
        observer.schedule(event_handler, str(self.local_folder), recursive=True)
        observer_thread = threading.Thread(target=observer.start)
        observer_thread.daemon = True
        observer_thread.start()

        try:
            while True:
                sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

class LocalFolderEventHandler(FileSystemEventHandler):
    """Handles filesystem events."""
    def __init__(self, drive_sync):
        self.drive_sync = drive_sync

    def on_created(self, event):
        if not event.is_directory:
            local_path = Path(event.src_path)
            file_id = self.drive_sync.upload_file(local_path)
            relative_path = local_path.relative_to(self.drive_sync.local_folder)
            self.drive_sync.files_mapping[str(relative_path)] = file_id

    def on_modified(self, event):
        if not event.is_directory:
            local_path = Path(event.src_path)
            relative_path = local_path.relative_to(self.drive_sync.local_folder)
            file_id = self.drive_sync.files_mapping.get(str(relative_path))
            if file_id:
                self.drive_sync.update_file(local_path, file_id)
            else:
                file_id = self.drive_sync.upload_file(local_path)
                self.drive_sync.files_mapping[str(relative_path)] = file_id

    def on_deleted(self, event):
        if not event.is_directory:
            local_path = Path(event.src_path)
            relative_path = local_path.relative_to(self.drive_sync.local_folder)
            file_id = self.drive_sync.files_mapping.get(str(relative_path))
            if file_id:
                self.drive_sync.delete_file(file_id)
                del self.drive_sync.files_mapping[str(relative_path)]

if __name__ == '__main__':
    LOCAL_FOLDER_PATH = r'C:\Users\Abhis\Desktop\Desktop-Agent'  

    DriveSync(LOCAL_FOLDER_PATH)
