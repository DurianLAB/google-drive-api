# Google Drive Manager

[![GitHub Repo](https://img.shields.io/badge/GitHub-DurianLAB/google--drive--api-blue)](https://github.com/DurianLAB/google-drive-api)

A Python script to interact with Google Drive for listing folders, uploading local folders, and creating backups using the Google Drive API.

## Requirements

- **Python**: Version 3.6 or higher
- **Google Cloud Project**: Set up a project at [Google Cloud Console](https://console.cloud.google.com/)
  - Enable the Google Drive API
  - Create OAuth 2.0 credentials (download `credentials.json`)
- **Dependencies**: Listed in `requirements.txt` (installed via pip in virtual environment)

## Installation

1. Clone or download the repository.
2. Create a virtual environment:
   ```
   python3 -m venv venv
   ```
3. Activate the virtual environment:
   ```
   source venv/bin/activate
   ```
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Setup

1. Obtain `credentials.json` from your Google Cloud Console and place it in the project directory.
2. Edit `drive_manager.py` and update the `LOCAL_FOLDER_PATH` variable to the path of the local folder you want to upload or back up (e.g., `/home/user/my_folder`).

## Usage

Run the script from the command line with one of the following commands:

- **List folders**: Lists folders in the root of your Google Drive.
  ```
  python drive_manager.py list
  ```

- **Upload folder**: Uploads the folder specified in `LOCAL_FOLDER_PATH` to the root of your Google Drive.
  ```
  python drive_manager.py upload
  ```

- **Create backup**: Creates a timestamped backup folder on Google Drive and uploads the contents of `LOCAL_FOLDER_PATH` into it.
  ```
  python drive_manager.py backup
  ```

On the first run, the script will open a browser for OAuth authorization. Follow the prompts to grant access.

## Testing

Run the test suite with:

```
python -m pytest
```

Or

```
python test_drive_manager.py
```

## Notes

- The script uses OAuth for secure authentication.
- Uploads handle folders recursively, creating subfolders as needed.
- Backups are stored in timestamped folders (e.g., `Backup_20231227_120000`).
- Ensure your Google account has sufficient storage space.
- For issues, check the Google Drive API documentation or verify your credentials.

## Issues

See [Issue #1](https://github.com/DurianLAB/google-drive-api/issues/1) for integration into LaTeX DocOps module.