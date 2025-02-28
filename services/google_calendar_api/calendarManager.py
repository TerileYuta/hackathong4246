#GooglecalendarManagerに当たるものだと思います...

from googleapiclient.discovery import build
from .authorize import get_credentials  # /google_calendar_api(同じフォルダ)/authorize.pyから認証情報を取得する関数get_credentialsをインポート

def create_google_calendar_service():
    """
    Google Calendar API サービスオブジェクトを作成する関数。
    :return: Google Calendar API サービスオブジェクト
    """
    
    creds = get_credentials()  # 認証情報を取得
    service = build('calendar', 'v3', credentials=creds)  # Google カレンダー API サービスオブジェクトの作成
    return service
