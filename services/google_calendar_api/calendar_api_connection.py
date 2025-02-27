# services/google_calendar_api/calendar_api_connection.py

import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

from ..firestore import db
from config import Config

class GoogleCalendarAPI():
    """

    calenderにアクセスするための認証情報に関連する処理行う。


    Methods
    ----------
        getToken() : FireStoreからtokenを取得する
        updateToken() : トークン情報を更新する
        addUser() : ユーザーの新規作成
        authenticate() : Google カレンダー API の認証を行い、認証済みのサービスオブジェクトを返す

    """
    def __init__(self, line_id:str):
        """
        
        Parameters
        ----------
            line_id(str) : LINE ID

        """

        self.SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

        self.line_id = line_id
        token = self.getToken()
        self.calendar = self.authenticate()

    def getToken(self):
        """
        
        FireStoreからtokenを取得する

        Parameters
        ----------
            None
            
        Returns
        ----------
            dict : トークン等の情報

        """

        users_ref = db.collection("users").document(self.line_id)
        results = users_ref.get().to_dict()

        if results:
            return results
        else:
            self.addUser()
            return None
    
    def updateToken(self, token:dict):
        """
        
        トークン情報を更新する

        Parameters
        ----------
            token(dict) : token情報

        Returns
        ----------
            None

        """
        user_ref = db.collection("users").document(self.line_id)
        user_ref.update(token)

    def addUser(self):
        """
        
        ユーザーの新規作成

        Parameters
        ----------
            None

        Returns
        ----------
            None

        """

        user = {
                "token": "",
                "refresh_token": "",
                "token_uri": "",
                "client_id": "",
                "client_secret": "",
                "scopes": ""
        }

        db.collection("users").document(self.line_id).set(user)

    def authenticate(self):
        """

        Google カレンダー API の認証を行い、認証済みのサービスオブジェクトを返す
        
        Parameters
        ----------
            None
        
        Returns
        ----------
            googleapiclient.discovery.Resource : 認証された Google カレンダー API サービスオブジェクト
        
        """

        token = self.getToken()
        creds = None

        credentials_path = Config.credentials_path

        if token:
            creds =  Credentials.from_authorized_user_info(token)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())

            else:
                flow = InstalledAppFlow.from_client_secrets_file(credentials_path, self.SCOPES)

                creds = flow.run_local_server(port=0)

            self.updateToken(json.loads(creds.to_json()))
    
        return build("calendar", "v3", credentials=creds)