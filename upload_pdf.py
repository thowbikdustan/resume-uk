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

def upload():
    # Authenticating using servcie account
    credentials = service_account.Credentials.from_service_account_info(
        SERVICE_ACCOUNT_SECRET, scopes=SCOPES)

    # Creating the dirve API client
    service = build('drive', 'v3', credentials=credentials)

    # Create a MediaFileUpload object
    media = MediaFileUpload(file, resumable=True)

    # Uploading File
    uploaded_file = service.files().create(
                        body=file_metadata,
                        media_body=media,
                        fields='id'
                        ).execute()
    
    print("\n--------- File Uploaded ----------")
    print(f'File ID: {uploaded_file.get("id")}')
    
upload()
