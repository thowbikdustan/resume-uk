from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os
import json

SERVICE_ACCOUNT_SECRET = json.loads(os.getenv('CRED'))

SCOPES = ['https://www.googleapis.com/auth/drive.file']

folder_name = 'master_resume'
folder_id = os.getenv('FOLDER_ID')

file = 'resume.pdf'

file_metadata = {
    'name': file,
    'parents': [folder_id]
}

# Authenticating using service account
def authenticate(service_account_secret, scopes):
    credentials = service_account.Credentials.from_service_account_info(
        service_account_secret, scopes=scopes)

    # Creating the dirve API client
    service = build('drive', 'v3', credentials=credentials)
    return service

def upload(service, file, folder_id, file_metadata):

    query = f"'{folder_id}' in parents and name = '{file}' and trashed = false"
    results = service.files().list(
        q=query,
        spaces='drive',
        fields='files(id, name)'
    ).execute()

    items = results.get('files', [])

    if items:
        # File exists, update it
        file_id = items[0]['id']
        media = MediaFileUpload(file, resumable=True)
        updated_file = service.files().update(
            fileId=file_id,
            media_body=media
        ).execute()
        print("\n---------File Exists Already, File Updated !! ----------")
        print(f'Updated file ID: {updated_file.get("id")}')
    else:
        # File does not exist, create it
        media = MediaFileUpload(file, resumable=True)
        new_file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        print("\n--------- File Doesn't Exists, New file created !! ----------")
        print(f'Uploaded new file ID: {new_file.get("id")}')

service = authenticate(SERVICE_ACCOUNT_SECRET, SCOPES)    
upload(service, file, folder_id, file_metadata)
