import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
FOLDER_ID = '1I7dX6DoAGE9LXEyQx99E9EpsZpQL2bZ9'
CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.pickle'

def get_drive_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    return build('drive', 'v3', credentials=creds)

def list_contents(service, folder_id):
    query = f"'{folder_id}' in parents"
    results = service.files().list(q=query, fields='files(id, name, mimeType)', pageSize=100).execute()
    items = results.get('files', [])
    if not items:
        print("No files or subfolders found.")
    else:
        print("Contents of folder:")
        for item in items:
            print(f"Name: {item['name']}, ID: {item['id']}, Type: {item['mimeType']}")

if __name__ == '__main__':
    service = get_drive_service()
    list_contents(service, FOLDER_ID)
