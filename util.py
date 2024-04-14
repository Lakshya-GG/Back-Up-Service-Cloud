from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64
import json
import os

SCOPES = ['https://www.googleapis.com/auth/drive']
SECRET_DIR = './secrets'
CLIENT_SECRET_FILE = os.path.join(SECRET_DIR,'client_secret_encoded.txt')  # Path to your downloaded credentials file
TOKEN_FILE = os.path.join(SECRET_DIR,'token_encoded.txt')

def load_secrets():
    # Read and decode client_secret.json
    with open(CLIENT_SECRET_FILE, 'r') as f:
        client_secret_data = json.loads(base64.b64decode(f.read()).decode())
    # Read and decode token.json
    with open(TOKEN_FILE, 'r') as f:
        token_data = json.loads(base64.b64decode(f.read()).decode())
    return client_secret_data, token_data

def dump_secrets(creds):
    with open(TOKEN_FILE, 'w') as token:
            encoded_bytes = base64.b64encode(creds.to_json())
            token.write(encoded_bytes.decode('utf-8'))

def authenticate():
    creds = None
    CLIENT_SECRET_DATA, TOKEN_DATA = load_secrets()
    if TOKEN_DATA:
        creds = Credentials.from_authorized_user_info(TOKEN_DATA, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config(CLIENT_SECRET_DATA, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials
            dump_secrets(creds)
    return creds