from driveAPI import authenticateDrive

from googleapiclient.http import MediaIoBaseUpload


def insert_file(file_name, mime_type, file_data):
    service = authenticateDrive.authenticateDrive()

    generate_ids_result = service.generateIds(count=1).execute()
    file_id = generate_ids_result['ids'][0]

    body = {
        'id': file_id,
        'name': file_name,
        'mimeType': mime_type,
    }

    media_body = MediaIoBaseUpload(file_data,
                                   mimetype=mime_type,
                                   resumable=True)

    service.create(body=body,
                   media_body=media_body,
                   fields='id,name,mimeType,createdTime,modifiedTime').execute()

    return file_id

# def insert_file(file, foldername):
#     # Call the Drive v3 API
#     service = authenticateDrive.authenticateDrive()
#     results = service.files().list(
#         pageSize=10, fields="nextPageToken, files(id, name)").execute()
#     items = results.get('files', [])
#
#     if not items:
#         print('No files found.')
#     else:
#         for item in items:
#             print('Files: ' + item['name'])
#
#             page_token = None
#             while True:
#                 response = service.files().list(q="'1xlz7xDQrkjMU1iR2qqG9kKS0mPuMULKO' in parents",
#                                                 spaces='drive',
#                                                 fields='nextPageToken, files(id, name)',
#                                                 pageToken=page_token).execute()
#                 file_metadata = {'name': filename}
#                 media = MediaFileUpload(filename)
#                 service.files().create(body=file_metadata, media_body=media, fields='id').execute()
#
#                 page_token = response.get('nextPageToken', None)
#                 if page_token is None:
#                     break
#
# if not items:
#     print('No files found.')
# else:
#     print('Files:')
#     for item in items:
#         print(item['name'])
#         if item['name'] == foldername:
#             # TODO: have to retrieve folderid given the folder name
#             folder_id = item['id']
#             print(foldername + folder_id)
#             file_metadata = {
#                 'name': [filename],
#                 'parents': [folder_id]
#             }
#             media = MediaFileUpload('files/' + foldername,
#                                     resumable=True)
#             service.files().create(body=file_metadata,
#                                    media_body=media,
#                                    fields='id').execute()
