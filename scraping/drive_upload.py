from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime
import time
import os
import shutil



def find_or_create_folder(service, folder_name):
    """
    Searches for a folder by name in Google Drive and returns its ID.
    If the folder does not exist, it is created.

    Args:
        service: Authorized Google Drive service instance.
        folder_name (str): The name of the folder to search or create.

    Returns:
        str: The ID of the existing or newly created folder.
    """
    # Search for the folder
    results = service.files().list(
        q=f"mimeType='application/vnd.google-apps.folder' and name='{folder_name}' and trashed=false",
        spaces='drive',
        fields='files(id, name)').execute()
    items = results.get('files', [])

    # If found, return the first folder's ID
    if items:
        print(f"Found folder: {items[0]['name']} with ID: {items[0]['id']}")
        return items[0]['id']
    else:
        # If not found, create the folder
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = service.files().create(body=file_metadata, fields='id').execute()
        print(f"Folder created: {folder_name} with ID: {folder.get('id')}")
        return folder.get('id')


def upload_file(service, file_name, file_path,
                folder_id, mime_type='image/png'):
    """
    Uploads a file to Google Drive under a specific folder.

    Args:
        service: Authorized Google Drive service instance.
        file_name (str): The name of the file to be uploaded.
        file_path (str): The local path of the file to be uploaded.
        folder_id (str): The ID of the folder in which to upload the file.
        mime_type (str, optional): The MIME type of the file. Defaults to 'image/png'.

    Returns:
        None
    """
    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }
    media = MediaFileUpload(file_path, mimetype=mime_type)
    file = service.files().create(body=file_metadata,
                                  media_body=media, fields='id').execute()
    print(f'File ID: {file.get("id")}')


def auth():
    """
    Authenticates the user with Google Drive API and returns the service object.

    This function handles token creation and refresh for Google Drive API access.
    It uses a token.json file for storing user credentials.

    Returns:
        service: An authorized Google Drive service instance.
    """
    creds = None
    SCOPES = ['https://www.googleapis.com/auth/drive']
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("./token.json"):
        creds = Credentials.from_authorized_user_file("./token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "./credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    service = build("drive", "v3", credentials=creds)

    return service


def upload_to_drive(dir, target):
    """
    Uploads all files from a specified directory to a Google Drive folder.

    Args:
        dir (str): The directory containing files to upload.
        target (str): The name of the target folder in Google Drive.

    Returns:
        None
    """
    service = auth()
    folder_id = find_or_create_folder(service, target)
    for filename in os.listdir(dir):
        upload_file(service, filename, os.path.join(dir, filename), folder_id)