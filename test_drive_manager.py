import unittest
from unittest.mock import Mock, patch, mock_open
import os
import sys
from drive_manager import authenticate, list_folders, upload_folder, create_backup, main

class TestDriveManager(unittest.TestCase):

    @patch('drive_manager.pickle.load')
    @patch('drive_manager.pickle.dump')
    @patch('drive_manager.build')
    @patch('drive_manager.InstalledAppFlow.from_client_secrets_file')
    def test_authenticate_with_existing_creds(self, mock_flow, mock_build, mock_dump, mock_load):
        mock_creds = Mock()
        mock_creds.valid = True
        mock_load.return_value = mock_creds
        with patch('os.path.exists', return_value=True):
            service = authenticate()
            mock_build.assert_called_once()

    @patch('drive_manager.build')
    def test_list_folders(self, mock_build):
        mock_service = Mock()
        mock_files = Mock()
        mock_files.list.return_value.execute.return_value = {'files': [{'name': 'test', 'id': '123'}]}
        mock_service.files.return_value = mock_files
        mock_build.return_value = mock_service

        with patch('drive_manager.authenticate', return_value=mock_service):
            list_folders(mock_service)
            mock_files.list.assert_called_once()

    @patch('os.path.isdir', return_value=True)
    @patch('os.path.basename', return_value='test_folder')
    @patch('drive_manager.build')
    def test_upload_folder(self, mock_build, mock_basename, mock_isdir):
        mock_service = Mock()
        mock_files = Mock()
        mock_create = Mock()
        mock_create.execute.return_value = {'id': 'folder_id'}
        mock_files.create.return_value = mock_create
        mock_service.files.return_value = mock_files
        mock_build.return_value = mock_service

        with patch('os.walk', return_value=[('/path', [], ['file1.txt'])]):
            with patch('os.path.join', return_value='/path/file1.txt'):
                with patch('drive_manager.MediaFileUpload') as mock_upload:
                    with patch('drive_manager.authenticate', return_value=mock_service):
                        upload_folder(mock_service, '/path')
                        self.assertEqual(mock_files.create.call_count, 2)  # folder and file

    @patch('drive_manager.datetime')
    @patch('drive_manager.build')
    def test_create_backup(self, mock_build, mock_datetime):
        mock_datetime.datetime.now.return_value.strftime.return_value = '20231227_120000'
        mock_service = Mock()
        mock_files = Mock()
        mock_create = Mock()
        mock_create.execute.return_value = {'id': 'backup_id'}
        mock_files.create.return_value = mock_create
        mock_service.files.return_value = mock_files
        mock_build.return_value = mock_service

        with patch('drive_manager.authenticate', return_value=mock_service):
            with patch('drive_manager.upload_folder') as mock_upload:
                create_backup(mock_service, '/path')
                mock_upload.assert_called_once_with(mock_service, '/path', 'backup_id')

    @patch('sys.argv', ['drive_manager.py', 'list'])
    @patch('drive_manager.authenticate')
    @patch('drive_manager.list_folders')
    def test_main_list(self, mock_list, mock_auth):
        main()
        mock_auth.assert_called_once()
        mock_list.assert_called_once()

if __name__ == '__main__':
    unittest.main()