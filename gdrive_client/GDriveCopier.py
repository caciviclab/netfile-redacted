import os
import json
from google.oauth2 import service_account
from oauth2client.service_account import ServiceAccountCredentials
from pydrive.auth import GoogleAuth 
from pydrive.drive import GoogleDrive

'''
This copier class supports uploading and downloading files between a local folder
and a folder on Google Drive.  The following has to be done to set up
for this:
    1. A service account has to be created in a project with access to the Google Drive API.
       It's probably best to create a GCP project specifically just for access to the 
       Google Drive API and create the service account in that project.  
    2. The directory on Google Drive has to be shared with the service account.  This is
       done by getting the e-mail of the service account and sharing with that e-mail 
       instead of a real person's e-mail.
    3. A private key (in JSON) has to be created for the service account.  The private key 
       should be placed in an environment variable, SERVICE_ACCOUNT_KEY_JSON.  For
       GitHub Actions, we can simply get the value from a secret of the same name.
'''
class GDriveCopier:
    def __init__(self, target_folder):
        self.target_folder = target_folder
        # Establish connection with Google Drive
        gauth = GoogleAuth() 
        gauth.credentials = self.get_service_account_credentials()
        self.drive = GoogleDrive(gauth)
        # Locate folder on Google Drive
        print(f'Checking for folder {self.target_folder}')
        self.folder_id = self.get_folder_id()
    
    def upload_from(self, local_folder):
        # Get list of files in folder on Google Drive
        folder_file_list_dict = self.get_drive_files()

        # Upload local files to folder on Google Drive
        local_files = os.listdir(local_folder)
        for local_file in local_files:
            print(f'Uploading {local_file}')
            if local_file not in folder_file_list_dict:
                drive_file = self.drive.CreateFile({'parents': [{'id': self.folder_id}], 'title':local_file})
            else:
                # overwrite if file exists on Google Drive
                drive_file = self.drive.CreateFile({'parents': [{'id': self.folder_id}], 'id':folder_file_list_dict[local_file]['id'], 'title':local_file})
            drive_file.SetContentFile(f'{self.target_folder}/{local_file}')
            drive_file.Upload()

    def download_to(self, local_folder):
        # Get list of files in folder on Google Drive
        folder_file_list_dict = self.get_drive_files()
        for file_name in folder_file_list_dict.keys():
            print(f'Downloading {file_name}')
            drive_file = folder_file_list_dict[file_name]
            drive_file.GetContentFile(f'{local_folder}/{file_name}')

    def get_service_account_credentials(self):
        scopes = ["https://www.googleapis.com/auth/drive"]
        key = self.get_private_key()
        key_dict = json.loads(key)
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(key_dict, scopes=scopes)
        return credentials

    def get_private_key(self):
        SERVICE_ACCOUNT_KEY_JSON = os.getenv('SERVICE_ACCOUNT_KEY_JSON','')
        if SERVICE_ACCOUNT_KEY_JSON == '':
            secret_file = os.path.join(os.getcwd(), 'SERVICE_ACCOUNT_KEY_JSON.json')
            with open(secret_file,'r') as f:
                SERVICE_ACCOUNT_KEY_JSON = f.read()
        return SERVICE_ACCOUNT_KEY_JSON

    def get_drive_files(self):
        # Get list of files in folder on Google Drive
        folder_file_list = self.drive.ListFile({'q':f"'{self.folder_id}' in parents and trashed=false"}).GetList()
        folder_file_list_dict = {}
        for folder_file in folder_file_list:
            folder_file_list_dict[folder_file['title']] = folder_file
        return folder_file_list_dict

    def get_folder_id(self):
        file_list = self.drive.ListFile({'q': "trashed=false"}).GetList()
        folder_id = None
        for file in file_list: 
            if (file['title'] == self.target_folder) and (file['mimeType'] == 'application/vnd.google-apps.folder'):
                print('title: %s, id: %s' % (file['title'], file['id']))
                folder_id = file['id']
        if folder_id is None:
            raise Exception(f'Missing folder {self.target_folder}.  Be sure to share the folder with the service account.')
        return folder_id
