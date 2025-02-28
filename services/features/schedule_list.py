import re
from pytz import timezone
from datetime import datetime, timedelta

from config import Config
from services.google_calendar_api import GoogleCalendarAPI
from .parse_date import parse_date

def get_events_for_date(date, line_id):
    """

    指定された日付に基づいてGoogleカレンダーからイベントを取得する

    Parameters
    ----------
        date(datetime) : イベントを取得したい日付
        line_id(str) : ユーザーのLINE ID

    Returns
    ----------
        list : 取得したイベントのリスト

    """

    if not date:
        return "無効な日付です。もう一度試してください。"
    
    try:
        # 日本標準時 (JST) に変換
        jst = timezone('Asia/Tokyo')  # 日本標準時
        date = date.replace(tzinfo=jst)
        time_min = date.isoformat()
        time_max = (date + timedelta(days=1)).isoformat()

        events = get_events_from_GcalenderAPI(time_min, time_max, line_id)

        extracted_events = []
        for event in events:
            extracted_events.append({
                "id": event.get("id"),
                "summary": event.get("summary", "（無題）"),
                "start": event.get("start", {}),
                "end": event.get("end", {}),
                "location": event.get("location", "未設定"),
                "attendees": [attendee["email"] for attendee in event.get("attendees", [])]
            })

        return extracted_events
    except Exception as e:
        return "イベントの取得中にエラーが発生しました。"

def get_events_from_GcalenderAPI(time_min, time_max, line_id):
    """

    GoogleカレンダーAPIから指定された期間のイベントを取得する
    
    Parameters
    ----------
        time_min(str) : 開始時刻（ISO 8601形式）
        time_max(str) : 終了時刻（ISO 8601形式）
        line_id(str) : ユーザーのLINE ID
    
    Returns
    ----------
        list : 取得したイベントのリスト
    
    """
    calendar_api = GoogleCalendarAPI(line_id)
    not_auth = calendar_api.authenticate()

    # Oauth承認が必要になった場合
    if not_auth:
        return False, Config.auth_error_msg
    
    service = calendar_api.calendar

    events_result = service.events().list(
        calendarId='primary', 
        timeMin=time_min,  
        timeMax=time_max,  
        singleEvents=True,  
        orderBy='startTime'  
    ).execute()  

    return events_result.get('items', [])