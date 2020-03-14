from __future__ import print_function
from driveAPI import authenticateDrive
import io
from googleapiclient.http import MediaIoBaseDownload


def readFromDrive():
    # Call the Drive v3 API
    service = authenticateDrive.authenticateDrive()
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            if item['name'] == "Resumes":
                downloadfiles(item['id'], service)


def downloadfiles(folder_id, service):
    page_token = None
    while True:
        response = service.files().list(q="'" + folder_id + "' in parents",
                                              spaces='drive',
                                              fields='nextPageToken, files(id, name)',
                                              pageToken=page_token).execute()
        for file in response.get('files', []):
            # Process change
            print('Found file: %s (%s)' % (file.get('name'), file.get('id')))

            request = service.files().get_media(fileId=file.get('id'))

            fh = io.FileIO('resumetemp/' + file.get('name'), 'wb')
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print("Download %d%%." % int(status.progress() * 100))

        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break

