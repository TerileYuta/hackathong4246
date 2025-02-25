# services/google_calendar_api/calendar_api_connection.py

import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def authenticate_google_calendar():
    """
    Google カレンダー API の認証を行い、認証済みのサービスオブジェクトを返す
    Parameters
    ----------
        なし
    Returns
    ----------
        googleapiclient.discovery.Resource : 認証された Google カレンダー API サービスオブジェクト
    """
    
    creds = None
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

    token_path = os.path.join(root_dir, "token.json")
    credentials_path = os.path.join(root_dir, "credentials.json")

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(token_path, "wb") as token:
            token.write(creds.to_json().encode())

    return build("calendar", "v3", credentials=creds)