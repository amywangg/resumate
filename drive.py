from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import io
from googleapiclient.http import MediaIoBaseDownload


def auth():
    gauth = GoogleAuth()
    # Try to load saved client credentials
    gauth.LoadCredentialsFile("driveAPI/mycreds.txt")
    if gauth.credentials is None:
        # Authenticate if they're not there
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
    else:
        # Initialize the saved creds
        gauth.Authorize()
    # Save the current credentials to a file
    gauth.SaveCredentialsFile("driveAPI/mycreds.txt")
    drive = GoogleDrive(gauth)

    return drive


def createFolder(folder_name):
    drive = auth()
    # Create folder
    folder_metadata = {'title': folder_name,
                       'mimeType': 'application/vnd.google-apps.folder'}
    folder = drive.CreateFile(folder_metadata)
    folder.Upload()
    return folder['id']


def uploadFile(file, folder_id, filename):
    drive = auth()
    # Upload file to folder.
    f = drive.CreateFile(
        {'title': filename, "parents": [{"kind": "drive#fileLink", "id": folder_id}]})
    f.SetContentFile('resumetemp/' + file.filename)
    f.Upload()
    # remove file from temp
    os.remove('resumetemp/'+file.filename)
    return f['id']


def getLink(folder_id, file_id):
    # Call the Drive v3 API
    drive = auth()

    results = drive.ListFile({'q': "'" + folder_id + "' in parents"}).GetList()
    link = ''
    for x in results:
        if x['id'] == file_id:
            return x['embedLink']
    return link

def deleteFolder(folder_id):
    drive = auth()
    file_list = drive.ListFile({'q': folder_id + " in parents"})
    file_list.Trash()
