from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

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
    folder_metadata = {'title': folder_name,'mimeType': 'application/vnd.google-apps.folder'}
    folder = drive.CreateFile(folder_metadata)
    folder.Upload()
    return folder['id']


def uploadFile(file, folder_id):
    drive = auth()
    # Upload file to folder.
    f = drive.CreateFile(
        {'title': file.filename, "parents": [{"kind": "drive#fileLink", "id": folder_id}]})
    f.SetContentFile('resumetemp/' + file.filename)
    f.Upload()
    # remove file from temp 
    os.remove('resumetemp/'+file.filename)
    return f['id']

