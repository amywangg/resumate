import authenticateDrive


def createJob():

    service = authenticateDrive.authenticateDrive()

    file_metadata = {
        'name': 'Invoices',
        'mimeType': 'application/vnd.google-apps.folder'
    }
    file = service.files().create(body=file_metadata, fields='id').execute()
    print('Folder ID: %s' & file.get('id'))