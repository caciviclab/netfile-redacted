import os
from pydrive.auth import GoogleAuth 
from pydrive.drive import GoogleDrive

gauth = GoogleAuth() 
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

def get_folder_id(drive, folderName):
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    print(len(file_list))
    folder_id = None
    for file in file_list: 
        if (file['title'] == target_folder) and (file['mimeType'] == 'application/vnd.google-apps.folder'):
            print(file['mimeType'])
            print('title: %s, id: %s' % (file['title'], file['id']))
            folder_id = file['id']
    return folder_id

def create_folder(drive, folderName):
    file_metadata = {
        'title': folderName,
        'mimeType': 'application/vnd.google-apps.folder'
    }

    folder = drive.CreateFile(file_metadata)
    folder.Upload()

target_folder = 'netfile_redacted'
folder_id = get_folder_id(drive, target_folder)

if folder_id is None:
    create_folder(drive, target_folder)
    folder_id = get_folder_id(drive, target_folder)

folder_file_list = drive.ListFile({'q':f"'{folder_id}' in parents and trashed=false"}).GetList()
folder_file_list_dict = {}
for folder_file in folder_file_list:
    folder_file_list_dict[folder_file['title']] = folder_file['id']
print(folder_file_list_dict)

local_files = os.listdir(target_folder)
print(local_files)
for local_file in local_files:
    if local_file not in folder_file_list_dict:
        file2 = drive.CreateFile({'parents': [{'id': folder_id}], 'title':local_file})
    else:
        file2 = drive.CreateFile({'parents': [{'id': folder_id}], 'id':folder_file_list_dict[local_file], 'title':local_file})
    file2.SetContentFile(f'{target_folder}/{local_file}')
    file2.Upload()