import os
import sys
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import pickle

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

# Local folder path to upload (user can modify this)
LOCAL_FOLDER_PATH = '/path/to/your/local/folder'  # Change this to your desired path

def authenticate():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('drive', 'v3', credentials=creds)

def list_folders(service, parent_id='root'):
    """List folders in Google Drive"""
    results = service.files().list(
        q=f"mimeType='application/vnd.google-apps.folder' and '{parent_id}' in parents",
        fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No folders found.')
    else:
        print('Folders:')
        for item in items:
            print(f"{item['name']} (ID: {item['id']})")

def upload_folder(service, local_path, parent_id='root'):
    """Upload a local folder to Google Drive"""
    if not os.path.isdir(local_path):
        print(f"Error: {local_path} is not a valid directory")
        return

    folder_name = os.path.basename(local_path)
    # Create the folder in Drive
    folder_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_id]
    }
    folder = service.files().create(body=folder_metadata, fields='id').execute()
    folder_id = folder.get('id')

    # Upload files recursively
    for root, dirs, files in os.walk(local_path):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(root, local_path)
            if relative_path == '.':
                current_parent = folder_id
            else:
                # Create subfolders if needed
                parts = relative_path.split(os.sep)
                current_parent = folder_id
                for part in parts:
                    subfolder_metadata = {
                        'name': part,
                        'mimeType': 'application/vnd.google-apps.folder',
                        'parents': [current_parent]
                    }
                    subfolder = service.files().create(body=subfolder_metadata, fields='id').execute()
                    current_parent = subfolder.get('id')

            # Upload file
            file_metadata = {
                'name': file,
                'parents': [current_parent]
            }
            media = MediaFileUpload(file_path, resumable=True)
            service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    print(f"Uploaded folder '{folder_name}' to Google Drive")

def create_backup(service, local_path, backup_name=None):
    """Create a backup by uploading the local folder with a timestamp"""
    if backup_name is None:
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"Backup_{timestamp}"

    # Create a backup folder
    backup_metadata = {
        'name': backup_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    backup_folder = service.files().create(body=backup_metadata, fields='id').execute()
    backup_id = backup_folder.get('id')

    upload_folder(service, local_path, backup_id)
    print(f"Backup created: {backup_name}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py [list|upload|backup]")
        return

    command = sys.argv[1]
    service = authenticate()

    if command == 'list':
        list_folders(service)
    elif command == 'upload':
        upload_folder(service, LOCAL_FOLDER_PATH)
    elif command == 'backup':
        create_backup(service, LOCAL_FOLDER_PATH)
    else:
        print("Invalid command. Use 'list', 'upload', or 'backup'")

if __name__ == '__main__':
    main()